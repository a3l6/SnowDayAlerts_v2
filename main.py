from tkinter import TRUE
from flask import *
import os
from datetime import timedelta
import databaseHandler

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.permanent_session_lifetime = timedelta(days=30)

@app.route('/')
def home():
  try:
    if session["loggedin"]:
      user = {
        "name": session["name"]
      }
      return render_template("index.html", logged_in=session["loggedin"], user=user)
  except KeyError:
    return render_template("index.html", logged_in=False)

@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    phone = request.form["loginphone"]
    password = request.form["password"].encode("utf-8")
    rememberMe = request.form.get("remember")
    
    if databaseHandler.auth(phone, password):
      session["phone"] = phone
      session["password"] = password
      session["loggedin"] = True
      if rememberMe != None:  # var rememberMe returns either "remember" when its True or None when its False
        session.permanent = True
      session["method"] = "login"
      return redirect(url_for("user"))
    else:
      flash("Invalid Credentials", "Warning")     # CSS styling added on <p> tag 
      return render_template("login.html")
  else:
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method == "POST":
    name = request.form["name"]
    phone = request.form["registerphone"]
    zone = request.form["zone"]
    password = request.form["registerpassword"]
    session["method"] = "register"

    response = databaseHandler.create(name, phone, zone, password)

    if response == True:
      # Add data to session
      session["name"] = name
      session["phone"] = phone
      session["zone"] = zone
      session["password"] = password
      session["loggedin"] = True

      flash("Successfully Created Account!", "info")
      return redirect(url_for("home"))

    elif response == False:
      flash("Account Already Exits!")
      return render_template("signup.html")

    else:
      flash(response, "warning")
      return render_template("signup.html")

  else:
    return render_template("signup.html")


# possibly useless
@app.route("/handleuser")
def user(): 
  if session["method"] == "login":
    return f"<h1>Your Phone number is: {phone}</h1>"
  elif session["method"] == "register":
    return "registerrte"
  else:
    return "What did you do? Method is not login or register"


@app.route("/logout")
def logout():
  # remove user data
  print(session)
  session.pop("password", None)
  session.pop("phone", None)
  session.pop("rememberMe", None)
  session.pop("loggedin", None)
  session.pop("method", None)
  session.pop("zone", None)
  session.pop("name", None)
  for i in session:
    print(i)
  flash("You have been logged out!", "info")
  # return home
  return redirect(url_for("home"))

@app.route("/test")
def test():
  databaseHandler.create("fdjf", "fjf", "dsfsdf", "dsfsdf")
  return "hi"

if __name__ == "__main__":
  app.run(debug=True)