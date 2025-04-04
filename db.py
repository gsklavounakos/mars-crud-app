"""
Module for initializing the Mars Resources database.
Creates the 'resources' table if it does not exist.
"""

import sqlite3

def init_db():
    """
    Initializes the Mars Resources database by creating the 'resources' table
    if it does not already exist.
    """
    connection = sqlite3.connect("mars_resources.db")  # Creates the database file
    cursor = connection.cursor()

    # Create the "resources" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")