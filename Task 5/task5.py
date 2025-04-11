import os
import math
from collections import defaultdict

TF_IDF_FOLDER = "../Task 4/results"
TOKENS_FOLDER = "../Task 2/tokens"
TOP_K = 10


def load_tf_idf_vectors():
    vectors = {}
    for filename in os.listdir(TF_IDF_FOLDER):
        if filename.startswith("tf_idf_tokens_") and filename.endswith(".txt"):
            filepath = os.path.join(TF_IDF_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                vector = {}
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        term, idf, tf_idf = parts
                        vector[term] = float(tf_idf)
                vectors[filename] = vector
    return vectors


def tokenize_query(query):
    return [word.lower() for word in query.strip().split() if word.isalpha()]


def build_query_vector(query_tokens, doc_vectors):
    df = defaultdict(int)
    for vec in doc_vectors.values():
        for term in vec.keys():
            df[term] += 1

    total_docs = len(doc_vectors)

    tf = defaultdict(int)
    for token in query_tokens:
        tf[token] += 1

    query_vector = {}
    for token, freq in tf.items():
        idf = math.log((total_docs / df[token])) if df[token] > 0 else 0
        query_vector[token] = freq * idf

    return query_vector


def cosine_similarity(vec1, vec2):
    dot = 0
    norm1 = 0
    norm2 = 0

    for key in vec1:
        dot += vec1[key] * vec2.get(key, 0)
        norm1 += vec1[key] ** 2
    for val in vec2.values():
        norm2 += val ** 2

    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (math.sqrt(norm1) * math.sqrt(norm2))


def search(query, doc_vectors):
    query_tokens = tokenize_query(query)
    query_vector = build_query_vector(query_tokens, doc_vectors)

    scores = {}
    for doc, vec in doc_vectors.items():
        score = cosine_similarity(query_vector, vec)
        if score > 0:
            scores[doc] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    doc_vectors = load_tf_idf_vectors()

    while True:
        user_query = input("\nВведите поисковый запрос (или 'exit' для выхода): ").strip()
        if user_query.lower() == "exit":
            break

        results = search(user_query, doc_vectors)
        if results:
            print("\n Найденные документы:")
            for filename, score in results[:TOP_K]:
                print(f"{filename} — релевантность: {score:.4f}")
        else:
            print("Ничего не найдено.")
