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

# cursor.execute("DROP TABLE IF EXISTS accounts")
# cursor.execute("DROP TABLE IF EXISTS transactions")
# cursor.execute("DROP TABLE IF EXISTS users")
# conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        password varchar(255),
        first_name varchar(255),
        last_name varchar(255)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INT AUTO_INCREMENT  PRIMARY KEY,
        user_id int,
        account_name varchar(255),
        balance decimal(65,2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
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
        REFERENCES users(user_id)
        
    )
''')

def get_balance(user_id, account_id):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s AND account_id = %s", (user_id,account_id))
    balance = float(cursor.fetchone()[0])
    return balance

def get_name(user_id):
    cursor.execute("SELECT first_name FROM users WHERE user_id = %s", (user_id,))
    name = (cursor.fetchone()[0])
    return name

# def get_account_name(user_id):
#     cursor.execute("SELECT account_name FROM accounts WHERE user_id = %s", (user_id,))
#     account_name = (cursor.fetchone()[0])
#     return account_name


def create_user(first_name,last_name,password):
    # Updating Users Table

    cursor.execute("INSERT INTO users (password, first_name, last_name) VALUES (%s, %s, %s)", (password, first_name, last_name))
    conn.commit()
    user_id = cursor.lastrowid
    return user_id

def create_account(user_id, account_name,initial_deposit):
    cursor.execute("INSERT INTO accounts (user_id,account_name, balance) VALUES (%s, %s, %s)", (user_id, account_name, initial_deposit))
    conn.commit()



def get_accounts(user_id):
    cursor.execute("SELECT account_id, account_name, balance FROM accounts WHERE user_id =%s", (user_id,))
    accounts = cursor.fetchall()
    return accounts

def withdraw (user_id, account_id, amount):
    balance = get_balance(user_id, account_id)

    if balance < amount:
        return False
    balance -= amount
    #Update Transaction & Account Tables

    cursor.execute("INSERT INTO transactions(user_id, transaction_type,amount) VALUES(%s,%s,%s)", (user_id,"W",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance, user_id, account_id))
    conn.commit()
    return True

def deposit (user_id, account_id,amount):
    balance = get_balance(user_id,account_id)
    balance += amount

    #Update Transaction & Account Tables

    cursor.execute("INSERT INTO transactions(user_id, transaction_type,amount) VALUES(%s,%s,%s)", (user_id,"D",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance, user_id, account_id))
    conn.commit()

