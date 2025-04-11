import os
import math
import re
from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

TF_IDF_FOLDER = "../Task 4/results"
HTML_FOLDER = "../Task 1/downloaded_pages"
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
                        term, _, tf_idf = parts
                        vector[term.lower()] = float(tf_idf)
                vectors[filename] = vector
    return vectors

def tokenize_query(query):
    return [word.lower() for word in re.findall(r'\b\w+\b', query)]

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

def extract_snippet(text, query_tokens):
    for token in query_tokens:
        match = re.search(re.escape(token), text, re.IGNORECASE)
        if match:
            idx = match.start()
            start = max(idx - 50, 0)
            end = min(idx + 100, len(text))
            snippet = text[start:end]
            for t in query_tokens:
                snippet = re.sub(f"(?i)({re.escape(t)})", r"<mark>\1</mark>", snippet)
            return snippet
    return ""

def search(query, doc_vectors):
    query_tokens = tokenize_query(query)
    query_vector = build_query_vector(query_tokens, doc_vectors)

    scores = {}
    for doc, vec in doc_vectors.items():
        score = cosine_similarity(query_vector, vec)
        if score > 0:
            scores[doc] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:TOP_K]

    results = []
    for filename, score in ranked:
        page_number = filename.replace("tf_idf_tokens_tokens_page_", "").replace(".txt", "")
        html_path = os.path.join(HTML_FOLDER, f"page_{page_number}.txt")

        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
                clean_text = re.sub(r"<[^>]+>", "", html)
                snippet = extract_snippet(clean_text, query_tokens)
                results.append((f"Страница {page_number}", float(score), snippet))
        else:
            results.append((f"Страница {page_number}", float(score), "<em>HTML не найден</em>"))

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("query", "")
        if query:
            results = search(query, doc_vectors)
    return render_template("index.html", query=query, results=results)

if __name__ == "__main__":
    doc_vectors = load_tf_idf_vectors()
    app.run(debug=True)
