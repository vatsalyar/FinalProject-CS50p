import pytest
import sqlite3 as db
from project import hash_password, create_db, add_user, check_credentials

@pytest.fixture
def setup_database():
    """Set up a test database before each test and tear it down after."""
    conn = db.connect('test_users.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            transaction_type TEXT,
            amount REAL,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    yield conn  # Provide the connection to the test

    conn.close()

@pytest.fixture
def setup_users(setup_database):
    """Insert test users into the test database."""
    conn = setup_database
    c = conn.cursor()

    # Add test user
    c.execute("INSERT INTO users (user_id, username, password, balance) VALUES (?, ?, ?, ?)",
              (1, 'test_user', hash_password('test_password'), 100.0))
    conn.commit()
    yield conn  # Provide the connection to the test

@pytest.mark.parametrize("password,expected", [
    ("test_password", hash_password("test_password")),
    ("another_password", hash_password("another_password"))
])
def test_hash_password(password, expected):
    """Test the hash_password function."""
    assert hash_password(password) == expected

def test_create_db():
    """Test the create_db function."""
    create_db()  # Should not throw any errors
    conn = db.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    users_table = c.fetchone()
    assert users_table is not None

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    transactions_table = c.fetchone()
    assert transactions_table is not None

    conn.close()

def test_add_user(setup_database):
    """Test the add_user function."""
    conn = setup_database
    c = conn.cursor()

    # Add a new user to the test database
    add_user(2, 'new_user', 'new_password', None, db_name='test_users.db')

    c.execute("SELECT * FROM users WHERE user_id = ?", (2,))
    user = c.fetchone()

    assert user is not None
    assert user[1] == 'new_user'
    assert user[2] == hash_password('new_password')

def test_check_credentials(setup_users):
    """Test the check_credentials function."""
    conn = setup_users
    c = conn.cursor()

    # Ensure only the test user exists
    c.execute("SELECT * FROM users WHERE user_id = ?", (1,))
    user = c.fetchone()

    assert user is not None
    assert user[2] == hash_password('test_password')

    # Clear data after the test
    c.execute("DELETE FROM users WHERE user_id = ?", (1,))
    conn.commit()

