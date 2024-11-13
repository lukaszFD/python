def sprawdz_silne_haslo(x):
    if len(x) >= 8 and any(char.isdigit() for char in x) and any(char.isupper() for char in x):
        return True
    else:
        return False

haslo = input("Podaj haslo : ")
print(f"Twoje haslo to : {haslo} i spelnia watunki :  {sprawdz_silne_haslo(haslo)}")