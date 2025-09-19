import os
import re
import psycopg2
from content_mngmt_funcs.html_category_placeholder_template import category_template
from content_mngmt_funcs.html_topic_paceholder_template import content_template



class ContentManager:
    file_path = os.path.join('..', 'index.html')

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        self.conn.autocommit = True


    @staticmethod
    def safe_id(name: str) -> str:
        name = name.strip()
        # Replace any non-alphanumeric character with an underscore
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure it doesn't start with a digit (HTML IDs can't start with a number)
        if safe and safe[0].isdigit():
            safe = '_' + safe
        return safe


    def create_nav_category(self, category_name):
        if not category_name.strip():
            return "Empty category name"

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO nav_categories (name) VALUES (%s) ON CONFLICT DO NOTHING;",
                (category_name,)
            )

        safe_name = self.safe_id(category_name)
        file_path = os.path.join('..', f"{safe_name}.html")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(category_template)

        return f"Category '{category_name}' saved to DB and created HTML file at {file_path}"


    def add_topic(self, topic, category):
        if topic.strip() == '':
            return 'Empty string'
        topic_id = self.safe_id(topic)
        category_file = os.path.join('..', f"{self.safe_id(category)}.html")

        with open(category_file, 'r', encoding='utf-8') as page:
            html_content = page.read()

        new_item = content_template.replace("TITLE_ID", topic_id).replace("TITLE_NAME", topic)
        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        #save to DB
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO notes (topic, from_category)
                VALUES (%s, (SELECT id FROM nav_categories WHERE name = %s))
                ON CONFLICT DO NOTHING;
            """, (topic, category))
        #save to HTML
        with open(category_file, 'w', encoding='utf-8') as page:
            page.write(html_content)
        return 'added cat to html and DB'


    def save_image_or_text_content_helper(self, category_name, formatted_content, topic):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO notes (topic, content, from_category)
                VALUES (%s, %s, (SELECT id FROM nav_categories WHERE name = %s))
                RETURNING id;
            """, (topic, formatted_content, category_name))
            note_id = cur.fetchone()[0]

        category_id = self.safe_id(category_name)

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
        self.save_image_or_text_content_helper(category_name, formatted_content)


    def add_pic_to_cat(self, category_name, image_name, width: int):
        formatted_content = f'<img src="cat_images/{image_name}.png" alt="{category_name}" width="{width}" style="display:block; margin-right:auto;">'
        self.save_image_or_text_content_helper(category_name, formatted_content)


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

c = ContentManager()
c.create_nav_category('test13')