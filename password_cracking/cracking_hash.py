import requests
from bs4 import BeautifulSoup
import re
import random
import hashlib
import json
import os

# Pobiera HTML strony
def get_html_of(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Sprawdza, czy kod odpowiedzi jest 2xx
        return resp.content.decode()
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania strony {url}: {e}")
        return None  # Zwraca None, gdy nie uda się pobrać strony

# Wyodrębnia słowa ze strony
def get_all_words_from(url):
    html = get_html_of(url)
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return [word for word in re.findall(r'\w+', raw_text) if len(word) >= 5]

# Zlicza wystąpienia słów
def count_occurrences_in(word_list):
    word_count = {}
    for word in word_list:
        word_count[word] = word_count.get(word, 0) + 1
    return sorted(word_count.items(), key=lambda item: item[1], reverse=True)

# Generuje mutacje dla słowa
def generate_password_mutations(word):
    mutations = [word, word.capitalize(), word.upper(), word + "123", word + "!", word + "@2023"]
    mutations.append(word * 2)
    mutations.append(word.capitalize() + word.upper())

    # Zamiana liter na symbole
    substitutions = {
        'a': '@', 's': '$', 'o': '0', 'e': '3', 'i': '1', 't': '7'
    }
    mutated_word = ''.join(substitutions.get(c, c) for c in word.lower())
    mutations.append(mutated_word)

    # Losowe mieszanie wielkości liter
    mixed_case = ''.join(random.choice([str.upper, str.lower])(c) for c in word)
    mutations.append(mixed_case)

    # Dodawanie zakończeń do słowa
    endings = ["123", "01", "99", "999", "!", "!!!", "@2023", "2023", "2024", "2025", "_", "*"]
    for ending in endings:
        mutations.append(word + ending)

    # Same symbole na końcu słowa
    symbols = ["*", "#", "@", "$", "##", "#@"]
    for symbol in symbols:
        mutations.append(word + symbol)

    return mutations


# Funkcja do generowania hash'a hasła
def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Zapisuje listę loginów i ich mutacji do pliku JSON w bieżącym katalogu
def save_to_json(data, filename):
    current_directory = os.getcwd()  # Bieżący katalog roboczy
    file_path = os.path.join(current_directory, filename)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Wyniki zapisane do {file_path}")

# Wczytanie danych z pliku data.json
def load_data_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return []
    except json.JSONDecodeError:
        print(f"Plik {filename} zawiera nieprawidłowy format JSON.")
        return []

# Wczytanie danych z pliku
data = load_data_from_json('data.json')

# Lista do zapisania wyników
output_data = []

# Wyodrębnij i przetwórz dane
for entry in data:
    print(f"Przetwarzam: {entry['login']}")
    url = 'https://en.wikipedia.org/wiki/' + entry["login"]
    all_words = get_all_words_from(url)

    # Sprawdzanie, czy udało się pobrać słowa
    if not all_words:
        print(f"Pominięto login {entry['login']} z powodu błędu pobierania strony.")
        continue  # Pomija wpis, jeśli strona nie została pobrana

    occurrences = count_occurrences_in(all_words)

    # Generowanie mutacji dla każdego słowa z listy occurrences
    for word, _ in occurrences:
        mutations = generate_password_mutations(word)

        # Dodajemy dodatkową mutację z połączeniem loginu i słowa
        login_word_mutation = entry['login'] + word
        mutations.append(login_word_mutation)

        # Dodanie loginu oraz mutacji do listy
        for mutation in mutations:
            entry_copy = entry.copy()
            entry_copy["password"] = mutation
            entry_copy["password_hash"] = generate_password_hash(mutation)
            output_data.append(entry_copy)

# Zapisanie danych do pliku JSON w bieżącym katalogu
save_to_json(output_data, 'output_data.json')

# Wczytanie danych z pliku JSON
def load_data_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return []
    except json.JSONDecodeError:
        print(f"Plik {filename} zawiera nieprawidłowy format JSON.")
        return []

# Zapisanie danych do pliku JSON
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Wyniki zapisane do {filename}")

# Funkcja do porównania danych
def compare_and_extract(data_file, output_file):
    # Wczytanie danych
    data = load_data_from_json(data_file)
    output_data = load_data_from_json(output_file)

    matched_data = []

    # Tworzymy słownik loginów i haszy z output_data
    output_dict = {entry["login"]: entry["password_hash"] for entry in output_data}

    # Porównujemy dane z data.json z output_dict
    for entry in data:
        login = entry.get("login")
        password = entry.get("password")
        password_hash = output_dict.get(login)

        # Sprawdzamy, czy istnieje dopasowanie
        if password_hash and hashlib.sha256(password.encode()).hexdigest() == password_hash:
            matched_data.append({"login": login, "password": password})

    # Zapisanie dopasowanych danych do nowego pliku JSON
    save_to_json(matched_data, 'matched_data.json')

# Uruchomienie funkcji porównującej dane
compare_and_extract('data.json', 'output_data.json')

