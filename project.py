"""
Children's Bank of Canada - Banking Application
A simple banking application built with Python and Tkinter that allows users to:
- Create and manage accounts
- Perform deposits and withdrawals
- View transaction history
- Reset passwords

Features:
- Secure password hashing
- SQLite database for data persistence
- Transaction history tracking
- User-friendly GUI interface
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3 as db
import hashlib

def hash_password(password):
    """Hash a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_db():
    """
    Initialize the SQLite database and create necessary tables if they don't exist.
    Tables:
    - users: Stores user account information
    - transactions: Stores transaction history
    """
    conn = db.connect('users.db')
    c = conn.cursor()

    # Create users table with user details and balance
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')

    # Create transactions table to track all financial activities
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
    conn.close()

def check_credentials(user_id, password, root):
    """
    Verify user credentials during login.
    
    Args:
        user_id: User's identification number
        password: User's password
        root: Current Tkinter window
    """
    conn = db.connect('users.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()

    conn.close()
    if user is None:
        messagebox.showerror("Failure", "User Id not found, Try again!")
        login_page()
    else:
        if user[2] == hash_password(password):
            account_dashboard(user_id, user[1], user[3])
        else:
            messagebox.showerror("Failure", "Incorrect Password, Try again!")
            login_page()
        close_window(root)

def account_dashboard(user_id, username, balance):
    """
    Display the main dashboard after successful login.
    Shows user information and provides access to various banking functions.
    
    Args:
        user_id: User's identification number
        username: User's name
        balance: Current account balance
    """
    # Create main dashboard window
    dashboard_window = tk.Tk()
    dashboard_window.title("Account Dashboard")
    dashboard_window.geometry("650x400")
    dashboard_window.config(bg='black')

    # Close button configuration
    button = tk.Button(dashboard_window, text="X", font=("Arial Black", 12), fg='#fdf4dc', bg='black', 
                      command=lambda: close_window(dashboard_window), bd=0, highlightcolor='red')
    button.grid(row=0, column=4, sticky='ne', padx=10, pady=5)

    # Bank name header
    label = tk.Label(dashboard_window, text="Children's Bank of Canada", font=('Arial', 18), fg='#ED254E', bg='black')
    label.grid(row=0, column=1, sticky='nsew', padx=10, pady=20)

    # Display user information
    user_id_label = tk.Label(dashboard_window, text="User ID: ", font=('Arial', 14), bg='black', fg='#FFD6BA')
    user_id_label.grid(row=1, column=0, padx=25, pady=10, sticky="e")

    user_id_tab = tk.Label(dashboard_window, text=user_id, font=('Arial', 14), bg='black', fg='#FAF9F9')
    user_id_tab.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    username_label = tk.Label(dashboard_window, text="Username: ", font=('Arial', 14), bg='black', fg='#FFD6BA')
    username_label.grid(row=1, column=2, padx=0, pady=10, sticky="e")

    username_tab = tk.Label(dashboard_window, text=username, font=('Arial', 14), bg='black', fg='#FAF9F9')
    username_tab.grid(row=1, column=3, padx=0, pady=10, sticky="w")

    # Balance display
    balance_tab = tk.Label(dashboard_window, text="Balance : ", font=("Arial", 16), bg="black", fg="#FFD6BA")
    balance_tab.grid(row=3, column=1, sticky='new', padx=5, pady=10)

    balance_label = tk.Label(dashboard_window, text=balance, fg="#FAF9F9", bg="black", font=("Arial", 14))
    balance_label.grid(row=5, column=1, padx=5, pady=0, sticky='new')

    # Action buttons
    transaction_button = tk.Button(dashboard_window, text="Make Transaction", font=('Arial', 10), 
                                 fg='white', bg='black', command=lambda: make_transaction(user_id, dashboard_window))
    transaction_button.grid(row=6, column=0, sticky='e', padx=5, pady=70)

    history_button = tk.Button(dashboard_window, text="View Transaction History", font=('Arial', 10), 
                              fg='white', bg='black', command=lambda: view_transaction_history(user_id, dashboard_window))
    history_button.grid(row=6, column=1, padx=75, pady=70)

    logout_button = tk.Button(dashboard_window, text="Logout", font=('Arial', 10), 
                            fg='white', bg='black', command=lambda: logout(dashboard_window))
    logout_button.grid(row=7, column=3, sticky='sw', padx=5, pady=0)

def make_transaction(user_id, root):
    """
    Handle deposit and withdrawal transactions.
    
    Args:
        user_id: User's identification number
        root: Current Tkinter window
    """
    close_window(root)
    conn = db.connect('users.db')
    c = conn.cursor()

    # Get user information
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        tk.messagebox.showerror("Error", "User not found.")
        return

    # Create transaction window
    root = tk.Tk()
    root.geometry("650x300")
    root.title("New Transaction")
    root.config(bg="black")

    # Window elements
    close_button = tk.Button(root, text="X", font=("Arial Black", 12), fg='#fdf4dc', bg='black',
                           command=lambda: close_window(root), bd=0, highlightcolor='red')
    close_button.grid(row=0, column=4, sticky='ne', padx=10, pady=5)

    header_label = tk.Label(root, text="Children's Bank of Canada", font=('Arial', 18), fg='#ED254E', bg='black')
    header_label.grid(row=0, column=1, sticky='nsew', padx=10, pady=20)

    # Transaction amount input
    amount_label = tk.Label(root, text="Amount", font=("Arial", 14), fg="#FFD6BA", bg="black")
    amount_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)

    amount_entry = tk.Entry(root, font=("Arial", 14), fg="#FAF9F9", bg="#0D1821")
    amount_entry.grid(row=1, column=1, pady=10)

    # Transaction type selection
    type_label = tk.Label(root, text="Type", font=("Arial", 14), fg="#FFD6BA", bg="Black")
    type_label.grid(row=2, column=0, padx=10, pady=10)

    options = ["Withdraw", "Deposit"]
    selected_option = tk.StringVar(value=options[0])

    dropdown = tk.OptionMenu(root, selected_option, *options)
    dropdown.config(bg="black", fg='#FFD6BA', font=("Arial", 12))
    dropdown.grid(row=2, column=1, pady=10)

    def process_transaction():
        """Process the transaction and update the database."""
        amount_str = amount_entry.get()
        transaction_type = selected_option.get()

        # Validate amount
        if not amount_str.isdigit():
            tk.messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
            return

        amount = float(amount_str)

        # Database operation
        conn = db.connect('users.db')
        c = conn.cursor()

        # Get current balance
        c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        current_balance = c.fetchone()[0]

        new_balance = current_balance
        if transaction_type == "Withdraw":
            if current_balance < amount:
                tk.messagebox.showerror("Error", "Insufficient balance for withdrawal.")
                conn.close()
                return
            new_balance -= amount
        elif transaction_type == "Deposit":
            new_balance += amount

        # Update balance
        c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()

        # Record transaction
        c.execute(
            "INSERT INTO transactions (user_id, transaction_type, amount, date) VALUES (?, ?, ?, datetime('now'))",
            (user_id, transaction_type, amount)
        )
        conn.commit()
        conn.close()

        tk.messagebox.showinfo("Success", f"{transaction_type} of ${amount} successful!")
        root.destroy()
        account_dashboard(user[0], user[1], new_balance)

    # Process transaction button
    process_button = tk.Button(root, text="Process Transaction", font=("Arial", 14), fg="#FFD6BA", bg="black",
                             command=process_transaction)
    process_button.grid(row=3, column=1, pady=20)

