import os
import re
import pymorphy2
from collections import defaultdict

INPUT_DIR = "../Task 1/downloaded_pages"
OUTPUT_DIR = "tokens"
os.makedirs(OUTPUT_DIR, exist_ok=True)

morph = pymorphy2.MorphAnalyzer()

# Список стоп-слов
STOP_WORDS = {"и", "в", "на", "с", "под", "за", "но", "а", "что", "как", "к", "до", "по", "из", "о", "у", "не", "же",
              "ли", "бы", "то", "от", "при", "для", "об", "про", "через"}


def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"\b[а-яё]+\b", text)
    tokens = set(tokens) - STOP_WORDS
    return sorted(tokens)



def lemmatize(tokens):
    lemmas = defaultdict(set)
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemmas[lemma].add(token)
    return lemmas

def process_files():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(INPUT_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            tokens = tokenize(text)
            lemmas = lemmatize(tokens)

            tokens_file = os.path.join(OUTPUT_DIR, f"tokens_{filename}")
            lemmas_file = os.path.join(OUTPUT_DIR, f"lemmas_{filename}")

            with open(tokens_file, "w", encoding="utf-8") as f:
                f.write("\n".join(tokens) + "\n")

            with open(lemmas_file, "w", encoding="utf-8") as f:
                for lemma, forms in lemmas.items():
                    f.write(f"{lemma} {' '.join(forms)}\n")

            print(f"Обработан {filename}")

if __name__ == "__main__":
    process_files()
