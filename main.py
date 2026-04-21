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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        password varchar(255),
        first_name varchar(255),
        last_name varchar(255),
        phone_number varchar(255),
        total_balance dec(65,2),
        join_date DATETIME DEFAULT CURRENT_TIMESTAMP

        
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
        account_id int,
        transaction_type varchar(255),
        amount DECIMAL(65,2),
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),
        FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
        
    )
''')
def check_admin():
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (1,))
    admin_info = cursor.fetchall()

    if admin_info == None:
        cursor.execute("INSERT INTO users  (password, first_name, last_name, total_balance, phone_number) VALUES ( %s, %s, %s, %s,%s)", ("adminpassword", "Admin", "Admin",0.0, 000000))
        conn.commit()
        print("Admin Created!")
    else:
        print("Admin Already Created!")


check_admin()


def get_balance(user_id, account_id):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s AND account_id = %s", (user_id,account_id))
    balance = float(cursor.fetchone()[0])
    return balance

def get_name(user_id):
    cursor.execute("SELECT first_name FROM users WHERE user_id = %s", (user_id,))
    name = (cursor.fetchone()[0])
    return name

def delete_account(account_id):
    cursor.execute("DELETE FROM transactions WHERE account_id = %s", (account_id,))
    cursor.fetchall()
    cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
    conn.commit()
    #Documents number of rows affected by Delete
    return cursor.rowcount > 0 


    


def get_phone_number(user_id):
    cursor.execute("SELECT phone_number FROM users WHERE user_id = %s", (user_id,))
    phone_number = (cursor.fetchone()[0])
    return phone_number

def get_account_name(account_id):
    cursor.execute("SELECT account_name FROM accounts WHERE account_id = %s", (account_id,))
    account_name = "Yeehaw"
    # account_name = (cursor.fetchone()[0])
    return account_name


def create_user(first_name,last_name,password, phone_number):
    # Updating Users Table

    cursor.execute("INSERT INTO users (password, first_name, last_name, total_balance, phone_number) VALUES (%s, %s, %s, %s,%s)", (password, first_name, last_name,0.0, phone_number))
    conn.commit()
    user_id = cursor.lastrowid
    return user_id

def create_account(user_id, account_name,initial_deposit):
    cursor.execute("INSERT INTO accounts (user_id,account_name, balance) VALUES (%s, %s, %s)", (user_id, account_name, initial_deposit))
    conn.commit()

def transfer(user_id,account_from,account_to,  amount):
    balance_1 = get_balance(user_id, account_from)
    balance_2 = get_balance(user_id, account_to)

    if balance_1 < amount:
        return False
    
    balance_1 -= amount
    balance_2+=amount

    cursor.execute( "INSERT INTO transactions(user_id, account_id, transaction_type, amount) VALUES(%s,%s,%s,%s)",(user_id, account_from, "Transfer Out", amount)
    )
    cursor.execute(
        "INSERT INTO transactions(user_id, account_id, transaction_type, amount) VALUES(%s,%s,%s,%s)",(user_id, account_to, "Transfer In", amount)
    )

    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance_1, user_id, account_from))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s",(balance_2, user_id, account_to))

    return True

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
            int(account[2])
            total_balance +=account[2]
    return total_balance

def get_accounts(user_id):
    cursor.execute("SELECT account_id, account_name, balance FROM accounts WHERE user_id =%s", (user_id,))
    accounts = cursor.fetchall()
    return accounts

def get_transactions(user_id):
    cursor.execute("SELECT trans_id, account_id, transaction_type, amount, date FROM transactions WHERE user_id = %s ORDER BY date DESC", (user_id,))
    transactions = cursor.fetchall()
    result = []

    for trans_id, account_id, transaction_type, amount, date in transactions:
        
        cursor.execute("SELECT account_name FROM accounts WHERE account_id = %s", (account_id,))
        account_name = cursor.fetchone()[0]

        result.append({
            "transaction_id": trans_id,
            "account_name": account_name,
            "type": transaction_type,
            "amount": float(amount),
            "date": date
        })

    return result

def withdraw (user_id, account_id, amount):
    balance = get_balance(user_id, account_id)
    accounts = get_accounts(user_id)
    if balance < amount:
        return False
    balance -= amount
    #Update Transaction & Account Tables

    total_balance = get_total_balance(accounts)
    cursor.execute("INSERT INTO transactions(user_id, account_id, transaction_type,amount) VALUES(%s,%s,%s, %s)", (user_id,account_id,"Withdraw",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance, user_id, account_id))
    cursor.execute("UPDATE users SET total_balance = %s WHERE user_id =%s",(total_balance,user_id) )

    conn.commit()
    return True

def get_all_accounts():
    cursor.execute("SELECT * FROM accounts")
    all_accounts = cursor.fetchall()
    return all_accounts



def deposit (user_id, account_id,amount):
    balance = get_balance(user_id,account_id)
    accounts = get_accounts(user_id)
    balance += amount

    #Update Transaction & Account Tables

    total_balance = get_total_balance(accounts)
    cursor.execute("INSERT INTO transactions(user_id, account_id, transaction_type,amount) VALUES(%s,%s,%s, %s)", (user_id,account_id,"Deposit",amount))
    cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s AND account_id = %s", (balance, user_id, account_id))
    cursor.execute("UPDATE users SET total_balance = %s WHERE user_id =%s",(total_balance,user_id) )
    conn.commit()
