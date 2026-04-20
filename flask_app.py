import os
from markupsafe import escape
import main
from flask import Flask

from flask import request, render_template, redirect, url_for,session



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
        balance = main.get_balance(user_id)
        return render_template("home.html", balance=balance)
      
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            password = request.form["password"]
            user_id = main.create_account(first_name, last_name, password)
            session["user_id"] = user_id
            return redirect(url_for("home"))
        return render_template("register.html")

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

