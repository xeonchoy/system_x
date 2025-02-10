import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS sync_status (
        id INTEGER PRIMARY KEY,
        active INTEGER DEFAULT 0,
        last_sync TIMESTAMP
    )
    ''')
    conn.commit()

def add_user(username, password):
    hashed_password = generate_password_hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
             (username, hashed_password))
    conn.commit()

def get_user_by_username(username):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    return c.fetchone()

def verify_user(username, password):
    user = get_user_by_username(username)
    if user:
        return check_password_hash(user[2], password)
    return False

def get_contacts():
    c.execute("SELECT username FROM users")
    return [{'name': row[0], 'id': i+1, 'status': 'online'} for i, row in enumerate(c.fetchall())]

def get_messages(contact_id):
    c.execute("SELECT sender, content, timestamp FROM messages WHERE receiver = ?", (contact_id,))
    return [{'sender': row[0], 'content': row[1], 'timestamp': row[2]} for row in c.fetchall()]

def send_message(message):
    # Placeholder - Replace with actual message sending logic
    c.execute("INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)", ('me', 1, message))
    conn.commit()

def set_sync_status(active, last_sync=None):
    if last_sync:
        c.execute("UPDATE sync_status SET active = ?, last_sync = ?", (active, last_sync))
    else:
        c.execute("UPDATE sync_status SET active = ?", (active,))
    conn.commit()

def get_sync_status():
    c.execute("SELECT active, last_sync FROM sync_status")
    row = c.fetchone()
    return {
        'active': row[0] if row else False,
        'lastSync': row[1] if row else None
    }

def stop_sync():
    set_sync_status(0)

def message_exists(message_id):
    c.execute("SELECT 1 FROM messages WHERE id = ?", (message_id,))
    return c.fetchone() is not None

def store_messages(messages):
    c.executemany("INSERT INTO messages (id, sender, receiver, content) VALUES (?, ?, ?, ?)", [(msg['id'], msg['sender'], msg['receiver'], msg['content']) for msg in messages])
    conn.commit()
