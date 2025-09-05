import sys
import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import pytesseract
import re

# Coordinate da cui estrarre
box1 = (595, 1615, 760, 1750) # numero documento
box2 = (230, 720, 1085, 785)  # ragione sociale

def pulisci_nome(testo):
    clean = re.sub(r'[^\w\s.-]', '', testo).replace('\n', ' ').strip()[:60]
  
    # Rimuove uno o più zeri in testa se il nome inizia con cifre
    clean = re.sub(r'^0+', '', clean)
    return clean

if len(sys.argv) < 2:
    print("Uso: main.py <path_file_pdf>")
    sys.exit(1)

path_pdf = sys.argv[1]
cartella = os.path.dirname(path_pdf)

try:
    immagini = convert_from_path(path_pdf, dpi=300, first_page=1, last_page=1)
    img = immagini[0]
##########################################################################
    # (FACOLTATIVO) Visualizza l'immagine con rettangoli rossi
    show_rects = False
    if show_rects:
        draw = ImageDraw.Draw(img)
        draw.rectangle(box1, outline="red", width=3)
        draw.rectangle(box2, outline="red", width=3)
        img.show()
##########################################################################
  
    ritaglio1 = img.crop(box1)
    ritaglio2 = img.crop(box2)

    testo_estratto1 = pytesseract.image_to_string(ritaglio1, lang='eng')
    testo_estratto2 = pytesseract.image_to_string(ritaglio2, lang='eng')

    nuovo_nome_base = pulisci_nome(testo_estratto1) + " " + pulisci_nome(testo_estratto2)
    nuovo_nome_file = nuovo_nome_base + ".pdf"
    nuovo_path = os.path.join(cartella, nuovo_nome_file)

    if not os.path.exists(nuovo_path):
        os.rename(path_pdf, nuovo_path)
        print(f"Rinominato '{os.path.basename(path_pdf)}' in '{nuovo_nome_file}'")
    else:
        print(f"File '{nuovo_nome_file}' esiste già! Rinominazione saltata.")
except Exception as e:
    print(f"Errore elaborando '{os.path.basename(path_pdf)}': {e}")
