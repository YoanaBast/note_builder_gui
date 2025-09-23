import os
import tkinter as tk
from canvas import app

def clean_screen():
    for widget in app.winfo_children():
        if hasattr(app, 'background_label') and widget == app.background_label:
            print(f"Keeping {widget} (background)")
            continue
        print(f"Destroying {widget}")
        widget.destroy()


def add_background():
    img_path = os.path.join('backgrounds', 'bg1.png')
    bg_image = tk.PhotoImage(file=img_path)

    background_label = tk.Label(app, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # keep reference to avoid garbage collection
    background_label.image = bg_image
    app.background_label = background_label


def clear_labels(frame):
    if frame.error_label:
        frame.error_label.destroy()
        frame.error_label = None
    if frame.success_label:
        frame.success_label.destroy()
        frame.success_label = None


def show_enter_back_buttons(enter_com, back_com, *args):
    """this is a reusable back/enter duo, back renders to main and enter takes a function"""
    frame = tk.Frame(app)
    frame.pack(anchor='w', pady=10, padx=20)

    enter_button = tk.Button(frame, text="Enter", font=("Arial", 14, "bold"),
                             padx=9, pady=5, bg="blue", fg="white",
                             command=lambda: enter_com(*args))
    enter_button.pack(side="left", padx=(0, 10))

    back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"),
                            padx=9, pady=5, bg="black", fg="white",
                            command=lambda: back_com(*args))
    back_button.pack(side="left")


def create_category_topic_labels(frame, result):
    """ calls create_nav_category and creates labels based on the result"""
    clear_labels(frame)

    if result == "That already exists":
        frame.error_label = tk.Label(
            frame,
            text='That already exists',
            font=("Arial", 18),
            width=25,
            anchor="w",
            fg="red"
        )
        frame.error_label.pack(side='left')

    elif result == 'Empty entry':
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


def update_status(frame, state):
    clear_labels(frame)

    if state == "no_topic":
        frame.error_label = tk.Label(
            frame,
            text="Please select a topic first!",
            font=("Arial", 16),
            fg="red",
            anchor="w"
        )
        frame.error_label.pack(side='left')

    elif state == "empty_content":
        frame.error_label = tk.Label(
            frame,
            text="Content cannot be empty!",
            font=("Arial", 16),
            fg="red",
            anchor="w"
        )
        frame.error_label.pack(side='left')

    elif state == "success":
        frame.success_label = tk.Label(
            frame,
            text="Operation run successfully!",
            font=("Arial", 18),
            width=30,
            anchor="w",
            fg="green"
        )
        frame.success_label.pack(side='left')


