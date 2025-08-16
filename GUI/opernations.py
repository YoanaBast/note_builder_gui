import tkinter as tk
from helpers import clean_screen, add_background
from canvas import app
from content_adder import AddContentToPage

content_manager = AddContentToPage()

def render_back_to_main():
    clean_screen()
    render_main_enter_screen()

def render_category():
    clean_screen()
    cat_name_frame = tk.Frame(app)
    cat_name_frame.pack(fill='x', pady=10, padx=15)

    tk.Label(cat_name_frame, text="Category Name:", font=("Arial", 18), width=15, anchor="w").pack(side='left')

    cat_name = tk.Entry(cat_name_frame, width=15, font=("Arial", 18))
    cat_name.pack(side='left', padx=5)

    frame = tk.Frame(app)
    frame.pack(anchor='w', pady=10, padx=20)

    enter_button = tk.Button(frame, text="Enter", font=("Arial", 14, "bold"),
                             padx=9, pady=5, bg="blue", fg="white",
                             command=lambda: content_manager.add_category(cat_name.get()))
    enter_button.pack(side="left", padx=(0, 10))  # right padding

    back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=render_back_to_main)
    back_button.pack(side="left")

def render_add_content():
    clean_screen()
    cat_con_name_frame = tk.Frame(app)
    cat_con_name_frame.pack(fill='x', pady=10, padx=15)

    if len(content_manager.category_name_content_pairs.keys()) < 1:
        tk.Label(cat_con_name_frame, text="Please add categories first", font=("Arial", 18), width=25, anchor="w").pack(side='left')
        frame = tk.Frame(app)
        frame.pack(anchor='w', pady=10, padx=20)

        back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_back_to_main)
        back_button.pack(side="left")

    else:
        # Frame for dropdown
        dropdown_frame = tk.Frame(app)
        dropdown_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        tk.Label(cat_con_name_frame, text="Category:", font=("Arial", 18), anchor="w").pack(anchor='w')

        selected = tk.StringVar(value="Choose a category")
        options = list(content_manager.category_name_content_pairs.keys())

        dropdown = tk.OptionMenu(dropdown_frame, selected, *options)
        dropdown.config(font=("Arial", 16), width=20, bg="white", fg="black")
        dropdown.pack(anchor="w")  # align left

        # Frame for entry
        cat_con_name_frame = tk.Frame(app)
        cat_con_name_frame.pack(fill='x', pady=5, padx=15, anchor='w')

        # Label on top
        tk.Label(cat_con_name_frame, text="Category content:", font=("Arial", 18), anchor="w").pack(anchor='w')

        # Multi-line text area
        content = tk.Text(cat_con_name_frame, width=80, height=20, font=("Arial", 16), wrap='word')
        content.pack(fill='x', pady=5)

        frame = tk.Frame(app)
        frame.pack(anchor='w', pady=10, padx=20)


        enter_button = tk.Button(frame, text="Enter", font=("Arial", 14, "bold"),
                                 padx=9, pady=5, bg="blue", fg="white",
                                 command=lambda: content_manager.add_content_to_cat(selected.get(), content.get("1.0", "end-1c")))

        enter_button.pack(side="left", padx=(0, 10))  # right padding

        back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_back_to_main)
        back_button.pack(side="left")



def remove_category():
    pass

def render_main_enter_screen():
    clean_screen()
    add_background()
    tk.Label(app, text="Welcome to the Web Content Creator!", font=("Arial", 20, "bold")) \
        .pack(anchor="w", padx=5, pady=10)  # anchor left with padding

    tk.Label(app, text="Please choose an option:", font=("Arial", 15, "italic")) \
        .pack(anchor="w", padx=5, pady=(0, 20))

    frame = tk.Frame(app)
    frame.pack(anchor="w", pady=(0, 20))

    add_category_button = tk.Button(frame, text="Add Category", font=("Arial", 14, "bold"),
                             padx=9, pady=5, bg="blue", fg="white",
                             command=render_category)
    add_category_button.pack(side="left", padx=(10, 5))

    add_content_to_cat_button = tk.Button(frame, text="Add Content", font=("Arial", 14, "bold"),
                                padx=9, pady=5, bg="black", fg="white",
                                command=render_add_content)
    add_content_to_cat_button.pack(side="left", padx=(5, 10))







