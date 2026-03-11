import tkinter as tk
from tkinter import filedialog
import os
# import pii_tokenizer


def run_tokenize():
    path = file_label.cget("text")

    if os.path.exists(path):
        output_file = pii_tokenizer.tokenize_file(path)
        status_label.config(text=f"Tokenization complete: {output_file}")
        os.startfile(output_file)
    else:
        status_label.config(text="No file selected")

# button functions


def select_file():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        file_label.config(text=path)
        status_label.config(text="File selected")


def protect_info():
    status_label.config(text="Protect Personal Information clicked")


def run_tokenize():

    path = file_label.cget("text")

    if os.path.exists(path):
        output_file = pii_tokenizer.tokenize_file(path)

        status_label.config(text=f"Tokenization complete: {output_file}")

        # open the tokenized file automatically
        os.startfile(output_file)

    else:
        status_label.config(text="No file selected")


def ask_ai():
    status_label.config(text="Ask AI clicked")


def clear_document():
    file_label.config(text="<Path of selected file>")
    status_label.config(text="Document cleared")


# main window
# Create the main application window
root = tk.Tk()
root.title("Reversible Tokenization Tool")
root.geometry("900x550")  # Width x Height


# main frame
main_frame = tk.Frame(root, bg="#f2f2f2", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

title_label = tk.Label(
    main_frame,
    text="Private AI application",
    font=("Arial", 14, "bold"),
    bg="#f2f2f2"
)
title_label.pack(pady=10)
select_button = tk.Button(
    main_frame,
    text="Select File",
    width=25,
    command=select_file
)
select_button.pack(pady=5)


file_label = tk.Label(
    main_frame,
    text="<Path of selected file>",
    width=30,
    relief="sunken"
)
file_label.pack(pady=5)


protect_button = tk.Button(
    main_frame,
    text="Protect Personal Information",
    width=25,
    command=protect_info
)
protect_button.pack(pady=10)

tokenize_button = tk.Button(
    main_frame,
    text="Tokenize",
    width=25,
    command=run_tokenize
)
tokenize_button.pack(pady=5)


ask_ai_button = tk.Button(
    main_frame,
    text="Ask AI",
    width=25,
    command=ask_ai
)
ask_ai_button.pack(pady=5)


clear_button = tk.Button(
    main_frame,
    text="Clear",
    width=25,
    command=clear_document
)
clear_button.pack(pady=5)


status_label = tk.Label(
    main_frame,
    text="Status Bar",
    relief="sunken",
    anchor="w"
)
status_label.pack(side="bottom", fill="x", pady=20)


root.mainloop()
