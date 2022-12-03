from flask import Flask,render_template,session,redirect,send_from_directory,request,url_for,Blueprint
from datetime import timedelta
import time
import datetime
import pyodbc


from scan import *
from admin import *
from index import *
from user import *
from propertyregister import *
from helpdesk import *
from contacts import *
from profile import *
from booking import *
from noti import *


app = Flask(__name__)

app.secret_key = "cesadmin"
app.permanent_session_lifetime = timedelta(hours=1)

app.register_blueprint(contacts)
app.register_blueprint(scan)
app.register_blueprint(admin)
app.register_blueprint(index)
app.register_blueprint(user)
app.register_blueprint(propertyregister)
app.register_blueprint(helpdesk)
app.register_blueprint(profile)
app.register_blueprint(booking)
app.register_blueprint(noti)



@app.route("/")
def home():
    if "username" not in session:
        return render_template("/login.html")
    return redirect(url_for('admin.Profile'))

if __name__== '__main__':
    app.run(host = "0.0.0.0",port=789,debug = True )
