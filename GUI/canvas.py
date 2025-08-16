import tkinter as tk
import os


def create_app():
    root = tk.Tk()
    root.state("zoomed")
    # root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    root.title("Web Content Creator")

    img_path = os.path.join('backgrounds', 'bg1.png')
    bg_image = tk.PhotoImage(file=img_path)

    # Create a label with the image
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    background_label.image = bg_image # Keep a reference to the image to prevent garbage collection
    # Assign background_label to root before returning
    root.background_label = background_label     # Assign background_label to root before returning - , remember this background_label widget so I can easily find and control it later!

    close_button = tk.Button(root, text="X", font=("Arial", 14, "bold"), bg="red", fg="white",
                             command=root.destroy)
    # Use place with relative coordinates so it stays on top-right
    close_button.place(relx=0.98, rely=0.02, anchor='ne')

    return root

app = create_app()