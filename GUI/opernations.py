import os
import tkinter as tk
from helpers import clean_screen, add_background, clear_labels, show_enter_back_buttons, create_category_topic_labels, \
    check_img_name, update_status
from canvas import app
from content_mngmt_funcs.content_manager import ContentManager

content_manager = ContentManager()

def create_category_topic_dropdown(frame, category_label="Category:", topic_label="Topic:"):
    """Creates a category dropdown and a dependent topic dropdown inside frame."""
    frame.success_label = None
    frame.error_label = None

    #Category
    tk.Label(frame, text=category_label, font=("Arial", 18), anchor="w").pack(anchor='w')
    with content_manager.conn.cursor() as cur:
        cur.execute("SELECT name FROM nav_categories;")
        categories = [row[0] for row in cur.fetchall()]

    if not categories:
        render_no_topic_selected(frame)
        return None, None, None

    category_var = tk.StringVar(value="Choose a category")
    category_dropdown = tk.OptionMenu(frame, category_var, *categories)
    category_dropdown.config(font=("Arial", 16), width=25, bg="white", fg="black")
    category_dropdown.pack(anchor="w")

    #Topic
    tk.Label(frame, text=topic_label, font=("Arial", 18), anchor="w").pack(anchor='w', pady=(10, 0))
    topic_var = tk.StringVar(value="Choose a topic")
    topic_dropdown = tk.OptionMenu(frame, topic_var, "")
    topic_dropdown.config(font=("Arial", 16), width=25, bg="white", fg="black")
    topic_dropdown.pack(anchor="w")

    # Update topic dropdown when category changes
    def update_topic_dropdown(*args):
        clear_labels(frame)
        category = category_var.get()
        menu = topic_dropdown["menu"]
        menu.delete(0, "end")
        if category == "Choose a category":
            topic_var.set("Choose a topic")
            return

        with content_manager.conn.cursor() as cur:
            cur.execute(
                "SELECT topic FROM notes n JOIN nav_categories nc ON n.category_id = nc.id WHERE nc.name = %s",
                (category,)
            )
            topics = [row[0] for row in cur.fetchall()]

        if topics:
            for t in topics:
                menu.add_command(label=t, command=lambda value=t: topic_var.set(value))
            topic_var.set("Choose a topic")
        else:
            topic_var.set("No topics")

    category_var.trace_add("write", update_topic_dropdown)
    return category_var, topic_var, topic_dropdown



def create_category_labels(cat_name_entry, frame):
    create_category_topic_labels(frame, content_manager.create_nav_category(cat_name_entry.get().strip()))


def create_topic_labels(topic_name_entry, category, frame):
    result = content_manager.add_topic(topic_name_entry.get().strip(), category)
    create_category_topic_labels(frame, result)


def render_no_topic_selected(frame):
    frame.pack(fill='x', anchor='w', pady=10, padx=15)

    tk.Label(frame, text="Please add categories first!",
             font=("Arial", 18), anchor="w").pack(side='left')

    back_frame = tk.Frame(app)
    back_frame.pack(anchor='w', pady=10, padx=20)

    back_button = tk.Button(back_frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=render_back_to_main)
    back_button.pack(side="left")


def display_topic_dropdown():
    clean_screen()
    topic_dropdown_frame = tk.Frame(app)
    topic_dropdown_frame.success_label = None
    topic_dropdown_frame.pack(fill='x', pady=10, padx=15)

    with content_manager.conn.cursor() as cur:
        cur.execute("SELECT topic FROM notes;")
        topics = [row[0] for row in cur.fetchall()]

        dropdown_frame = tk.Frame(app)
        dropdown_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        tk.Label(topic_dropdown_frame, text="Topic:", font=("Arial", 18), anchor="w").pack(anchor='w')

        selected = tk.StringVar(value="Choose a topic")

        dropdown = tk.OptionMenu(dropdown_frame, selected, *topics)
        dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
        dropdown.pack(anchor="w")  # align left
        return selected, topic_dropdown_frame


