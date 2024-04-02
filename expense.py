import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QComboBox, QFileDialog
import mysql.connector
from datetime import datetime
import pandas as pd
import os

def fetch_expenses_data(month, year):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Update with your MySQL password
        database="personal_finance"
    )

    cursor = conn.cursor()
    query = "SELECT date, category, amount FROM expenses WHERE MONTH(date) = %s AND YEAR(date) = %s"
    cursor.execute(query, (month, year))
    rows = cursor.fetchall()
    conn.close()

    return rows

def display_expenses(month_combo, year_combo, tableWidget):
    tableWidget.clear()
    selected_month = month_combo.currentIndex() + 1
    selected_year = int(year_combo.currentText())

    expenses_data = fetch_expenses_data(selected_month, selected_year)
    if not expenses_data:
        print(f"No expenses recorded for {selected_month}-{selected_year}")
        return

    tableWidget.setColumnCount(3)
    tableWidget.setRowCount(len(expenses_data))
    tableWidget.setHorizontalHeaderLabels(["Date", "Category", "Amount"])

    for i, row in enumerate(expenses_data):
        for j, item in enumerate(row):
            tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

    tableWidget.resizeColumnsToContents()

def export_expenses(month_combo, year_combo):
    selected_month = month_combo.currentIndex() + 1
    selected_year = int(year_combo.currentText())
    month_name = month_combo.currentText()

    expenses_data = fetch_expenses_data(selected_month, selected_year)

    df = pd.DataFrame(expenses_data, columns=["Date", "Category", "Amount"])
    try:
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Expenses to Excel", f"{month_name}_expenses.xlsx", "Excel Files (*.xlsx *.xls)", options=options)

        if file_path:
            df.to_excel(file_path, index=False)
            print(f"Expenses exported to '{file_path}' successfully.")
    except Exception as e:
        print("Error exporting expenses to Excel:", e)

def create_main_window():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Expense Viewer")
    main_window.setGeometry(100, 100, 800, 600)

    centralWidget = QWidget()
    main_window.setCentralWidget(centralWidget)

    layout = QVBoxLayout()
    centralWidget.setLayout(layout)

    # Month Selection Widget
    month_label = QLabel("Select Month:")
    month_combo = QComboBox()
    month_combo.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    year_label = QLabel("Select Year:")
    year_combo = QComboBox()
    year_combo.addItems([str(year) for year in range(2010, 2051)])

    load_button = QPushButton("Load Expenses")
    load_button.clicked.connect(lambda: display_expenses(month_combo, year_combo, tableWidget))

    export_button = QPushButton("Export Expenses to Excel")
    export_button.clicked.connect(lambda: export_expenses(month_combo, year_combo))

    month_layout = QHBoxLayout()
    month_layout.addWidget(month_label)
    month_layout.addWidget(month_combo)
    month_layout.addWidget(year_label)
    month_layout.addWidget(year_combo)
    month_layout.addWidget(load_button)
    month_layout.addWidget(export_button)

    layout.addLayout(month_layout)

    # Expenses Table
    tableWidget = QTableWidget()
    layout.addWidget(tableWidget)

    # Exit Button
    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(main_window.close)
    layout.addWidget(exit_button)

    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    create_main_window()
