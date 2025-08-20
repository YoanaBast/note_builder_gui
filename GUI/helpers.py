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

    # Keep reference to avoid garbage collection
    background_label.image = bg_image
    app.background_label = background_label


