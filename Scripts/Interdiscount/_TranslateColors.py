# Translation dictionary for German to English
translation_dict = {
    "Titan Natur": "Nature Titanium",
    "Titan Blau": "Blue Titanium",
    "Titan": "Titanium",
    "Schwarz": "Black",
    "Blau": "Blue",
    "Mitternacht": "Midnight",
    "Polarstern": "Polar Star",
    "Grün": "Green",
    "Weiss": "White",
    "Violett": "Violet",
    "Gelb": "Yellow",
    "Schwarzblau": "Black-blue",
    "Dunkelblau": "Dark blue",
    "Mintgrün": "Mint green",
    "Mattschwarz": "Matte black",
    "Grau": "Gray",
    "Waldgrün": "Forest green",
    "Hellblau": "Light blue",
    "Rot": "Red",
    "Eisblau": "Ice blue",
    "Hellgrün": "Light green",
    "Silber": "Silver",
    "Mitternachtsblau": "Midnight blue",
}

def translate_and_lowercase(color):
    if color:
        # Replace German words with English equivalents
        for german_word in sorted(translation_dict.keys(), key=len, reverse=True):
            english_word = translation_dict[german_word]
            color = color.replace(german_word, english_word)
        return color.lower()
    else:
        return None

def corrector(color):
    if color:
        words = color.split()
        # Replace "titaniumnium" with "titan" for each word
        updated_words = [word.replace('titaniumium', 'titanium') for word in words]
        return ' '.join(updated_words)
    else:
        return None