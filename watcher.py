import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class Watcher:
    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Take any action here when a file is modified.
            if event.src_path.endswith("esume.md") or event.src_path.endswith("resume.css"):
                print(f'{event.src_path} updated. Running resume.py...')
                subprocess.run(
                    ["python", "resume.py", "JD_Lien_-_Resume.md"], check=True)


if __name__ == '__main__':
    w = Watcher()
    w.run()
