import sqlite3

conn = sqlite3.connect("todo.db")  # Warning: This file is created in the current directory
conn.execute(
    "CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)"
)
conn.commit()
