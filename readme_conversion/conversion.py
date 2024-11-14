import os
import markdown

# Ścieżka do katalogu z repozytoriami w folderze Dokumentów
base_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub")

# Przejście przez wszystkie podkatalogi w katalogu bazowym
for root, dirs, files in os.walk(base_path):
    if "README.md" in files:
        # Znaleziono README.md - utworzenie pełnej ścieżki
        readme_path = os.path.join(root, "README.md")

        # Wczytanie zawartości README.md
        with open(readme_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Konwersja markdown na HTML
        html_content = markdown.markdown(markdown_content)

        # Ścieżka do zapisu pliku HTML w tym samym katalogu co README.md
        html_output_path = os.path.join(root, "README.html")

        # Zapisanie wynikowego HTML
        with open(html_output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Skonwertowano {readme_path} na {html_output_path}")
