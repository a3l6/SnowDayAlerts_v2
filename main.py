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
      return render_template("index.html", logged_in=session["loggedin"])
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
      if rememberMe != None:
        session.permanent = True
      return redirect(url_for("user", method="login"))
    else:
      flash("Invalid Credentials", "Warning")     # CSS styling added on <p> tag 
      return render_template("login.html")
  else:
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method == "POST":
    phone = request.form["registerphone"]
    zone = request.form["zone"]
    password = request.form["password"]
  else:
    return render_template("signup.html")


# possibly useless
@app.route("/handleuser")
def user(method="login"):
  if method == "login":
    if "phone" in session:
      phone = session["phone"]
      return f"<h1>Your Phone number is: {phone}</h1>"
    else:
      return redirect(url_for("login"))
  elif method == "register":
    pass
  else:
    return "What did you do? Method is not login or register"


@app.route("/logout")
def logout():
  # remove user data
  session.pop("password", None)
  session.pop("phone", None)
  session.pop("rememberMe", None)
  session.pop("loggedin", None)
  for i in session:
    print(i)
  flash("You have been logged out!", "info")
  # return home
  return redirect(url_for("home"))


if __name__ == "__main__":
  app.run(debug=True)