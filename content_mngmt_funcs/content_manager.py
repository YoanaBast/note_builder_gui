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
        """Refresh navigation bar with latest info"""

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
        "Delete a category from the nav bar and remove its HTML file"

        if not category_name.strip():
            log(f"{category_name} is an empty string")
            return "Empty entry"

        # del from PSQL
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM nav_categories WHERE name = %s RETURNING id;",
                (category_name,)
            )
            row = cur.fetchone()  # Will be None if category didn't exist

        if not row:
            log(f"Category '{category_name}' does not exist")
            return "Category does not exist"

        # del HTML
        safe_name = safe_id(category_name)
        file_path = os.path.join('..', f"{safe_name}.html")
        if os.path.exists(file_path):
            os.remove(file_path)
            log(f"Deleted HTML file {file_path}")
        else:
            log(f"No HTML file to delete for {file_path}")

        self.update_navigation_bar()
        return log(f"Category '{category_name}' deleted successfully")


    def add_topic(self, topic, category):
        """Add topic to a category"""

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


    def remove_topic(self, topic, category):
        """Remove a topic from a category (DB + HTML)"""

        topic = topic.strip()
        category = category.strip()
        if not topic:
            log("Topic is empty")
            return "Empty entry"

        topic_id = safe_id(topic)
        category_file = os.path.join('..', f"{safe_id(category)}.html")

        # remove from PSQL
        with self.conn.cursor() as cur:
            cur.execute("""
                DELETE FROM notes
                WHERE topic = %s
                  AND category_id = (SELECT id FROM nav_categories WHERE name ILIKE %s)
                RETURNING id;
            """, (topic, category))
            row = cur.fetchone()

        if not row:
            log(f"Topic '{topic}' does not exist in category '{category}'")
            return "Topic does not exist"

        # remove from HTML
        if os.path.exists(category_file):
            with open(category_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            import re
            # Match everything from <!-- topic --> to <!-- END OF topic -->
            pattern = rf'<!-- {re.escape(topic)} -->.*?<!-- END OF {re.escape(topic)} -->\s*'
            new_content, count = re.subn(pattern, '', html_content, flags=re.DOTALL)

            if count == 0:
                log(f"Warning: topic '{topic}' not found in HTML")

            with open(category_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

        log(f"Removed topic '{topic}' from category '{category}' (DB + HTML)")
        return f"Removed '{topic}'"


    def save_image_or_text_content_helper(self, topic_name, formatted_content):
        """Update the content column for an existing topic and update the topic's HTML placeholder."""

        # update the content in the database
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

            # get the category name to locate the correct HTML file
            cur.execute("SELECT name FROM nav_categories WHERE id = %s", (category_id_db,))
            category_name = cur.fetchone()[0]

        category_file = os.path.join('..', f"{safe_id(category_name)}.html")

        with open(category_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # replace the topic placeholder while keeping it for future updates
        topic_placeholder = f"<!--CONTENT-{safe_id(topic_name)}-->"
        html_content = html_content.replace(topic_placeholder, formatted_content + '\n' + topic_placeholder)

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


    def remove_content_from_topic(self, topic, category):
        topic = topic.strip()
        category = category.strip()
        if not topic or not category:
            log("Topic or category is empty")
            return "Empty entry"

        topic_id = safe_id(topic)
        category_id = safe_id(category)
        category_file = os.path.join('..', f"{category_id}.html")

        #remove content from SQL
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE notes
                SET content = ''
                WHERE topic ILIKE %s
                  AND category_id = (SELECT id FROM nav_categories WHERE name ILIKE %s)
                RETURNING id;
            """, (topic, category))
            row = cur.fetchone()
            if not row:
                log(f"No content found for topic '{topic}' in category '{category}'")

        #remove content from HTML
        if os.path.exists(category_file):
            with open(category_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Remove only the content between the START-CONTENT and CONTENT placeholders for this topic
            pattern = re.compile(
                rf'(<!--START-CONTENT-{re.escape(topic_id)}-->).*?(<!--CONTENT-{re.escape(topic_id)}-->)',
                re.DOTALL
            )
            new_html_content, count = pattern.subn(r'\1\n\2', html_content)
            if count == 0:
                log(f"Warning: content placeholder not found in HTML for topic '{topic}'")

            with open(category_file, 'w', encoding='utf-8') as f:
                f.write(new_html_content)

        log(f"Cleared content for topic '{topic}' in category '{category}' (DB + HTML)")
        return f"Content cleared for '{topic}'"


