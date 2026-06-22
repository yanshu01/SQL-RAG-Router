import sqlite3
import pandas as pd

# Read CSV
df = pd.read_csv("data/employees.csv")

# Create SQLite database
conn = sqlite3.connect("employees.db")

# Create table
df.to_sql(
    "employees",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Database created successfully!")