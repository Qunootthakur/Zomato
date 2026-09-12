import tkinter as tk
from tkinter import ttk

import database
import styles


class Dashboard:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(
            parent,
            bg=styles.BACKGROUND
        )

        self.create_dashboard()

    # --------------------------------------------------------
    # SHOW
    # --------------------------------------------------------

    def show(self):

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.refresh()

    # --------------------------------------------------------
    # HIDE
    # --------------------------------------------------------

    def hide(self):

        self.frame.pack_forget()

    # --------------------------------------------------------
    # CREATE DASHBOARD
    # --------------------------------------------------------

    def create_dashboard(self):

        # Header
        header = tk.Frame(
            self.frame,
            bg=styles.BACKGROUND
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 10)
        )

        tk.Label(
            header,
            text="Dashboard",
            font=styles.FONT_TITLE,
            bg=styles.BACKGROUND,
            fg=styles.TEXT
        ).pack(side="left")

        tk.Label(
            header,
            text="Monthly Food Overview",
            font=("Arial", 11),
            bg=styles.BACKGROUND,
            fg=styles.SECONDARY_TEXT
        ).pack(
            side="right",
            pady=10
        )

        # Cards
        self.cards_frame = tk.Frame(
            self.frame,
            bg=styles.BACKGROUND
        )

        self.cards_frame.pack(
            fill="x",
            padx=35,
            pady=15
        )

        # Budget
        self.budget_frame = tk.Frame(
            self.frame,
            bg=styles.WHITE
        )

        self.budget_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )

        # Recent
        tk.Label(
            self.frame,
            text="Recent Expenses",
            font=styles.FONT_HEADING,
            bg=styles.BACKGROUND
        ).pack(
            anchor="w",
            padx=35,
            pady=(20, 10)
        )

        self.table_frame = tk.Frame(
            self.frame,
            bg=styles.WHITE
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 20)
        )

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    def refresh(self):

        stats = database.get_monthly_statistics()

        # Clear cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        cards = [
            (
                "💰",
                "Total Spent",
                f"₹{stats['total']:.2f}",
                styles.PRIMARY
            ),
            (
                "🍱",
                "Tiffin",
                f"₹{stats['tiffin']:.2f}",
                styles.ORANGE
            ),
            (
                "🍔",
                "Other Food",
                f"₹{stats['other']:.2f}",
                styles.BLUE
            ),
            (
                "📋",
                "Transactions",
                str(stats["count"]),
                styles.GREEN
            )
        ]

        for card in cards:

            widget = styles.create_card(
                self.cards_frame,
                card[0],
                card[1],
                card[2],
                card[3]
            )

            widget.pack(
                side="left",
                fill="both",
                expand=True,
                padx=6
            )

        self.update_budget(stats)
        self.update_recent()

    # --------------------------------------------------------
    # BUDGET
    # --------------------------------------------------------

    def update_budget(self, stats):

        for widget in self.budget_frame.winfo_children():
            widget.destroy()

        budget = database.get_budget()

        remaining = budget - stats["total"]

        tk.Label(
            self.budget_frame,
            text="Monthly Budget",
            font=styles.FONT_SUBHEADING,
            bg=styles.WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        tk.Label(
            self.budget_frame,
            text=(
                f"₹{stats['total']:.2f} spent  /  "
                f"₹{budget:.2f} budget  →  "
                f"₹{remaining:.2f} remaining"
            ),
            font=styles.FONT_NORMAL,
            bg=styles.WHITE,
            fg=styles.SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=20
        )

        progress = ttk.Progressbar(
            self.budget_frame,
            orient="horizontal",
            mode="determinate"
        )

        progress.pack(
            fill="x",
            padx=20,
            pady=15
        )

        if budget > 0:
            percentage = (
                stats["total"] /
                budget
            ) * 100
        else:
            percentage = 0

        progress["value"] = min(
            percentage,
            100
        )

    # --------------------------------------------------------
    # RECENT EXPENSES
    # --------------------------------------------------------

    def update_recent(self):

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        columns = (
            "date",
            "item",
            "category",
            "amount",
            "payment"
        )

        tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "date": "Date",
            "item": "Food Item",
            "category": "Category",
            "amount": "Amount",
            "payment": "Payment"
        }

        for column in columns:

            tree.heading(
                column,
                text=headings[column]
            )

        tree.column("date", width=120)
        tree.column("item", width=250)
        tree.column("category", width=150)
        tree.column("amount", width=120)
        tree.column("payment", width=130)

        rows = database.get_recent_expenses()

        for row in rows:

            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    f"₹{row[3]:.2f}",
                    row[4]
                )
            )

        scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )