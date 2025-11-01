# ...existing code...
import os
import time
import threading
import difflib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MultiFileWatcher:
    def __init__(self, paths, callback):
        self.paths = paths
        self.callback = callback
        self.observers = []
        self.running = False

    def start(self):
        self.running = True
        for path in self.paths:
            handler = WatchHandler(self.callback)
            # build initial cache for existing files under this path
            try:
                handler.build_initial_cache(path)
            except Exception:
                # if initial caching fails, continue — diffs will be skipped until cache is populated
                pass
            observer = Observer()
            observer.schedule(handler, path, recursive=True)
            observer.start()
            self.observers.append(observer)

    def stop(self):
        self.running = False
        for observer in self.observers:
            observer.stop()
        for observer in self.observers:
            observer.join()

class WatchHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        # cache: path -> text content (or None if skipped)
        self.cache = {}

    def build_initial_cache(self, root_path):
        for dirpath, _, filenames in os.walk(root_path):
            for fname in filenames:
                full = os.path.join(dirpath, fname)
                try:
                    stat = os.path.getsize(full)
                    if stat > 1_000_000:  # skip big files (>1MB) for initial cache
                        self.cache[full] = None
                        continue
                    with open(full, "r", encoding="utf-8", errors="replace") as f:
                        self.cache[full] = f.read()
                except Exception:
                    self.cache[full] = None

    def on_any_event(self, event):
        if event.is_directory:
            return

        event_type = event.event_type
        if event_type == "modified":
            self._handle_modified(event)
        else:
            # created, deleted, moved, etc. — forward without diff
            self._update_cache_on_nonmodify(event)
            self.callback(event_type, event.src_path, None)

    def _update_cache_on_nonmodify(self, event):
        # keep cache in sync for created/deleted/moved
        try:
            if event.event_type == "deleted":
                self.cache.pop(event.src_path, None)
            elif event.event_type == "created":
                try:
                    stat = os.path.getsize(event.src_path)
                    if stat > 1_000_000:
                        self.cache[event.src_path] = None
                    else:
                        with open(event.src_path, "r", encoding="utf-8", errors="replace") as f:
                            self.cache[event.src_path] = f.read()
                except Exception:
                    self.cache[event.src_path] = None
            elif event.event_type == "moved":
                # watchdog provides dest_path for moved events as attribute; handle best-effort
                dest = getattr(event, "dest_path", None)
                if dest:
                    self.cache[dest] = self.cache.pop(event.src_path, None)
                else:
                    self.cache.pop(event.src_path, None)
        except Exception:
            pass

    def _handle_modified(self, event):
        path = event.src_path
        try:
            stat = os.path.getsize(path)
            if stat > 2_000_000:  # avoid diffing extremely large files (>2MB)
                # update cache entry to None (skip diff) and notify without details
                self.cache[path] = None
                self.callback("modified", path, None)
                return
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                new_text = f.read()
        except Exception:
            # can't read (maybe deleted right after modify) — clear cache and notify
            self.cache.pop(path, None)
            self.callback("modified", path, None)
            return

        prev_text = self.cache.get(path)
        if prev_text is None:
            # we didn't have previous content — store and notify without diff
            self.cache[path] = new_text
            self.callback("modified", path, None)
            return

        if prev_text == new_text:
            # no effective change (some editors trigger modify without content change)
            return

        # compute unified diff
        diff_lines = difflib.unified_diff(
            prev_text.splitlines(),
            new_text.splitlines(),
            fromfile=path,
            tofile=path,
            lineterm=""
        )
        diff_text = "\n".join(diff_lines)
        # guard diff size
        if len(diff_text) > 20000:
            diff_text = diff_text[:20000] + "\n...truncated..."
        # update cache and callback with diff
        self.cache[path] = new_text
        self.callback("modified", path, diff_text)
# ...existing code...