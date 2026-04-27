# elite102-banking-app
BankApp is a final project developed for Code2College's Elite102 Class. It integrates Python, MySQL, HTML, Flask to create a fully functional banking web app.

### FEATURES

**With BankApp, customers can...**
- View accounts and their balances
- Create multiple bank accounts
- Modify bank accounts
- Deposit/Withdraw funds from accounts
- Transfer funds between accounts
- View past transactions

**In addition to customer capabilities, ***designated admin accounts*** can...**
- View each customer's balance, accounts, and transactions
- View the bank's total balance
- Create accounts for customers
- Transfer funds between customers
- Modify customers' account names and balances
- Delete bank and user account

### DATA MANAGEMENT
**This program creates 3 MySQL tables to manage data**

***Users:***
*Manages user accounts within database*
- user_id INT AUTO_INCREMENT PRIMARY KEY, password varchar(255), first_name varchar(255), last_name varchar(255), phone_number varchar(255), total_balance dec(65,2), join_date DATETIME DEFAULT CURRENT_TIMESTAMP
  
***Accounts:***
*Manages bank accounts within database*
-  account_id INT AUTO_INCREMENT  PRIMARY KEY, user_id int, account_name varchar(255), balance decimal(65,2)

***Transactions***
*Manages transactions between accounts within database*
- trans_id INT AUTO_INCREMENT PRIMARY KEY, account_id int, transaction_type varchar(255), amount DECIMAL(65,2), date DATETIME DEFAULT CURRENT_TIMESTAMP

### SET-UP INSTRUCTIONS

**Prerequisites**
- Python 3.8+
- MySQL Server (Local)
- pip


- [ ] **1) Clone Repository**<br>
bash git clone https://github.com/your-username/elite102-banking-app.git
cd elite102-banking-app

- [ ] **2) Set Up the MySQL Database**<br>
- Log into MySQL and create a database:
sqlCREATE DATABASE banking_app;

- [ ] **4) Create env Variables**<br>
- Create a .env file in the root of the project to hold database information. This file should go in .gitignore:
DB_PASSWORD=your_mysql_root_password
DB_NAME=banking_app

- [ ] **5) Run the App**<br>
- Run flask_app.py
- Use a browser to go to: http://127.0.0.1:5000/login


## Admin Account Info
An admin account is automatically created upon table creation. To login, use the following credentials:
- **User ID:** 100
- **Password:** adminpassword
