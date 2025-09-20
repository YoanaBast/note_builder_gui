import re
import logging

logging.basicConfig(
    filename="content_manager.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def safe_id(name: str) -> str:
    """Convert name into a safe HTML ID."""
    name = name.strip()
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if safe and safe[0].isdigit():
        safe = '_' + safe
    return safe


def log_and_return(message: str) -> str:
    """Helper to log to file and return message."""
    logger.info(message)
    return message


def build_navigation(categories: list[str]) -> str:
    """Build the navigation bar HTML dynamically from categories."""
    nav_links = " | ".join(
        f'<a href="{safe_id(cat)}.html">{cat}</a>' if cat != "Python" else '<a href="index.html">Python</a>'
        for cat in categories
    )
    return f"<nav>{nav_links}</nav>"