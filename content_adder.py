import os
import re
import html
import json
from html_template import content_template


def extract_block(hc, category_name):
    pattern = re.compile(
        rf"<!-- {category_name} -->(.*?)<!-- ENF OF {category_name} -->",
        re.DOTALL
    )
    match = pattern.search(hc)
    return match.group(0) if match else None  # full block including comments


class AddContentToPage:
    DICT_FILE = os.path.join('..', 'DB', 'category_name_file_pairs.json')
    file_path = os.path.join('..', 'index.html')


    def __init__(self):
        # Load existing data from JSON or start empty
        if os.path.exists(self.DICT_FILE):
            with open(self.DICT_FILE, 'r', encoding='utf-8') as f:
                self.category_name_content_pairs = json.load(f)
        else:
            self.category_name_content_pairs = {}


    def save_pairs(self):
        with open(self.DICT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.category_name_content_pairs, f, indent=4)


    def add_category(self, category_name):
        self.category_name_content_pairs[category_name] = {
            "location": os.path.join('contents', f"{category_name}.html"),
            "content": ""
        }
        self.save_pairs()

        with open(self.file_path, 'r') as page:
            html_content = page.read()

        new_item = content_template.replace("TITLE", category_name)
        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        with open(self.file_path, 'w') as page:
            page.write(html_content)

    def add_content_to_cat(self, category_name, content):
        # Convert tabs and newlines; spaces can remain normal since CSS will preserve them
        formatted_content = content.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;').replace('\n', '<br>')

        # Wrap in a div styled for code, left-aligned
        formatted_content = (
            f'<div style="font-family: monospace; white-space: pre-wrap; text-align: left;">'
            f'{formatted_content}'
            f'</div>'
        )


        self.category_name_content_pairs[category_name]["content"] = formatted_content
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        placeholder = f"<!--CONTENT-{category_name}-->"
        html_content = html_content.replace(placeholder, formatted_content + '\n' + placeholder)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def remove_category(self, cat):
        self.category_name_content_pairs.pop(cat)
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        block = extract_block(html_content, cat)
        html_content = html_content.replace(block, '')

        with open(self.file_path, 'w') as page:
            page.write(html_content)


