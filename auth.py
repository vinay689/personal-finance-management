
 
from database import Database


class Auth:

    def __init__(self):
        self.db = Database()

    def register(self):

        username = input("Enter Username: ")
        password = input("Enter Password: ")

        try:
            self.db.cursor.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (username, password)
            )

            self.db.conn.commit()

            print("Registration Successful!")

        except:
            print("Username already exists!")


    def login(self):

        username = input("Enter Username: ")
        password = input("Enter Password: ")
    
        self.db.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
    
        user = self.db.cursor.fetchone()
    
        if user:
            print("Login Successful!")
            return user[0]

        else:
            print("Invalid Username or Password!")
            return None