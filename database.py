import sqlite3

# sqllite 3 Connect / Created
import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        # Users table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        # Transactions tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            category TEXT,
            amount REAL,
            date TEXT
        )
        """)

        # Budget table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT,
            amount REAL
        )
        """)

        self.conn.commit()
                            
                            
                            
                            
