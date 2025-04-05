import os
import math

tokens_path = "../Task 2/tokens"
lemmas_path = "../Task 2/lemmas"
OUTPUT_DIR = "tf_idf_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

token_files = [f for f in os.listdir(tokens_path) if f.endswith(".txt")]
lemma_files = [f for f in os.listdir(lemmas_path) if f.endswith(".txt")]


def compute_raw_tf(doc):
    tf = {}
    for term in doc:
        if term in tf:
            tf[term] += 1
        else:
            tf[term] = 1
    return tf


def compute_idf(files, path):
    idf = {}
    total_documents = len(files)

    term_document_frequency = {}
    for filename in files:
        with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
            terms = f.read().split()
            unique_terms = set(terms)
            for term in unique_terms:
                if term in term_document_frequency:
                    term_document_frequency[term] += 1
                else:
                    term_document_frequency[term] = 1

    for term, df in term_document_frequency.items():
        idf[term] = math.log(total_documents / df)

    return idf


def save_to_file(file_name, tf_data, idf_data):
    with open(file_name, "w", encoding="utf-8") as f:
        for term, tf in tf_data.items():
            idf_value = idf_data.get(term, 0)
            tf_idf = tf * idf_value
            f.write(f"{term} {idf_value} {tf_idf}\n")


idf_tokens = compute_idf(token_files, tokens_path)
idf_lemmas = compute_idf(lemma_files, lemmas_path)

for token_file, lemma_file in zip(token_files, lemma_files):
    print(f"Processing {token_file} and {lemma_file}...")

    with open(os.path.join(tokens_path, token_file), "r", encoding="utf-8") as f:
        tokens = f.read().split()

    with open(os.path.join(lemmas_path, lemma_file), "r", encoding="utf-8") as f:
        lemmas = f.read().split()

    tf_tokens = compute_raw_tf(tokens)
    tf_lemmas = compute_raw_tf(lemmas)

    save_to_file(f"tf_idf_tokens_{token_file}", tf_tokens, idf_tokens)

    save_to_file(f"tf_idf_lemmas_{lemma_file}", tf_lemmas, idf_lemmas)

    print(f"Results for {token_file} and {lemma_file} saved.")
