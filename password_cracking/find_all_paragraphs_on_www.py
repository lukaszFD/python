import requests
from bs4 import BeautifulSoup

url = 'https://pl-pl.facebook.com/public/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Znajdź wszystkie paragrafy na stronie
paragrafy = soup.find_all('p')

for p in paragrafy:
    print(p.text)