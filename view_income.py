import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
import mysql.connector


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = IncomeViewer()
    viewer.show()
    sys.exit(app.exec_())
