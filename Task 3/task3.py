import os
import re
import json
from collections import defaultdict

TOKENS_DIR = "../Task2/tokens"
INDEX_FILE = "inverted_index.json"


# Создание инвертированного индекса
def build_index():
    index = defaultdict(set)

    for filename in os.listdir(TOKENS_DIR):
        if filename.startswith("tokens_") and filename.endswith(".txt"):
            file_path = os.path.join(TOKENS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                tokens = f.read().splitlines()
                for token in tokens:
                    index[token.lower()].add(filename)

    # Преобразуем множества в списки для JSON
    index = {key: list(value) for key, value in index.items()}

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)

    print("Индекс создан и сохранен в", INDEX_FILE)


# Функция для обработки булевого запроса
def boolean_search(query):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    def get_files(term):
        return set(index.get(term.lower(), []))

    def evaluate(tokens):
        stack = []
        operators = []
        precedence = {"OR": 1, "AND": 2, "NOT": 3}

        def apply_operator():
            op = operators.pop()
            if op == "NOT":
                a = stack.pop()
                all_files = set(os.listdir(TOKENS_DIR))
                stack.append(all_files - a)
            else:
                b = stack.pop()
                a = stack.pop()
                if op == "AND":
                    stack.append(a & b)
                elif op == "OR":
                    stack.append(a | b)

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    apply_operator()
                operators.pop()  # Удаляем "("
            elif token in precedence:
                while (operators and operators[-1] in precedence and
                       precedence[operators[-1]] >= precedence[token]):
                    apply_operator()
                operators.append(token)
            else:
                stack.append(get_files(token))

        while operators:
            apply_operator()

        return stack[0] if stack else set()

    query = re.findall(r"\w+|AND|OR|NOT|\(|\)", query, re.IGNORECASE)
    return evaluate(query)


if __name__ == "__main__":
    build_index()
    while True:
        user_query = input("Введите поисковый запрос (или 'exit' для выхода): ")
        if user_query.lower() == "exit":
            break
        result = boolean_search(user_query)
        print("Найденные файлы:", result)