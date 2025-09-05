import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

cartella = r"<path main.py>"
script_rinomina = r"<path folder>"  # Path dello script di rinomina

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.pdf') and os.path.basename(event.src_path).startswith("DOC"):
            print(f"Nuovo file trovato: {event.src_path}")
            # Richiama lo script di rinomina con il percorso file
            subprocess.run(['pythonw', script_rinomina, event.src_path])

if __name__ == "__main__":
    # Processa i file già esistenti
    for filename in os.listdir(cartella):
        if filename.startswith("DOC") and filename.endswith(".pdf"):
            fullpath = os.path.join(cartella, filename)
            subprocess.run(['python', script_rinomina, fullpath])

    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, cartella, recursive=False)
    observer.start()
    print(f"Monitoraggio avviato su {cartella}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
