import sqlite3
import os
from datetime import datetime


# ------------------------------------------------------------
# DATABASE PATH
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

os.makedirs(DATABASE_DIR, exist_ok=True)

DB_PATH = os.path.join(DATABASE_DIR, "expenses.db")


# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)


# ------------------------------------------------------------
# CREATE TABLES
# ------------------------------------------------------------

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            item TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment TEXT NOT NULL,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            monthly_budget REAL DEFAULT 5000
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO settings
        (id, monthly_budget)
        VALUES (1, 5000)
    """)

    connection.commit()
    connection.close()


# ------------------------------------------------------------
# ADD EXPENSE
# ------------------------------------------------------------

def add_expense(date, item, category, amount, payment, notes):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (date, item, category, amount, payment, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        item,
        category,
        amount,
        payment,
        notes
    ))

    connection.commit()
    connection.close()


# ------------------------------------------------------------
# GET ALL EXPENSES
# ------------------------------------------------------------

def get_all_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, item, category, amount, payment, notes
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


# ------------------------------------------------------------
# SEARCH EXPENSES
# ------------------------------------------------------------

def search_expenses(search):

    connection = get_connection()
    cursor = connection.cursor()

    search = f"%{search}%"

    cursor.execute("""
        SELECT id, date, item, category, amount, payment, notes
        FROM expenses
        WHERE item LIKE ?
           OR category LIKE ?
           OR payment LIKE ?
           OR notes LIKE ?
        ORDER BY date DESC, id DESC
    """, (
        search,
        search,
        search,
        search
    ))

    data = cursor.fetchall()

    connection.close()

    return data


# ------------------------------------------------------------
# DELETE EXPENSE
# ------------------------------------------------------------

def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()


# ------------------------------------------------------------
# UPDATE EXPENSE
# ------------------------------------------------------------

def update_expense(
    expense_id,
    date,
    item,
    category,
    amount,
    payment,
    notes
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET date = ?,
            item = ?,
            category = ?,
            amount = ?,
            payment = ?,
            notes = ?
        WHERE id = ?
    """, (
        date,
        item,
        category,
        amount,
        payment,
        notes,
        expense_id
    ))

    connection.commit()
    connection.close()


# ------------------------------------------------------------
# MONTHLY STATISTICS
# ------------------------------------------------------------

def get_monthly_statistics():

    current_month = datetime.now().strftime("%Y-%m")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount), 0),
            COUNT(*)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
    """, (current_month,))

    result = cursor.fetchone()

    total = result[0]
    count = result[1]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE category = 'Tiffin'
        AND substr(date, 1, 7) = ?
    """, (current_month,))

    tiffin = cursor.fetchone()[0]

    other = total - tiffin

    connection.close()

    return {
        "total": total,
        "tiffin": tiffin,
        "other": other,
        "count": count
    }


# ------------------------------------------------------------
# GET MONTHLY CATEGORY DATA
# ------------------------------------------------------------

def get_category_data():

    current_month = datetime.now().strftime("%Y-%m")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (current_month,))

    data = cursor.fetchall()

    connection.close()

    return data


# ------------------------------------------------------------
# GET DAILY SPENDING
# ------------------------------------------------------------

def get_daily_spending():

    current_month = datetime.now().strftime("%Y-%m")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, SUM(amount)
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY date
        ORDER BY date
    """, (current_month,))

    data = cursor.fetchall()

    connection.close()

    return data


# ------------------------------------------------------------
# RECENT EXPENSES
# ------------------------------------------------------------

def get_recent_expenses(limit=8):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, item, category, amount, payment
        FROM expenses
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    connection.close()

    return data


# ------------------------------------------------------------
# BUDGET
# ------------------------------------------------------------

def get_budget():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT monthly_budget
        FROM settings
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 5000


def update_budget(budget):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE settings
        SET monthly_budget = ?
        WHERE id = 1
    """, (budget,))

    connection.commit()
    connection.close()