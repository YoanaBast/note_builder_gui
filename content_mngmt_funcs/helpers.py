import os
import re
import logging

log_file = os.path.join('..', 'Logs', 'content_manager.log')

# Make sure the folder exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)




def log(message: str):
    """Helper to log to file and return message."""
    logger.info(message)
    return message


def safe_id(name: str) -> str:
    """Convert name into a safe HTML ID."""
    name = name.strip()
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if safe and safe[0].isdigit():
        safe = '_' + safe
    return safe


def build_navigation(categories: list[str]) -> str:
    """Build the navigation bar HTML dynamically from categories."""
    nav_links = " | ".join(
        f'<a href="{safe_id(cat)}.html">{cat}</a>' if cat != "Python" else '<a href="index.html">Python</a>'
        for cat in categories
    )
    return f"<nav>{nav_links}</nav>"


def python_index_checker(cat):
    """I want the python category in the index file as it needs to be called index for publishing in github"""
    if cat == 'Python':
        cr = 'index'
    else:
        cr = cat
    return cr
