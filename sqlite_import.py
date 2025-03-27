import pandas as pd
import sqlite3

# Load CSV file
csv_file = "mutts_db.csv"
df = pd.read_csv(csv_file, delimiter=";", dtype=str)

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Get category IDs from the database
cursor.execute("SELECT id FROM products_category;")
valid_categories = {row[0] for row in cursor.fetchall()}  # Convert to a set

# Get unique category IDs from CSV
csv_categories = set(df["product_category"].dropna().astype(int))

# Find missing categories
missing_categories = csv_categories - valid_categories

# Show missing category IDs
if missing_categories:
    print("⚠️ These category IDs in CSV do NOT exist in the database:", missing_categories)
else:
    print("✅ All category IDs in CSV exist in the database.")


# Check column count
print("Columns in CSV:", len(df.columns))
print("Columns expected:", 19)

# Display column names
print("CSV Column Names:", df.columns)

# Check for missing values
print("Missing Values:\n", df.isnull().sum())

# Check data types
print("Data Types:\n", df.dtypes)

# Show first rows
print(df.head())



# Close connection
conn.close()
