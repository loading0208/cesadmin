from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
###########################################################
from songline import Sendline
###########################################################
import noti
import roles
############################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from datetime import datetime
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)

dateeven = datenow.strftime("%Y-%m-%d")

booking = Blueprint('booking',__name__)

@booking.route("/notifybooking")
def Notifybooking():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT meetingroom FROM role WHERE usr_employee_ID = '{session['employeeID']}' "
        cur.execute(sql)
        checkrole = cur.fetchall()
        checkrole = checkrole[0]
        checkrole = checkrole[0]
        if checkrole != 1:
            return redirect(url_for('booking.Booking'))
        sql = "SELECT * FROM db_booking"
        cur.execute(sql)
        booking = cur.fetchall()
        return render_template('notifybooking.html',booking=booking,month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions(),datenow=datenow)
    except Exception as e:
        print (e)
    finally:
        print("Close")
        cur.close()
        con.close()


@booking.route("/bookingroom")
def Booking():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_booking "
        cur.execute(sql)
        events = cur.fetchall()

        sql = f"SELECT * FROM db_booking where bk_dateuse between '{dateeven} 00:00:00' and  '{dateeven} 23:59:59' "
        cur.execute(sql)
        todayevents = cur.fetchall()

        sql = f"SELECT * FROM db_booking where bk_dateuse NOT between '{dateeven} 00:00:00' and  '{dateeven} 23:59:59' and bk_dateuse > '{dateeven} 00:00:00' "
        cur.execute(sql)
        nextevents = cur.fetchall()

        return render_template('bookingroom.html',part="bookingroom",events=events,nextevents=nextevents,snextevents=len(nextevents),todayevents=todayevents,stodayevents=len(todayevents),month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@booking.route("/howto")
def Howto():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("meetingroom/howto.html",sumnoti=notification.Notification(),permissions=roles.Checkpermissions())


@booking.route("/addbooking", methods=["POST"])
def Addbooking():
    if request.method == "POST":
        name = request.form["name"]
        employeeid = request.form["employeeid"]
        department = request.form["depart"]
        email = request.form["email"]
        room = request.form["room"]
        date = request.form["date"]
        dateend = request.form["dateend"]
        other = request.form["other"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into db_booking (bk_name,employeeID,bk_department,bk_email,bk_room,bk_dateuse,bk_dateend,bk_other) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(name,employeeid,department,email,room,date,dateend,other))
            con.commit()

            sql = "select * from db_booking ORDER BY bk_id DESC LIMIT 1"
            cur.execute(sql)
            checkdate = cur.fetchall()
            checkdate = checkdate[0]
            if checkdate[6] > checkdate[7] or checkdate[6] < datenow :
                sql = f"delete from db_booking where bk_id = '{checkdate[0]}'"
                cur.execute(sql)
                con.commit()
                flash("กรุณาเช็ควันที่")
                return redirect(url_for('booking.Booking'))
            #----แจ้งเตือนผ่านไลน์--------------------------------------------
            #token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
            #messenger = Sendline(token)
            #messenger.sendtext('คุณ' + session['fname']+' '+ 'จองห้องประชุม ห้อง' + room )
           #----สิ้นสุด----------------------------------------------------
            flash("จองห้องประชุมแล้ว")
            return redirect(url_for('booking.Booking'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@booking.route("/updatestatus",methods=["POST","GET"])
def Updatestatus():
    if request.method == "POST":
        id = request.form["id"]
        status = request.form["status"]
        room = request.form["room"]
        email = request.form["email"]
        actionby = request.form["actionby"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE  `db_booking` SET `bk_status` =%s,`bk_admin` =%s WHERE `bk_id`=%s"
            cur.execute(sql,(status,actionby,id))
            con.commit()
            if status == '8':
                flash('ยกเลิกการจองห้องประชุมสำเร็จ','error')
                return redirect(url_for('admin.Profile'))
            if status == '10':
                return redirect(url_for('booking.Notifybooking'))
            if status == '2':
                #----แจ้งเตือนผ่านไลน์--------------------------------------------
                messenger = Sendline('6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O')
                messenger.sendtext( room + ' '+ 'Close' )
                #----สิ้นสุด----------------------------------------------------
                return redirect(url_for('admin.Profile'))
#----แจ้งผลผ่าน e-mail----------------------------------------------------------------------------------
            def sendthai(sendto,subj,detail):
                try:
                	myemail = 'noreply@cesteam.co.th'
                	mypassword = 'iydot06)[q8ofu@@CES'
                	receiver = sendto

                	msg = MIMEMultipart('alternative')
                	msg['Subject'] = subj
                	msg['From'] = 'IT Support CES <noreply@cesteam.co.th>'
                	msg['To'] = receiver
                	html = detail

                	part1 = MIMEText(html, 'html')
                	msg.attach(part1)

                	s = smtplib.SMTP('mail.cesteam.co.th:25')
                	s.ehlo()
                	s.starttls()

                	s.login(myemail, mypassword)
                	s.sendmail(myemail, receiver.split(','), msg.as_string())
                	s.quit()
                except:
                    print('send failed')

            if status == '1':
                subject = 'แจ้งสถานะการขอใช้ห้องประชุม'
                msg = f"""
                        <html>

                        <head></head>

                        <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992;display:flex;justify-content:center;align-items: center;">
                            <table style='border-collapse: collapse;width:100%;'>
                                <tr style="text-align:center;">
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>ใบจอง</th>
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>สถานะ</th>
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>ผู้เจ้าหน้าที่ทำรายการ</th>
                                </tr>
                                <tr style="text-align:center;">
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>{id}</td>
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>ใช้งานได้</td>
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>{actionby}</td>
                                </tr>
                            </table>
                            <h3>IT Support CES</h3>
                            <a href="http://ceseservice.dyndns.org:88/">CES-ESERVICE</a>
                        </body>

                        </html>
                """
                sendthai(email,subject,msg)
            if status == '9':
                subject = 'แจ้งสถานะการขอใช้ห้องประชุม'
                msg = f"""
                        <html>

                        <head></head>

                        <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992;display:flex;justify-content:center;align-items: center;">
                            <table style='border-collapse: collapse;width:100%;'>
                                <tr style="text-align:center;">
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>ใบจอง</th>
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>สถานะ</th>
                                    <th style='border: 1px solid #dddddd;color:#079992;font-size:20px;width:25%;'>ผู้เจ้าหน้าที่ทำรายการ</th>
                                </tr>
                                <tr style="text-align:center;">
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>{id}</td>
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>ยกเลิยกเลิกโดยผู้ดูแล</td>
                                    <td style='border: 1px solid #dddddd;color:#079992;font-size:20px'>{actionby}</td>
                                </tr>
                            </table>
                            <h3>IT Support CES</h3>
                            <a href="http://ceseservice.dyndns.org:88/">CES-ESERVICE</a>
                        </body>

                        </html>
                """

                sendthai(email,subject,msg)

#-----------------------------------------------------------------------------------------------------------
            flash("Successfully")
            return redirect(url_for('booking.Notifybooking'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()





"""
    @booking.route("/updateroom",methods=["POST"])
    def Updateroom():
        if request.method == "POST":
            id = request.form["id"]
            status = request.form["status"]
            email = request.form["email"]
            try:
                con.connect()
                cur = con.cursor()
                sql = "UPDATE  `tb_user` SET `usr_status` =%s WHERE `usr_id`=%s"
                cur.execute(sql,(status,id))
                con.commit()
                cur.close()

                def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

                	myemail = 'not.reply.ces@gmail.com'
                	mypassword = 'sr3sr4sr5sr6'
                	receiver = sendto

                	msg = MIMEMultipart('alternative')
                	msg['Subject'] = subj
                	msg['From'] = 'IT Support CES'
                	msg['To'] = receiver
                	text = detail

                	part1 = MIMEText(text, 'plain')
                	msg.attach(part1)

                	s = smtplib.SMTP('smtp.gmail.com:587')
                	s.ehlo()
                	s.starttls()

                	s.login(myemail, mypassword)
                	s.sendmail(myemail, receiver.split(','), msg.as_string())
                subject = 'สมาชิกได้รับการอนุมัติ'
                msg = '''เจ้าหน้าที่อนุมัติการสมัครสมาชิกเข้าสู่ระบบแจ้งซ่อมของแผนก IT Support แล้วโดย '''+ ' ' + session ['fname'] +' '+ '''ท่านสามารถเข้าสู่ระบบได้ทาง itsupport.dyndns-web.com:88 '''

                sendthai(email,subject,msg)

                return redirect(url_for('dashboard.Dashboard'))

        """
