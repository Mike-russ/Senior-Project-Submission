import sqlite3
from datetime import date
import re

class Database:
    def __init__(self, db_name='TransactionDatabase.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def create_table(self, table_creation_sql):
        self.cursor.execute(table_creation_sql)
        self.commit()

    def insert_data(self, query, data):
        self.cursor.executemany(query, data)
        self.commit()

    def get_data(self, query, params=()):
        self.execute(query, params)
        return self.fetchall()

    def update_data(self, query, params=()):
        self.execute(query, params)
        self.commit()

    def drop_table(self, table_name):
        self.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.commit()

    def get_total_income(self):
        """Fetch the total income from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM INCOME")
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0

    def get_total_expenses(self):
        """Fetch the total expenses from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM SPEND")
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0


# Database Table Definitions
def create_spend_table(db):
    spend_table = """
    CREATE TABLE IF NOT EXISTS SPEND (
        Date TEXT NOT NULL,
        Type TEXT NOT NULL,
        Amount INTEGER NOT NULL
    );
    """
    db.create_table(spend_table)


def create_income_table(db):
    income_table = """
    CREATE TABLE IF NOT EXISTS INCOME (
        Date TEXT NOT NULL,
        Amount INTEGER NOT NULL
    );
    """
    db.create_table(income_table)


def create_monthly_balance_table(db):
    monthly_balance_table = """
    CREATE TABLE IF NOT EXISTS MONTHLY_BALANCE (
        Month TEXT PRIMARY KEY,
        Balance INTEGER NOT NULL
    );
    """
    db.create_table(monthly_balance_table)


# Data Handling Functions
def add_test_data(db):
    test_income = [
        ('2024-08', 1000),
        ('2024-09', 1000),
        ('2024-09', 1500),
        ('2024-10', 2000),
        ('2024-10', 2500),
    ]
    db.insert_data("INSERT INTO INCOME (Date, Amount) VALUES (?, ?)", test_income)

    test_spend = [
        ('2024-08', 'rent', 2200),
        ('2024-09', 'groceries', 200),
        ('2024-09', 'entertainment', 150),
        ('2024-09', 'utilities', 300),
        ('2024-10', 'groceries', 250),
        ('2024-10', 'rent', 1200),
    ]
    db.insert_data("INSERT INTO SPEND (Date, Type, Amount) VALUES (?, ?, ?)", test_spend)

    update_monthly_balance(db, '2024-08')
    update_monthly_balance(db, '2024-09')
    update_monthly_balance(db, '2024-10')


def get_monthly_balance(db):
    return db.get_data("SELECT * FROM MONTHLY_BALANCE")


def update_monthly_balance(db, month):
    total_income = db.get_data("SELECT IFNULL(SUM(Amount), 0) FROM INCOME WHERE Date = ?", (month,))[0][0]
    total_spending = db.get_data("SELECT IFNULL(SUM(Amount), 0) FROM SPEND WHERE Date = ?", (month,))[0][0]
    balance = total_income - total_spending
    db.update_data("INSERT INTO MONTHLY_BALANCE (Month, Balance) VALUES (?, ?) ON CONFLICT(Month) DO UPDATE SET Balance = ?", 
                   (month, balance, balance))


def get_monthly_spending(db, month):
    return db.get_data("SELECT Type, SUM(Amount) FROM SPEND WHERE Date = ? GROUP BY Type", (month,))


# Display Functions
def display_table(data, headers):
    if data:
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for row in data:
            print(" | ".join([str(item) for item in row]))
    else:
        print("No data found.")


def display_spend_table(db):
    data = db.get_data("SELECT * FROM SPEND")
    display_table(data, ["Date", "Type", "Amount"])


def display_income_table(db):
    data = db.get_data("SELECT * FROM INCOME")
    display_table(data, ["Date", "Amount"])


def display_monthly_balance(db):
    data = db.get_data("SELECT * FROM MONTHLY_BALANCE")
    display_table(data, ["Month", "Balance"])

def get_running_balance(db):
    """Calculate and return the running balance."""
    total_income = db.get_total_income()
    total_expenses = db.get_total_expenses()
    return total_income - total_expenses


def display_all_tables(db):
    display_income_table(db)
    display_spend_table(db)
    display_monthly_balance(db)


def add_spend(db, date, spend_type, amount):
    try:
        amount = int(amount)
        db.update_data("INSERT INTO SPEND (Date, Type, Amount) VALUES (?, ?, ?)", (date, spend_type, amount))
        update_monthly_balance(db, date)
    except ValueError:
        print("Invalid amount. Please provide a numeric value.")

def add_income(db, date, amount):
    try:
        amount = int(amount)
        db.update_data("INSERT INTO INCOME (Date, Amount) VALUES (?, ?)", (date, amount))
        update_monthly_balance(db, date)
    except ValueError:
        print("Invalid amount. Please provide a numeric value.")

def get_monthly_income(db):
    # Get total income for each month (assuming the "Date" column format is "YYYY-MM")
    return db.get_data("SELECT Date, SUM(Amount) FROM INCOME GROUP BY Date")

def get_and_plot_monthly_spending(db, month):
    spending_data = get_monthly_spending(db, month)
    if spending_data:
        spending_types = [row[0] for row in spending_data]
        spendings = [row[1] for row in spending_data]
        # visualization.plot_spending(spending_types, spendings)
    else:
        print(f"No spending data found for {month}.")


# Main Function to Run
def main():
    db = Database()

    # Create necessary tables
    create_spend_table(db)
    create_income_table(db)
    create_monthly_balance_table(db)

    # Add test data
    add_test_data(db)

    # User Interaction (Console-based)
    while True:
        choice = input("\nPlease choose one: Add Income, Add Spend, Display Tables, Plot Spending, Quit: ").lower()

        if choice == 'add income':
            add_income(db)
        elif choice == 'add spend':
            add_spend(db)
        elif choice == 'display tables':
            display_all_tables(db)
        elif choice == 'plot spending':
            month = input("Enter the month (YYYY-MM): ")
            if re.match(r'^\d{4}-\d{2}$', month):
                get_and_plot_monthly_spending(db, month)
            else:
                print("Invalid month format. Please enter in YYYY-MM format.")
        elif choice == 'quit':
            db.close()
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
