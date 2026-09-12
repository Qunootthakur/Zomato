import tkinter as tk
from tkinter import messagebox
import os

import database
import styles

from dashboard import Dashboard
from expenses import Expenses
from analytics import Analytics


class FoodExpenseTracker:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "FoodTrack - Food & Tiffin Expense Tracker"
        )

        self.root.geometry(
            "1200x750"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg=styles.BACKGROUND
        )

        # Configure application styles
        styles.configure_styles()

        # Initialize SQLite database
        database.initialize_database()

        # Create sidebar
        self.create_sidebar()

        # Main content area
        self.main_area = tk.Frame(
            self.root,
            bg=styles.BACKGROUND
        )

        self.main_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Create application pages
        self.dashboard = Dashboard(
            self.main_area
        )

        self.expenses = Expenses(
            self.main_area
        )

        self.analytics = Analytics(
            self.main_area
        )

        # Open Dashboard
        self.show_dashboard()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=styles.PRIMARY,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        # Logo
        tk.Label(
            self.sidebar,
            text="🍴",
            font=("Arial", 32),
            bg=styles.PRIMARY,
            fg=styles.WHITE
        ).pack(
            pady=(30, 0)
        )

        tk.Label(
            self.sidebar,
            text="FoodTrack",
            font=("Arial", 22, "bold"),
            bg=styles.PRIMARY,
            fg=styles.WHITE
        ).pack()

        tk.Label(
            self.sidebar,
            text="Food & Tiffin Manager",
            font=("Arial", 9),
            bg=styles.PRIMARY,
            fg="#FFE6E8"
        ).pack(
            pady=(0, 30)
        )

        # Navigation buttons
        self.create_nav_button(
            "🏠   Dashboard",
            self.show_dashboard
        )

        self.create_nav_button(
            "➕   Add Expense",
            self.show_add_expense
        )

        self.create_nav_button(
            "📋   Expense History",
            self.show_expenses
        )

        self.create_nav_button(
            "📊   Analytics",
            self.show_analytics
        )

        # Bottom text
        tk.Label(
            self.sidebar,
            text="SQLite Database",
            font=("Arial", 9),
            bg=styles.PRIMARY,
            fg="#FFD9DC"
        ).pack(
            side="bottom",
            pady=20
        )

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(
        self,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            activebackground=styles.PRIMARY_DARK,
            activeforeground=styles.WHITE,
            relief="flat",
            anchor="w",
            padx=25,
            pady=15,
            bd=0,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=10,
            pady=2
        )

    # ========================================================
    # HIDE ALL PAGES
    # ========================================================

    def hide_pages(self):

        self.dashboard.hide()
        self.expenses.hide()
        self.analytics.hide()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.hide_pages()

        self.dashboard.show()

    # ========================================================
    # ADD EXPENSE
    # ========================================================

    def show_add_expense(self):

        self.hide_pages()

        self.expenses.show()

        self.expenses.open_add_window()

    # ========================================================
    # EXPENSE HISTORY
    # ========================================================

    def show_expenses(self):

        self.hide_pages()

        self.expenses.show()

    # ========================================================
    # ANALYTICS
    # ========================================================

    def show_analytics(self):

        self.hide_pages()

        self.analytics.show()

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        confirm = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if confirm:

            self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    # --------------------------------------------------------
    # APPLICATION ICON
    # --------------------------------------------------------

    icon_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "zomato.ico"
    )

    if os.path.exists(icon_path):

        root.iconbitmap(
            icon_path
        )

    else:

        print(
            "Warning: app_icon.ico not found."
        )

    # --------------------------------------------------------
    # CREATE APPLICATION
    # --------------------------------------------------------

    app = FoodExpenseTracker(
        root
    )

    # --------------------------------------------------------
    # HANDLE WINDOW CLOSE
    # --------------------------------------------------------

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close_application
    )

    # --------------------------------------------------------
    # START TKINTER
    # --------------------------------------------------------

    root.mainloop()