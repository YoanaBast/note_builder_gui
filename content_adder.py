import os
import re
import json
from html_template import content_template


class AddContentToPage:
    DICT_FILE = os.path.join('..', 'DB', 'category_name_file_pairs.json')
    file_path = os.path.join('..', 'index.html')


    def __init__(self):
        if os.path.exists(self.DICT_FILE):
            with open(self.DICT_FILE, 'r', encoding='utf-8') as f:
                self.category_name_content_pairs = json.load(f)
        else:
            self.category_name_content_pairs = {}


    def save_pairs(self):
        with open(self.DICT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.category_name_content_pairs, f, indent=4)


    def add_category(self, category_name):
        if category_name in self.category_name_content_pairs:
            return False  # Already exists

        self.category_name_content_pairs[category_name] = {
            "location": os.path.join('contents', f"{category_name}.html"),
            "content": ""
        }
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as page:
            html_content = page.read()

        new_item = content_template.replace("TITLE", category_name)
        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        with open(self.file_path, 'w', encoding='utf-8') as page:
            page.write(html_content)


    def add_content_to_cat(self, category_name, content):
        if category_name not in self.category_name_content_pairs:
            raise ValueError("Category does not exist")

        formatted_content = (
            f'<div class="category-content">'
            f'{content.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\n", "<br>")}'
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


    def remove_category(self, category_name):
        self.category_name_content_pairs.pop(category_name)
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        content_placeholder = f"<!--CONTENT-{category_name}-->"
        html_content = html_content.replace(content_placeholder, '')

        # This pattern matches from the opening comment to the end comment
        block_pattern = re.compile(
            rf'<!--\s*{re.escape(category_name)}\s*-->.*?<!--\s*END\s+OF\s+{re.escape(category_name)}\s*-->',
            re.DOTALL
        )
        html_content = block_pattern.sub('', html_content)

        # Additionally, remove any empty whitespace that might be left
        html_content = re.sub(r'\n\s*\n', '\n', html_content)  # Remove empty lines

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


    def remove_content_from_cat(self, category_name):
        self.category_name_content_pairs[category_name]["content"] = ""
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Regex to match everything between START-CONTENT and CONTENT placeholders
        pattern = re.compile(
            rf"(<!--START-CONTENT-{re.escape(category_name)}-->)(.*?)(<!--CONTENT-{re.escape(category_name)}-->)",
            re.DOTALL | re.IGNORECASE
        )

        # Replace the inner content with nothing, keep the placeholders
        html_content = pattern.sub(r"\1\n\3", html_content)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)



