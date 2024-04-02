import os
import tkinter as tk
from tkinter import ttk, messagebox
import random
import mysql.connector
import subprocess
from tkcalendar import DateEntry  # Make sure to install the tkcalendar module
from datetime import datetime
from PIL import Image, ImageTk
from datetime import datetime
import pandas as pd
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton


class DetailsFrame(ttk.Frame):
    def __init__(self, master=None, home_callback=None):
        super().__init__(master)
        self.home_callback = home_callback
        self.create_widgets()

    def create_widgets(self):
        # Add widgets for the details page
        details_label = tk.Label(self, text="Details Page Content", font=("Helvetica", 16))
        details_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Define occupation_options within the scope of DetailsFrame
        occupation_options = ["Engineer", "Teacher", "Doctor", "Artist", "Programmer", "Entrepreneur", "Nurse",
                              "Student", "Manager", "Accountant"]

        # Add widgets for collecting personal details
        personal_details_widgets = [
            (tk.Label(self, text="Name:"), tk.Entry(self)),
            (tk.Label(self, text="Contact Number:"), tk.Entry(self)),
            (tk.Label(self, text="Email:"), tk.Entry(self)),
            (tk.Label(self, text="Gender:"), ttk.Combobox(self, values=["Male", "Female"])),
            (tk.Label(self, text="Occupation:"), ttk.Combobox(self, values=occupation_options)),
            (tk.Label(self, text="Source of Income:"), tk.Entry(self)),
        ]

        # Use grid for labels and entry widgets
        for row, (label, widget) in enumerate(personal_details_widgets, start=1):
            label.grid(row=row, column=0, padx=5, pady=5, sticky=tk.E)
            widget.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)

        # Add a button to submit the details
        submit_button = tk.Button(self, text="Submit", command=lambda: self.submit_to_database(
            personal_details_widgets[0][1].get(),  # Name
            personal_details_widgets[1][1].get(),  # Contact Number
            personal_details_widgets[2][1].get(),  # Email
            personal_details_widgets[3][1].get(),  # Gender
            personal_details_widgets[4][1].get(),  # Occupation
            personal_details_widgets[5][1].get(),  # Source of Income
        ))
        submit_button.grid(row=len(personal_details_widgets) + 1, columnspan=2, pady=10)

        # Add a button to go back to the home page
        back_button = tk.Button(self, text="Back", command=self.go_back)
        back_button.grid(row=len(personal_details_widgets) + 2, columnspan=2, pady=10)

    def submit_to_database(self, name, contact, email, gender, occupation, income):
        # Validate contact format (assuming it should be 10 digits)
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Invalid contact format. Please enter a 10-digit number.")
            return

        # Validate email format (you can use a more sophisticated email validation)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
            return

        # Validate gender selection
        if gender not in ("Male", "Female"):
            messagebox.showerror("Error", "Invalid gender selection. Please choose 'Male' or 'Female'.")
            return

        try:
            # Connect to the MySQL database (replace with your actual database connection)
            conn = mysql.connector.connect(
                host="localhost",  # Update with your MySQL host
                user="root",
                password="",  # Update with your MySQL password
                database="personal_finance"  # Update with your database name
            )

            cursor = conn.cursor()

            # Create a table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    contact VARCHAR(20) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    occupation VARCHAR(50) NOT NULL,
                    income VARCHAR(50) NOT NULL,
                    CONSTRAINT chk_contact CHECK (LENGTH(contact) = 10),
                    CONSTRAINT chk_email CHECK (email LIKE '%@%.%')  -- Example email validation (basic)
                )
            ''')

            # Insert data into the table
            cursor.execute('''
                INSERT INTO user_info (name, contact, email, gender, occupation, income)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, contact, email, gender, occupation, income))

            # Commit changes and close the connection
            conn.commit()

            messagebox.showinfo("Success", "Personal details saved successfully!")

        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "An error occurred while saving personal details.")

        finally:
            # Close the database connection
            conn.close()

        # Navigate back to the home page
        if hasattr(self, 'home_callback') and callable(self.home_callback):
            self.home_callback()

    def go_back(self):
        # Destroy the DetailsFrame
        self.destroy()

        # Navigate back to the home page
        if hasattr(self, 'home_callback') and callable(self.home_callback):
            self.home_callback()
