import mysql.connector
import random

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gearup4me",
    database="banking_app",
    consume_results=True
)
cursor = conn.cursor()

# UNCOMMENT TO RESET DATABASE
# cursor.execute("DROP DATABASE banking_app")
# cursor.execute("CREATE DATABASE banking_app")
# cursor.execute("USE banking_app")
# cursor.execute("DROP TABLE IF EXISTS accounts")
# cursor.execute("DROP TABLE IF EXISTS transactions")
# cursor.execute("DROP TABLE IF EXISTS users")
# conn.commit()

# User Table Setup
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        password varchar(255),
        first_name varchar(255),
        last_name varchar(255),
        phone_number varchar(255),
        total_balance dec(65,2),
        join_date DATETIME DEFAULT CURRENT_TIMESTAMP

    ) AUTO_INCREMENT =100
''')

# Accounts Table Setup
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INT AUTO_INCREMENT  PRIMARY KEY,
        user_id int,
        account_name varchar(255),
        balance decimal(65,2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

# Transactions Table Setup
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        trans_id INT AUTO_INCREMENT PRIMARY KEY,
        account_id int,
        transaction_type varchar(255),
        amount DECIMAL(65,2),
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        
    )
''')


# Returns list of all users in user table
def get_all_users():
    cursor.execute("SELECT * FROM users")
    all_users= cursor.fetchall()
    return all_users

# Returns balance from a specific account
def get_account_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = float(cursor.fetchone()[0]) # Returns first column of first row returned by query
    return balance


# Returns a user_id based on a given account_id
def get_user_id(account_id):
    cursor.execute("SELECT user_id FROM accounts WHERE account_id = %s", (account_id,))
    user_id= cursor.fetchone()[0]
    user_id = int(user_id)
    return user_id

# Returns first name of user
def get_name(user_id):
    cursor.execute("SELECT first_name FROM users WHERE user_id = %s", (user_id,))
    name = (cursor.fetchone()[0])
    return name


# Returns user's phone number
def get_phone_number(user_id):
    cursor.execute("SELECT phone_number FROM users WHERE user_id = %s", (user_id,))
    phone_number = (cursor.fetchone()[0])
    return phone_number

# Returns name of an account
def get_account_name(account_id):
    cursor.execute("SELECT account_name FROM accounts WHERE account_id = %s", (account_id,))

    account_name = cursor.fetchone()[0]
    return account_name


# Returns a user's total balance
def get_user_balance(user_id):
    cursor.execute("SELECT total_balance FROM users WHERE user_id = %s", (user_id,))
    user_balance = cursor.fetchone()[0]
    return user_balance

# Returns user's password 
def get_password(user_id):
    cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
    check = cursor.fetchone() 
    
    if check == None:
        return None
    
    password = check[0]
    return password

def get_total_balance(accounts):
    total_balance =0
    if accounts != None:
        for account in accounts:
            int(account[3])
            total_balance +=account[3]
    return total_balance

# Returns all accounts assigned to a user
def get_accounts(user_id):
    cursor.execute("SELECT * FROM accounts WHERE user_id =%s", (user_id,))
    accounts = cursor.fetchall()
    return accounts

# Returns all transactions assigned to a user
def get_transactions(user_id):
    cursor.execute("""
    SELECT t.trans_id, t.account_id, t.transaction_type, t.amount, t.date
    FROM transactions t
    JOIN accounts a ON t.account_id = a.account_id
    WHERE a.user_id = %s
    ORDER BY t.date DESC
""", (user_id,))
    transactions = cursor.fetchall()
    result = []

    for trans_id, account_id, transaction_type, amount, date in transactions:
        
        cursor.execute("SELECT user_id,account_name FROM accounts WHERE account_id = %s", (account_id,))
        query_result = cursor.fetchone()[0]
        user_id = int(query_result[2])
        account_name = query_result[1]

        result.append({
            "transaction_id": trans_id,
            "user_id": user_id,
            "account_name": account_name,
            "account_id": account_id,
            "type": transaction_type,
            "amount": float(amount),
            "date": date
        })

    return result

