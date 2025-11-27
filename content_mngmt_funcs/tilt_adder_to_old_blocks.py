import random
import re

def add_tilts_to_all_buttons(html: str) -> str:
    """
    Finds all <button> tags inside .grid-item divs and adds a random tilt class (tilt1-tilt5).
    Preserves existing classes.
    """
    def repl(match):
        tag = match.group(0)
        tilt_number = random.randint(1, 5)
        if 'class=' in tag:
            # Append the tilt class
            return re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} tilt{tilt_number}"', tag, count=1)
        else:
            # Add a new class attribute
            return tag.replace('<button', f'<button class="tilt{tilt_number}"', 1)

    # Replace all <button ...> tags inside .grid-item divs
    pattern = r'(<button[^>]*>)'
    return re.sub(pattern, repl, html)

# Example usage:
with open("../numpy.html", "r", encoding="utf-8") as f:
    html_content = f.read()

tilted_html = add_tilts_to_all_buttons(html_content)

with open("../numpy.html", "w", encoding="utf-8") as f:
    f.write(tilted_html)
