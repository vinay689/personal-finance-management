from database import Database
from datetime import datetime
import shutil


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


        # Budget Checking

        self.db.cursor.execute(
            """
            SELECT amount
            FROM budgets
            WHERE user_id = ? AND category = ?
            """,
            (user_id, category)
        )

        budget = self.db.cursor.fetchone()

        if budget:

            budget_amount = budget[0]

            self.db.cursor.execute(
                """
                SELECT SUM(amount)
                FROM transactions
                WHERE user_id = ?
                AND category = ?
                AND type = 'expense'
                """,
                (user_id, category)
            )

            total_expense = self.db.cursor.fetchone()[0] or 0

            if total_expense > budget_amount:
                print(f"Warning! You exceeded your {category} budget!")     


    def view_transactions(self, user_id):

        self.db.cursor.execute(
            """
            SELECT id, type, category, amount, date
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,)
        )

        records = self.db.cursor.fetchall()

        if records:

            print("\n===== Transaction History =====")

            for row in records:
                print(f"ID:{row[0]} | {row[1]} | {row[2]} | ₹{row[3]} | {row[4]}")

        else:
            print("No transactions found!")

    def update_transaction(self, user_id):

        self.view_transactions(user_id)

        transaction_id = input("Enter Transaction ID to update: ")

        new_amount = float(input("Enter New Amount: "))

        self.db.cursor.execute(
            """
            UPDATE transactions
            SET amount = ?
            WHERE id = ? AND user_id = ?
            """,
            (new_amount, transaction_id, user_id)
        )

        self.db.conn.commit()

        print("Transaction Updated Successfully!")

    def delete_transaction(self, user_id):

        self.view_transactions(user_id)

        transaction_id = input("Enter Transaction ID to delete: ")

        self.db.cursor.execute(
            """
            DELETE FROM transactions
            WHERE id = ? AND user_id = ?
            """,
            (transaction_id, user_id)
        )

        self.db.conn.commit()

        print("Transaction Deleted Successfully!")  

    def monthly_report(self, user_id):

    # Total Income
        self.db.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ? AND type = 'income'
            """,
            (user_id,)
        )

        income = self.db.cursor.fetchone()[0] or 0


        # Total Expense
        self.db.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ? AND type = 'expense'
            """,
            (user_id,)
        )

        expense = self.db.cursor.fetchone()[0] or 0


        savings = income - expense

        print("\n===== Monthly Report =====")
        print(f"Total Income: ₹{income}")
        print(f"Total Expense: ₹{expense}")
        print(f"Total Savings: ₹{savings}")     


    def category_report(self, user_id):

        self.db.cursor.execute(
            """
            SELECT category, SUM(amount)
            FROM transactions
            WHERE user_id = ?
            GROUP BY category
            """,
            (user_id,)
        )

        records = self.db.cursor.fetchall()

        if records:

            print("\n===== Category Report =====")

            for row in records:
                print(f"{row[0]} : ₹{row[1]}")

        else:
            print("No records found!")       

    def set_budget(self, user_id):

        categories = {
            "1": "Food",
            "2": "Rent",
            "3": "Shopping",
            "4": "Travel"
        }

        print("\nSelect Budget Category:")
        print("1. Food")
        print("2. Rent")
        print("3. Shopping")
        print("4. Travel")

        choice = input("Enter choice: ")

        if choice not in categories:
            print("Invalid category!")
            return

        category = categories[choice]

        amount = float(input("Enter Budget Amount: "))

        self.db.cursor.execute(
            """
            INSERT INTO budgets(user_id, category, amount)
            VALUES (?, ?, ?)
            """,
            (user_id, category, amount)
        )

        self.db.conn.commit()

        print("Budget Set Successfully!")          

    def view_budget_report(self, user_id):

        self.db.cursor.execute(
            """
            SELECT category, amount
            FROM budgets
            WHERE user_id = ?
            """,
            (user_id,)
        )

        budgets = self.db.cursor.fetchall()

        if budgets:

            print("\n===== Budget Report =====")

            for budget in budgets:

                category = budget[0]
                budget_amount = budget[1]

                self.db.cursor.execute(
                    """
                    SELECT SUM(amount)
                    FROM transactions
                    WHERE user_id = ?
                    AND category = ?
                    AND type = 'expense'
                    """,
                    (user_id, category)
                )

                spent = self.db.cursor.fetchone()[0] or 0

                remaining = budget_amount - spent

                print(f"\nCategory: {category}")
                print(f"Budget: ₹{budget_amount}")
                print(f"Spent: ₹{spent}")
                print(f"Remaining: ₹{remaining}")

        else:
            print("No budgets found!")    

    def yearly_report(self, user_id):

        year = input("Enter Year (YYYY): ")

        # Total Income

        self.db.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ?
            AND type = 'income'
            AND strftime('%Y', date) = ?
            """,
            (user_id, year)
        )

        income = self.db.cursor.fetchone()[0] or 0


        # Total Expense

        self.db.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ?
            AND type = 'expense'
            AND strftime('%Y', date) = ?
            """,
            (user_id, year)
        )

        expense = self.db.cursor.fetchone()[0] or 0


        savings = income - expense

        print("\n===== Yearly Financial Report =====")

        print(f"Year: {year}")
        print(f"Total Income: ₹{income}")
        print(f"Total Expense: ₹{expense}")
        print(f"Total Savings: ₹{savings}")        

    def backup_data(self):

        source = "finance.db"

        destination = "finance_backup.db"

        try:

            shutil.copy(source, destination)

            print("Backup Created Successfully!")

        except:
            print("Error creating backup!")    