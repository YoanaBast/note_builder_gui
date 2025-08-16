import os
import re
import json
import textwrap

class AddContentToPage:
    DICT_FILE = os.path.join('..', 'DB', 'category_name_file_pairs.json')

    content_template = textwrap.dedent("""\
        <!-- TITLE -->
        <div class="grid-item">
            <button id="openBtn-TITLE">TITLE</button>
            <div id="myModal-TITLE" class="modal">
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>TITLE</h2>
                    <p><!--CONTENT-TITLE--></p>
                </div>
            </div>
            <script>
                const modalTITLE = document.getElementById("myModal-TITLE");
                const btnTITLE = document.getElementById("openBtn-TITLE");
                const spanTITLE = modalTITLE.querySelector(".close");

                btnTITLE.onclick = () => modalTITLE.style.display = "block";
                spanTITLE.onclick = () => modalTITLE.style.display = "none";
                window.onclick = (event) => {
                    if(event.target === modalTITLE) modalTITLE.style.display = "none";
                }
            </script>
        </div>
        <!-- ENF OF TITLE -->
    """)


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
        if category_name in self.category_name_content_pairs:
            return f'Category {category_name} already exists'

        # track category file
        self.category_name_content_pairs[category_name] = {
            "location": os.path.join('contents', f"{category_name}.html"),
            "content": ""
        }
        self.save_pairs()

        main_web = os.path.join('..', 'main_web_folder', 'main_web.html')

        with open(main_web, 'r') as page:
            html_content = page.read()

        # replace placeholder in template
        new_item = self.content_template.replace("TITLE", category_name)

        # insert new grid-item before placeholder
        html_content = html_content.replace(
            "<!-- INSERT_CATEGORIES_HERE -->",
            f"{new_item}\n<!-- INSERT_CATEGORIES_HERE -->"
        )

        with open(main_web, 'w') as page:
            page.write(html_content)


    def add_content_to_cat(self, category_name, content):
        self.category_name_content_pairs[category_name]["content"] += f"<p>{content}</p>\n"
        self.save_pairs()

        file_path = os.path.join('..', 'main_web_folder', 'main_web.html')

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        placeholder = f"<!--CONTENT-{category_name}-->"
        html_content = html_content.replace(placeholder, f"<p>{content}</p>\n" + placeholder)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