# Returns all transactions 
def get_all_transactions():
    cursor.execute("SELECT trans_id, account_id, transaction_type, amount, date FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    result = []

    for trans_id, account_id, transaction_type, amount, date in transactions:
        
        cursor.execute("SELECT user_id,account_name FROM accounts WHERE account_id = %s", (account_id,))
        query_result = cursor.fetchone()
        user_id =int(query_result[0])
        account_name = query_result[1]

        result.append({
            "transaction_id": trans_id,
            "user_id": user_id,
            "account_name": account_name,
            "account_id": account_id,
            "type": transaction_type,
            "amount": float(amount),
            "date": date
        })

    return result



# Returns all accounts
def get_all_accounts():
    cursor.execute("SELECT * FROM accounts")
    all_accounts = cursor.fetchall()
    return all_accounts

# Updates balance of an account
def update_account_balance(new_balance, account_id):
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
    conn.commit()
    return True

# Updates an account name
def update_account_name(new_account_name, account_id):
    cursor.execute("UPDATE accounts SET account_name = %s WHERE account_id = %s", (new_account_name, account_id))
    conn.commit()
    return True

# Creates a new user
def create_user(first_name,last_name,password, phone_number):
    # Updating Users Table

    cursor.execute("INSERT INTO users (password, first_name, last_name, total_balance, phone_number) VALUES (%s, %s, %s, %s,%s)", (password, first_name, last_name,0.00, phone_number))
    conn.commit()
    user_id = cursor.lastrowid
    return user_id


# Creates an account
def create_account(user_id, account_name,initial_deposit, admin= False, selected_user_id = None): # Uses optional parameters based on admin status
    if admin:
        current_balance = get_user_balance(selected_user_id)
        new_balance = float(current_balance) + float(initial_deposit)
        print(current_balance)
        cursor.execute("INSERT INTO accounts (user_id,account_name, balance) VALUES (%s, %s, %s)", (selected_user_id, account_name, initial_deposit))
        cursor.execute("UPDATE users SET total_balance = %s WHERE user_id = %s", (new_balance,selected_user_id))
        conn.commit()
    else:
        current_balance = get_user_balance(user_id)
        new_balance = float(current_balance) + float(initial_deposit)
        print(current_balance)
        cursor.execute("INSERT INTO accounts (user_id,account_name, balance) VALUES (%s, %s, %s)", (user_id, account_name, initial_deposit))
        cursor.execute("UPDATE users SET total_balance = %s WHERE user_id = %s", (new_balance,user_id))
        conn.commit()


# Transfer between accounts
def transfer(account_from,account_to,  amount):
    balance_1 = get_account_balance(account_from)
    balance_2 = get_account_balance(account_to)

    if balance_1 < amount:
        return False
    
    balance_1 -= amount
    balance_2+=amount

    # Updating transactions and accounts after transfer
    cursor.execute( "INSERT INTO transactions(account_id, transaction_type, amount) VALUES(%s,%s,%s)",(account_from, "Transfer Out", amount))
    cursor.execute("INSERT INTO transactions(account_id, transaction_type, amount) VALUES(%s,%s,%s)",(account_to, "Transfer In", amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (balance_1, account_from))
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s",(balance_2, account_to))

    return True

# Withdraws amount from chosen account
def withdraw (user_id, account_id, amount):
    balance = get_account_balance(account_id)
    accounts = get_accounts(user_id)
    if balance < amount:
        return False
    new_balance = balance - amount
    #Update Transaction & Account Tables

    total_balance = get_total_balance(accounts)
    cursor.execute("INSERT INTO transactions( account_id, transaction_type,amount) VALUES(%s,%s,%s)", (account_id,"Withdraw",amount))
    update_account_balance(new_balance, account_id)

    cursor.execute("UPDATE users SET total_balance = %s WHERE user_id =%s",(total_balance,user_id) )
    conn.commit()
    return True


# Deposits amount from chosen account
def deposit (user_id, account_id,amount):
    balance = get_account_balance(account_id)
    accounts = get_accounts(user_id)
    balance += amount

    #Update Transaction & Account Tables

    total_balance = get_total_balance(accounts)
    cursor.execute("INSERT INTO transactions(account_id, transaction_type,amount) VALUES(%s,%s, %s)", (account_id,"Deposit",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance, user_id, account_id))
    cursor.execute("UPDATE users SET total_balance = %s WHERE user_id =%s",(total_balance,user_id) )
    conn.commit()


# Deletes an account based on account_id
def delete_account(account_id):
    cursor.execute("SELECT user_id,balance FROM accounts WHERE account_id = %s", (account_id,))

    query_result =cursor.fetchone()
    user_id = query_result[0]
    account_balance = query_result[1]

    cursor.execute("DELETE FROM transactions WHERE account_id = %s", (account_id,))
    cursor.fetchall()
    cursor.execute("UPDATE users SET total_balance = total_balance - %s WHERE user_id = %s", (account_balance,user_id))
    cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
    conn.commit()

    #Documents number of rows affected by Delete
    return cursor.rowcount > 0 

# Creates an admin account, if one does not exist
def check_admin():
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (100,))
    admin_info = cursor.fetchone()     # returns the one row from the query

    if admin_info ==None:
        cursor.execute("INSERT INTO users  (password, first_name, last_name, total_balance, phone_number) VALUES ( %s, %s, %s, %s,%s)", ("adminpassword", "Admin", "Admin",0.0, 000000))
        conn.commit()
        print("Admin Created!")
    else:
        print("Admin Already Created!")

check_admin()
