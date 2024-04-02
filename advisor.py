import tkinter as tk
from tkinter import ttk
import mysql.connector
import datetime

def provide_financial_advice(user_info):
    income = user_info.get('income', 0)
    expenses = user_info.get('expenses', 0)
    budget = user_info.get('budget', 0)
    savings = income - expenses

    advice = ""

    if savings > 0:
        advice += "You have a positive cash flow. Consider allocating some of your savings towards investments.\n"
    elif savings < 0:
        advice += "Your expenses exceed your income. Review your budget and look for areas to cut back on spending.\n"
    else:
        advice += "Your income equals your expenses. Consider finding ways to increase your income or reduce expenses.\n"

    if income > expenses:
        advice += "Consider setting aside a portion of your income for emergency savings or retirement funds.\n"

    return advice

def fetch_monthly_total_expenses(year, month):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"
        )

        cursor = conn.cursor()

        # Calculate the start and end dates of the month
        start_date = datetime.datetime(year, month, 1)
        end_date = start_date + datetime.timedelta(days=32)

        # Fetch total expenses for the specified month
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN %s AND %s",
                       (start_date, end_date))
        row = cursor.fetchone()

        total_expenses = row[0] if row and row[0] else 0

        return total_expenses

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def fetch_monthly_data_from_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"
        )

        cursor = conn.cursor()

        # Fetch total income
        cursor.execute("SELECT SUM(amount) FROM income")
        total_income = next(cursor)[0]

        # Fetch total expenses for the current month
        today = datetime.date.today()
        year, month = today.year, today.month
        total_expenses = fetch_monthly_total_expenses(year, month)

        # Fetch the total budget limit for the current month
        cursor.execute("SELECT SUM(budget_limit) FROM budget WHERE YEAR(budget_date) = %s AND MONTH(budget_date) = %s",
                       (year, month))
        total_budget = next(cursor)[0]

        return {
            'income': total_income,
            'expenses': total_expenses,
            'total_budget': total_budget
        }

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def display_advice():
    user_info = fetch_monthly_data_from_database()
    if user_info:
        # Create a new window
        advisor_window = tk.Tk()
        advisor_window.title("Financial Advice")

        # Create a frame to display totals and advice
        totals_frame = ttk.Frame(advisor_window, padding="10")
        totals_frame.pack(fill="both", expand=True)

        # Get financial totals in Kenyan Shillings
        total_income = user_info.get('income', 0)
        total_expenses = user_info.get('expenses', 0)
        total_budget = user_info.get('total_budget', 0)

        # Display total income in Kenyan Shillings
        income_label = ttk.Label(totals_frame, text=f"Total Income: KES {total_income:,.2f}")
        income_label.pack(pady=5)

        # Display total expenses in Kenyan Shillings
        expenses_label = ttk.Label(totals_frame, text=f"Total Expenses: KES {total_expenses:,.2f}")
        expenses_label.pack(pady=5)

        # Display total budget in Kenyan Shillings
        budget_label = ttk.Label(totals_frame, text=f"Total Budget: KES {total_budget:,.2f}")
        budget_label.pack(pady=5)

        # Get financial advice
        advice = provide_financial_advice(user_info)

        # Create a frame for displaying advice
        advice_frame = ttk.Frame(advisor_window, padding="10")
        advice_frame.pack(fill="both", expand=True)

        # Display financial advice
        advice_label = ttk.Label(advice_frame, text=advice, wraplength=400)
        advice_label.pack(pady=10)

        # Run the Tkinter event loop
        advisor_window.mainloop()


# Example usage:
display_advice()
