import os
from fpdf import FPDF, XPos, YPos
import urllib.request

# Ustawienia FTP
ftp_url = "ftp://192.168.56.101/test.txt"  # Podmień na właściwy adres FTP
local_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "test.txt")

# Funkcja do pobierania pliku z FTP
def download_file(ftp_url, local_file_path):
    try:
        urllib.request.urlretrieve(ftp_url, local_file_path)
        print(f"Pobrano plik na pulpit: {local_file_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania pliku: {e}")

# Tworzenie pliku PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Dodanie linku do PDF
pdf.cell(200, 10, text="Kliknij tutaj, aby pobrać plik test.txt",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT,
         link=ftp_url)

# Zapisz PDF
pdf_output_path = os.path.join(os.getcwd(), "ftp_link_example.pdf")
pdf.output(pdf_output_path)
print(f"Plik PDF został zapisany jako: {pdf_output_path}")

# Użytkownik musi samodzielnie pobrać plik, klikając w link w PDF
print("Aby pobrać plik, otwórz PDF i kliknij w link.")