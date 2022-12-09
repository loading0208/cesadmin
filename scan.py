from flask import Blueprint,render_template,request,redirect,url_for,session,flash
###########################################################
import pyodbc #access
###########################################################
from datetime import timedelta
from datetime import datetime
###########################################################
import noti
import roles
############################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)

scan = Blueprint('scan',__name__)


@scan.route("/checkmyscan")
def Checkmyscan():
    if "username" not in session:
        return render_template("/login.html")
    part = "checkmyscan"
    employee = session['employeeID']

    try:
        conn = pyodbc.connect(con_string)
        cur = conn.cursor()
        sql = (f'''
                    SELECT TOP 100 CHECKINOUT.CHECKTIME
                    FROM CHECKINOUT INNER JOIN USERINFO ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber WHERE USERINFO.SSN = '{session['employeeID']}'  ORDER BY CHECKINOUT.CHECKTIME DESC;
                ''')
        cur.execute(sql)
        row = cur.fetchall()



        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_leave WHERE my_employeeID = '{employee}'  "
        cur.execute(sql)
        myleave = cur.fetchall()
        mysearch = 0

        sql = (f'''
                    SELECT * FROM holidays
                ''')
        cur.execute(sql)
        holiday = cur.fetchall()
        return render_template("/checkmyscan.html",part=part,month=month,myleave=myleave,holiday=holiday, row=row,sumrow=len(row),summysearch=mysearch,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except pyodbc.Error as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        conn.close()




@scan.route("/searchmyscan",methods=['POST'])
def Searchmyscan():
    if request.method == "POST":
        employee = session['employeeID']
        dstart = request.form['dstart']
        dend = request.form['dend']
        try:
            conn = pyodbc.connect(con_string)
            cur = conn.cursor()
            sql = (f'''
                        SELECT TOP 100 CHECKINOUT.CHECKTIME
                        FROM CHECKINOUT INNER JOIN USERINFO ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber WHERE USERINFO.SSN = '{session['employeeID']}'  ORDER BY CHECKINOUT.CHECKTIME DESC;
                    ''')
            cur.execute(sql)
            row = cur.fetchall()

            sql = (f'''
                        SELECT CHECKINOUT.CHECKTIME FROM CHECKINOUT INNER JOIN USERINFO ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber WHERE USERINFO.SSN = '{session['employeeID']}' AND (CHECKINOUT.CHECKTIME between #{dstart} 00:00:00# and #{dend} 23:59:59#) ;
                    ''')
            cur.execute(sql)
            mysearch = cur.fetchall()

            con.connect()
            cur = con.cursor()
            sql = f"SELECT * from db_leave WHERE my_employeeID = '{employee}'  "
            cur.execute(sql)
            myleave = cur.fetchall()

            sql = (f'''
                        SELECT * FROM holidays
                    ''')
            cur.execute(sql)
            holiday = cur.fetchall()
            return render_template("checkmyscan.html",month=month,mysearch=mysearch,holiday=holiday,myleave=myleave,row=row,summysearch=len(mysearch),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except pyodbc.Error as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            conn.close()





@scan.route("/checkscan")
def Checkscan():
    if "username" not in session:
        return render_template("/login.html")
    try:
        conn = pyodbc.connect(con_string)
        cur = conn.cursor()
        sql = ('''
                    SELECT TOP 5000 USERINFO.Name,DEPARTMENTS.DEPTNAME, format(CHECKINOUT.CHECKTIME,'dd/MM/yyyy hh:mm:ss'),CHECKINOUT.VERIFYCODE
                    FROM CHECKINOUT
                    INNER JOIN (DEPARTMENTS INNER JOIN USERINFO ON DEPARTMENTS.DEPTID = USERINFO.DEFAULTDEPTID)
                    ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber ORDER BY CHECKINOUT.CHECKTIME DESC;
                ''')
        cur.execute(sql)
        row = cur.fetchall()
        return render_template("/checkscan.html",month=month, row=row,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except pyodbc.Error as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        conn.close()



@scan.route("/research",methods=['POST'])
def Research():
    if request.method == "POST":
        dstart = request.form['dstart']
        dend = request.form['dend']
        try:
            conn = pyodbc.connect(con_string)
            cur = conn.cursor()
            sql = (f'''
                        SELECT USERINFO.Name,DEPARTMENTS.DEPTNAME,format(CHECKINOUT.CHECKTIME,'dd/MM/yyyy hh:mm:ss'),CHECKINOUT.VERIFYCODE
                        FROM CHECKINOUT
                        INNER JOIN (DEPARTMENTS INNER JOIN USERINFO ON DEPARTMENTS.DEPTID = USERINFO.DEFAULTDEPTID)
                        ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber where CHECKINOUT.CHECKTIME between  #{dstart} 00:00:00# AND  #{dend} 23:59:59#  order by CHECKINOUT.id DESC;
                    ''')
            cur.execute(sql)
            search = cur.fetchall()
            return render_template("search.html",month=month,search=search,sunsearch=len(search),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except pyodbc.Error as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            conn.close()


@scan.route("/researchdep",methods=['POST'])
def Researchdep():
    if request.method == "POST":
        dep = request.form['dep']
        dstart = request.form['dstart']
        dend = request.form['dend']
        try:
            conn = pyodbc.connect(con_string)
            cur = conn.cursor()
            sql = (f'''
                        SELECT USERINFO.Name,DEPARTMENTS.DEPTNAME,format(CHECKINOUT.CHECKTIME,'dd/MM/yyyy hh:mm:ss'),CHECKINOUT.VERIFYCODE
                        FROM CHECKINOUT
                        INNER JOIN (DEPARTMENTS INNER JOIN USERINFO ON DEPARTMENTS.DEPTID = USERINFO.DEFAULTDEPTID)
                        ON CHECKINOUT.Badgenumber = USERINFO.Badgenumber where DEPARTMENTS.DEPTNAME = '{dep}' AND (CHECKINOUT.CHECKTIME between #{dstart} 00:00:00# and #{dend} 23:59:59#) order by CHECKINOUT.id DESC;
                    ''')
            cur.execute(sql)
            search = cur.fetchall()
            return render_template("search.html",month=month,search=search,sunsearch=len(search),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except pyodbc.Error as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            conn.close()
