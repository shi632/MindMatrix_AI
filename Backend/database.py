import sqlite3

def connect():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no TEXT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        status TEXT,
        mood TEXT,
        stress INTEGER,
        result TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_user(data):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO users (reg_no, name, age, gender, status, mood, stress, result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['reg_no'],
        data['name'],
        data['age'],
        data['gender'],
        data['status'],
        data['mood'],
        data['stress'],
        data['result']
    ))
    conn.commit()
    conn.close()