def display_category_dropdown():
    clean_screen()
    category_dropdown_frame = tk.Frame(app)
    category_dropdown_frame.success_label = None
    category_dropdown_frame.pack(fill='x', pady=10, padx=15)

    with content_manager.conn.cursor() as cur:
        cur.execute("SELECT name FROM nav_categories;")
        categories = [row[0] for row in cur.fetchall()]
    if len(categories) < 1:
        render_no_topic_selected(category_dropdown_frame)

    else:
        dropdown_frame = tk.Frame(app)
        dropdown_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        tk.Label(category_dropdown_frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

        selected = tk.StringVar(value="Choose a category")

        dropdown = tk.OptionMenu(dropdown_frame, selected, *categories)
        dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
        dropdown.pack(anchor="w")  # align left
        return selected, category_dropdown_frame




def render_back_to_main():
    clean_screen()
    render_main_enter_screen()


def render_add_category():
    clean_screen()

    cat_name_frame = tk.Frame(app)
    cat_name_frame.error_label = None
    cat_name_frame.success_label = None
    cat_name_frame.pack(fill='x', pady=10, padx=15)

    tk.Label(cat_name_frame, text="Category Name:", font=("Arial", 18), width=15, anchor="w").pack(side='left')

    cat_name = tk.Entry(cat_name_frame, width=15, font=("Arial", 18))
    cat_name.pack(side='left', padx=5)

    show_enter_back_buttons(lambda: create_category_labels(cat_name, cat_name_frame), render_back_to_main)


def render_remove_cat():
    clean_screen()

    frame = tk.Frame(app)
    frame.pack(fill='x', pady=10, padx=15, anchor='w')
    frame.success_label = None
    frame.error_label = None

    tk.Label(frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

    # get categories from SQL
    with content_manager.conn.cursor() as cur:
        cur.execute("SELECT name FROM nav_categories;")
        categories = [row[0] for row in cur.fetchall()]

    if not categories:
        render_no_topic_selected(frame)
        return

    dropdown_var = tk.StringVar(value="Choose a category")
    dropdown = tk.OptionMenu(frame, dropdown_var, *categories)
    dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
    dropdown.pack(anchor="w")

    # hide labels when dropdown changes
    def on_dropdown_change(*args):
        clear_labels(frame)

    dropdown_var.trace_add("write", on_dropdown_change)

    # callback
    def remove_category():
        cat = dropdown_var.get()
        if cat == "Choose a category":
            update_status(frame, "no_topic")
            return

        # delet category in DB and HTML
        content_manager.delete_nav_category(cat)

        update_status(frame, "success")

        # refresh dropdown
        with content_manager.conn.cursor() as cur:
            cur.execute("SELECT name FROM nav_categories;")
            new_categories = [row[0] for row in cur.fetchall()]

        menu = dropdown["menu"]
        menu.delete(0, "end")
        for c in new_categories:
            menu.add_command(label=c, command=lambda value=c: dropdown_var.set(value))

        if not new_categories:
            dropdown_var.set("No categories")
            dropdown.config(state="disabled")

    #Enter/Back
    show_enter_back_buttons(remove_category, render_back_to_main)


def render_add_topic():
    clean_screen()

    # get the selected category dropdown
    category_dropdown_var, category_frame = display_category_dropdown()
    if category_dropdown_var is None:
        return  # no categories available

    topic_name_frame = tk.Frame(app)
    topic_name_frame.error_label = None
    topic_name_frame.success_label = None
    topic_name_frame.pack(fill='x', pady=10, padx=15)

    tk.Label(topic_name_frame, text="Topic Name:", font=("Arial", 18), width=15, anchor="w").pack(side='left')

    topic_name_entry = tk.Entry(topic_name_frame, width=15, font=("Arial", 18))
    topic_name_entry.pack(side='left', padx=5)

    # callback
    def on_enter():
        category = category_dropdown_var.get()
        if category == "Choose a category":
            if not topic_name_frame.error_label:
                topic_name_frame.error_label = tk.Label(
                    topic_name_frame,
                    text='Please select a category first!',
                    font=("Arial", 16),
                    fg="red",
                    anchor="w"
                )
                topic_name_frame.error_label.pack(side='left')
            return
        if topic_name_frame.error_label:
            topic_name_frame.error_label.destroy()
            topic_name_frame.error_label = None

        create_topic_labels(topic_name_entry, category, topic_name_frame)

    # Enter/Back
    show_enter_back_buttons(on_enter, render_back_to_main)


def render_remove_topic():
    clean_screen()

    frame = tk.Frame(app)
    frame.pack(fill='x', pady=10, padx=15, anchor='w')
    frame.success_label = None
    frame.error_label = None

    tk.Label(frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

    # get categories from SQL
    with content_manager.conn.cursor() as cur:
        cur.execute("SELECT name FROM nav_categories;")
        categories = [row[0] for row in cur.fetchall()]

    if not categories:
        render_no_topic_selected(frame)
        return

    category_var = tk.StringVar(value="Choose a category")
    category_dropdown = tk.OptionMenu(frame, category_var, *categories)
    category_dropdown.config(font=("Arial", 16), width=25, bg="white", fg="black")
    category_dropdown.pack(anchor="w")

    tk.Label(frame, text="Topic:", font=("Arial", 18), anchor="w").pack(anchor='w', pady=(10, 0))
    topic_var = tk.StringVar(value="Choose a topic")
    topic_dropdown = tk.OptionMenu(frame, topic_var, "")
    topic_dropdown.config(font=("Arial", 16), width=25, bg="white", fg="black")
    topic_dropdown.pack(anchor="w")

    # update topic dropdown when category changes
    def update_topic_dropdown(*args):
        clear_labels(frame)
        category = category_var.get()
        if category == "Choose a category":
            menu = topic_dropdown["menu"]
            menu.delete(0, "end")
            topic_var.set("Choose a topic")
            return

        with content_manager.conn.cursor() as cur:
            cur.execute("SELECT topic FROM notes n JOIN nav_categories nc ON n.category_id = nc.id WHERE nc.name = %s", (category,))
            topics = [row[0] for row in cur.fetchall()]

        menu = topic_dropdown["menu"]
        menu.delete(0, "end")
        if topics:
            for t in topics:
                menu.add_command(label=t, command=lambda value=t: topic_var.set(value))
            topic_var.set("Choose a topic")
        else:
            topic_var.set("No topics")

    category_var.trace_add("write", update_topic_dropdown)

    # callback
    def remove_topic_callback():
        category = category_var.get()
        topic = topic_var.get()
        if category == "Choose a category" or topic in ["Choose a topic", "No topics"]:
            update_status(frame, "no_topic")
            return

        content_manager.remove_topic(topic, category)
        update_status(frame, "success")
        update_topic_dropdown()  # refresh topics

    #Enter/Back
    show_enter_back_buttons(remove_topic_callback, render_back_to_main)


def render_add_text_content():
    clean_screen()

    frame = tk.Frame(app)
    frame.pack(fill='x', pady=5, padx=15, anchor='w')

    # category + topic dropdowns
    category_var, topic_var, topic_dropdown = create_category_topic_dropdown(frame)
    if not category_var:
        return  # no categories/topics available

    # text content entry
    tk.Label(frame, text="Topic content:", font=("Arial", 18), anchor="w").pack(anchor='w', pady=(10,0))
    content = tk.Text(frame, width=80, height=20, font=("Arial", 16), wrap='word')
    content.pack(fill='x', pady=5)

    def add_content_callback():
        category = category_var.get()
        topic = topic_var.get()

        if category == "Choose a category" or topic in ["Choose a topic", "No topics"]:
            update_status(frame, "no_topic")
            return

        raw_text = content.get("1.0", "end-1c").strip()
        if not raw_text:
            update_status(frame, "empty_content")
            return

        content_manager.add_content_to_topic(topic, raw_text)
        update_status(frame, "success")

    # Enter/Back
    show_enter_back_buttons(add_content_callback, render_back_to_main)


def render_add_img():
    clean_screen()
    frame = tk.Frame(app)
    frame.pack(fill='x', pady=5, padx=15, anchor='w')

    # category + topic dropdowns
    category_var, topic_var, topic_dropdown = create_category_topic_dropdown(frame)
    if not category_var:
        return  # no categories/topics available

    # image name entry
    tk.Label(frame, text="Image name (as saved in cat_images):", font=("Arial", 18), anchor="w").pack(anchor='w', pady=(10,0))
    img_name = tk.Entry(frame, width=15, font=("Arial", 18))
    img_name.pack(side='left', padx=5)

    # image size dropdown
    dropdown_w_frame = tk.Frame(frame)
    dropdown_w_frame.pack(fill='x', pady=5, padx=15, anchor='w')
    tk.Label(dropdown_w_frame, text="Image size:", font=("Arial", 18), anchor="w").pack(anchor='w')
    selected = tk.StringVar(value="Choose a size")
    options = [300, 500, 600]
    dropdown_w = tk.OptionMenu(dropdown_w_frame, selected, *options)
    dropdown_w.config(font=("Arial", 16), width=20, bg="white", fg="black")
    dropdown_w.pack(anchor="w")

    # callback
    def add_img_callback():
        category = category_var.get()
        topic = topic_var.get()
        image = img_name.get().strip()
        size = selected.get()

        if category == "Choose a category" or topic in ["Choose a topic", "No topics"]:
            update_status(frame, "no_topic")
            return

        if not check_img_name(image, frame):
            return

        if size == "Choose a size":
            update_status(frame, "empty_content")
            return

        content_manager.add_pic_to_topic(topic, image, size)
        update_status(frame, "success")

    #Enter/Back
    show_enter_back_buttons(add_img_callback, render_back_to_main)


def render_remove_content():
    clean_screen()
    frame = tk.Frame(app)
    frame.pack(fill='x', pady=10, padx=15, anchor='w')

    category_var, topic_var, topic_dropdown = create_category_topic_dropdown(frame)
    if not category_var:
        return  # no categories/topics available

    def remove_content_callback():
        category = category_var.get()
        topic = topic_var.get()
        if category == "Choose a category" or topic in ["Choose a topic", "No topics"]:
            update_status(frame, "no_topic")
            return

        content_manager.remove_content_from_topic(topic, category)
        update_status(frame, "success")

    #Enter/Back
    show_enter_back_buttons(remove_content_callback, render_back_to_main)




def render_main_enter_screen():
    clean_screen()
    add_background()

    tk.Label(app, text="Welcome to the Web Content Creator!", font=("Arial", 20, "bold")) \
        .pack(anchor="w", padx=5, pady=10)
    tk.Label(app, text="Please choose an option:", font=("Arial", 15, "italic")) \
        .pack(anchor="w", padx=5, pady=(0, 20))

    #FRAME 1
    top_frame = tk.Frame(app)
    top_frame.pack(anchor="w", pady=(0, 20))

    #ADD CATEGORY - Y
    add_category_button = tk.Button(top_frame, text="Add Category", font=("Arial", 14, "bold"),
                                    padx=9, pady=5, bg="blue", fg="white",
                                    command=render_add_category)
    add_category_button.pack(side="left", padx=(5, 10))

    #REMOVE CATEGORY - Y
    remove_cat_button = tk.Button(top_frame, text="Remove Category", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_cat)
    remove_cat_button.pack(side="left", padx=(5, 10))

    #ADD TOPIC - Y
    add_topic_button = tk.Button(top_frame, text="Add Topic", font=("Arial", 14, "bold"),
                                    padx=9, pady=5, bg="blue", fg="white",
                                    command=render_add_topic)
    add_topic_button.pack(side="left", padx=(5, 10))

    #REMOVE TOPIC - Y
    remove_topic_button = tk.Button(top_frame, text="Remove Topic", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_topic)
    remove_topic_button.pack(side="left", padx=(5, 10))

    #FRAME 2

    bot_frame = tk.Frame(app)
    bot_frame.pack(anchor="w", pady=(0, 20))

    #ADD CONTENT TEXT - Y
    add_content_to_cat_button = tk.Button(bot_frame, text="Add Text Content", font=("Arial", 14, "bold"),
                                          padx=9, pady=5, bg="blue", fg="white",
                                          command=render_add_text_content)
    add_content_to_cat_button.pack(side="left", padx=(5, 10))

    # ADD CONTENT IMAGE - Y
    add_img_to_cat_button = tk.Button(bot_frame, text="Add Image Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="blue", fg="white",
                                command=render_add_img)
    add_img_to_cat_button.pack(side="left", padx=(5, 10))

    #REMOVE CONTENT
    remove_content_to_cat_button = tk.Button(bot_frame, text="Clear Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_content)
    remove_content_to_cat_button.pack(side="left", padx=(5, 10))




