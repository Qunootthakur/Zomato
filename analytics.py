import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import database
import styles


class Analytics:

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

        self.refresh()

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
            text="Analytics",
            font=styles.FONT_TITLE,
            bg=styles.BACKGROUND
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.frame,
            text="Current Month",
            font=("Arial", 11),
            bg=styles.BACKGROUND,
            fg=styles.SECONDARY_TEXT
        ).pack(
            anchor="w",
            padx=35
        )

        self.chart_frame = tk.Frame(
            self.frame,
            bg=styles.WHITE
        )

        self.chart_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    def refresh(self):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        figure = Figure(
            figsize=(10, 6),
            dpi=100
        )

        # ====================================================
        # PIE CHART
        # ====================================================

        ax1 = figure.add_subplot(121)

        category_data = database.get_category_data()

        if category_data:

            labels = [
                row[0]
                for row in category_data
            ]

            amounts = [
                row[1]
                for row in category_data
            ]

            ax1.pie(
                amounts,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90
            )

            ax1.set_title(
                "Spending by Category",
                fontsize=12,
                fontweight="bold"
            )

        else:

            ax1.text(
                0.5,
                0.5,
                "No expense data",
                ha="center",
                va="center"
            )

            ax1.set_title(
                "Spending by Category"
            )

        # ====================================================
        # DAILY LINE GRAPH
        # ====================================================

        ax2 = figure.add_subplot(122)

        daily_data = database.get_daily_spending()

        if daily_data:

            dates = [
                row[0]
                for row in daily_data
            ]

            amounts = [
                row[1]
                for row in daily_data
            ]

            ax2.plot(
                dates,
                amounts,
                marker="o"
            )

            ax2.set_title(
                "Daily Spending",
                fontsize=12,
                fontweight="bold"
            )

            ax2.set_xlabel(
                "Date"
            )

            ax2.set_ylabel(
                "Amount (₹)"
            )

            ax2.tick_params(
                axis="x",
                rotation=45
            )

            ax2.grid(
                True,
                alpha=0.3
            )

        else:

            ax2.text(
                0.5,
                0.5,
                "No expense data",
                ha="center",
                va="center"
            )

            ax2.set_title(
                "Daily Spending"
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )