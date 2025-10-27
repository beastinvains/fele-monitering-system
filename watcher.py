import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event): self.callback("created", event.src_path)
    def on_deleted(self, event): self.callback("deleted", event.src_path)
    def on_modified(self, event): self.callback("modified", event.src_path)
    def on_moved(self, event): self.callback("moved", f"{event.src_path} → {event.dest_path}")

class FileWatcher:
    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.observer = None
        self.thread = None
        self.running = False

    def start(self):
        if self.running: return
        self.observer = Observer()
        self.observer.schedule(Handler(self.callback), self.path, recursive=True)
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self.running = True

    def _run(self):
        self.observer.start()
        try:
            while self.running:
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()

    def stop(self):
        self.running = False
