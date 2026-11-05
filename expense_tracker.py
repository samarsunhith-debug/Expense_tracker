"""Personal Expense Tracker with CSV (InternCircle Project 3).

Record daily expenses by category, save them to expenses.csv so they survive
restarts, then view, filter and summarise them from a simple menu.
"""

import csv
import math
import os
from collections import defaultdict
from datetime import date, datetime

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun"]
DATE_FORMAT = "%Y-%m-%d"


# ---------- Storage helpers ----------

def ensure_file():
    """Create expenses.csv with the header row if it does not exist yet."""
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, FIELDS).writeheader()


def ends_with_newline():
    """Return True if the file is empty or its last character is a newline."""
    with open(FILE, "rb") as f:
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            return True
        f.seek(-1, os.SEEK_END)
        return f.read(1) in (b"\n", b"\r")


def save_expense(row):
    """Append one expense (a dict with the four fields) to the CSV file."""
    ensure_file()
    # A file edited by hand may lack a final newline; without this fix the new
    # row would be glued onto the end of the last line.
    if not ends_with_newline():
        with open(FILE, "a", newline="", encoding="utf-8") as f:
            f.write("\n")
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, FIELDS).writerow(row)


def load_expenses():
    """Return all expenses as a list of dicts, with amount converted to float."""
    ensure_file()
    expenses = []
    with open(FILE, newline="", encoding="utf-8") as f:
        for line_number, row in enumerate(csv.DictReader(f), start=2):
            try:
                row["amount"] = float(row["amount"])
                datetime.strptime(row["date"], DATE_FORMAT)
            except (ValueError, TypeError, KeyError):
                print(f"Skipping unreadable row {line_number} in {FILE}.")
                continue
            expenses.append(row)
    return expenses


# ---------- Input helpers (validate at the moment of input) ----------

def read_date(prompt):
    """Ask for a date as YYYY-MM-DD; Enter means today."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return date.today().strftime(DATE_FORMAT)
        try:
            datetime.strptime(text, DATE_FORMAT)
            return text
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-10-04.")


def read_category(prompt):
    """Ask until the user types one of the known categories (any letter case)."""
    options = ", ".join(CATEGORIES)
    while True:
        text = input(prompt).strip().title()
        if text in CATEGORIES:
            return text
        print(f"Unknown category. Choose one of: {options}.")


def read_description(prompt):
    """Ask until the description is not empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Description cannot be empty.")


def read_amount(prompt):
    """Ask until the user types a valid, non-negative amount."""
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
        except ValueError:
            print("Amount must be a number, for example 120.50.")
            continue
        if not math.isfinite(amount):
            print("Please enter a normal number.")
        elif amount < 0:
            print("Amount cannot be negative.")
        else:
            return round(amount, 2)


def read_month(prompt):
    """Ask for a month as YYYY-MM."""
    while True:
        text = input(prompt).strip()
        try:
            datetime.strptime(text, "%Y-%m")
            return text
        except ValueError:
            print("Invalid month. Use YYYY-MM, for example 2026-10.")


# ---------- Features ----------

def add_expense():
    """Ask for the four fields and save the new expense."""
    row = {
        "date": read_date("Date (YYYY-MM-DD, Enter for today): "),
        "category": read_category(f"Category ({', '.join(CATEGORIES)}): "),
        "description": read_description("Description: "),
        "amount": f"{read_amount('Amount: '):.2f}",
    }
    save_expense(row)
    print("Expense saved.")


def print_table(rows):
    """Print expenses (oldest first) in a tidy table with a total."""
    if not rows:
        print("No expenses to show.")
        return
    print(f"\n{'Date':<12}{'Category':<10}{'Description':<28}{'Amount':>10}")
    print("-" * 60)
    for r in sorted(rows, key=lambda r: r["date"]):
        description = r["description"][:26]
        print(f"{r['date']:<12}{r['category']:<10}{description:<28}{r['amount']:>10.2f}")
    print("-" * 60)
    print(f"{len(rows)} expense(s), total {sum(r['amount'] for r in rows):.2f}")


def filter_expenses(expenses):
    """Filter by category or by month and show the matching expenses."""
    print("\nFilter by: 1) Category  2) Month  3) Back")
    choice = input("Choose: ").strip()
    if choice == "1":
        category = read_category("Category: ")
        print_table([r for r in expenses if r["category"] == category])
    elif choice == "2":
        month = read_month("Month (YYYY-MM): ")
        print_table([r for r in expenses if r["date"][:7] == month])
    elif choice != "3":
        print("Invalid choice.")


def totals_by_category(expenses):
    """Return a dict of total spending per category."""
    totals = defaultdict(float)
    for r in expenses:
        totals[r["category"]] += r["amount"]
    return dict(totals)


def show_summary(expenses):
    """Show totals per category, the grand total and the biggest expense."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    totals = totals_by_category(expenses)
    print(f"\n{'Category':<12}{'Total':>12}")
    print("-" * 24)
    for category, total in sorted(totals.items(), key=lambda item: -item[1]):
        print(f"{category:<12}{total:>12.2f}")
    print("-" * 24)
    print(f"{'GRAND TOTAL':<12}{sum(totals.values()):>12.2f}")
    biggest = max(expenses, key=lambda r: r["amount"])
    print(f"\nBiggest expense: {biggest['amount']:.2f} - {biggest['description']} "
          f"({biggest['category']}, {biggest['date']})")


# ---------- Menu ----------

def main():
    """Run the menu until the user chooses Quit."""
    while True:
        print("\n===== Expense Tracker =====")
        print("1) Add expense")
        print("2) View all")
        print("3) Filter")
        print("4) Summary")
        print("5) Quit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            print_table(load_expenses())
        elif choice == "3":
            filter_expenses(load_expenses())
        elif choice == "4":
            show_summary(load_expenses())
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")


if __name__ == "__main__":
    main()
