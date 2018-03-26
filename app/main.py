import time


from flask import Flask, request, render_template, make_response, redirect
from sqlalchemy import create_engine, MetaData, Table

from models import User

from database import db_session, init_db

from passlib.hash import pbkdf2_sha256




app = Flask(__name__)
init_db()

@app.route('/')
def index():
    print("User cookie: {}".format(request.cookies.get("user_email")))
    return render_template("index.html", user_email=request.cookies.get("user_email"))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email_exists = db_session.query(User).filter_by(email=request.form["email"]).first() is not None
        if email_exists:
            # check if hashes match
            user = db_session.query(User).filter_by(email=request.form["email"]).first()
            if pbkdf2_sha256.verify(request.form["password"], user.password):
                resp = make_response(redirect("/"))
                resp.set_cookie("user_email", value=request.form["email"])
                return resp
            else:
                return "Password mismatch!"
        else:
            return "Email not found!"
    else:
        return render_template("login_form.html")

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie("user_email", "")
    return resp

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        hashed_psw = pbkdf2_sha256.encrypt(request.form["password"], rounds=200000, salt_size=16)

        # check if email already exists
        print("checking if {} already exists..".format(request.form["email"]))
        email_exists = db_session.query(User).filter_by(email=request.form["email"]).first() is not None
        if email_exists:
            return "Email already exists!"

        # add user to DB
        usr = User(email=request.form["email"], password=hashed_psw)
        db_session.add(usr)
        db_session.commit()

        # log the user in
        resp = make_response(redirect("/"))
        resp.set_cookie("user_email", value=request.form["email"])
        return resp
    else:
        return render_template("register_form.html")




if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
