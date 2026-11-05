Personal Expense Tracker with CSV

A menu-driven command-line program that records daily expenses by category, saves them to expenses.csv so they survive restarts, and shows totals.

How to run

Requires Python 3.10+ (only the standard library is used).

python expense_tracker.py

expenses.csv is created automatically (with the header row) if it is missing.

Menu
Option	What it does
1 Add expense	Asks for date, category, description and amount, then saves it
2 View all	Shows every expense in a table, oldest first, with a total
3 Filter	Filter by category, or by month (YYYY-MM)
4 Summary	Total per category, grand total and the biggest single expense
5 Quit	Exit the program

Categories: Food, Travel, Study, Bills, Fun.

Validation
Date must be a real date in YYYY-MM-DD format (press Enter for today).
Category must be one of the five above (any letter case).
Description cannot be empty (commas are fine).
Amount must be a number and cannot be negative.
Invalid input is rejected immediately and the question is asked again.
Example expenses.csv
date,category,description,amount
2026-09-03,Food,"Lunch, thali",120.50
2026-09-05,Travel,Metro card recharge,500.00
2026-10-02,Bills,Electricity bill,1120.00
2026-10-15,Study,Online course,1999.00

All data in the sample file is made up.

Files
expense_tracker.py - the program
expenses.csv - sample data (12 made-up expenses across September and October 2026)