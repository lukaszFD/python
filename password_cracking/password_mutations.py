import random

def generate_password_mutations(password_file):
    mutations = []
    endings = ["2024", "2025", "2023", "2026", "_2024", "_2025"]  # Lista zakończeń, które mają być dodawane

    # Open the password file and read each line (password)
    with open(password_file, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()

            # Base mutations
            word_mutations = [
                word,  # Original password
                word.capitalize(),  # Capitalized version
                word.upper(),  # Uppercase version
                word + "123",  # Add a number at the end
                word + "!",  # Add a symbol
                word + "@2023"  # Add a year-based suffix
            ]
            word_mutations.append(word * 2)  # Repeated word
            word_mutations.append(word.capitalize() + word.upper())  # Capital + Uppercase

            # Zamiana liter na symbole
            substitutions = {
                'a': '@', 's': '$', 'o': '0', 'e': '3', 'i': '1', 't': '7'
            }
            mutated_word = ''.join(substitutions.get(c, c) for c in word.lower())
            word_mutations.append(mutated_word)

            # Random letter case mixing
            mixed_case = ''.join(random.choice([str.upper, str.lower])(c) for c in word)
            word_mutations.append(mixed_case)

            # Adding endings to the word
            for ending in endings:
                word_mutations.append(word + ending)

            # Same symbols at the end of the word
            symbols = ["*", "#", "@", "$", "##", "#@"]
            for symbol in symbols:
                word_mutations.append(word + symbol)

            # New mutation: Capitalize first two letters and add endings
            if word.isalpha():  # Check if the word contains only letters
                capitalized_first_two = word[:2].upper() + word[2:]  # Capitalize first two letters
                for ending in endings:
                    word_mutations.append(capitalized_first_two + ending)  # Add endings to the capitalized word

            mutations.extend(word_mutations)

    return mutations
