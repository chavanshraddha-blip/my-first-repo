import re
import bleach

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
    'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'span',
    'u', 's', 'strike', 'sub', 'sup', 'br', 'hr', 'img'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height', 'class'],
    '*': ['class', 'style']
}

ALLOWED_STYLES = [
    'color', 'background-color', 'font-size', 'text-align', 'font-weight', 'text-decoration'
]


def clean_html(raw_html):
    """Sanitize HTML from rich text editor to prevent XSS attacks."""
    if not raw_html:
        return ''
    try:
        cleaned = bleach.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            styles=ALLOWED_STYLES,
            strip=True
        )
        return cleaned
    except Exception:
        # Fallback if bleach fails
        return raw_html


def generate_slug(text):
    """Generate a clean URL slug from title text."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:160]
