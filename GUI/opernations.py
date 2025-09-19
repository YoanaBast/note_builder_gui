import os
import tkinter as tk
from helpers import clean_screen, add_background
from canvas import app
from content_mngmt_funcs.content_manager import ContentManager

content_manager = ContentManager()


def enter_back(enter_com, *args):
    frame = tk.Frame(app)
    frame.pack(anchor='w', pady=10, padx=20)

    enter_button = tk.Button(frame, text="Enter", font=("Arial", 14, "bold"),
                             padx=9, pady=5, bg="blue", fg="white",
                             command=lambda: enter_com(*args))
    enter_button.pack(side="left", padx=(0, 10))

    back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=render_back_to_main)
    back_button.pack(side="left")

def category_dropdown_label_check(cat, frame):
    if cat == "Choose a category":
        if not frame.error_label:
            frame.error_label = tk.Label(
                frame,
                text='Please select a category first!',
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


def content_added(frame):
    if frame.error_label:
        frame.error_label.destroy()
        frame.error_label = None
    if frame.success_label:
        frame.success_label.destroy()
        frame.success_label = None

    frame.success_label = tk.Label(
        frame,
        text='Added successfully!',
        font=("Arial", 18),
        width=30,
        anchor="w",
        fg="green"
    )
    frame.success_label.pack(side='left')


def check_cat(cat_name, frame):
    if frame.error_label:
        frame.error_label.destroy()
        frame.error_label = None
    if frame.success_label:
        frame.success_label.destroy()
        frame.success_label = None

    if cat_name.get() not in content_manager.category_name_content_pairs.keys():
        result = content_manager.add_category(cat_name.get())
        if result == 'Empty string':
            frame.error_label = tk.Label(
                frame,
                text='Please no empty strings :(',
                font=("Arial", 18),
                width=25,
                anchor="w",
                fg="red"
            )
            frame.error_label.pack(side='left')
        else:

            frame.success_label = tk.Label(
                frame,
                text='Category added successfully!',
                font=("Arial", 18),
                width=25,
                anchor="w",
                fg="green"
            )
            frame.success_label.pack(side='left')
    else:
        frame.error_label = tk.Label(
            frame,
            text='Category already exists',
            font=("Arial", 18),
            width=25,
            anchor="w",
            fg="red"
        )
        frame.error_label.pack(side='left')

def check_img_name(name, frame):
    if frame.error_label:
        frame.error_label.destroy()
        frame.error_label = None
    if frame.success_label:
        frame.success_label.destroy()
        frame.success_label = None

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



def render_no_category(frame):
    frame.pack(fill='x', anchor='w', pady=10, padx=15)

    tk.Label(frame, text="Please add categories first!",
             font=("Arial", 18), anchor="w").pack(side='left')

    back_frame = tk.Frame(app)
    back_frame.pack(anchor='w', pady=10, padx=20)

    back_button = tk.Button(back_frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=render_back_to_main)
    back_button.pack(side="left")


def cat_dropdown():
    clean_screen()
    cat_dropdown_frame = tk.Frame(app)
    cat_dropdown_frame.success_label = None
    cat_dropdown_frame.pack(fill='x', pady=10, padx=15)

    if len(content_manager.category_name_content_pairs.keys()) < 1:
        render_no_category(cat_dropdown_frame)

    else:
        dropdown_frame = tk.Frame(app)
        dropdown_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        tk.Label(cat_dropdown_frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

        selected = tk.StringVar(value="Choose a category")
        options = list(content_manager.category_name_content_pairs.keys())

        dropdown = tk.OptionMenu(dropdown_frame, selected, *options)
        dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
        dropdown.pack(anchor="w")  # align left
        return selected, cat_dropdown_frame




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

    enter_back(lambda: check_cat(cat_name, cat_name_frame))


def render_add_content():
    dropdown = cat_dropdown()[0]

    cat_con_name_frame = tk.Frame(app)
    cat_con_name_frame.success_label = None
    cat_con_name_frame.error_label = None

    cat_con_name_frame.pack(fill='x', pady=5, padx=15, anchor='w')

    tk.Label(cat_con_name_frame, text="Category content:", font=("Arial", 18), anchor="w").pack(anchor='w')

    content = tk.Text(cat_con_name_frame, width=80, height=20, font=("Arial", 16), wrap='word')
    content.pack(fill='x', pady=5)

    def add_content():
        category = dropdown.get()
        category_dropdown_label_check(category, cat_con_name_frame)

        raw_text = content.get("1.0", "end-1c")
        content_manager.add_content_to_cat(category, raw_text)

        content_added(cat_con_name_frame)

    enter_back(add_content)


def render_add_img():
    cat_dropdown_selected, cat_frame = cat_dropdown()

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
            content_manager.add_pic_to_cat(category, image, size)
            # content_added(cat_dropdown_selected)

    enter_back(add_img)


def render_remove_cat():
    clean_screen()

    if not content_manager.category_name_content_pairs:
        temp_frame = tk.Frame(app)
        temp_frame.pack(pady=10, padx=15)
        render_no_category(temp_frame)
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
    def remove_category():
        cat = dropdown_var.get()
        if cat in content_manager.category_name_content_pairs:
            content_manager.remove_category(cat)

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
                             command=remove_category)
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
        render_no_category(temp_frame)
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

    enter_back(remove_content)

def render_main_enter_screen():
    clean_screen()
    add_background()

    tk.Label(app, text="Welcome to the Web Content Creator!", font=("Arial", 20, "bold")) \
        .pack(anchor="w", padx=5, pady=10)
    tk.Label(app, text="Please choose an option:", font=("Arial", 15, "italic")) \
        .pack(anchor="w", padx=5, pady=(0, 20))

    frame = tk.Frame(app)
    frame.pack(anchor="w", pady=(0, 20))

    add_category_button = tk.Button(frame, text="Add Category", font=("Arial", 14, "bold"),
                                    padx=9, pady=5, bg="blue", fg="white",
                                    command=render_add_category)
    add_category_button.pack(side="left", padx=(10, 5))

    remove_cat_button = tk.Button(frame, text="Remove Category", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="blue", fg="white",
                                command=render_remove_cat)
    remove_cat_button.pack(side="left", padx=(5, 10))


    add_content_to_cat_button = tk.Button(frame, text="Add Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_add_content)
    add_content_to_cat_button.pack(side="left", padx=(5, 10))


    add_img_to_cat_button = tk.Button(frame, text="Add Image", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_add_img)
    add_img_to_cat_button.pack(side="left", padx=(5, 10))


    remove_content_to_cat_button = tk.Button(frame, text="Remove Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_remove_content)
    remove_content_to_cat_button.pack(side="left", padx=(5, 10))