def view_transaction_history(user_id, root):
    """
    Display user's transaction history in a tabular format.
    
    Args:
        user_id: User's identification number
        root: Current Tkinter window
    """
    close_window(root)
    conn = db.connect('users.db')
    c = conn.cursor()

    # Fetch transaction history
    c.execute('SELECT transaction_type, amount, date FROM transactions WHERE user_id = ? ORDER BY date DESC', (user_id,))
    transactions = c.fetchall()

    # Get user details
    c.execute('SELECT user_id, username, balance FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        tk.messagebox.showerror("Error", "User not found.")
        return

    # Create history window
    root = tk.Tk()
    root.title("Transaction History")
    root.geometry("550x350")
    root.config(bg="black")

    # Window elements
    close_button = tk.Button(root, text="X", font=("Arial Black", 12), fg='#fdf4dc', bg='black',
                           command=lambda: close_window(root), bd=0, highlightcolor='red')
    close_button.grid(row=0, column=3, sticky='ne', padx=10, pady=5)

    bank_label = tk.Label(root, text="Children's Bank of Canada", font=('Arial', 18), fg='#ED254E', bg='black')
    bank_label.grid(row=0, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)

    balance_label = tk.Label(root, text=f"Current Balance: ${user[2]:.2f}", font=('Arial', 14), fg="white", bg="black")
    balance_label.grid(row=1, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    # Display transaction data
    if not transactions:
        no_data_label = tk.Label(root, text="No transactions found.", font=('Arial', 14), fg="white", bg="black")
        no_data_label.grid(row=2, column=0, columnspan=4, pady=20)
    else:
        # Headers
        headers = ["Type", "Amount", "Date"]
        for idx, header in enumerate(headers):
            label = tk.Label(root, text=header, font=('Arial', 12, 'bold'), fg="#FFD6BA", bg="black",
                           borderwidth=1, relief="solid")
            label.grid(row=2, column=idx, padx=5, pady=5, sticky="nsew")

        # Transaction data
        for row_idx, transaction in enumerate(transactions, start=3):
            for col_idx, value in enumerate(transaction):
                label = tk.Label(root, text=value, font=('Arial', 12), fg="white", bg="black",
                               borderwidth=1, relief="solid")
                label.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")

    def combined(user_id, username, balance, root):
        """Return to dashboard."""
        close_window(root)
        account_dashboard(user[0], user[1], user[2])

    # Back button
    back_button = tk.Button(root, text="Back", font=("Arial", 11), fg="#FFD6BA", bg="black",
                          command=lambda: combined(user[0], user[1], user[2], root))
    back_button.grid(row=20, column=3, columnspan=2, padx=75, pady=55)

def logout(root):
    """
    Handle user logout.
    
    Args:
        root: Current Tkinter window
    """
    close_window(root)
    login_page()

def new_user(root):
    """
    Display the new user registration window.
    
    Args:
        root: Current Tkinter window
    """
    close_window(root)

    # Create registration window
    root2 = tk.Tk()
    root2.title("New Account Registration")
    root2.geometry("650x250")
    root2.config(bg='black')

    # Window elements
    button = tk.Button(root2, text="X", font=("Arial Black", 12), fg='red', bg='black',
                      command=lambda: close_window(root2), bd=0, highlightcolor='red')
    button.grid(row=0, column=4, sticky='ne', padx=10, pady=5)

    label = tk.Label(root2, text="Children's Bank of Canada", font=('Arial', 18), fg='sky blue', bg='black')
    label.grid(row=0, column=1, sticky='nsew', padx=10, pady=20)

    # User input fields
    user_id_label = tk.Label(root2, text='User Id', font=('Arial', 14), bg='black', fg='white')
    user_id_label.grid(row=1, column=0, padx=25, pady=10, sticky="e")

    user_id_entry = tk.Entry(root2, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    user_id_entry.grid(row=1, column=1, padx=0, pady=10)

    username_label = tk.Label(root2, text='Username', font=('Arial', 14), bg='black', fg='white')
    username_label.grid(row=2, column=0, padx=25, pady=10, sticky="e")

    username_entry = tk.Entry(root2, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    username_entry.grid(row=2, column=1, padx=0, pady=10)

    password_label = tk.Label(root2, text='Password', font=('Arial', 14), bg='black', fg='white')
    password_label.grid(row=3, column=0, padx=25, pady=10, sticky="e")

    password_entry = tk.Entry(root2, show='*', font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    password_entry.grid(row=3, column=1, padx=0, pady=10)

    submit_button2 = tk.Button(root2, command=lambda: create_acc(user_id_entry, username_entry, password_entry, root2),
                              text='Submit', font=('Arial', 10), fg='white', bg='black')
    submit_button2.grid(row=3, column=2, padx=5, pady=10)

def create_acc(user_id_entry, username_entry, password_entry, root2):
    """
    Create a new user account with the provided information.
    
    Args:
        user_id_entry: Entry widget containing user ID
        username_entry: Entry widget containing username
        password_entry: Entry widget containing password
        root2: Current Tkinter window
    """
    user_id = user_id_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    if not user_id or not password or not username:
        messagebox.showerror("Input Error", "All fields are required")
    else:
        user_id_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        add_user(user_id, username, password, root2)

def add_user(user_id, username, password, root2, db_name='users.db'):
    """
    Add a new user to the database.
    
    Args:
        user_id: User's identification number
        username: User's chosen username
        password: User's password
        root2: Current Tkinter window
        db_name: Database file name (default: 'users.db')
    """
    conn = db.connect(db_name)
    c = conn.cursor()

    # Check for existing user
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = c.fetchone()

    if existing_user:
        if root2:
            messagebox.showerror("Failure", "User Id already exists, please try a different one.")
    else:
        try:
            c.execute(
                'INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                (user_id, username, hash_password(password))
            )
            conn.commit()
            if root2:
                messagebox.showinfo("Success", "User added successfully!")
                close_window(root2)
                login_page()
        except db.Error as e:
            if root2:
                messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

def close_window(root):
    """
    Close the current Tkinter window.
    
    Args:
        root: Tkinter window to close
    """
    root.destroy()

def submit_action(entry, entry2, root):
    """
    Handle login form submission.
    
    Args:
        entry: User ID entry widget
        entry2: Password entry widget
        root: Current Tkinter window
    """
    user_id = entry.get()
    password = entry2.get()
    if not user_id or not password:
        messagebox.showerror("Input Error", "Both user_id and password are required")
    else:
        check_credentials(user_id, password, root)

def forgot_password_window(root):
    """
    Display the password reset window.
    
    Args:
        root: Current Tkinter window
    """
    close_window(root)

    root2 = tk.Tk()
    root2.title("Change Password")
    root2.geometry("650x300")
    root2.config(bg='black')

    # Window elements
    button = tk.Button(root2, text="X", font=("Arial Black", 12), fg='red', bg='black',
                      command=lambda: close_window(root2), bd=0, highlightcolor='red')
    button.grid(row=0, column=4, sticky='ne', padx=10, pady=5)

    label = tk.Label(root2, text="Children's Bank of Canada", font=('Arial', 18), fg='#ED254E', bg='black')
    label.grid(row=0, column=1, sticky='nsew', padx=10, pady=20)

    # User input fields
    user_id_label = tk.Label(root2, text='User Id', font=('Arial', 14), bg='black', fg='white')
    user_id_label.grid(row=1, column=0, sticky='ew', padx=25, pady=10)

    user_id_entry = tk.Entry(root2, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    user_id_entry.grid(row=1, column=1, padx=0, pady=10)

    username_label = tk.Label(root2, text='Username', font=('Arial', 14), bg='black', fg='white')
    username_label.grid(row=2, column=0, sticky='ew', padx=25, pady=10)

    username_entry = tk.Entry(root2, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    username_entry.grid(row=2, column=1, padx=0, pady=10)

    password_label = tk.Label(root2, text='New Password', font=('Arial', 14), bg='black', fg='white')
    password_label.grid(row=3, column=0, sticky='ew', padx=25, pady=10)

    password_entry = tk.Entry(root2, show='*', font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    password_entry.grid(row=3, column=1, padx=0, pady=10)

    confirm_password_label = tk.Label(root2, text='Confirm Password', font=('Arial', 14), bg='black', fg='white')
    confirm_password_label.grid(row=4, column=0, sticky='ew', padx=25, pady=10)

    confirm_password_entry = tk.Entry(root2, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    confirm_password_entry.grid(row=4, column=1, padx=0, pady=10)

    submit_button2 = tk.Button(root2, command=lambda: reset_password(user_id_entry, username_entry,
                                                                   password_entry, confirm_password_entry, root2),
                              text='Submit', font=('Arial', 10), fg='white', bg='black')
    submit_button2.grid(row=4, column=2, padx=5, pady=10)

def reset_password(user_id_entry, username_entry, password_entry, confirm_password_entry, root2):
    """
    Process password reset request.
    
    Args:
        user_id_entry: Entry widget containing user ID
        username_entry: Entry widget containing username
        password_entry: Entry widget containing new password
        confirm_password_entry: Entry widget containing password confirmation
        root2: Current Tkinter window
    """
    user_id = user_id_entry.get()
    username = username_entry.get()
    new_password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not user_id or not new_password or not username or not confirm_password:
        messagebox.showerror("Input Error", "All fields are required")
    elif new_password != confirm_password:
        messagebox.showerror("Input Error", "Passwords do not match")
    else:
        conn = db.connect('users.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()

        if user:
            c.execute('UPDATE users SET password = ? WHERE user_id = ?', (hash_password(new_password), user_id))
            conn.commit()
            messagebox.showinfo("Success", "Password updated successfully!")
            close_window(root2)
            login_page()
        else:
            messagebox.showerror("Failure", "User ID not found!")
        conn.close()

def login_page():
    """Display the main login page."""
    root = tk.Tk()
    root.title("Main Project")
    root.geometry("550x300")
    root.config(bg='black')

    # Window elements
    button = tk.Button(root, text="X", font=("Arial Black", 12), fg='#fdf4dc', bg='black',
                      command=lambda: close_window(root), bd=0, highlightcolor='red')
    button.grid(row=0, column=4, sticky='ne', padx=10, pady=5)

    label = tk.Label(root, text="Children's Bank of Canada", font=('Arial', 18), fg='#ED254E', bg='black')
    label.grid(row=0, column=1, sticky='nsew', padx=10, pady=20)

    # Login form
    user_id_label = tk.Label(root, text='User Id', font=('Arial', 14), bg='black', fg='#FFD6BA')
    user_id_label.grid(row=1, column=0, padx=25, pady=10, sticky="e")

    entry = tk.Entry(root, font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    entry.grid(row=1, column=1, padx=0, pady=10)

    password_label = tk.Label(root, text='Password', font=('Arial', 14), bg='black', fg='#FFD6BA')
    password_label.grid(row=2, column=0, padx=25, pady=10, sticky="e")

    entry2 = tk.Entry(root, show='*', font=('Arial', 14), bg='#28282B', fg='white', bd=0)
    entry2.grid(row=2, column=1, padx=0, pady=10)

    # Buttons
    submit_button2 = tk.Button(root, command=lambda: submit_action(entry, entry2, root),
                              text='Log in', font=('Arial', 10), fg='white', bg='black')
    submit_button2.grid(row=2, column=2, sticky='w', padx=5, pady=10)

    forgot_password_label = tk.Label(root, text="Forgot Password?", font=("Arial", 10), bd=0, fg="#FFD6BA", bg="black")
    forgot_password_label.grid(row=3, column=0, sticky='e', padx=0, pady=10)

    forgot_password_button = tk.Button(root, text="Reset Password", font=("Arial", 10),
                                     fg='white', bg='black', command=lambda: forgot_password_window(root))
    forgot_password_button.grid(row=3, column=1, sticky='w', padx=5, pady=10)

    new_account_label = tk.Label(root, text="New User ?", font=("Arial", 10), bd=0, fg="#FFD6BA", bg="black")
    new_account_label.grid(row=4, column=0, sticky='e', padx=0, pady=10)

    create_account_button = tk.Button(root, text="Create Account", font=("Arial", 10),
                                    fg='white', bg='black', command=lambda: new_user(root))
    create_account_button.grid(row=4, column=1, sticky='w', padx=5, pady=10)

    root.mainloop()

def main():
    """Initialize the application by creating the database and launching the login page."""
    create_db()
    login_page()

if __name__ == "__main__":
    main()