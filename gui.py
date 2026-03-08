import tkinter as tk

# -------------------------
# Main Window
# -------------------------

root = tk.Tk()
root.title("Private AI Application")
root.geometry("900x550")


# Left Panel

left_frame = tk.Frame(root, bg="#f2f2f2", padx=10, pady=10)
left_frame.pack(side="left", fill="y")

title_label = tk.Label(
    left_frame,
    text="Private AI Application",
    font=("Arial", 14, "bold"),
    bg="#f2f2f2"
)
title_label.pack(pady=10)
# -------------------------
# Button
# -------------------------


root.mainloop()