def income():
    income_frame = tk.Frame(main_frame)

    # Add your income-related widgets here
    date_label = ttk.Label(income_frame, text="Date:")
    date_label.grid(row=0, column=0, pady=2)

    date_picker = DateEntry(income_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=0, column=1, pady=5)

    income_type_label = ttk.Label(income_frame, text="Income Type:")
    income_type_label.grid(row=1, column=0, pady=5)

    income_type_entry = ttk.Entry(income_frame)
    income_type_entry.grid(row=1, column=1, pady=5)

    source_label = ttk.Label(income_frame, text="Source of Income:")
    source_label.grid(row=2, column=0, pady=5)

    source_entry = ttk.Entry(income_frame)
    source_entry.grid(row=2, column=1, pady=5)

    amount_label = ttk.Label(income_frame, text="Amount:")
    amount_label.grid(row=3, column=0, pady=5)

    amount_entry = ttk.Entry(income_frame)
    amount_entry.grid(row=3, column=1, pady=5)

    description_label = ttk.Label(income_frame, text="Income Description:")
    description_label.grid(row=4, column=0, pady=5)

    income_description_text = tk.Text(income_frame, height=5, width=25)
    income_description_text.grid(row=4, column=1, pady=5)

    submit_button = ttk.Button(income_frame, text="Submit Income", command=lambda:submit_income(
        date_picker.get(),
        income_type_entry.get(),
        source_entry.get(),
        amount_entry.get(),
        income_description_text.get("1.0", tk.END).strip(),
    ))

    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Create a View Income button
    view_income_button = ttk.Button(income_frame, text="View Income", command=lambda: open_view())
    view_income_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Add a button to go back to the home page
    back_button = tk.Button(income_frame, text="Back", command=lambda: self.show_frame(self.initial_home_frame))
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    income_frame.pack(pady=20)
class IncomeViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Income Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        self.load_income_data()

        self.saveButton = QPushButton("Save Changes")
        self.layout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.save_changes)

    def load_income_data(self):
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM income")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Set number of rows and columns in the table
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0]))  # Assuming all rows have the same number of columns

        # Set table headers
        headers = [description[0] for description in cursor.description]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Populate the table with data
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

        # Close the database connection
        conn.close()

    def save_changes(self):
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"
        )

        cursor = conn.cursor()

        # Iterate over all table cells
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                changed_value = item.text()
                column_name = self.tableWidget.horizontalHeaderItem(column).text()
                row_id = self.tableWidget.item(row, 0).text()  # Assuming the first column is the ID

                # Update the value in the database
                cursor.execute(f"UPDATE income SET {column_name} = %s WHERE ID = %s", (changed_value, row_id))

        conn.commit()

        # Close the database connection
        conn.close()

def open_view():
    app = QApplication(sys.argv)
    income_viewer = IncomeViewer()  # Create an instance of the IncomeViewer class
    income_viewer.show()  # Show the IncomeViewer window
    sys.exit(app.exec_())  # Execute the application

def open_expense_view():
    subprocess.Popen(["python", "expense.py"])
