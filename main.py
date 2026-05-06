from database import Database
from auth import Auth
db = Database()

print("Database Created Successfully!")

# Authentication Check
auth = Auth()

while True:

    print("1.Register")
    print("2. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        auth.register()

    elif choice == "2":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")