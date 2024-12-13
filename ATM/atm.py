import mysql.connector
from tkinter import *
from tkinter import messagebox

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="atm_db"
)
cursor = db.cursor()

logged_in_user = None

def login():
    global logged_in_user
    username = username_entry.get()
    pin = pin_entry.get()

    query = "SELECT * FROM accounts WHERE username = %s AND pin = %s"
    cursor.execute(query, (username, pin))
    account = cursor.fetchone()

    if account:
        logged_in_user = account
        messagebox.showinfo("Login", "Login Successful!")
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")

def check_balance():
    messagebox.showinfo("Balance", f"Your balance is: Rs. {logged_in_user[3]}")

def deposit_money():
    global logged_in_user
    amount = float(amount_entry.get())
    query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
    cursor.execute(query, (amount, logged_in_user[0]))
    db.commit()

    transaction_query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Deposit', %s)"
    cursor.execute(transaction_query, (logged_in_user[0], amount))
    db.commit()

    cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (logged_in_user[0],))
    logged_in_user = cursor.fetchone()

    messagebox.showinfo("Deposit", f"Rs. {amount} deposited successfully!\nUpdated Balance: Rs. {logged_in_user[3]}")
    main_menu()

def withdraw_money():
    global logged_in_user
    amount = float(amount_entry.get())

    if amount > logged_in_user[3]:
        messagebox.showerror("Withdraw Failed", "Insufficient Funds!")
        return

    query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
    cursor.execute(query, (amount, logged_in_user[0]))
    db.commit()

    transaction_query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Withdraw', %s)"
    cursor.execute(transaction_query, (logged_in_user[0], amount))
    db.commit()

    cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (logged_in_user[0],))
    logged_in_user = cursor.fetchone()

    messagebox.showinfo("Withdraw", f"Rs. {amount} withdrawn successfully!\nUpdated Balance: Rs. {logged_in_user[3]}")
    main_menu()

def main_menu():
    global logged_in_user
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text=f"Welcome, {logged_in_user[1]}!", font=("Arial", 18)).pack(pady=10)

    Button(root, text="Check Balance", width=20, command=check_balance).pack(pady=5)
    Button(root, text="Deposit Money", width=20, command=lambda: transaction_screen("Deposit")).pack(pady=5)
    Button(root, text="Withdraw Money", width=20, command=lambda: transaction_screen("Withdraw")).pack(pady=5)
    Button(root, text="Logout", width=20, command=logout).pack(pady=5)

def transaction_screen(transaction_type):
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text=f"{transaction_type} Money", font=("Arial", 18)).pack(pady=10)

    global amount_entry
    amount_entry = Entry(root, font=("Arial", 14))
    amount_entry.pack(pady=10)

    if transaction_type == "Deposit":
        Button(root, text="Deposit", command=deposit_money).pack(pady=10)
    elif transaction_type == "Withdraw":
        Button(root, text="Withdraw", command=withdraw_money).pack(pady=10)

    Button(root, text="Back to Main Menu", command=main_menu).pack(pady=5)

def logout():
    global logged_in_user
    logged_in_user = None
    home_screen()

def home_screen():
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="ATM Login", font=("Arial", 18)).pack(pady=10)

    global username_entry, pin_entry
    username_entry = Entry(root, font=("Arial", 14))
    username_entry.pack(pady=5)
    username_entry.insert(0, "Username")

    pin_entry = Entry(root, font=("Arial", 14), show="*")
    pin_entry.pack(pady=5)
    pin_entry.insert(0, "PIN")

    Button(root, text="Login", command=login).pack(pady=10)

root = Tk()
root.title("ATM Interface")
root.geometry("400x400")
home_screen()
root.mainloop()
