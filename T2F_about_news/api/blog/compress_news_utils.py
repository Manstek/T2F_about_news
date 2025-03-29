from newspaper import Article
import requests


API_KEY = "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"
MODEL = "deepseek/deepseek-r1"


def fetch_article_text(url):
    """Извлекает текст статьи по указанному URL."""
    article = Article(url)
    article.download()
    article.parse()
    return article.text


def process_content(content):
    """Удаляет теги <think> и </think> из текста."""
    return content.replace('<think>', '').replace('</think>', '')


def chat(prompt):
    """Отправляет запрос к модели и возвращает ответ целиком."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты — инструмент для сжатия текста. Твоя задача — сокращать текст так, чтобы его можно было прочитать за 10-15 секунд и понять главное. Оставляй только ключевые моменты, удаляя всё лишнее."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        print("Ошибка API:", response.status_code)
        return ""

    response_data = response.json()
    if "choices" in response_data:
        content = response_data["choices"][0]["message"].get("content", "")
        return process_content(content)
    return ""
