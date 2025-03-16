import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ru.top-cat.org/breeds-articles?page={}"
OUTPUT_DIR = "downloaded_pages"
INDEX_FILE = "index.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_article_links():
    links = []
    for page in range(1, 7):
        url = BASE_URL.format(page)
        print(f"Скачиваем список статей с {url}...")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка загрузки {url}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.select("a[href^='/breeds-articles/']"):
            href = a["href"]
            full_url = "https://ru.top-cat.org" + href
            if href.startswith("/breeds-articles/") and href.count("/") == 2:
                links.append(full_url)

    links = list(set(links))[:120]
    return links


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style", "link"]):
        script.decompose()
    return str(soup)


def download_page(url, file_number):
    print(f"Скачиваем: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка загрузки {url}: {response.status_code}")
        return None

    cleaned_html = clean_html(response.text)
    filename = os.path.join(OUTPUT_DIR, f"page_{file_number}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_html)

    print(f"Сохранено: {filename}")
    return filename


def main():
    links = get_article_links()
    if not links:
        print("Список ссылок пуст. Проверьте структуру страниц.")
        return

    with open(INDEX_FILE, "w", encoding="utf-8") as index:
        for i, link in enumerate(links):
            filename = download_page(link, i + 1)
            if filename:
                index.write(f"{i + 1} {link}\n")

if __name__ == "__main__":
    main()