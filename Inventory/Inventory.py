import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="inventory_system"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", str(e))

def authenticate_user(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    connection.close()
    if user and password == user[2]:
        return True
    return False

def login_window():
    login_win = tk.Tk()
    login_win.title("Login")
    
    tk.Label(login_win, text="Username").pack(padx=10, pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack(padx=10, pady=5)
    
    tk.Label(login_win, text="Password").pack(padx=10, pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack(padx=10, pady=5)
    
    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate_user(username, password):
            login_win.destroy()
            main_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid credentials. Please try again.")
    
    tk.Button(login_win, text="Login", command=login_action).pack(pady=10)
    login_win.mainloop()

def main_dashboard():
    main_win = tk.Tk()
    main_win.title("Inventory Management System")
    
    def add_product():
        add_prod_win = tk.Toplevel(main_win)
        add_prod_win.title("Add Product")
        
        tk.Label(add_prod_win, text="Product Name").pack(padx=10, pady=5)
        product_name_entry = tk.Entry(add_prod_win)
        product_name_entry.pack(padx=10, pady=5)
        
        tk.Label(add_prod_win, text="Description").pack(padx=10, pady=5)
        description_entry = tk.Entry(add_prod_win)
        description_entry.pack(padx=10, pady=5)
        
        tk.Label(add_prod_win, text="Price").pack(padx=10, pady=5)
        price_entry = tk.Entry(add_prod_win)
        price_entry.pack(padx=10, pady=5)
        
        tk.Label(add_prod_win, text="Stock Quantity").pack(padx=10, pady=5)
        stock_quantity_entry = tk.Entry(add_prod_win)
        stock_quantity_entry.pack(padx=10, pady=5)
        
        tk.Label(add_prod_win, text="Supplier").pack(padx=10, pady=5)
        supplier_entry = tk.Entry(add_prod_win)
        supplier_entry.pack(padx=10, pady=5)
        
        def save_product():
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO products (product_name, description, price, stock_quantity, supplier) VALUES (%s, %s, %s, %s, %s)",
                           (product_name_entry.get(), description_entry.get(), price_entry.get(), stock_quantity_entry.get(), supplier_entry.get()))
            connection.commit()
            connection.close()
            add_prod_win.destroy()
            messagebox.showinfo("Success", "Product added successfully")
        
        tk.Button(add_prod_win, text="Save", command=save_product).pack(pady=10)
    
    tk.Button(main_win, text="Add Product", command=add_product).pack(pady=10)
    
    def view_products():
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        connection.close()

        view_prod_win = tk.Toplevel(main_win)
        view_prod_win.title("View Products")
        
        for prod in products:
            tk.Label(view_prod_win, text=f"Product ID: {prod[0]}, Name: {prod[1]}, Stock: {prod[4]}").pack()
    
    tk.Button(main_win, text="View Products", command=view_products).pack(pady=10)
    
    def generate_report():
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE stock_quantity < 10")
        low_stock = cursor.fetchall()
        connection.close()
        
        report_win = tk.Toplevel(main_win)
        report_win.title("Low Stock Report")
        
        for product in low_stock:
            tk.Label(report_win, text=f"Product ID: {product[0]}, Name: {product[1]}, Stock: {product[4]}").pack()

    tk.Button(main_win, text="Low Stock Report", command=generate_report).pack(pady=10)
    
    main_win.mainloop()

login_window()
