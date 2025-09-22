import os
import tkinter as tk
from helpers import clean_screen, add_background, clear_labels, show_enter_back_buttons, create_category_topic_labels
from canvas import app
from content_mngmt_funcs.content_manager import ContentManager

content_manager = ContentManager()

def create_category_labels(cat_name_entry, frame):
    create_category_topic_labels(frame, content_manager.create_nav_category(cat_name_entry.get().strip()))

def create_topic_labels(topic_name_entry, category, frame):
    result = content_manager.add_topic(topic_name_entry.get().strip(), category)
    create_category_topic_labels(frame, result)

def check_img_name(name, frame):
    clear_labels(frame)

    if not f"{name}.png" in os.listdir(os.path.join("..", "cat_images")):
        frame.error_label = tk.Label(
            frame,
            text='Please check the image name',
            font=("Arial", 18),
            width=25,
            anchor="w",
            fg="red"
        )
        frame.error_label.pack(side='left')
        return False
    else:
        frame.success_label = tk.Label(
            frame,
            text='Image added successfully!',
            font=("Arial", 18),
            width=25,
            anchor="w",
            fg="green"
        )
        frame.success_label.pack(side='left')
        return True


def topics_dropdown_labels(cat, frame):
    if cat == "Choose a topic":
        if not frame.error_label:
            frame.error_label = tk.Label(
                frame,
                text='Please select a topic first!',
                font=("Arial", 16),
                fg="red",
                anchor="w"
            )
            frame.error_label.pack(side='left')
        return  # don’t add anything
    # clear error if category is valid
    if frame.error_label:
        frame.error_label.destroy()
        frame.error_label = None


def content_added_label(frame):
    clear_labels(frame)

    frame.success_label = tk.Label(
        frame,
        text='Added successfully!',
        font=("Arial", 18),
        width=30,
        anchor="w",
        fg="green"
    )
    frame.success_label.pack(side='left')



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
    if len(topics) < 1:
        render_no_topic_selected(topic_dropdown_frame)

    else:
        dropdown_frame = tk.Frame(app)
        dropdown_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        tk.Label(topic_dropdown_frame, text="Topic:", font=("Arial", 18), anchor="w").pack(anchor='w')

        selected = tk.StringVar(value="Choose a category")

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


def render_add_topic():
    clean_screen()

    # Get the selected category dropdown
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

    # Define enter callback
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

    show_enter_back_buttons(on_enter, render_back_to_main)





def render_add_content():
    clean_screen()

    topics_dropdown = display_topic_dropdown()[0]

    topic_content_name_frame = tk.Frame(app)
    topic_content_name_frame.success_label = None
    topic_content_name_frame.error_label = None

    topic_content_name_frame.pack(fill='x', pady=5, padx=15, anchor='w')

    tk.Label(topic_content_name_frame, text="Topic content:", font=("Arial", 18), anchor="w").pack(anchor='w')

    content = tk.Text(topic_content_name_frame, width=80, height=20, font=("Arial", 16), wrap='word')
    content.pack(fill='x', pady=5)

    def add_content():
        topic = topics_dropdown.get()
        topics_dropdown_labels(topic, topic_content_name_frame)

        raw_text = content.get("1.0", "end-1c")
        content_manager.add_content_to_topic(topic, raw_text)

        content_added_label(topic_content_name_frame)

    show_enter_back_buttons(add_content, render_back_to_main)


def render_add_img():
    cat_dropdown_selected, cat_frame = display_topic_dropdown()

    image_name_frame = tk.Frame(app)
    image_name_frame.error_label = None
    image_name_frame.success_label = None
    image_name_frame.pack(fill='x', pady=5, padx=15, anchor='w')

    tk.Label(image_name_frame, text="Image name (as saved in cat_images):",
             font=("Arial", 18), anchor="w").pack(anchor='w')

    img_name = tk.Entry(image_name_frame, width=15, font=("Arial", 18))
    img_name.pack(side='left', padx=5)


    dropdown_w_frame = tk.Frame(app)
    dropdown_w_frame.pack(fill='x', pady=5, padx=15, anchor='w')

    tk.Label(dropdown_w_frame, text="Image size:", font=("Arial", 18), anchor="w").pack(anchor='w')

    selected = tk.StringVar(value="Choose a size")
    options = [300, 500, 600]

    dropdown_w = tk.OptionMenu(dropdown_w_frame, selected, *options)
    dropdown_w.config(font=("Arial", 16), width=20, bg="white", fg="black")
    dropdown_w.pack(anchor="w")

    # Define a callback
    def add_img():
        print(img_name.get())

        # category = cat_dropdown_selected.get()
        # category_dropdown_label_check(category, cat_frame)

        if check_img_name(img_name.get(), image_name_frame):
            category = cat_dropdown_selected.get()
            image = img_name.get()
            size = selected.get()
            print("debug:", category, image, size)
            content_manager.add_pic_to_topic(category, image, size)
            # content_added(cat_dropdown_selected)

    show_enter_back_buttons(add_img, render_back_to_main)


