import os
import re
import json
from content_mngmt_funcs.html_template import content_template


class ContentManager:
    DICT_FILE = os.path.join('../..', 'DB', 'category_name_file_pairs.json')
    file_path = os.path.join('../..', 'index.html')


    def __init__(self):
        if os.path.exists(self.DICT_FILE):
            with open(self.DICT_FILE, 'r', encoding='utf-8') as f:
                self.category_name_content_pairs = json.load(f)
        else:
            self.category_name_content_pairs = {}


    @staticmethod
    def safe_id(name: str) -> str:
        name = name.strip()
        # Replace any non-alphanumeric character with an underscore
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure it doesn't start with a digit (HTML IDs can't start with a number)
        if safe and safe[0].isdigit():
            safe = '_' + safe
        return safe

    def save_pairs(self):
        with open(self.DICT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.category_name_content_pairs, f, indent=4)


    def add_category(self, category_name):
        if category_name.strip() == '':
            return 'Empty string'

        category_id = self.safe_id(category_name)

        self.category_name_content_pairs[category_name] = {
            "location": os.path.join('contents', f"{category_name}.html"),
            "content": ""
        }
        self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as page:
            html_content = page.read()

        new_item = content_template.replace("TITLE_ID", category_id).replace("TITLE_NAME", category_name)

        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        with open(self.file_path, 'w', encoding='utf-8') as page:
            page.write(html_content)

        return 'all good'

    def save_content(self, category_name, formatted_content):
        # Save in dictionary
        self.category_name_content_pairs[category_name]["content"] = formatted_content
        self.save_pairs()

        category_id = self.safe_id(category_name)  # <-- use safe ID

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        placeholder = f"<!--CONTENT-{category_id}-->"
        html_content = html_content.replace(placeholder, formatted_content + '\n' + placeholder)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def add_content_to_cat(self, category_name, content):
        formatted_content = (
            f'<div class="category-content">'
            f'{content.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\n", "<br>")}'
            f'</div>'
        )
        self.save_content(category_name, formatted_content)


    def add_pic_to_cat(self, category_name, image_name, width: int):
        formatted_content = f'<img src="cat_images/{image_name}.png" alt="{category_name}" width="{width}" style="display:block; margin-right:auto;">'
        self.save_content(category_name, formatted_content)


    def remove_category(self, category_name):
        if category_name in self.category_name_content_pairs:
            self.category_name_content_pairs.pop(category_name)
            self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        category_id = self.safe_id(category_name)

        # Remove the content placeholder if present
        content_placeholder = f"<!--CONTENT-{category_id}-->"
        html_content = html_content.replace(content_placeholder, '')

        # Remove the full category block, from opening comment to END comment
        block_pattern = re.compile(
            rf'<!--\s*{re.escape(category_name)}\s*-->.*?<!--\s*END\s+OF\s+{re.escape(category_name)}\s*-->',
            re.DOTALL
        )
        html_content = block_pattern.sub('', html_content)

        # Clean up extra empty lines
        html_content = re.sub(r'\n\s*\n', '\n', html_content)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def remove_content_from_cat(self, category_name):
        category_id = self.safe_id(category_name)

        if category_name in self.category_name_content_pairs:
            self.category_name_content_pairs[category_name]["content"] = ""
            self.save_pairs()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Remove only the content between the START-CONTENT and CONTENT placeholders
        pattern = re.compile(
            rf'(<!--START-CONTENT-{re.escape(category_id)}-->).*?(<!--CONTENT-{re.escape(category_id)}-->)',
            re.DOTALL
        )
        html_content = pattern.sub(r'\1\n\2', html_content)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
