import sqlite3
import csv
import os

def export_to_csv():
    # Connect to the database
    db_path = "database.db"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if table exists
    try:
        c.execute("SELECT id, name, regNo, result FROM users")
        users = c.fetchall()
    except sqlite3.OperationalError:
        print("Table 'users' does not exist yet.")
        conn.close()
        return
        
    conn.close()

    if not users:
        print("No users found in the database.")
        return

    csv_file = "users_report_standalone.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Reg No', 'Result'])
        writer.writerows(users)

    print(f"Successfully generated {csv_file} with {len(users)} users.")

if __name__ == "__main__":
    export_to_csv()
