import sqlite3

conn = sqlite3.connect('event_management.db')
cursor = conn.cursor()

# Create Events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    location TEXT,
    price REAL,
    quota INTEGER
)
''')

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    birthdate TEXT,
    membership_type TEXT DEFAULT 'standard'
)
''')

# Create Participations table
cursor.execute('''
CREATE TABLE IF NOT EXISTS participations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    registration_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (event_id) REFERENCES events (id)
)
''')

conn.commit()
conn.close()

print("Database initialized successfully.")