def submit_income(date_value, income_type_value, source_of_income_value, amount_value,
                  income_description_value):
    try:
        # Check if the date format is valid
        try:
            formatted_date = datetime.strptime(date_value, "%m/%d/%y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please enter the date in MM/DD/YY format.")

        # Connect to the MySQL database (replace with your actual database connection)
        conn = mysql.connector.connect(
            host="localhost",  # Update with your MySQL host
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"  # Update with your database name
        )

        cursor = conn.cursor()

        # Check for mandatory fields
        if not (
                date_value and income_type_value and source_of_income_value and amount_value and income_description_value):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Convert amount_value to Decimal
        amount_value = "{:.2f}".format(float(amount_value))

        # Create 'income' table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS income (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            income_type VARCHAR(255) NOT NULL,
            source_of_income VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            income_description TEXT NOT NULL
        )
        """
        cursor.execute(create_table_query)

        # Insert data into 'income' table
        insert_query = "INSERT INTO income (date, income_type, source_of_income, amount, income_description) VALUES (%s, %s, %s, %s, %s)"
        values = (formatted_date, income_type_value, source_of_income_value, amount_value, income_description_value)

        cursor.execute(insert_query, values)
        conn.commit()

        # Show success message
        messagebox.showinfo("Success", "Income submitted successfully!")

        # Close the window after successful submission
        self.destroy()

    except ValueError as ve:
        # Handle date format errors
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        # Handle other exceptions
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        if 'conn' in locals():
            conn.close()

def expense():
    expense_frame = tk.Frame(main_frame)

    # Add your income-related widgets here
    date_label = ttk.Label(expense_frame, text="Date:")
    date_label.grid(row=0, column=0, pady=2)

    date_picker = DateEntry(expense_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_picker.grid(row=0, column=1, pady=5)

    expense_category_label = ttk.Label(expense_frame, text="Expense Category:")
    expense_category_label.grid(row=1, column=0, pady=5)

    # Define your categories
    categories = ["Groceries", "Utilities", "Entertainment", "Airtime", "Fees", "Rent", "Transportation", "Other"]

    # Create a Combobox to display the categories
    expense_category_combobox = ttk.Combobox(expense_frame, values=categories)
    expense_category_combobox.grid(row=1, column=1, pady=5)
    expense_category_combobox.set(categories[0])  # Set default value

    payment_methods = ["Mpesa", "Cash", "Credit card", "Paypal"]

    # Create and place the label for payment method
    payment_method_label = ttk.Label(expense_frame, text="Payment Method:")
    payment_method_label.grid(row=2, column=0, pady=5)

    # Create and place the combo box for payment method
    payment_method_combobox = ttk.Combobox(expense_frame, values=payment_methods)
    payment_method_combobox.grid(row=2, column=1, pady=5)
    payment_method_combobox.set(payment_methods[0])  # Set default value

    amount_label = ttk.Label(expense_frame, text="Amount:")
    amount_label.grid(row=3, column=0, pady=5)

    amount_entry = ttk.Entry(expense_frame)
    amount_entry.grid(row=3, column=1, pady=5)

    description_label = ttk.Label(expense_frame, text="Income Description:")
    description_label.grid(row=4, column=0, pady=5)

    expense_description_text = tk.Text(expense_frame, height=5, width=25)
    expense_description_text.grid(row=4, column=1, pady=5)

    submit_button = ttk.Button(expense_frame, text="Submit Income", command=lambda:submit_expense(
        date_picker.get(),
        expense_category_combobox.get(),
        payment_method_combobox.get(),
        amount_entry.get(),
        expense_description_text.get("1.0", tk.END).strip(),
    ))

    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Create a View Income button
    view_expense_button = ttk.Button(expense_frame, text="View Expense", command=lambda: open_expense_view())
    view_expense_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Add a button to go back to the home page
    back_button = tk.Button(expense_frame, text="Back", command=lambda:show_frame(initial_home_frame))
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    expense_frame.pack(pady=20)

def submit_expense(date_value, expense_category, payment_method, amount_value, expense_description_value):
    try:
        # Convert date_value to the correct format (MM/DD/YY)
        formatted_date = datetime.strptime(date_value, "%m/%d/%y").strftime("%Y-%m-%d")

        # Convert amount_value to Decimal
        amount_value = "{:.2f}".format(float(amount_value))

        # Connect to the MySQL database (replace with your actual database connection)
        conn = mysql.connector.connect(
            host="localhost",  # Update with your MySQL host
            user="root",
            password="",  # Update with your MySQL password
            database="personal_finance"  # Update with your database name
        )

        cursor = conn.cursor()

        # Create 'income' table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            category VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            payment_method VARCHAR(100),
            expense_description TEXT
        )
        """
        cursor.execute(create_table_query)

        # Insert data into 'income' table
        insert_query = "INSERT INTO expenses (date, category, amount, payment_method, expense_description) VALUES (%s, %s, %s, %s, %s)"
        values = (formatted_date, expense_category, amount_value, payment_method, expense_description_value)

        cursor.execute(insert_query, values)
        conn.commit()

        # Show success message
        messagebox.showinfo("Success", "Expense submitted successfully!")

        # Close the window after successful submission
        self.destroy()

    except ValueError:
        # Handle parsing errors
        messagebox.showerror("Error", "Invalid date format. Please enter the date in MM/DD/YY format.")
    except Exception as e:
        # Handle other exceptions
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        if 'conn' in locals():
            conn.close()


