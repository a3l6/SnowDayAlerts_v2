from flask import *
import os
from datetime import timedelta
import databaseHandler
import messaging
import threading
import string

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.permanent_session_lifetime = timedelta(days=30)

@app.route('/')
def home():
  try:
    if session["loggedin"]:
      client = {
        "name": session["name"],
        "phone": session["phone"]
      }
      return render_template("index.html", logged_in=session["loggedin"], user=client)
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
      session["loggedin"] = True
      if rememberMe != None:  # var rememberMe returns either "remember" when its True or None when its False
        session.permanent = True
      response = databaseHandler.getuser(session["phone"], includepass=False)
      for key in response:
        session[key] = response[key]
      flash("Successful Login!")
      return redirect(url_for('home'))
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

    response = databaseHandler.create(name, phone, zone, password)

    if response == True:
      # Add data to session
      session["name"] = name
      session["phone"] = phone
      session["zone"] = zone
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

@app.route("/logout")
def logout():
  session.clear()     # remove user data
  flash("You have been logged out!", "info")
  # return home
  return redirect(url_for("home"))

@app.route("/settings/<number>", methods=["POST", "GET"])
def settings(number):
  if request.method == "POST":
    name = request.form["name"]
    zone = request.form["zone"]
    phonenumber = request.form["phone"]

    for i in name:
        if i not in string.printable:
            flash("Invalid Name!")
            render_template("settings.html", user=user)
    if zone.lower() not in ["north", "central", "muskoka", "south", "west"]:
        flash("Invalid Zone!")
        render_template("settings.html", user=user)
    if len(phonenumber) != 10:
        flash("Phone Number Too Long!")
        render_template("settings.html", user=user)
    else:
      for i in phonenumber:
        if i not in "0123456789":
          flash("Only Include Numbers!")
          render_template("settings.html", user=user)
    



    databaseHandler.changeinformation(phonenumber, zone, name, session_phone=session["phone"])
    session["phone"] = phonenumber
    session["zone"] = zone
    session["name"] = name
    #number = phonenumber
    user = databaseHandler.getuser(session["phone"], includepass=False)
    return redirect(url_for("settingsredirect", number=session["phone"]))
  else:
    try:
      user = databaseHandler.getuser(number, includepass=False)
      return render_template("settings.html", user=user)
    except TypeError as e:
      return e

@app.route("/redirect/<number>")
def settingsredirect(number):
  flash("Successfully Changed Account Details!")
  return redirect(url_for("settings", number=number))


@app.route("/admin/console", methods=["POST", "GET"])
def admin():
  if request.method == "POST":
    message = request.form["admininput"]
    messaging.send_admin_message(message)
    return render_template("admin.html")
  else:
    try:
      if session["phone"] == "admin":
        return render_template("admin.html")
      else:
        return "<h1>NOT LOGGED IN AS ADMIN</h1>"
    except KeyError:
      return "<h1>NOT LOGGED IN AS ADMIN</h1>"
  
@app.route("/deleteuser/<client>")
def deleteuser(client):
  try:
    if session["phone"] == client:
      databaseHandler.delete(toRemove=client)
      session.clear()
      flash("Deleted User!")
      return redirect(url_for("home"))
    else:
      return "Cannot Delete Other Users Profile!"
  except KeyError:
    return "Cannot Delete Other Users Profile!"

if __name__ == "__main__":
  thread1 = threading.Thread(target=messaging.main)
  thread1.start()
  app.run(debug=True) #use_reloader=False)
  thread1.join()