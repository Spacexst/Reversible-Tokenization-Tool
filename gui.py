from db import (
    get_all_tokens,
    get_audit_logs,

    get_original
)
import pii_tokenizer
import datetime
import webbrowser
import os
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk


# USER DATABASE + LOGGER
USERS = {
    "alice": {"password": "1234", "role": "admin"},
    "bob": {"password": "abcd", "role": "operator"},
    "carol": {"password": "pass", "role": "auditor"},
}


def log_action(user, action, reason=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] User={user}, Action={action}"
    if reason:
        entry += f", Reason={reason}"
    print(entry)  # Replace with file logging if needed


# LOGIN WINDOW

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x280")

        tk.Label(self, text="Username").pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = USERS.get(username)

        if user and user["password"] == password:
            self.destroy()
            launch_main_app(username, user["role"])
        else:
            messagebox.showerror("Error", "Invalid username or password")


# ADMIN WINDOW

class AdminWindow(tk.Toplevel):
    def __init__(self, username, role):
        super().__init__()
        self.title("Admin Tools")
        self.geometry("600x500")

        self.username = username
        self.role = role

        tk.Label(
            self,
            text=f"Admin Panel (User: {username})",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            self,
            text="View Token Mappings",
            width=30,
            command=self.view_token_mappings
        ).pack(pady=5)

        tk.Button(
            self,
            text="View Audit Logs",
            width=30,
            command=self.view_audit_logs
        ).pack(pady=5)

        tk.Button(
            self,
            text="Search by Token",
            width=30,
            command=self.search_by_value
        ).pack(pady=5)

    # SEARCH BY TOKEN

    def search_by_value(self):
        win = tk.Toplevel(self)
        win.title("Search by Token")
        win.geometry("350x180")

        tk.Label(win, text="Enter token to search:",
                 font=("Arial", 12)).pack(pady=10)

        entry = tk.Entry(win, width=30)
        entry.pack(pady=5)

        def do_search():
            token = entry.get().strip()
            if not token:
                messagebox.showwarning(
                    "Missing Input", "Please enter a token.")
                return

            value = get_original(token)
            if value is None:
                messagebox.showinfo(
                    "Not Found", "No value found for that token.")
            else:
                messagebox.showinfo(
                    "Original Value", f"Token: {token}\nValue: {value}")

        tk.Button(win, text="Search", width=12, command=do_search).pack(pady=5)

        # Cancel button closes the window
        tk.Button(win, text="Cancel", width=12,
                  command=win.destroy).pack(pady=5)

    # VIEW TOKEN MAPPINGS

    def view_token_mappings(self):
        if self.role != "admin":
            messagebox.showwarning(
                "Access Denied",
                "Only admins can view token mappings."
            )
            log_action(self.username, "DENIED: Token Mapping Access")
            return

        reason = simpledialog.askstring(
            "Reason Required",
            "Why do you need to view token mappings?"
        )
        if not reason:
            return

        log_action(self.username, "Viewed Token Mappings", reason)

        win = tk.Toplevel(self)
        win.title("Token Mappings")
        win.geometry("600x400")

        canvas = tk.Canvas(win)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        mappings = get_all_tokens(mask=False)

        if not mappings:
            tk.Label(
                scroll_frame,
                text="No token mappings found.",
                font=("Arial", 12)
            ).pack(pady=10)
            return

        for token, original in mappings:
            tk.Label(
                scroll_frame,
                text=f"{token}  →  {original}",
                font=("Arial", 11),
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=10, pady=2)

    # VIEW AUDIT LOGS

    def view_audit_logs(self):
        if self.role not in ("admin", "auditor"):
            messagebox.showwarning(
                "Access Denied",
                "You do not have permission to view audit logs."
            )
            log_action(self.username, "DENIED: Audit Log Access")
            return

        log_action(self.username, "Viewed Audit Logs")

        win = tk.Toplevel(self)
        win.title("Audit Logs")
        win.geometry("600x400")

        canvas = tk.Canvas(win)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        logs = get_audit_logs()

        if not logs:
            tk.Label(
                scroll_frame,
                text="No audit logs found.",
                font=("Arial", 12)
            ).pack(pady=10)
            return

        for log_id, token, action, timestamp in logs:
            tk.Label(
                scroll_frame,
                text=f"[{timestamp}]  {action}  →  {token}",
                font=("Arial", 11),
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=10, pady=2)


# MAIN APPLICATION

