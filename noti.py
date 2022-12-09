from flask import Blueprint,session
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)

noti = Blueprint('noti',__name__)

def Notification():
    name = session['fname'] + ' ' + session['lname']
    employee = session['employeeID']
    department = session['department']
    level = session['level']

    try:
        con.connect()
        cur = con.cursor()
        rolesql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}' "
        cur.execute(rolesql)
        role = cur.fetchall()
        role2 =role[0][2]
        sql = f'''
                    SELECT *
                    from db_leave
                    WHERE head_employeeID = '{employee}' AND lea_status = 0
                    or manager_employeeID = '{employee}' AND lea_status = 1
                    or lea_status = 2 AND '{department}' = 'Human Resources' AND '{role2}' = 1
                '''
        cur.execute(sql)
        myreview = cur.fetchall()
        myreview = len(myreview)

        sql = f"SELECT * FROM db_helpdesk WHERE jobstatus = 0 AND '{level}' = 'admin' "
        cur.execute(sql)
        newdesk = cur.fetchall()
        snewdesk = len(newdesk)

        cur.execute("select * from db_comments where comment_status = 0")
        sumcomments =len(cur.fetchall())

        cur.execute("select * from db_comments where comment_status = 2")
        sumtrashcomments =len(cur.fetchall())


        sql = f"SELECT * FROM db_helpdesk WHERE jobstatus = 2 AND '{level}' = 'admin'"
        cur.execute(sql)
        waitdesk = cur.fetchall()
        swaitdesk = len(waitdesk)

        sql = f"SELECT * FROM tb_user WHERE usr_status = 0 AND '{level}' = 'admin'"
        cur.execute(sql)
        nuser = cur.fetchall()
        suser = len(nuser)

        rolesql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}' "
        cur.execute(rolesql)
        rolebooking = cur.fetchall()
        rolebooking = rolebooking[0][5]
        sqlbooking = f"SELECT * FROM db_booking WHERE '{rolebooking}' = 1 AND bk_status = 0"
        cur.execute(sqlbooking)
        booing = cur.fetchall()
        sbooing = len(booing)


        sql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}'"
        cur.execute(sql)
        rolecheckid = cur.fetchall()
        rolecheckid=rolecheckid[0]
        sumnoti = str(myreview+snewdesk+swaitdesk+suser+sbooing)

        return sumnoti,myreview,snewdesk,swaitdesk,suser,sbooing,sumcomments,sumtrashcomments,rolecheckid
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()





def Employee():
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_contact WHERE con_employee_ID = '{employee}' "
        cur.execute(sql)
        employee = cur.fetchall()
        return employee
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()