def details(home_frame):
    global current_home_frame  # Declare current_home_frame as a global variable
    current_home_frame = home_frame  # Store the home frame in the global variable
    home_frame.pack_forget()  # Hide the home frame

    # Create and pack the DetailsFrame on the main frame
    details_frame = DetailsFrame(main_frame, home_callback=lambda: show_frame(home_frame))
    details_frame.pack()
def show_frame(frame):
    frame.pack()


def create_budget_table():
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your actual password
            database="personal_finance"
        )

        cursor = db_connection.cursor()

        # Create the budget table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            budget_limit DECIMAL(10, 2) NOT NULL,
            budget_month CHAR NOT NULL,
            budget_year INT NOT NULL,
            CONSTRAINT uc_category_month_year UNIQUE (category(100), budget_month, budget_year)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')

        # Commit changes to the database
        db_connection.commit()

    except mysql.connector.Error as err:
        print("Error:", err)
        messagebox.showerror("Error", "An error occurred while creating the budget table.")

    finally:
        # Close the database connection
        if 'db_connection' in locals():
            db_connection.close()

def budget(parent):
    # Create a frame without border
    budget_frame = tk.Frame(parent, relief=tk.FLAT, borderwidth=0)
    budget_frame.pack()

    ttk.Label(budget_frame, text="Set Budget Limits").grid(row=0, column=0, columnspan=2, pady=5)

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years = list(range(2020, datetime.now().year + 1))

    budget_month = tk.StringVar(value=months[0])  # Set default month to January
    budget_year = tk.IntVar(value=datetime.now().year)  # Set default year to current year

    ttk.Label(budget_frame, text="Select Month:").grid(row=1, column=0, pady=5, sticky=tk.W)
    month_combo = ttk.Combobox(budget_frame, textvariable=budget_month, values=months, state="readonly")
    month_combo.grid(row=1, column=1, padx=10, pady=3, sticky=tk.W)

    ttk.Label(budget_frame, text="Select Year:").grid(row=2, column=0, pady=5, sticky=tk.W)
    year_combo = ttk.Combobox(budget_frame, textvariable=budget_year, values=years, state="readonly")
    year_combo.grid(row=2, column=1, padx=10, pady=3, sticky=tk.W)

    categories = ["Groceries", "Utilities", "Entertainment", "Airtime", "Fees", "Rent", "Transportation", "Other"]

    budget_limits = {category: tk.DoubleVar() for category in categories}

    for index, category in enumerate(categories):
        ttk.Label(budget_frame, text=f"{category}:").grid(row=index + 3, column=0, padx=10, pady=3, sticky=tk.W)
        budget_entry = ttk.Entry(budget_frame, textvariable=budget_limits[category])
        budget_entry.grid(row=index + 3, column=1, padx=10, pady=3, sticky=tk.W)

    # Date Entry
    ttk.Label(budget_frame, text="Select Budget Date:").grid(row=len(categories) + 3, column=0, pady=5, sticky=tk.W)
    date_entry = DateEntry(budget_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=len(categories) + 3, column=1, padx=10, pady=3, sticky=tk.W)

    # Summary display
    ttk.Label(budget_frame, text="Budget Summary:").grid(row=len(categories) + 4, column=0, columnspan=2, pady=5)
    summary_text = tk.Text(budget_frame, height=6, width=40)  # Increased width to fit larger frame
    summary_text.grid(row=len(categories) + 3, column=0, columnspan=2, pady=3)

    # Submit button
    submit_button = ttk.Button(budget_frame, text="Set Budget", command=lambda: set_budget(parent, budget_limits, month_combo, year_combo, date_entry, summary_text))
    submit_button.grid(row=len(categories) + 5, column=2, columnspan=2, pady=5)

    view_button = ttk.Button(budget_frame,text='View Budget', command= lambda : open_budget_viewer())
    view_button.grid(row=len(categories) + 5, column=0, columnspan=2, pady=5)

