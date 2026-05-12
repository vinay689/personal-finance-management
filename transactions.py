from database import Database
from datetime import datetime


class Transaction:

    def __init__(self):
        self.db = Database()

    def add_income(self, user_id):

        categories = {
            "1": "Salary",
            "2": "Freelancing",
            "3": "Bonus",
            "4": "Business"
        }

        print("\nSelect Income Category:")
        print("1. Salary")
        print("2. Freelancing")
        print("3. Bonus")
        print("4. Business")

        choice = input("Enter choice: ")

        if choice not in categories:
            print("Invalid category!")
            return

        category = categories[choice]

        amount = float(input("Enter amount: "))

        date = datetime.now().strftime("%Y-%m-%d")

        self.db.cursor.execute(
            """
            INSERT INTO transactions(user_id, type, category, amount, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, "income", category, amount, date)
        )

        self.db.conn.commit()

        print("Income Added Successfully!")


    def add_expense(self, user_id):

        categories = {
            "1": "Food",
            "2": "Rent",
            "3": "Shopping",
            "4": "Travel"
        }

        print("Select Expense Category:")
        print("1. Food")
        print("2. Rent")
        print("3. Shopping")
        print("4. Travel")

        choice = input("Enter choice: ")

        if choice not in categories:
            print("Invalid category!")
            return

        category = categories[choice]

        amount = float(input("Enter amount: "))

        date = datetime.now().strftime("%Y-%m-%d")

        self.db.cursor.execute(
            """
            INSERT INTO transactions(user_id, type, category, amount, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, "expense", category, amount, date)
        )

        self.db.conn.commit()

        print("Expense Added Successfully!")        


    def view_transactions(self, user_id):

        self.db.cursor.execute(
        """
        SELECT type, category, amount, date
        FROM transactions
        WHERE user_id = ?
        """,
        (user_id,)
    )

        records = self.db.cursor.fetchall() # pyr

        if records:

            print("\n===== Transaction History =====")

            for row in records:
                print(f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}")

        else:
            print("No transactions found!")    