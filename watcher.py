import os
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
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
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
            if event.src_path.endswith(".md") or event.src_path.endswith(".css"):
                # If the file was README.md, skip
                if event.src_path.endswith("README.md"):
                    return None

                # Split the file path into the root and extension
                root, ext = os.path.splitext(event.src_path)
                # Change the extension to .md
                md_path = root + ".md"

                print(f'{event.src_path} updated. Running resume.py')

                # Get the directory of the modified file
                file_dir = os.path.dirname(md_path)

                # Change to the directory of the modified file
                original_dir = os.getcwd()
                os.chdir(file_dir)

                # Run the resume.py script
                try:
                    subprocess.run(
                        ["python", os.path.join(
                            original_dir, "resume.py"), os.path.basename(md_path)],
                        check=True
                    )
                finally:
                    # Change back to the original directory
                    os.chdir(original_dir)


if __name__ == '__main__':
    w = Watcher()
    w.run()
