import os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOGS: list[dict[str, str]] = []

class UploadEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            LOGS.append({
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'action':    'CREATED',
                'file':      os.path.basename(event.src_path)
            })

    def on_modified(self, event):
        if not event.is_directory:
            LOGS.append({
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'action':    'MODIFIED',
                'file':      os.path.basename(event.src_path)
            })

def start_monitor(path: str):
    handler  = UploadEventHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()





