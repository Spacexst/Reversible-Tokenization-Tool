import tkinter as tk
from tkinter import filedialog
import os

# button functions


def select_file():
    path = fileDialog.askopenfilename()
    if path:
        file_label.config(text=path)
        status_label.config(text="File selected")


def protect_info():
    status_label.config(text="Protect Personal Information clicked")


def tokenize():
    status_label.config(text="Tokenize clicked")


def ask_ai():
    status_label.config(text="Ask AI clicked")


def clear_document():
    document.delete("1.0", tk.END)
    file_label.config(text="Path of the selected file")
    status_label.config(text="Document clear")


# main window
# Create the main application window
root = tk.Tk()
root.title("Reversible Tokenization Tool")
root.geometry("300x200")  # Width x Height


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
    command=tokenize
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
