import requests
from bs4 import BeautifulSoup
import re

def get_html_of(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'Błąd pobierania strony: kod {resp.status_code}')
        exit(1)
    return resp.content.decode()

def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    # Zwracamy tylko słowa o długości co najmniej 5 znaków
    return [word for word in re.findall(r'\w+', raw_text) if len(word) >= 5]


print(get_all_words_from('https://en.wikipedia.org/wiki/leonardo_da_vinci'))  # wyświetl pierwsze 10 słów