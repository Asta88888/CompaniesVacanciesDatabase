import re
import html

def cleaner(raw_html: str) -> str:
    """Удаляет HTML-теги и декодирует HTML-сущности из строки"""
    no_tags = re.sub(r'<[^>]+>', '', raw_html)
    clean_text = html.unescape(no_tags)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()