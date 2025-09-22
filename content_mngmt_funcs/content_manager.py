import os
import re
import psycopg2

from content_mngmt_funcs.helpers import build_navigation, safe_id, log
from content_mngmt_funcs.html_category_placeholder_template import category_template
from content_mngmt_funcs.html_topic_paceholder_template import content_template



class ContentManager:
    file_path = os.path.join('..', 'index.html')


    def __init__(self):
        """connect to PSQL"""
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        self.conn.autocommit = True


    def update_navigation_bar(self):
        """Update navigation bar with new cats"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM nav_categories ORDER BY name;")
            categories = [row[0] for row in cur.fetchall()]

        nav_html = build_navigation(categories)

        files_to_update = [os.path.join('..', 'index.html')] + [
            os.path.join('..', f"{safe_id(cat)}.html") for cat in categories
        ]

        for file_path in files_to_update:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()

                updated_html = re.sub(
                    r"<nav>.*?</nav>",
                    nav_html,
                    html_content,
                    flags=re.DOTALL
                )

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_html)
        return log(f"Navigation updated for {len(files_to_update)} files.")

    def create_nav_category(self, category_name):
        "Create new category (those on the navigation bar)"
        if not category_name.strip():
            log(f"{category_name} is an empty string")
            return "Empty entry"

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO nav_categories (name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;",
                (category_name,)
            )
            row = cur.fetchone()  # Will be None if conflict happened
        if not row:
            log(f"{category_name} already exists")
            return "That already exists"

        safe_name = safe_id(category_name)
        file_path = os.path.join('..', f"{safe_name}.html")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(category_template)

        self.update_navigation_bar()
        return log(f"Category '{category_name}' saved to PSQL and created HTML file at {file_path}")


    def delete_nav_category(self, category_name):
        pass


    def add_topic(self, topic, category):
        if topic.strip() == '':
            log(f"{topic} is an empty string")
            return "Empty entry"

        topic_id = safe_id(topic)
        category_file = os.path.join('..', f"{safe_id(category)}.html")

        with open(category_file, 'r', encoding='utf-8') as page:
            html_content = page.read()

        new_item = content_template.replace("TITLE_ID", topic_id).replace("TITLE_NAME", topic)
        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO notes (topic, category_id)
                VALUES (%s, (SELECT id FROM nav_categories WHERE name = %s))
                ON CONFLICT (topic, category_id) DO NOTHING
                RETURNING id;
            """, (topic, category))
            row = cur.fetchone()
        if not row:
            log(f"{topic} already exists")
            return "That already exists"

        with open(category_file, 'w', encoding='utf-8') as page:
            page.write(html_content)
        return log(f'added {topic} to html and PSQL')

    def save_image_or_text_content_helper(self, topic_name, formatted_content):
        """Update the content column for an existing topic and update the topic's HTML placeholder."""

        # Update the content in the database
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE notes
                SET content = %s
                WHERE topic = %s
                RETURNING category_id;
            """, (formatted_content, topic_name))
            row = cur.fetchone()

            if not row:
                log(f"No existing topic '{topic_name}' found to update")
                return
            category_id_db = row[0]

            # Get the category name to locate the correct HTML file
            cur.execute("SELECT name FROM nav_categories WHERE id = %s", (category_id_db,))
            category_name = cur.fetchone()[0]

        # Determine HTML file path
        category_file = os.path.join('..', f"{safe_id(category_name)}.html")

        # Read HTML
        with open(category_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Replace the topic placeholder while keeping it for future updates
        topic_placeholder = f"<!--CONTENT-{safe_id(topic_name)}-->"
        html_content = html_content.replace(topic_placeholder, formatted_content + '\n' + topic_placeholder)

        # Write back
        with open(category_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        log(f"Content updated for topic '{topic_name}' in {category_file}")

    def add_content_to_topic(self, topic_name, content):
        formatted_content = (
            f'<div class="category-content">'
            f'{content.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\n", "<br>")}'
            f'</div>'
        )
        self.save_image_or_text_content_helper(topic_name, formatted_content)

    def add_pic_to_topic(self, topic_name, image_name, width: int):
        formatted_content = (
            f'<img src="cat_images/{image_name}.png" alt="{topic_name}" '
            f'width="{width}" style="display:block; margin-right:auto;">'
        )
        self.save_image_or_text_content_helper(topic_name, formatted_content)

    def delete_topic(self, category_name): #tipic
        # if category_name in self.category_name_content_pairs:
        #     self.category_name_content_pairs.pop(category_name)
        #     self.save_pairs() >> AD SQL check here

        with open(self.file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        category_id = safe_id(category_name)

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
        category_id = safe_id(category_name)

        # if category_name in self.category_name_content_pairs:
        #     self.category_name_content_pairs[category_name]["content"] = ""
        #     self.save_pairs() # Add SQL here

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
c.save_image_or_text_content_helper('test', "<div class='category-content'>Test content</div>")