import re

_TELEGRAM_MD_CHARS = r"_*[]()~`>#+-=|{}.!\\"

def escape_md(text: str) -> str:
    return re.sub(r"([%s])" % re.escape(_TELEGRAM_MD_CHARS), r"\\\1", text or "")

def render_markdown(text: str) -> str:
    """
    Render markdown text for Telegram.
    Currently a pass-through, but provides a single place to tweak formatting.

    Args:
        text: Raw text to render

    Returns:
        Formatted text (currently unchanged)
    """
    return text

