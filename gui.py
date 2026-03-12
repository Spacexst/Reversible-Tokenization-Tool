import tkinter as tk
from tkinter import filedialog
import os
import pii_tokenizer


def run_tokenize():
    path = file_label.cget("text")

    if os.path.exists():
        output_file = pii_tokenizer.tokenize_file(path)
        status_label.config(Text=f"Tokenization complete: {output_file}")
        os.startfile(out_file)
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
        status_label.config(Text=f"Tokenization complete: {output_file}")

 # opens the file automatically
        os.startfile(output_file)
    else:
        status_label.config(text="No file selected")


def run_detokenize():
    path = file_label.cget("text")
    if os.path.exists(path):
        output_file = pii_tokenizer.detokenize_file(path)
        status_label.config(Text=f"Detokenization complete: {output_file}")
        messagebox.showinfo("Success", "Detokenization completed")

 # opens the file automatically
        os.startfile(output_file)
    else:
        status_label.config(text="No file selected")


def ask_ai():
    status_label.config(text="Ask AI clicked")


def clear_document():
    file_label.config(text="<Path of the file selected>")
    status_label.config(text="Document cleared")


# window
root = tk.Tk()
root.title("Reversible Tokenization Tool")
root.geometry("700x450")  # widthx height
root.configure(bg="#f2f2f2")


# title

title_label = tk.Label(
    root,
    text="Private AI application",
    font=("Arial", 14, "bold"),
    bg="#f2f2f2"
)
title_label.pack(pady=10)

# main frame

main_frame = tk.Frame(root, bg="#f2f2f2", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)
button_width = 30

# Select file

select_button = tk.Button(
    main_frame,
    text="Select File",
    width=25,
    command=select_file
)
select_button.pack(pady=5)

# filepath label

file_label = tk.Label(
    main_frame,
    text="<Path of the selected file>",
    width=40,
    relief="sunken",
    bg="white"
)
file_label.pack(pady=5)


# Protect PII button

protect_button = tk.Button(
    main_frame,
    text="Protect Personal Information",
    width=button_width,
    command=protect_info
)
protect_button.pack(pady=8)

# Tokenize button

tokenize_button = tk.Button(
    main_frame,
    text="Tokenize",
    width=button_width,
    command=run_tokenize
)
tokenize_button.pack(pady=5)

# Detokenize button

detokenize_button = tk.Button(
    main_frame,
    text="Detokenize",
    width=button_width,
    command=run_detokenize
)
detokenize_button.pack(pady=5)


# Ask AI button

ask_ai_button = tk.Button(
    main_frame,
    text="Ask AI",
    width=button_width,
    command=ask_ai
)
ask_ai_button.pack(pady=5)

# Clear button
clear_button = tk.Button(
    main_frame,
    text="Clear",
    width=button_width,
    command=clear_document
)
clear_button.pack(pady=5)

# Status Bar

status_label = tk.Label(
    main_frame,
    text="Status Bar",
    relief="sunken",
    anchor="w"
)

status_label.pack(side="bottom", fill="x", pady=10)


root.mainloop()
