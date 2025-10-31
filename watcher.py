import os
import time
import threading
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

    def on_any_event(self, event):
        if not event.is_directory:
            event_type = event.event_type
            self.callback(event_type, event.src_path)