def set_budget(parent, budget_limits, month_combo, year_combo, date_entry, summary_text):
    try:
        # Clear previous content
        summary_text.delete(1.0, tk.END)
        summary_text.insert(tk.END, "Budget Summary:\n")

        # Process budget limits and display summary
        budget_month = month_combo.get()
        budget_year = year_combo.get()
        budget_date_str = date_entry.get()
        budget_date = datetime.strptime(budget_date_str, "%m/%d/%y").strftime("%Y-%m-%d")
        summary_text.insert(tk.END, f"Month: {budget_month}\n")
        summary_text.insert(tk.END, f"Year: {budget_year}\n")
        summary_text.insert(tk.END, f"Date: {budget_date}\n\n")

        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your actual password
            database="personal_finance"
        )

        cursor = db_connection.cursor()

        # Check if entry already exists for the month and year
        cursor.execute("SELECT id FROM budget WHERE budget_month = %s AND budget_year = %s", (budget_month, budget_year))
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Entry already exists for the month and year
            messagebox.showerror("Error", f"Budget for {budget_month} {budget_year} has already been set.")
            return

        # Insert budget data into the table
        for category, limit in budget_limits.items():
            # Skip categories with zero budget limits
            if limit.get() == 0.00:
                continue

            # Insert new entry
            insert_query = "INSERT INTO budget (category, budget_limit, budget_month, budget_year) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (category, limit.get(), budget_month, budget_year))

        # Commit changes to the database
        db_connection.commit()

        # Show success message
        messagebox.showinfo("Success", f"Budget for {budget_month} {budget_year} submitted successfully!")

    except mysql.connector.Error as err:
        print("Error:", err)
        messagebox.showerror("Error", "An error occurred while submitting the budget.")

    finally:
        # Close the database connection
        if 'db_connection' in locals():
            db_connection.close()

# Call function to create budget table
create_budget_table()


class BudgetViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Viewer")
        self.setGeometry(100, 100, 500, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Budget Table
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        # Load Budget Button
        self.load_button = QPushButton("Load Budget")
        self.load_button.clicked.connect(self.load_budget)
        self.layout.addWidget(self.load_button)

        # Exit Button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close_viewer)
        self.layout.addWidget(self.exit_button)

    def close_viewer(self):
        self.close()

    def load_budget(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Update with your MySQL password
                database="personal_finance"
            )

            cursor = conn.cursor()
            query = "SELECT category, budget_limit, budget_month, budget_year FROM budget"
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                print("No budget data found.")
                return

            self.tableWidget.setColumnCount(4)
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setHorizontalHeaderLabels(["Category", "Budget Limit", "Month", "Year"])

            for i, row in enumerate(rows):
                for j, item in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

        except mysql.connector.Error as err:
            print("Error:", err)

def open_budget_viewer():
    app = QApplication(sys.argv)
    budget_viewer = BudgetViewer()
    budget_viewer.show()
    sys.exit(app.exec_())




def home():
    home_frame = tk.Frame(main_frame)

    # Add widgets for the landing page
    welcome_label = tk.Label(home_frame, text="Welcome to Personal Finance Management Tool!", font=("Helvetica", 10))
    welcome_label.pack(pady=20)

    # Add image to the home page (make sure "img.png" is in the correct path)
    img = tk.PhotoImage(file="img.png")
    img_label = tk.Label(home_frame, image=img)
    img_label.image = img  # Keep a reference to the image to avoid garbage collection
    img_label.pack(pady=10)

    # Display a random quotation
    selected_quotation = random.choice(["\"Money is a terrible master but an excellent servant.\"",
                                        "\"Savings represent much more than just money.\""])
    quotation_label = tk.Label(home_frame, text=selected_quotation)
    quotation_label.pack(pady=5)

    detail_btn = tk.Button(home_frame, text="Details", bg='white', command=lambda: details(home_frame))
    detail_btn.pack()

    advisor_btn = tk.Button(home_frame,text="Adivisor", bg='gray',command= lambda: open_advisor())
    advisor_btn.pack(pady = 5)

    home_frame.pack(pady=20)

    return home_frame  # Return the created frame
def open_advisor():
    # Open the advisor.py file using subprocess
    try:
        subprocess.Popen(["python", "advisor.py"])
    except FileNotFoundError:
        messagebox.showerror("Error", "advisor.py file not found.")
def hide_indicator():
    home_indicate.config(bg='#c3c3c3')
    budget_indicate.config(bg='#c3c3c3')
    income_indicate.config(bg='#c3c3c3')
    expense_indicate.config(bg='#c3c3c3')

def indicate(lb, page_func):
    hide_indicator()
    lb.config(bg='#158aff')

    # Check if the function is not None before calling
    if page_func:
        # Destroy the current frame in the main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Call the respective function to set up the pressed page
        page_func()
def setup_home_page():
    global initial_home_frame
    initial_home_frame = home()
    initial_home_frame.pack()

root = tk.Tk()
root.geometry('600x600')
root.title("M&R finance App")

options_frame = tk.Frame(root, bg='#c3c3c3')

home_btn = tk.Button(options_frame, text="Home", font=('bold', 15), fg='#158aff', bd=0, bg='#c3c3c3',
                     command=lambda: indicate(home_indicate, home))
home_btn.place(x=10, y=50)

home_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
home_indicate.place(x=3, y=50, width=5, height=40)

budget_btn = tk.Button(options_frame, text="Budget", font=('bold', 15), fg='#158aff', bd=0, bg='#c3c3c3',
                       command=lambda: indicate(budget_indicate, lambda: budget(main_frame)))

budget_btn.place(x=10, y=100)

budget_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
budget_indicate.place(x=3, y=100, width=5, height=40)

# Define the income button before using it in the command parameter
income_btn = tk.Button(options_frame, text="Income", font=('bold', 15), fg='#158aff', bd=0, bg='#c3c3c3',
                       command=lambda: indicate(income_indicate, income))
income_btn.place(x=10, y=150)

income_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
income_indicate.place(x=3, y=150, width=5, height=40)

expense_btn = tk.Button(options_frame, text="Expenses", font=('bold', 15), fg='#158aff', bd=0, bg='#c3c3c3',
                        command=lambda: indicate(expense_indicate, expense))
expense_btn.place(x=10, y=200)

expense_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
expense_indicate.place(x=3, y=200, width=5, height=40)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=100, height=600)

main_frame = tk.Frame(root)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=600, width=600)

# Initial call to home() to set up the home frame
initial_home_frame = home()
initial_home_frame.pack_forget()  # Initially hide the home frame
setup_home_page()
root.mainloop()
