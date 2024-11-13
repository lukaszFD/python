import re
tekst = ['Użytkownik1 uruchomił komendę: ls -la /home/użytkownik',
          'Użytkownik2 uruchomił komendę: rm -rf /home/użytkownik',
          'Użytkownik3 uruchomił komendę: sudo rm -rf /']

wzorzec = r"\b(sudo)\b"

for test in tekst:
    if re.findall(wzorzec, test):
        print(f"jest sudo w {test}.")
    else:
        print(f"brak sudo w {test}.")
