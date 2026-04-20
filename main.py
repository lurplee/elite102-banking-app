import mysql.connector
import random

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gearup4me",
    database="banking_app"
)
cursor = conn.cursor()

# Create the contacts table


cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        user_id INT AUTO_INCREMENT  PRIMARY KEY,
        password varchar(255),
        first_name varchar(255),
        last_name varchar(255),
        balance decimal(65,2)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        trans_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id int,
        transaction_type varchar(255),
        amount DECIMAL(65,2),
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id)
        REFERENCES accounts(user_id)
        
    )
''')

def get_balance(user_id):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
    balance = float(cursor.fetchone()[0])
    return balance

def get_name(user_id):
    cursor.execute("SELECT first_name FROM accounts WHERE user_id = %s", (user_id,))
    name = (cursor.fetchone()[0])
    return name

def create_user(first_name,last_name,password):

    #print("ACCOUNT INFO")
   # print(f"First Name: {first_name}\nLast Name: {last_name}\nUser ID: {user_id}\nPassword: {password}")
    # Updating Accounts Table

    cursor.execute("INSERT INTO accounts (password, first_name, last_name, balance) VALUES (%s, %s, %s, %s)", (password, first_name, last_name, 0.00))
    conn.commit()

    user_id = cursor.lastrowid

    return user_id

def withdraw (user_id, amount):
    balance = get_balance(user_id)
    balance -= amount
    #Update Transaction & Account Tables

    cursor.execute("INSERT INTO transactions(user_id, transaction_type,amount) VALUES(%s,%s,%s)", (user_id,"W",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s", (balance,user_id))
    conn.commit()


def deposit (user_id, amount):
    balance = get_balance(user_id)
    balance += amount

    #Update Transaction & Account Tables

    cursor.execute("INSERT INTO transactions(user_id, transaction_type,amount) VALUES(%s,%s,%s)", (user_id,"D",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s", (balance,user_id))
    conn.commit()

