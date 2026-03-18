import tkinter as tk
import webbrowser
from tkinter import filedialog
import os
from tkinter import messagebox
import pii_tokenizer


def run_tokenize():
    path = file_label.cget("text")
    if path != "No file selected" and os.path.exists(path):
        output_file = pii_tokenizer.tokenize_file(path)
        status_label.config(text=f"Tokenization complete: {output_file}")
        os.startfile(output_file)

    else:
        status_label.config(text="Please select a valid file")


# button functions

def select_file():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        file_label.config(text=path)
        status_label.config(text="File selected")


def ask_ai():
    status_label.config(text="Select an AI tool")

    ai_window = tk.Toplevel()
    ai_window.title("Choose AI Tool")
    ai_window.geometry("330x230")
    ai_window.resizable(False, False)

    tk.Label(ai_window, text="Choose an AI tool",
             font=("Arial", 14, "bold")).pack(pady=10)

    def open_chatgpt():
        webbrowser.open("https://chat.openai.com/")
        status_label.config(text="Opening ChatGPT...")
        ai_window.destroy()

    def open_gemini():
        webbrowser.open("https://gemini.google.com/")
        status_label.config(text="Opening Gemini...")
        ai_window.destroy()

    def open_copilot():
        webbrowser.open("https://copilot.microsoft.com")
        status_label.config(text="Opening Copilot...")
        ai_window.destroy()

    tk.Button(ai_window,
              text="ChatGPT",
              width=25,
              bg="#10a37f",
              fg="white",
              command=open_chatgpt
              ).pack(pady=5)

    tk.Button(ai_window,
              text="Google Gemini",
              width=25,
              command=open_gemini
              ).pack(pady=5)

    tk.Button(ai_window,
              text="Microsoft Copilot",
              width=25,
              command=open_copilot
              ).pack(pady=5)

    tk.Button(ai_window,
              text="Cancel",
              width=25,
              command=ai_window.destroy
              ).pack(pady=5)
    ai_window.grab_set()


def run_detokenize():
    path = file_label.cget("text")

    if os.path.exists(path):
        try:
            output_file = pii_tokenizer.detokenize_file(path)

            status_label.config(text=f"Detokenization complete: {output_file}")
            messagebox.showinfo("Success", "Detokenization completed")

            os.startfile(output_file)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    else:
        status_label.config(text="No file selected")


def run_detokenize():
    path = file_label.cget("text")
    if os.path.exists(path):
        output_file = pii_tokenizer.detokenize_file(path)
        status_label.config(text=f"Detokenization complete: {output_file}")
        messagebox.showinfo("Success", "Detokenization completed")

    # opens the file automatically
        os.startfile(output_file)
    else:
        status_label.config(text="No file selected")


# def ask_ai():
    # status_label.config(text="Ask AI clicked")


def clear_document():
    file_label.config(text="No file selected")
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
    text="No file selected",
    width=40,
    relief="sunken",
    bg="white"
)
file_label.pack(pady=5)


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
