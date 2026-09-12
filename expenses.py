import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import database
import styles


class Expenses:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(
            parent,
            bg=styles.BACKGROUND
        )

        self.create_page()

    # --------------------------------------------------------
    # SHOW
    # --------------------------------------------------------

    def show(self):

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.load_expenses()

    # --------------------------------------------------------
    # HIDE
    # --------------------------------------------------------

    def hide(self):

        self.frame.pack_forget()

    # --------------------------------------------------------
    # CREATE PAGE
    # --------------------------------------------------------

    def create_page(self):

        tk.Label(
            self.frame,
            text="Expense History",
            font=styles.FONT_TITLE,
            bg=styles.BACKGROUND
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 15)
        )

        # Search bar
        search_frame = tk.Frame(
            self.frame,
            bg=styles.BACKGROUND
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search",
            font=("Arial", 10, "bold"),
            bg=styles.BACKGROUND
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 10),
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        styles.create_button(
            search_frame,
            "Search",
            self.search
        ).pack(side="left")

        styles.create_button(
            search_frame,
            "Show All",
            self.load_expenses,
            bg=styles.DARK
        ).pack(
            side="left",
            padx=5
        )

        # Add expense button
        styles.create_button(
            search_frame,
            "+ Add Expense",
            self.open_add_window
        ).pack(
            side="right"
        )

        # Table
        table_frame = tk.Frame(
            self.frame,
            bg=styles.WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        columns = (
            "id",
            "date",
            "item",
            "category",
            "amount",
            "payment",
            "notes"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "date": "Date",
            "item": "Food Item",
            "category": "Category",
            "amount": "Amount",
            "payment": "Payment",
            "notes": "Notes"
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

        self.tree.column("id", width=50)
        self.tree.column("date", width=110)
        self.tree.column("item", width=200)
        self.tree.column("category", width=130)
        self.tree.column("amount", width=100)
        self.tree.column("payment", width=120)
        self.tree.column("notes", width=200)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Bottom buttons
        bottom = tk.Frame(
            self.frame,
            bg=styles.BACKGROUND
        )

        bottom.pack(
            pady=(0, 20)
        )

        styles.create_button(
            bottom,
            "✏ Edit Selected",
            self.edit_selected,
            bg=styles.BLUE
        ).pack(
            side="left",
            padx=5
        )

        styles.create_button(
            bottom,
            "🗑 Delete Selected",
            self.delete_selected,
            bg=styles.DARK
        ).pack(
            side="left",
            padx=5
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.edit_selected()
        )

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    def load_expenses(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        data = database.get_all_expenses()

        self.insert_rows(data)

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    def search(self):

        text = self.search_entry.get().strip()

        if not text:

            self.load_expenses()
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        data = database.search_expenses(text)

        self.insert_rows(data)

    # --------------------------------------------------------
    # INSERT ROWS
    # --------------------------------------------------------

    def insert_rows(self, data):

        for row in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    f"₹{row[4]:.2f}",
                    row[5],
                    row[6]
                )
            )

    # --------------------------------------------------------
    # ADD WINDOW
    # --------------------------------------------------------

    def open_add_window(self):

        self.open_form()

    # --------------------------------------------------------
    # EDIT
    # --------------------------------------------------------

    def edit_selected(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense first."
            )

            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.open_form(values)

    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    def open_form(self, values=None):

        edit_mode = values is not None

        window = tk.Toplevel(
            self.parent
        )

        window.title(
            "Edit Expense"
            if edit_mode
            else
            "Add Expense"
        )

        window.geometry("520x600")
        window.resizable(False, False)
        window.configure(
            bg=styles.WHITE
        )

        tk.Label(
            window,
            text=(
                "Edit Expense"
                if edit_mode
                else
                "Add Food Expense"
            ),
            font=("Arial", 20, "bold"),
            bg=styles.WHITE
        ).pack(
            pady=(25, 20)
        )

        form = tk.Frame(
            window,
            bg=styles.WHITE
        )

        form.pack(
            padx=40,
            fill="both"
        )

        # Date
        self.form_label(
            form,
            "Date"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        date_entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=35
        )

        date_entry.grid(
            row=1,
            column=0,
            pady=(0, 12)
        )

        date_entry.insert(
            0,
            values[1]
            if edit_mode
            else datetime.now().strftime("%Y-%m-%d")
        )

        # Item
        self.form_label(
            form,
            "Food / Item Name"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        item_entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=35
        )

        item_entry.grid(
            row=3,
            column=0,
            pady=(0, 12)
        )

        if edit_mode:
            item_entry.insert(0, values[2])

        # Category
        self.form_label(
            form,
            "Category"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        category_combo = ttk.Combobox(
            form,
            values=[
                "Tiffin",
                "Breakfast",
                "Lunch",
                "Dinner",
                "Snacks",
                "Biryani",
                "Fast Food",
                "Beverages",
                "Groceries",
                "Other"
            ],
            state="readonly",
            width=32
        )

        category_combo.grid(
            row=5,
            column=0,
            pady=(0, 12)
        )

        category_combo.set(
            values[3]
            if edit_mode
            else "Tiffin"
        )

        # Amount
        self.form_label(
            form,
            "Amount (₹)"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        amount_entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=35
        )

        amount_entry.grid(
            row=7,
            column=0,
            pady=(0, 12)
        )

        if edit_mode:

            amount = str(
                values[4]
            ).replace("₹", "")

            amount_entry.insert(
                0,
                amount
            )

        # Payment
        self.form_label(
            form,
            "Payment Method"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        payment_combo = ttk.Combobox(
            form,
            values=[
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Other"
            ],
            state="readonly",
            width=32
        )

        payment_combo.grid(
            row=9,
            column=0,
            pady=(0, 12)
        )

        payment_combo.set(
            values[5]
            if edit_mode
            else "UPI"
        )

        # Notes
        self.form_label(
            form,
            "Notes"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            pady=(5, 3)
        )

        notes_entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=35
        )

        notes_entry.grid(
            row=11,
            column=0,
            pady=(0, 20)
        )

        if edit_mode:
            notes_entry.insert(
                0,
                values[6]
            )

        # Save
        def save():

            date = date_entry.get().strip()
            item = item_entry.get().strip()
            category = category_combo.get()
            amount = amount_entry.get().strip()
            payment = payment_combo.get()
            notes = notes_entry.get().strip()

            if not date or not item or not amount:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all required fields."
                )

                return

            try:

                datetime.strptime(
                    date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date",
                    "Date must be YYYY-MM-DD."
                )

                return

            try:

                amount = float(amount)

                if amount <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid amount."
                )

                return

            if edit_mode:

                database.update_expense(
                    values[0],
                    date,
                    item,
                    category,
                    amount,
                    payment,
                    notes
                )

            else:

                database.add_expense(
                    date,
                    item,
                    category,
                    amount,
                    payment,
                    notes
                )

            window.destroy()

            self.load_expenses()

        styles.create_button(
            window,
            "✓ Save Expense",
            save
        ).pack(
            pady=10
        )

    # --------------------------------------------------------
    # LABEL HELPER
    # --------------------------------------------------------

    def form_label(self, parent, text):

        return tk.Label(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg=styles.WHITE
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete_selected(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an expense first."
            )

            return

        values = self.tree.item(
            selected[0]
        )["values"]

        expense_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        database.delete_expense(
            expense_id
        )

        self.load_expenses()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully."
        )