def launch_main_app(username, role):
    global root
    root = tk.Tk()
    root.title("Reversible Tokenization Tool")
    root.geometry("900x650")
    root.configure(bg="#f2f2f2")

    # store user info
    root.username = username
    root.role = role

    # LOGOUT FUNCTION
    def logout():
        root.destroy()
        messagebox.showinfo("Logout", "Logged out successfully")
        LoginWindow().mainloop()

    # FILE FUNCTION
    def select_file():
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            file_label.config(text=path)
            status_label.config(text="File selected")

    def run_tokenize():
        path = file_label.cget("text")
        if path != "No file selected" and os.path.exists(path):
            output_file = pii_tokenizer.tokenize_file(path)
            status_label.config(text=f"Tokenization complete: {output_file}")
            messagebox.showinfo("Success", "Your sensitive info is protected")
            os.startfile(output_file)
        else:
            status_label.config(text="Please select a valid file")

    def ask_ai():
        status_label.config(text="Select an AI tool")

        ai_window = tk.Toplevel()
        ai_window.title("Choose AI Tool")
        ai_window.geometry("400x330")
        ai_window.resizable(True, True)

        tk.Label(ai_window, text="Choose an AI tool", bg="white",
                 highlightbackground="gray",
                 highlightthickness=1,
                 relief="solid",
                 bd=1,
                 font=("Arial", 14, "bold")).pack(padx=20, fill="x", pady=10)

        def open_ai_tool(url, name):
            webbrowser.open(url)
            status_label.config(text=f"Opening {name}...")
            ai_window.destroy()

        tk.Button(ai_window, text="ChatGPT", width=25, bg="#10a37f",
                  font=("Arial", 11),
                  command=lambda: open_ai_tool("https://chat.openai.com/", "ChatGPT")).pack(pady=5)

        tk.Button(ai_window, text="Google Gemini", width=25,
                  font=("Arial", 11),
                  command=lambda: open_ai_tool("https://gemini.google.com/", "Gemini")).pack(pady=5)

        tk.Button(ai_window, text="Microsoft Copilot", width=25,
                  font=("Arial", 11),
                  command=lambda: open_ai_tool("https://copilot.microsoft.com/", "Copilot")).pack(pady=5)

        tk.Button(ai_window, text="Grok", width=25,
                  font=("Arial", 11),
                  command=lambda: open_ai_tool("https://grok.com/", "Grok")).pack(pady=5)

        tk.Button(ai_window, text="Claude", width=25,
                  font=("Arial", 11),
                  command=lambda: open_ai_tool("https://claude.ai/", "Claude")).pack(pady=5)

        tk.Button(ai_window, text="Cancel", width=25,
                  font=("Arial", 11),
                  command=ai_window.destroy).pack(pady=5)

        ai_window.grab_set()

    def run_detokenize():
        path = file_label.cget("text")
        if os.path.exists(path):
            try:
                output_file = pii_tokenizer.detokenize_file(path)
                status_label.config(
                    text=f"Detokenization complete: {output_file}")
                messagebox.showinfo(
                    "Success", "Your original data is restored")
                os.startfile(output_file)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            status_label.config(text="No file selected")

    def clear_document():
        file_label.config(text="No file selected")
        status_label.config(text="Document cleared")

    # ADMIN BUTTON HANDLER

    def open_admin_tools():
        if root.role not in ("admin", "auditor"):
            messagebox.showwarning(
                "Access Denied", "You do not have permission to access admin tools.")
            log_action(root.username, "DENIED: Attempted to open Admin Tools")
            return

        reason = simpledialog.askstring(
            "Access Reason", "Enter reason for accessing admin tools:")
        if not reason:
            return

        log_action(root.username, "Opened Admin Tools", reason)
        AdminWindow(root.username, root.role)

    # GUI LAYOUT

    title_label = tk.Label(root, text="Private AI application",
                           font=("Arial", 18, "bold"), bg="#f2f2f2")
    title_label.pack(pady=10)

    tk.Button(root, text="Logout",
              bg="blue", fg="white",
              command=logout).place(x=620, y=10)

    main_frame = tk.Frame(root, bg="#f2f2f2", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    button_width = 30
    button_font = ("Arial", 11)

    tk.Button(main_frame, text="Select File", width=25,
              font=button_font, command=select_file).pack(pady=5)

    file_label = tk.Label(main_frame, text="No file selected", width=50,
                          font=button_font, relief="sunken", bg="white")
    file_label.pack(pady=15)

    tk.Button(main_frame, text="Protect Data", width=button_width,
              font=button_font, command=run_tokenize).pack(pady=15)

    tk.Button(main_frame, text="Ask AI", width=button_width,
              font=button_font, command=ask_ai).pack(pady=15)

    tk.Button(main_frame, text="Restore Data", width=button_width,
              font=button_font, command=run_detokenize).pack(pady=15)

    tk.Button(main_frame, text="Clear", width=button_width,
              font=button_font, command=clear_document).pack(pady=5)

    # NEW ADMIN BUTTON
    tk.Button(main_frame, text="Admin Tools", width=button_width,
              font=button_font, command=open_admin_tools).pack(pady=10)

    status_label = tk.Label(main_frame, text="Status Bar",
                            font=button_font, relief="sunken", anchor="w")
    status_label.pack(side="bottom", fill="x", pady=10)

    root.mainloop()


# START APP

LoginWindow().mainloop()
