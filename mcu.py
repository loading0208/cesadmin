from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
from datetime import datetime
from datetime import date
###########################################################
import roles
import noti
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)

date = date.today()

mcu = Blueprint('mcu',__name__)


@mcu.route('/editcovid',methods=['POST'])
def Editcovid():
    if request.method == 'POST':
        employeeid = request.form['employeeid']
        date = request.form['date']
        try:
            con.connect()
            cur = con.cursor()
            sql = ("SELECT max(needle) FROM db_covid WHERE employeeID = %s")
            cur.execute(sql,(employeeid))
            chkneedle = cur.fetchall()
            chkneedle = chkneedle[0]
            chkneedle = chkneedle[0]+1
            sql = ("INSERT INTO db_covid (employeeID,needle,date_covid) VALUES(%s, %s, %s)")
            cur.execute(sql,(employeeid,chkneedle,date))
            con.commit()
            return redirect(url_for('admin.Profile'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
