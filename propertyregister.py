from flask import Flask,render_template,session,redirect,send_from_directory,request,url_for,Blueprint,flash
import os
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from flask_paginate import Pagination,get_page_args #แบ่งหน้าข้อมูล
###########################################################
import noti
###########################################################
from datetime import datetime
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)
###########################################################


propertyregister = Blueprint('propertyregister',__name__)
@propertyregister.route("/goods")
def Goods():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM dbgoods ORDER BY id_goods DESC"
        cur.execute(sql)
        propertyregister = cur.fetchall()
        return render_template('goods.html',part="goods",propertyregister=propertyregister,month=month,employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()

@propertyregister.route("/addgoods")
def Addgoods():
    if "username" not in session:
        return render_template("/login.html")
    now = datetime.today()
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_contact"
        cur.execute(sql)
        useruse = cur.fetchall()
        sql = "SELECT * FROM category"
        cur.execute(sql)
        category = cur.fetchall()
        sql = "SELECT * FROM db_department"
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template('addgoods.html',category = category, useruse=useruse,dep=dep, now=now.strftime("%d/%m/%Y %H:%M"))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@propertyregister.route("/signature")
def Signature():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("/signature.html")



@propertyregister.route("/category")
def Category():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM category"
        cur.execute(sql)
        category = cur.fetchall()
        return render_template('category.html',category = category)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()

@propertyregister.route("/addcategory", methods=[ "POST"])
def Addcategory():
    category = request.form["category"]
    date = request.form["date"]
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into category (category,date) values(%s,%s)"
        cur.execute(sql,(category,date))
        con.commit()
        return redirect(url_for('propertyregister.Category'))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()

@propertyregister.route("/borrow",methods=["POST"])
def Borrow():
    if request.method =="POST":
        id = request.form["id"]
        now = datetime.today()
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE id_goods=%s"
            cur.execute(sql,(id))
            datas = cur.fetchall()
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
            #-----ดึงประเภทมาโชว์
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_contact"
            cur.execute(sql)
            useruse = cur.fetchall()
            sql = "SELECT * FROM category"
            cur.execute(sql)
            category = cur.fetchall()
            sql = "SELECT * FROM db_department"
            cur.execute(sql)
            dep = cur.fetchall()
            return render_template('addborrow.html',datas = datas,category=category,useruse=useruse,dep=dep,now=now.strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@propertyregister.route("/borrowlist")
def Borrowlist():
    if "username" not in session:
        return render_template("/login.html")
    now = datetime.today()
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM borrow_db ORDER BY id_borrow DESC"
        cur.execute(sql)
        borrowlist = cur.fetchall()

        return render_template('borrow.html',part="borrowlist",borrowlist = borrowlist,now=now.strftime("%d/%m/%Y %H:%M"),month=month,employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()



@propertyregister.route("/addborrow", methods=["POST"])
def Addborrow():
    id = request.form["id"]
    useruse = request.form["useruse"]
    depborrow = request.form["depborrow"]
    type = request.form["type"]
    brand = request.form["brand"]
    serialnumber = request.form["serialnumber"]
    itcode = request.form["itcode"]
    note = request.form["note"]
    noteit = request.form["noteit"]
    canvassignature = request.form["canvassignature"]
    itadd = request.form["itadd"]
    dateborrow = request.form["dateborrow"]
    idgoods = request.form["idgoods"]
    st = request.form["st"]
    if st == "0":
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE dbgoods SET status_goods=%s,user_use=%s,department=%s,note=%s WHERE id_goods=%s"
            cur.execute(sql,(st,useruse,depborrow,noteit,id))
            con.commit()
            cur.close()
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into borrow_db (name_borrow,dep_borrow,type_borrow,brand_borrow,sn_boorow,itcode_boorow,note_borrow,it_borrow,date_borrow,idgoods,signature) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(useruse,depborrow,type,brand,serialnumber,itcode,note,itadd,dateborrow,idgoods,canvassignature))
        con.commit()
        return redirect(url_for('propertyregister.Goods'))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@propertyregister.route("/returngoods", methods=["POST"])
def Returngoods():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM borrow_db WHERE id_borrow = %s"
            cur.execute(sql,(id))
            returngoods = cur.fetchall()
            return render_template("returngoods.html",returngoods=returngoods)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@propertyregister.route("/return", methods=["POST"])
def Return():
    id = request.form["id"]
    idgoods = request.form["idgoods"]
    canvassignature = request.form["canvassignature"]
    returnborrow = request.form["returnborrow"]
    returngoods = request.form["returngoods"]
    itreturn = request.form["itreturn"]
    datereturn = datetime.today()
    datereturn=datereturn.strftime("%d/%m/%Y %H:%M")
    if returnborrow == "0":
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE dbgoods SET status_goods=%s WHERE id_goods=%s"
            cur.execute(sql,(returngoods,idgoods))
            con.commit()
            cur.close()
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
    try:
        con.connect()
        cur = con.cursor()
        sql = "UPDATE borrow_db SET status_borrow=%s,it_return=%s,signature_return=%s,date_return=%s WHERE id_borrow=%s"
        cur.execute(sql,(returnborrow,itreturn,canvassignature,datereturn,id))
        con.commit()
        cur.close()
        return redirect(url_for("propertyregister.Borrowlist"))
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()




@propertyregister.route("/borrowing",methods=["POST"])
def Borrowing():
    if request.method =="POST":
        id = request.form["id"]
        now = datetime.today()
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM borrow_db WHERE id_borrow=%s"
            cur.execute(sql,(id))
            datas = cur.fetchall()
            return render_template('borrowing.html',datas = datas,now=now.strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@propertyregister.route("/deletecategory",methods=["POST"])
def Deletecategory():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from category where id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for("propertyregister.Category"))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@propertyregister.route("/deletegoods",methods=["POST"])
def Deletegoods():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from dbgoods where id_goods = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for("propertyregister.Goods"))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@propertyregister.route("/showcategory")
def Showcategory():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM category"
        cur.execute(sql)
        category = cur.fetchall()
        return render_template('category.html',category = category)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@propertyregister.route("/addgoodsf",methods=["POST"])
def Addgoodsf():
    if request.method =="POST":
        # Save img ---------------------------------------------------------------------
        file = request.files['file']
        upload_folder = 'static/imggoods'
        app_folder = os.path.dirname(__file__)
        img_folder = os.path.join(app_folder,upload_folder)
        try: ## เลือกรูป
            file.save(os.path.join(img_folder,file.filename))
            path = upload_folder + "/" + file.filename
        except:## ไม่เลือก รูป
            path = ""
        purchase_date = request.form["purchase_date"]
        po_no =request.form["po_no"]
        price = request.form["price"]
        typegoods = request.form["typegoods"]
        brand = request.form["brand"]
        serialnumber = request.form["serialnumber"]
        #----check SN
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE s_n = %s "
            cur.execute(sql,(serialnumber))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("มีการบันทึก Serial Number นี้แล้ว")
                return redirect(url_for('propertyregister.Addgoods'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #----END----------------------------------------------------
        itcode = request.form["itcode"]
        #--- check ทะเบียนทรัพย์สิน IT
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE it_code = %s "
            cur.execute(sql,(itcode))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("ทะเบียนทรัพย์สินถูกใช้งานแล้ว")
                return redirect(url_for('propertyregister.Addgoods'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #----END----------------------------------------------------
        useruse = request.form["useruse"]
        department = request.form["department"]
        note = request.form["note"]
        itadmin = request.form["itadmin"]
        statusgoods = request.form["statusgoods"]
        status = request.form["status"]
        linkpo = request.form['linkpo']
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into dbgoods (purchase_date,po_no,price,type_goods,brand,s_n,it_code,user_use,department,note,pic_goods,itadmin,status,status_goods,link_po) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(purchase_date,po_no,price,typegoods,brand,serialnumber,itcode,useruse,department,note,path,itadmin,statusgoods,status,linkpo))
            con.commit()
            return redirect(url_for('propertyregister.Goods'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()

@propertyregister.route("/coppy",methods=["POST"])
def Coppy():
    if request.method =="POST":
        id = request.form["id"]
        now = datetime.today()
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE id_goods=%s"
            cur.execute(sql,(id))
            datas = cur.fetchall()

            #-----ดึงประเภทมาโชว์

            sql = "SELECT * FROM category"
            cur.execute(sql)
            category = cur.fetchall()

            sql = "SELECT * FROM db_department "
            cur.execute(sql)
            dep = cur.fetchall()

            sql = "SELECT * FROM db_contact"
            cur.execute(sql)
            useruse = cur.fetchall()

            return render_template('coppygoods.html',datas = datas,category=category,now=now.strftime("%d/%m/%Y %H:%M"),dep=dep,useruse=useruse)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()




@propertyregister.route("/detail",methods=["POST"])
def Detail():
    if request.method =="POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE id_goods=%s"
            cur.execute(sql,(id))
            datas = cur.fetchall()
            return render_template('Detailgoods.html',datas = datas)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@propertyregister.route("/detailgoods")
def Detailgoods():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("/detailgoods.html")


@propertyregister.route("/goodedit",methods=["POST"])
def Goodedit():
    if request.method == "POST":
        id = request.form["id"]
        useruse = request.form["useruse"]
        department =request.form["department"]
        note = request.form["note"]
        statusgoods = request.form["statusgoods"]
        itupdate = request.form["itupdate"]
        lastupdate = request.form["lastupdate"]
        status = request.form["status"]
        linkpo = request.form['linkpo']
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE dbgoods SET user_use=%s,department=%s,note=%s,status=%s,itupdate=%s,last_update=%s,status_goods=%s,link_po=%s WHERE id_goods=%s"
            cur.execute(sql,(useruse,department,note,statusgoods,itupdate,lastupdate,status,linkpo,id))
            con.commit()
            cur.close()
            return redirect(url_for('propertyregister.Goods'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()




@propertyregister.route("/editgoods",methods=["POST"])
def Editgoods():
    if request.method =="POST":
        id = request.form["id"]
        now = datetime.today()
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM dbgoods WHERE id_goods=%s"
            cur.execute(sql,(id))
            datas = cur.fetchall()

            #-----ดึงประเภทมาโชว์

            sql = "SELECT * FROM category"
            cur.execute(sql)
            category = cur.fetchall()

            sql = "SELECT * FROM db_department "
            cur.execute(sql)
            dep = cur.fetchall()
            return render_template('editgoods.html',datas = datas,category=category,now=now.strftime("%d/%m/%Y %H:%M"),dep=dep)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@propertyregister.route("/dashboardgoods")
def Dashboardgoods():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'QA/QC' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        qaqcAccessory = cur.fetchall()
###-------------------------------------------------------QA/QC--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Engineering' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        EngineeringAccessory = cur.fetchall()
###-------------------------------------------------------Engineering--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Business Development' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bdAccessory = cur.fetchall()
###-------------------------------------------------------Business Development--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinancePrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Finance' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        FinanceAccessory = cur.fetchall()
##------------------------------------------------------Financet--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Grounp manager' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gmAccessory = cur.fetchall()
##------------------------------------------------------Grounp manager--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Human Resources' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        hrAccessory = cur.fetchall()
##------------------------------------------------------Human Resources--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSENotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSEComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSEMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSEPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSEWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSETV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSETelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSECamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        HSEAccessory = cur.fetchall()
##------------------------------------------------------HSE--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Scaffolding&painting' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        sfpAccessory = cur.fetchall()
##------------------------------------------------------Scaffolding&painting--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'HSE' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'MSR' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        MSRAccessory = cur.fetchall()
##----------------------------------------------------MSR--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Febrication' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        fbAccessory = cur.fetchall()
##----------------------------------------------------Febrication--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Logistic & Transportation' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        ltAccessory = cur.fetchall()
##----------------------------------------------------Logistic & Transportation--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        mePrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'Manintenance/Equipment' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        meAccessory = cur.fetchall()
##----------------------------------------------------Manintenance/Equipment--------------------------------------------------------------###
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'CES-BKK' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        bkkAccessory = cur.fetchall()
##----------------------------------------------------CES-BKK--------------------------------------------------------------###

        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itNotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE department = 'IT Support' AND type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        itAccessory = cur.fetchall()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Notebook' "
        cur.execute(sql)
        notebook = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Notebook' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gnotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Notebook' and status = 'รอซ่อม' "
        cur.execute(sql)
        wnotebook = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Notebook' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dnotebook = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Computer PC' "
        cur.execute(sql)
        ComputerPC = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Computer PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Computer PC' and status = 'รอซ่อม' "
        cur.execute(sql)
        wComputerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Computer PC' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dComputerPC = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Monitor' "
        cur.execute(sql)
        Monitor = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Monitor' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Monitor' and status = 'รอซ่อม' "
        cur.execute(sql)
        wMonitor = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Monitor' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dMonitor = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Printer' "
        cur.execute(sql)
        Printer = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Printer' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Printer' and status = 'รอซ่อม' "
        cur.execute(sql)
        wPrinter = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Printer' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dPrinter = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Server PC' "
        cur.execute(sql)
        ServerPC = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Server PC' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gServerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Server PC' and status = 'รอซ่อม' "
        cur.execute(sql)
        wServerPC = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Server PC' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dServerPC = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Projector' "
        cur.execute(sql)
        Projector = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Projector' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gProjector = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Projector' and status = 'รอซ่อม' "
        cur.execute(sql)
        wProjector = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Projector' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dProjector = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'WalkieTalkie' "
        cur.execute(sql)
        WalkieTalkie = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'WalkieTalkie' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'WalkieTalkie' and status = 'รอซ่อม' "
        cur.execute(sql)
        wWalkieTalkie = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'WalkieTalkie' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dWalkieTalkie = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'TV' "
        cur.execute(sql)
        TV = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'TV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'TV' and status = 'รอซ่อม' "
        cur.execute(sql)
        wTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'TV' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dTV = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Telephone' "
        cur.execute(sql)
        Telephone = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Telephone' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Telephone' and status = 'รอซ่อม' "
        cur.execute(sql)
        wTelephone = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Telephone' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dTelephone = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Camera' "
        cur.execute(sql)
        Camera = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Camera' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Camera' and status = 'รอซ่อม' "
        cur.execute(sql)
        wCamera = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Camera' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dCamera = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Accessory' "
        cur.execute(sql)
        Accessory = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Accessory' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gAccessory = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Accessory' and status = 'รอซ่อม' "
        cur.execute(sql)
        wAccessory = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Accessory' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dAccessory = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'CCTV' "
        cur.execute(sql)
        CCTV = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'CCTV' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gCCTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'CCTV' and status = 'รอซ่อม' "
        cur.execute(sql)
        wCCTV = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'CCTV' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dCCTV = cur.fetchall()

        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Network' "
        cur.execute(sql)
        Network = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Network' and status = 'ใช้งานได้' "
        cur.execute(sql)
        gNetwork = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Network' and status = 'รอซ่อม' "
        cur.execute(sql)
        wNetwork = cur.fetchall()
        sql = "SELECT * FROM dbgoods WHERE type_goods = 'Network' and status = 'เสีย/จำหน่าย' "
        cur.execute(sql)
        dNetwork = cur.fetchall()
        data = [0,0,0,0]
        chart_data = data
        return render_template('dashboardgoods.html',part ="dashboardgoods",Notebook=len(notebook),ComputerPC=len(ComputerPC),Monitor=len(Monitor),Printer=len(Printer),ServerPC=len(ServerPC),Projector=len(Projector),WalkieTalkie=len(WalkieTalkie),TV=len(TV),Telephone=len(Telephone),Camera=len(Camera),Accessory=len(Accessory),CCTV=len(CCTV),Network=len(Network),
                                                    chart_data=chart_data,gnotebook=len(gnotebook),wnotebook=len(wnotebook),dnotebook=len(dnotebook),gComputerPC=len(gComputerPC),wComputerPC=len(wComputerPC),dComputerPC=len(dComputerPC),gMonitor=len(gMonitor),wMonitor=len(wMonitor),dMonitor=len(dMonitor),gPrinter=len(gPrinter),wPrinter=len(wPrinter),dPrinter=len(dPrinter),
                                                    gServerPC=len(gServerPC),wServerPC=len(wServerPC),dServerPC=len(dServerPC),gProjector=len(gProjector),wProjector=len(wProjector),dProjector=len(dProjector),gWalkieTalkie=len(gWalkieTalkie),wWalkieTalkie=len(wWalkieTalkie),dWalkieTalkie=len(dWalkieTalkie),gTV=len(gTV),wTV=len(wTV),dTV=len(dTV),gTelephone=len(gTelephone),wTelephone=len(wTelephone),dTelephone=len(dTelephone),
                                                    gCamera=len(gCamera),wCamera=len(wCamera),dCamera=len(dCamera),gAccessory=len(gAccessory),wAccessory=len(wAccessory),dAccessory=len(dAccessory),gCCTV=len(gCCTV),wCCTV=len(wCCTV),dCCTV=len(dCCTV),gNetwork=len(gNetwork),wNetwork=len(wNetwork),dNetwork=len(dNetwork),
                                                    qaqcNotebook=len(qaqcNotebook),qaqcComputerPC=len(qaqcComputerPC),qaqcMonitor=len(qaqcMonitor),qaqcPrinter=len(qaqcPrinter),qaqcWalkieTalkie=len(qaqcWalkieTalkie),qaqcTV=len(qaqcTV),qaqcTelephone=len(qaqcTelephone),qaqcCamera=len(qaqcCamera),qaqcAccessory=len(qaqcAccessory),EngineeringNotebook=len(EngineeringNotebook),EngineeringComputerPC=len(EngineeringComputerPC),EngineeringMonitor=len(EngineeringMonitor),
                                                    EngineeringPrinter=len(EngineeringPrinter),EngineeringWalkieTalkie=len(EngineeringWalkieTalkie),EngineeringTV=len(EngineeringTV),EngineeringTelephone=len(EngineeringTelephone),EngineeringCamera=len(EngineeringCamera),EngineeringAccessory=len(EngineeringAccessory),
                                                    bdNotebook=len(bdNotebook),bdComputerPC=len(bdComputerPC),bdMonitor=len(bdMonitor),bdPrinter=len(bdPrinter),bdWalkieTalkie=len(bdWalkieTalkie),bdTV=len(bdTV),bdTelephone=len(bdTelephone),bdCamera=len(bdCamera),bdAccessory=len(bdAccessory),
                                                    FinanceNotebook=len(FinanceNotebook),FinanceComputerPC=len(FinanceComputerPC),FinanceMonitor=len(FinanceMonitor),FinancePrinter=len(FinancePrinter),FinanceWalkieTalkie=len(FinanceWalkieTalkie),FinanceTV=len(FinanceTV),FinanceTelephone=len(FinanceTelephone),FinanceCamera=len(FinanceCamera),FinanceAccessory=len(FinanceAccessory),
                                                    gmNotebook=len(gmNotebook),gmComputerPC=len(gmComputerPC),gmMonitor=len(gmMonitor),gmPrinter=len(gmPrinter),gmWalkieTalkie=len(gmWalkieTalkie),gmTV=len(gmTV),gmTelephone=len(gmTelephone),gmCamera=len(gmCamera),gmAccessory=len(gmAccessory),
                                                    hrNotebook=len(hrNotebook),hrComputerPC=len(hrComputerPC),hrMonitor=len(hrMonitor),hrPrinter=len(hrPrinter),hrWalkieTalkie=len(hrWalkieTalkie),hrTV=len(hrTV),hrTelephone=len(hrTelephone),hrCamera=len(hrCamera),hrAccessory=len(hrAccessory),
                                                    HSENotebook=len(HSENotebook),HSEComputerPC=len(HSEComputerPC),HSEMonitor=len(HSEMonitor),HSEPrinter=len(HSEPrinter),HSEWalkieTalkie=len(HSEWalkieTalkie),HSETV=len(HSETV),HSETelephone=len(HSETelephone),HSECamera=len(HSECamera),HSEAccessory=len(HSEAccessory),
                                                    sfpNotebook=len(sfpNotebook),sfpComputerPC=len(sfpComputerPC),sfpMonitor=len(sfpMonitor),sfpPrinter=len(sfpPrinter),sfpWalkieTalkie=len(sfpWalkieTalkie),sfpTV=len(sfpTV),sfpTelephone=len(sfpTelephone),sfpCamera=len(sfpCamera),sfpAccessory=len(sfpAccessory),
                                                    MSRNotebook=len(MSRNotebook),MSRComputerPC=len(MSRComputerPC),MSRMonitor=len(MSRMonitor),MSRPrinter=len(MSRPrinter),MSRWalkieTalkie=len(MSRWalkieTalkie),MSRTV=len(MSRTV),MSRTelephone=len(MSRTelephone),MSRCamera=len(MSRCamera),MSRAccessory=len(MSRAccessory),
                                                    fbNotebook=len(fbNotebook),fbComputerPC=len(fbComputerPC),fbMonitor=len(fbMonitor),fbPrinter=len(fbPrinter),fbWalkieTalkie=len(fbWalkieTalkie),fbTV=len(fbTV),fbTelephone=len(fbTelephone),fbCamera=len(fbCamera),fbAccessory=len(fbAccessory),
                                                    ltNotebook=len(ltNotebook),ltComputerPC=len(ltComputerPC),ltMonitor=len(ltMonitor),ltPrinter=len(ltPrinter),ltWalkieTalkie=len(ltWalkieTalkie),ltTV=len(fbTV),ltTelephone=len(ltTelephone),ltCamera=len(ltCamera),ltAccessory=len(ltAccessory),
                                                    meNotebook=len(meNotebook),meComputerPC=len(meComputerPC),meMonitor=len(meMonitor),mePrinter=len(mePrinter),meWalkieTalkie=len(meWalkieTalkie),meTV=len(meTV),meTelephone=len(meTelephone),meCamera=len(meCamera),meAccessory=len(meAccessory),
                                                    bkkNotebook=len(bkkNotebook),bkkComputerPC=len(bkkComputerPC),bkkMonitor=len(bkkMonitor),bkkPrinter=len(bkkPrinter),bkkWalkieTalkie=len(bkkWalkieTalkie),bkkTV=len(bkkTV),bkkTelephone=len(bkkTelephone),bkkCamera=len(bkkCamera),bkkAccessory=len(bkkAccessory),
                                                    itNotebook=len(itNotebook),itComputerPC=len(itComputerPC),itMonitor=len(itMonitor),itPrinter=len(itPrinter),itWalkieTalkie=len(itWalkieTalkie),itTV=len(itTV),itTelephone=len(itTelephone),itCamera=len(itCamera),itAccessory=len(itAccessory),
                                                    month=month,employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()
