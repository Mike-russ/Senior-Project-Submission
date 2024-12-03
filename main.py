import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QSpacerItem, QSizePolicy, QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QLineEdit, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import database
import interest

class GraphWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.ax = ax
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def plot_balance(self, db):
        # Fetch monthly balance data from the database
        balance_data = database.get_monthly_balance(db)
        if balance_data:  # Check if data exists
            months = [row[0] for row in balance_data]
            balances = [row[1] for row in balance_data]

            # Clear the axes and plot the balance data
            self.ax.clear()
            self.ax.bar(months, balances, label='Balance', color='blue')
            self.ax.set_title('Monthly Balance')
            self.ax.set_xlabel('Month')
            self.ax.set_ylabel('Balance')
            self.ax.legend()

            # Adjust x-axis labels for better readability (if needed)
            self.ax.tick_params(axis='x', rotation=0)

            self.draw()

    def plot_expenses(self, db):
        # Fetch monthly expenses data from the database
        expense_data = database.get_monthly_spending(db, "2024-09")
        if expense_data:  # Check if data exists
            categories = [row[0] for row in expense_data]
            expenses = [row[1] for row in expense_data]

            # Clear the axes and plot the expenses data
            self.ax.clear()
            self.ax.bar(categories, expenses, label='Expenses', color='red')
            self.ax.set_title('Monthly Expenses')
            self.ax.set_xlabel('Category')
            self.ax.set_ylabel('Amount')
            self.ax.legend()

            # Adjust x-axis labels for better readability (if needed)
            self.ax.tick_params(axis='x', rotation=0)

            self.draw()

    def plot_income(self, db):
        # Fetch monthly income data from the database
        income_data = database.get_monthly_income(db)
        if income_data:  # Check if data exists
            months = [row[0] for row in income_data]
            incomes = [row[1] for row in income_data]

            # Clear the axes and plot the income data
            self.ax.clear()
            self.ax.plot(months, incomes, label='Income', color='green', marker='o')
            self.ax.set_title('Monthly Income')
            self.ax.set_xlabel('Month')
            self.ax.set_ylabel('Income')
            self.ax.legend()

            # Adjust x-axis labels for better readability (if needed)
            self.ax.tick_params(axis='x', rotation=0)

            self.draw()

class AddIncomeDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add Income")

        layout = QVBoxLayout()
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Enter Date (YYYY-MM)")
        layout.addWidget(self.date_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter Income Amount")
        layout.addWidget(self.amount_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_income)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def add_income(self):
        date = self.date_input.text()
        amount = self.amount_input.text()
        if date and amount:
            database.add_income(self.db, date, amount)
            self.accept()

class AddExpenseDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add Expense")

        layout = QVBoxLayout()

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Enter Date (YYYY-MM)")
        layout.addWidget(self.date_input)

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Enter Expense Type")
        layout.addWidget(self.type_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter Expense Amount")
        layout.addWidget(self.amount_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_expense)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def add_expense(self):
        date = self.date_input.text()
        spend_type = self.type_input.text()
        amount = self.amount_input.text()
        if date and spend_type and amount:
            database.add_spend(self.db, date, spend_type, amount)
            self.accept()

class DebtCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Debt Calculator")
        self.setMinimumSize(400, 300)
        self.setModal(True)

        layout = QVBoxLayout()

        # Loan Amount Input
        self.loan_amount_input = QLineEdit()
        self.loan_amount_input.setPlaceholderText("Enter loan amount ($)")
        layout.addWidget(self.loan_amount_input)

        # Interest Rate Input
        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Enter interest rate (%)")
        layout.addWidget(self.interest_rate_input)

        # Monthly Payment Input
        self.monthly_payment_input = QLineEdit()
        self.monthly_payment_input.setPlaceholderText("Enter monthly payment ($)")
        layout.addWidget(self.monthly_payment_input)

        # Results Label
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)

        # Calculate Button
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_interest)
        layout.addWidget(calculate_button)

        # Close Button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class DebtCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Debt Calculator")
        self.setMinimumSize(400, 300)  # Set a minimum size for the dialog
        self.setModal(True)

        layout = QVBoxLayout()

        # Loan Amount Input
        self.loan_amount_input = QLineEdit()
        self.loan_amount_input.setPlaceholderText("Enter loan amount ($)")
        layout.addWidget(self.loan_amount_input)

        # Interest Rate Input
        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Enter interest rate (%)")
        layout.addWidget(self.interest_rate_input)

        # Monthly Payment Input
        self.monthly_payment_input = QLineEdit()
        self.monthly_payment_input.setPlaceholderText("Enter monthly payment ($)")
        layout.addWidget(self.monthly_payment_input)

        # Scrollable Area for Results
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Results Label
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        scroll_layout.addWidget(self.results_label)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Calculate Button
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_interest)
        layout.addWidget(calculate_button)

        # Close Button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def calculate_interest(self):
        """Perform the interest calculation and display results."""
        try:
            loan_amount = float(self.loan_amount_input.text())
            interest_rate = float(self.interest_rate_input.text()) / 100  # Convert to decimal
            monthly_payment = float(self.monthly_payment_input.text())

            if loan_amount <= 0 or interest_rate < 0 or monthly_payment <= 0:
                raise ValueError("All values must be positive.")

            # Call the interest calculation function
            months, total_paid, balances, interests = interest.Calculate_compound_interest(
                loan_amount, interest_rate, monthly_payment
            )

            # Display results
            self.results_label.setText(
                f"Loan Amount: ${loan_amount:.2f}\n"
                f"Interest Rate: {interest_rate * 100:.2f}%\n"
                f"Monthly Payment: ${monthly_payment:.2f}\n"
                f"Time to Pay Off: {months} months\n"
                f"Total Paid: ${total_paid:.2f}\n"
                f"Total Interest Paid: ${total_paid - loan_amount:.2f}\n"
                f"Time to Save for Purchase: {loan_amount / monthly_payment:.2f} months"
            )
        except ValueError as e:
            self.results_label.setText(f"Error: {e}")


class GraphSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Graph")
        self.setModal(True)

        layout = QVBoxLayout()

        # Create radio buttons for each graph
        self.balance_radio = QRadioButton("Monthly Balance")
        self.expenses_radio = QRadioButton("Monthly Expenses")
        self.income_radio = QRadioButton("Monthly Income")

        # Set the default option (Monthly Balance)
        self.balance_radio.setChecked(True)

        layout.addWidget(self.balance_radio)
        layout.addWidget(self.expenses_radio)
        layout.addWidget(self.income_radio)

        # Create a button box (OK, Cancel)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_selected_graph(self):
        if self.balance_radio.isChecked():
            return 'balance'
        elif self.expenses_radio.isChecked():
            return 'expenses'
        elif self.income_radio.isChecked():
            return 'income'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Planner")
        self.setMinimumSize(1200, 600)

        # Initialize database
        self.db = database.Database()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        # Add Running Balance Label
        self.running_balance_label = QLabel("Total Balance: $0.00")
        self.running_balance_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        layout.addWidget(self.running_balance_label, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add Income Button
        add_income_button = QPushButton("Add Income")
        add_income_button.setFixedHeight(50)
        add_income_button.clicked.connect(self.open_add_income_dialog)  # Connect to income dialog
        layout.addWidget(add_income_button, 2, 1)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 2, 1)

        # Add Expense Button
        add_expenses_button = QPushButton("Add Expenses")
        add_expenses_button.setFixedHeight(50)
        add_expenses_button.clicked.connect(self.open_add_expense_dialog)  # Connect to expense dialog
        layout.addWidget(add_expenses_button, 4, 1)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 4, 1)

        # Add Debt Calculator Button
        debt_calculator_button = QPushButton("Debt Calculator")
        debt_calculator_button.setFixedHeight(50)
        debt_calculator_button.clicked.connect(self.open_debt_calculator_dialog)
        layout.addWidget(debt_calculator_button, 6, 1)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 6, 1)

        # Create the graph widget first
        self.graph_widget = GraphWidget(self, width=5, height=4)

        # Create a container for the graph widget
        graph_container = QWidget(self)
        graph_container.setStyleSheet("""
            border: 3px solid black;
            border-radius: 10px;
            background-color: #f9f9f9;
            padding: 10px;
        """)

        # Set layout for the container and add the graph widget to it
        container_layout = QVBoxLayout(graph_container)
        container_layout.addWidget(self.graph_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)  # No extra margin inside the container
        container_layout.setSpacing(0)

        # Add the container to the main layout
        layout.addWidget(graph_container, 1, 3, 6, 2)

        # Default graph (Monthly Balance)
        self.graph_widget.plot_balance(self.db)

        # Add the "Switch Graphs" button
        graphs_button = QPushButton("Switch Graphs")
        graphs_button.clicked.connect(self.open_graph_selection_dialog)
        layout.addWidget(graphs_button, 7, 4)

        # Set the layout on the central widget
        central_widget.setLayout(layout)

        # Update the running balance on startup
        self.update_running_balance()

    def update_running_balance(self):
        """Fetch the current running balance and update the label."""
        running_balance = main.get_running_balance(self.db)
        self.running_balance_label.setText(f"Running Balance: ${running_balance:.2f}")

    def open_add_income_dialog(self):
        dialog = AddIncomeDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.graph_widget.plot_balance(self.db)  # Refresh graph
            self.update_running_balance()  # Refresh balance label

    def open_add_expense_dialog(self):
        dialog = AddExpenseDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.graph_widget.plot_balance(self.db)  # Refresh graph
            self.update_running_balance()  # Refresh balance label

    def open_debt_calculator_dialog(self):
        """Open the Debt Calculator Dialog."""
        dialog = DebtCalculatorDialog(self)
        dialog.exec_()

    def open_graph_selection_dialog(self):
        dialog = GraphSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_graph = dialog.get_selected_graph()
            self.switch_graph(selected_graph)

    def switch_graph(self, graph_type):
        # Switch between the graphs based on the selected type
        if graph_type == 'balance':
            self.graph_widget.plot_balance(self.db)
        elif graph_type == 'expenses':
            self.graph_widget.plot_expenses(self.db)
        elif graph_type == 'income':
            self.graph_widget.plot_income(self.db)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
