import os
from markupsafe import escape
import main
from flask import Flask

from flask import request, render_template, redirect, url_for, session



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    
    @app.route('/home')
    def home():
        user_id = session.get("user_id")
        user_id = int(user_id)

        all_accounts = main.get_all_accounts()
        user_name = main.get_name(user_id)
        accounts = main.get_accounts(user_id)
        total_balance = main.get_total_balance(accounts)


        return render_template("home.html",accounts = accounts, user_name = user_name, user_id = user_id, total_balance = total_balance, all_accounts=all_accounts)
    
    @app.route('/delete_account', methods=["GET", "POST"])
    def delete_account():
        user_id = session.get("user_id")
        all_accounts = main.get_all_accounts()
        update= None

        if request.method == 'POST':
            deleted_account = int(request.form["chosen_account"])
            deleted_account_name = main.get_account_name(deleted_account)
            delete_success = main.delete_account(deleted_account)    

            if delete_success:
        
                update = f"{deleted_account_name} successfully deleted!"
            
            else:
                update= (f"{deleted_account_name} could not be deleted!")
        
        # account_id = request.args.get("account_id")


        return render_template("delete_account.html", all_accounts=all_accounts, update=update)
    
    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == 'POST':
            entered_user_id = request.form["entered_user_id"]
            entered_password = request.form["entered_password"]

            password= main.get_password(entered_user_id)

            if password == "None":
                error = "Incorrect PASSWORD or USER ID!"
                return render_template("login.html", error=error)

            elif entered_password and password == entered_password:
                session["user_id"] = entered_user_id
                return redirect(url_for("home"))
            
            else:
                error = "Incorrect PASSWORD or USER ID!"
                return render_template("login.html", error=error)

        return render_template("login.html")
    
    @app.route('/past_transactions')
    def past_transactions():
        user_id = session.get("user_id")
        user_name = main.get_name(user_id)
        transactions = main.get_transactions(user_id)
        return render_template("past_transactions.html",transactions=transactions, user_name = user_name)

    @app.route('/withdraw', methods=["GET", "POST"])
    def withdraw():
        user_id = session.get("user_id")
        accounts = main.get_accounts(user_id)
        balance = None
        account_id =None

        if request.method == 'POST':
            account_id = request.form["account_id"]

            amount = float(request.form["amount"])
            amount = round(amount,2)

            success = main.withdraw(user_id, account_id, amount)

            if success:
                #Redirects so that the selected account's balance shows up
                return redirect(url_for("withdraw", account_id=account_id))
            else:
                error = "Insufficient Funds!"
                return render_template("withdraw.html", accounts=accounts, balance=balance, account_id=account_id,error=error)

            
        
        account_id = request.args.get("account_id")

        if (account_id != None):
            account_id = int(account_id)
            balance = main.get_balance(user_id, account_id)

        return render_template("withdraw.html", accounts=accounts, balance=balance, account_id=account_id)
    

    @app.route('/transfer', methods=["GET", "POST"])
    def transfer():
        user_id = session.get("user_id")
        accounts = main.get_accounts(user_id)
        balance = None
        account_id =None

        if request.method == 'POST':
            account_from = request.form["account_1"]
            account_to = request.form["account_2"]

            amount = float(request.form["amount"])
            amount = round(amount,2)

            success = main.transfer(user_id, account_from,account_to, amount)

            if success:
                #Redirects so that the selected account's balance shows up
                return redirect(url_for("transfer", account_id=account_id))
            else:
                error = "Insufficient Funds!"
                return render_template("transfer.html", accounts=accounts, balance=balance, account_id=account_id,error=error)

            
        
        account_id = request.args.get("account_id")

        if (account_id != None):
            account_id = int(account_id)
            balance = main.get_balance(user_id, account_id)

        return render_template("transfer.html", accounts=accounts, balance=balance, account_id=account_id)
    
    @app.route('/deposit', methods=["GET", "POST"])
    def deposit():
        user_id = session.get("user_id")
        accounts = main.get_accounts(user_id)
        balance = None
        account_id =None

        if request.method == 'POST':
            account_id = request.form["account_id"]

            amount = float(request.form["amount"])
            amount = round(amount,2)

            main.deposit(user_id, account_id, amount)

            #Redirects so that the selected account's balance shows up
            return redirect(url_for("deposit", account_id=account_id))
            
        
        account_id = request.args.get("account_id")

        if (account_id != None):
            
            int(account_id)
            balance = main.get_balance(user_id, int(account_id))

  
        return render_template("deposit.html", accounts=accounts, balance=balance, account_id=account_id)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            password = request.form["password"]
            phone_number = request.form["phone_number"]
            user_id = main.create_user(first_name, last_name, password,phone_number)
            session["user_id"] = user_id
            return redirect(url_for("home"))
        return render_template("register.html")

    @app.route('/create_account', methods=['GET', 'POST'])
    def create_account():
        if request.method == 'POST':
            user_id = session.get("user_id")
            account_name = request.form["account_name"]
            initial_deposit = float(request.form["initial_deposit"])
            main.create_account(user_id, account_name,initial_deposit)

        return render_template("create_account.html")

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

