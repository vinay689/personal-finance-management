from database import Database
from auth import Auth
from transactions import Transaction

db = Database()

transaction = Transaction()

print("Database Created Successfully!")

# Authentication Check
auth = Auth()

while True:

    print("1.Register")
    print("2.Login")
    print("3.Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        auth.register()

    elif choice == "2":

        user_id = auth.login()
    else:
        break    

    if user_id:

        while True:

            print("1.Add Income")
            print("2.Add Expenses")
            print("3.View Transactions")
            print("4.Update Transaction")
            print("5.Delete Transaction")
            print("6.Monthly Report")
            print("7.Logout")

            user_choice = input("Enter choice: ")

            if user_choice == "1":
                transaction.add_income(user_id)

            elif user_choice == "2":
                transaction.add_expense(user_id)

            elif user_choice == "3":
                transaction.view_transactions(user_id)

            elif user_choice == "4":
                transaction.update_transaction(user_id)  

            elif user_choice == "5":
                transaction.delete_transaction(user_id)      

            elif user_choice == "6":
                transaction.monthly_report(user_id)    

            elif user_choice == "7":
                break    

    elif choice == "8":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")