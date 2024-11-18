from PIL import Image
import pytesseract
import os

# https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Funkcja OCR i zapisu do pliku
def ocr_image_to_text(image_path, output_path):
    try:
        # Wczytaj obraz
        img = Image.open(image_path)
        # Rozpoznaj tekst
        text = pytesseract.image_to_string(img, lang='pol')  # 'pol' dla polskiego
        # Zapisz tekst do pliku
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Rozpoznany tekst zapisano do pliku: {output_path}")
    except Exception as e:
        print(f"Błąd podczas przetwarzania obrazu: {e}")


# Test funkcji
if __name__ == "__main__":
    image_path = "Bez tytułu.jpg"
    output_path = "rozpoznany_tekst.txt"  # Ścieżka do pliku wynikowego
    ocr_image_to_text(image_path, output_path)
