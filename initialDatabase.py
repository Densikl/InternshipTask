import sqlite3


connection = sqlite3.connect('finance.db')

# Creating a cursor
cursor = connection.cursor()

# Creating a table for budget
cursor.execute("""CREATE TABLE finance (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                category TEXT,
                amount INTEGER,
                description TEXT,
                date INTEGER
                )
""")

# Creating a table for categories
cursor.execute("""CREATE TABLE categories (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                name TEXT
                )
""")


connection.commit()
connection.close()