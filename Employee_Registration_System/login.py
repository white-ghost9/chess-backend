import tkinter as tk
from tkinter import messagebox
from . import styles
from . import database
from . import dashboard


def launch_login(root):
    root.title("Employee Management System - Login")
    root.geometry("500x420")
    root.configure(bg=styles.BG_COLOR)
    root.resizable(True, True)
    root.state("zoomed")  # Open in maximized position

    # ======================================================
    # Login Card
    # ======================================================
    card = tk.Frame(
        root,
        bg=styles.CARD_COLOR,
        bd=0,
        relief="flat",
        padx=30,
        pady=30,
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="Admin Login",
        bg=styles.CARD_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.TITLE_FONT,
    ).pack(pady=(0, 20))

    # Username
    tk.Label(
        card,
        text="Username",
        bg=styles.CARD_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
        anchor="w",
    ).pack(fill="x")

    username_entry = tk.Entry(card, font=styles.NORMAL_FONT, width=30)
    username_entry.pack(ipady=6, pady=(5, 15))

    # Password
    tk.Label(
        card,
        text="Password",
        bg=styles.CARD_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
        anchor="w",
    ).pack(fill="x")

    password_entry = tk.Entry(card, font=styles.NORMAL_FONT, width=30, show="*")
    password_entry.pack(ipady=6, pady=(5, 20))

    # ======================================================
    # Login Function
    # ======================================================
    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both username and password.",
                parent=root,
            )
            return

        if database.validate_admin(username, password):
            root.destroy()
            dashboard.open_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=root,
            )

    # Login Button
    tk.Button(
        card,
        text="🔐 Login",
        bg=styles.BUTTON_COLOR,
        activebackground=styles.BUTTON_HOVER,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=20,
        relief="flat",
        cursor="hand2",
        command=attempt_login,
    ).pack(pady=5, ipady=4)

    # Press Enter to login
    root.bind("<Return>", lambda event: attempt_login())

    # Footer
    tk.Label(
        root,
        text="Employee Management System",
        bg=styles.BG_COLOR,
        fg=styles.SUBTEXT_COLOR,
        font=styles.SMALL_FONT,
    ).pack(side="bottom", pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    launch_login(root)
    root.mainloop()
