import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


# -------------------------
# Button Functions (Stage 1)
# -------------------------

def select_file():
    path = filedialog.askopenfilename()
    if path:
        file_label.config(text=path)
        status_label.config(text="File selected")


def protect_info():
    status_label.config(text="Protect Personal Information clicked")


def detokenize():
    status_label.config(text="Detokenize clicked")


def ask_ai():
    status_label.config(text="Ask AI clicked")


def clear_document():
    document_box.delete("1.0", tk.END)
    file_label.config(text="<Path of selected file>")
    status_label.config(text="Document cleared")


# -------------------------
# Main Window
# -------------------------

root = tk.Tk()
root.title("Private AI Application")
root.geometry("900x550")


# -------------------------
# Left Panel
# -------------------------

left_frame = tk.Frame(root, bg="#f2f2f2", padx=10, pady=10)
left_frame.pack(side="left", fill="y")

title_label = tk.Label(
    left_frame,
    text="Private AI Application",
    font=("Arial", 14, "bold"),
    bg="#f2f2f2"
)
title_label.pack(pady=10)


select_button = tk.Button(
    left_frame,
    text="Select File",
    width=25,
    command=select_file
)
select_button.pack(pady=5)


file_label = tk.Label(
    left_frame,
    text="<Path of selected file>",
    width=30,
    relief="sunken"
)
file_label.pack(pady=5)


protect_button = tk.Button(
    left_frame,
    text="Protect Personal Information",
    width=25,
    command=protect_info
)
protect_button.pack(pady=10)


detokenize_button = tk.Button(
    left_frame,
    text="Detokenize",
    width=25,
    command=detokenize
)
detokenize_button.pack(pady=5)


ask_ai_button = tk.Button(
    left_frame,
    text="Ask AI",
    width=25,
    command=ask_ai
)
ask_ai_button.pack(pady=5)


clear_button = tk.Button(
    left_frame,
    text="Clear",
    width=25,
    command=clear_document
)
clear_button.pack(pady=5)


status_label = tk.Label(
    left_frame,
    text="Status Bar",
    relief="sunken",
    anchor="w"
)
status_label.pack(side="bottom", fill="x", pady=20)


# -------------------------
# Right Panel
# -------------------------

right_frame = tk.Frame(root)
right_frame.pack(side="right", expand=True, fill="both")


doc_label = tk.Label(
    right_frame,
    text="Document",
    font=("Arial", 12, "bold")
)
doc_label.pack(pady=5)


document_box = ScrolledText(
    right_frame,
    width=60,
    height=25
)
document_box.pack(padx=10, pady=10)


# -------------------------
# Run Application
# -------------------------

root.mainloop()
