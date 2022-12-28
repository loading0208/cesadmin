from flask import Flask,render_template,session,redirect,send_from_directory,request,url_for,Blueprint,jsonify
import os
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
conn = pymysql.connect(HOSTpost,USERpost,PASSpost,DATABASEpost)
###########################################################



api = Blueprint('api',__name__)

@api.route("/api/apigoods",methods=["POST","GET"])
def API():
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT id_goods,purchase_date,po_no,type_goods,brand,s_n,it_code,user_use,department,link_po FROM dbgoods ORDER BY id_goods DESC"
        cur.execute(sql)
        goods = cur.fetchall()
        mydata = []
        for i in range(len(goods)):
            task = {
            'id':i,
            'id_goods':goods[i][0],
            'purchase_date':goods[i][1],
            'po_no':goods[i][2],
            'type_goods':goods[i][3],
            'brand':goods[i][4],
            's_n':goods[i][5],
            'it_code':goods[i][6],
            'user_use':goods[i][7],
            'department':goods[i][8],
            'link_po':goods[i][9],
            }
            mydata.append(task)
        return jsonify(mydata),201,{'Content-Type': "application/json"}
    except Exception as e:
        print (e)
    finally:
        cur.close()
        con.close()