def render_remove_cat():
    clean_screen()

    if not content_manager.category_name_content_pairs:
        temp_frame = tk.Frame(app)
        temp_frame.pack(pady=10, padx=15)
        render_no_topic_selected(temp_frame)
        return

    frame = tk.Frame(app)
    frame.pack(fill='x', pady=10, padx=15, anchor='w')
    frame.success_label = None

    tk.Label(frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

    dropdown_var = tk.StringVar(value="Choose a category")
    dropdown = tk.OptionMenu(frame, dropdown_var, *content_manager.category_name_content_pairs.keys())
    dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
    dropdown.pack(anchor="w")

    # Hide success label when selection changes
    def on_dropdown_change(*args):
        if frame.success_label:
            frame.success_label.destroy()
            frame.success_label = None
    dropdown_var.trace_add("write", on_dropdown_change)

    # Function to remove category
    def remove_topic():
        cat = dropdown_var.get()
        if cat in content_manager.category_name_content_pairs:
            content_manager.delete_topic(cat)

            if frame.success_label:
                frame.success_label.destroy()
            frame.success_label = tk.Label(
                frame,
                text='Category removed successfully!',
                font=("Arial", 18),
                width=25,
                anchor="w",
                fg="green"
            )
            frame.success_label.pack(side='left', pady=5)

            # Refresh dropdown menu
            menu = dropdown["menu"]
            menu.delete(0, "end")
            for c in content_manager.category_name_content_pairs.keys():
                menu.add_command(label=c, command=lambda value=c: dropdown_var.set(value))

            # Disable Enter button if no categories left
            if not content_manager.category_name_content_pairs:
                dropdown_var.set("No categories")
                dropdown.config(state="disabled")
                enter_button.pack_forget()

    enter_button = tk.Button(frame, text="Enter", font=("Arial", 14, "bold"),
                             padx=9, pady=5, bg="blue", fg="white",
                             command=remove_topic)
    enter_button.pack(side="left", padx=(0, 10))
    back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=render_back_to_main)
    back_button.pack(side="left")

def render_remove_content():
    clean_screen()
    if not content_manager.category_name_content_pairs:
        temp_frame = tk.Frame(app)
        temp_frame.pack(pady=10, padx=15)
        render_no_topic_selected(temp_frame)
        return

    frame = tk.Frame(app)
    frame.pack(fill='x', pady=10, padx=15, anchor='w')
    frame.success_label = None

    tk.Label(frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

    dropdown_var = tk.StringVar(value="Choose a category")
    dropdown = tk.OptionMenu(frame, dropdown_var, *content_manager.category_name_content_pairs.keys())
    dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
    dropdown.pack(anchor="w")

    def remove_content():
        cat = dropdown_var.get()
        if cat in content_manager.category_name_content_pairs:
            content_manager.remove_content_from_cat(cat)

            if frame.success_label:
                frame.success_label.destroy()
            frame.success_label = tk.Label(
                frame,
                text='Content removed successfully!',
                font=("Arial", 18),
                width=25,
                anchor="w",
                fg="green"
            )
            frame.success_label.pack(side='left', pady=5)

    show_enter_back_buttons(remove_content, render_back_to_main)

def render_main_enter_screen():
    clean_screen()
    add_background()

    tk.Label(app, text="Welcome to the Web Content Creator!", font=("Arial", 20, "bold")) \
        .pack(anchor="w", padx=5, pady=10)
    tk.Label(app, text="Please choose an option:", font=("Arial", 15, "italic")) \
        .pack(anchor="w", padx=5, pady=(0, 20))

    top_frame = tk.Frame(app)
    top_frame.pack(anchor="w", pady=(0, 20))

    #ADD CATEGORY
    add_category_button = tk.Button(top_frame, text="Add Category", font=("Arial", 14, "bold"),
                                    padx=9, pady=5, bg="blue", fg="white",
                                    command=render_add_category)
    add_category_button.pack(side="left", padx=(5, 10))

    #REMOVE CATEGORY
    remove_cat_button = tk.Button(top_frame, text="Remove Category", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_cat)
    remove_cat_button.pack(side="left", padx=(5, 10))

    #ADD TOPIC
    add_topic_button = tk.Button(top_frame, text="Add Topic", font=("Arial", 14, "bold"),
                                    padx=9, pady=5, bg="blue", fg="white",
                                    command=render_add_topic)
    add_topic_button.pack(side="left", padx=(5, 10))

    #REMOVE TOPIC
    remove_topic_button = tk.Button(top_frame, text="Remove Topic", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_cat)
    remove_topic_button.pack(side="left", padx=(5, 10))


    bot_frame = tk.Frame(app)
    bot_frame.pack(anchor="w", pady=(0, 20))

    #ADD CONTENT TEXT
    add_content_to_cat_button = tk.Button(bot_frame, text="Add Text Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="blue", fg="white",
                                command=render_add_content)
    add_content_to_cat_button.pack(side="left", padx=(5, 10))

    # ADD CONTENT IMAGE
    add_img_to_cat_button = tk.Button(bot_frame, text="Add Image Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="blue", fg="white",
                                command=render_add_img)
    add_img_to_cat_button.pack(side="left", padx=(5, 10))

    #REMOVE CONTENT
    remove_content_to_cat_button = tk.Button(bot_frame, text="Clear Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_content)
    remove_content_to_cat_button.pack(side="left", padx=(5, 10))




