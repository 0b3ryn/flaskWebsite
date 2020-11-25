from flask import Flask
from flask import Flask, render_template, request, url_for
from flask import request
from flask import render_template
import sqlite3 as lite
from sqlalchemy import schema, types
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete,join
from passlib.hash import pbkdf2_sha256
from sqlalchemy import *
from flask import Flask
import sqlite3 as lite
from flask import request
from flask import render_template
from passlib.hash import pbkdf2_sha256
from flask import Flask, session, redirect, url_for, escape, request,g, flash
import os
import re



class Admin:

    app = Flask(__name__)
    app.secret_key = os.urandom(24)


    conn = lite.connect('data.db')
    c = conn.cursor()

    @app.route('/')
    def n1():
        session.pop('client',None)
        session.pop('admin',None)
        session.pop('seller',None)
        return render_template("home.html")

    @app.route('/about')
    def about():
        return render_template("about.html")

    @app.route('/contact')
    def contact():
        return render_template("contact.html")

    @app.route('/program')
    def program():
        conn = lite.connect('data.db')
        conn.row_factory = lite.Row

        cur = conn.cursor()
        cur.execute("select * from program")

        rows = cur.fetchall();

        return render_template("program.html",rows = rows)
        c.close

    @app.route('/loginclient' , methods = ['POST', 'GET'])
    def loginclient():
        session.pop('client',None)
        session.pop('admin',None)
        session.pop('seller',None)
        return render_template("loginclient.html")

    @app.route('/loginclient1' , methods = ['POST', 'GET'])
    def loginclient1():
        error=""
        try:
            session.pop('client',None)
            session.pop('admin',None)
            session.pop('seller',None)
            if request.method == "POST":
                conn = lite.connect('data.db')
                c = conn.cursor()
                usern = request.form['username']
                c.execute("SELECT * FROM customer WHERE username = ?",(usern,))
                data = c.fetchone()[4]
                conn.close()


                if pbkdf2_sha256.verify(request.form['password'], data):
                    session['client'] = request.form['username']
                    return redirect(url_for('cl'))


                else:
                    msg = "Invalid Credentials..."
                    return render_template("check.html",msg = msg)


            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)

        except Exception as e:
            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)

    @app.before_request
    def before_reguest():
        g.client = None
        if 'client' in session:
            g.client = session['client']

        g.admin = None
        if 'admin' in session:
            g.admin = session['admin']

        g.seller = None
        if 'seller' in session:
            g.seller = session['seller']


#________________________________________________________________________________________________


    @app.route('/loginseller' , methods = ['POST', 'GET'])
    def loginseller():
        session.pop('client',None)
        session.pop('admin',None)
        session.pop('seller',None)
        return render_template("loginseller.html")

    @app.route('/loginseller1' , methods = ['POST', 'GET'])
    def loginseller1():
        error=""
        try:
            session.pop('client',None)
            session.pop('admin',None)
            session.pop('seller',None)
            if request.method == "POST":
                conn = lite.connect('data.db')
                c = conn.cursor()
                usern = request.form['username']
                c.execute("SELECT * FROM seller WHERE username = ?",(usern,))
                data1 = c.fetchone()[4]


                if pbkdf2_sha256.verify(request.form['password'], data1):
                    session['seller'] = request.form['username']
                    return redirect(url_for('sel'))

                else:
                    msg = "Invalid Credentials..."
                    return render_template("check.html",msg = msg)


            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)

        except Exception as e:
            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)



#____________________________________________________________________________________________________


    @app.route('/loginadmin' , methods = ['POST', 'GET'])
    def loginadmin():
        session.pop('client',None)
        session.pop('admin',None)
        session.pop('seller',None)
        return render_template("loginadmin.html")

    @app.route('/loginadmin1' , methods = ['POST', 'GET'])
    def loginadmin1():
        try:
            session.pop('client',None)
            session.pop('admin',None)
            session.pop('seller',None)
            if request.method == "POST":
                conn = lite.connect('data.db')
                c = conn.cursor()
                usern = request.form['username']
                c.execute("SELECT * FROM admin WHERE username = ?",(usern,))
                data2 = c.fetchone()[4]


                if pbkdf2_sha256.verify(request.form['password'], data2):
                    session['admin'] = request.form['username']
                    return redirect(url_for('adm'))

                else:
                    msg = "Invalid Credentials..."
                    return render_template("check.html",msg = msg)


            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)

        except Exception as e:
            msg = "Invalid Credentials..."
            return render_template("check.html",msg = msg)



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    @app.route('/admin')
    def adm():
        if g.admin:
            return render_template("admin.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

#____________________________________________________________________________

    @app.route('/adminclient')
    def adminclient():
        if g.admin:
            return render_template("adminclient.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/showclients')
    def showclient():
        if g.admin:
            conn = lite.connect('data.db')
            conn.row_factory = lite.Row

            cur = conn.cursor()
            cur.execute("select * from customer")

            rows = cur.fetchall();
            return render_template("showclient.html",rows = rows)
            c.close
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            conn = lite.connect('data.db')
            conn.row_factory = lite.Row

            cur = conn.cursor()
            cur.execute("select * from customer")

            rows = cur.fetchall();
            return render_template("showclient.html",rows = rows)
            c.close
        return redirect(url_for('n1'))

    @app.route('/addclient')
    def addclient():
        if g.admin:
            return render_template("addclient.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            return render_template("addclient.html")
        return redirect(url_for('n1'))



    @app.route('/removeclient')
    def removeclient():
        if g.admin:
            return render_template("removeclient.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            return render_template("removeclient.html")
        return redirect(url_for('n1'))



    @app.route('/addcl',methods = ['POST', 'GET'])
    def addcl():
        if g.admin or g.seller:
            if request.method == 'POST':
                try:
                    idd = request.form['cid']
                    uname = request.form['uname']
                    firstname = request.form['firstname']
                    firstname = str(firstname)
                    lastname = request.form['lastname']
                    lastname = str(lastname)
                    number = request.form['number']
                    number = int(number)
                    password = request.form['password']
                    if (password == "" or uname == "" or idd == "" or firstname == "" or lastname == "" or number==""):
                        raise ValueError
                    if (re.match("^[A-Za-z]*$", firstname) and re.match("^[A-Za-z]*$", lastname)  and number>1000000000 and number<9999999999):
                        password=pbkdf2_sha256.encrypt(password , rounds=20000 , salt_size = 16)
                        pid = request.form['pid']
                        pid = int(pid)
                        conn = lite.connect('data.db')
                        c = conn.cursor()
                        c.execute('SELECT COUNT(*) FROM customer WHERE username=?', (uname,))
                        d = c.fetchone()[0]
                        c.execute('SELECT COUNT(*) FROM program WHERE programid=?', (pid,))
                        d1 = c.fetchone()[0]
                        if (d==1):
                            msg = "Username already exists!"
                        if (d1!=1):
                            msg ="There is no such program!"
                        else:
                            c.execute("INSERT INTO customer(customerid,username,firstname,lastname,password,number,programid) VALUES (?, ?,?, ?, ?, ?,?)", (idd,uname, firstname, lastname, password ,number,pid))
                            conn.commit()
                            msg = "Client successfully added!"
                        return render_template("result.html",msg = msg)
                    else:
                        raise ValueError
                except:
                    msg = "Error during insertion..."
                    return render_template("result.html",msg = msg)
            else:
                msg = "Error during insertion..."
                return render_template("result.html",msg = msg)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        return redirect(url_for('n1'))

    @app.route('/recl',methods = ['POST', 'GET'])
    def recl():
        if g.admin or g.seller:
            if request.method == 'POST':
                try:
                    iddd = request.form['id2']

                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT COUNT(*) FROM customer WHERE customerid=?', (iddd,))
                    d = c.fetchone()[0]
                    if (d==1):
                        c.execute('DELETE FROM customer WHERE customerid=?', (iddd,))
                        conn.commit()
                        msg2 = "Client successfully removed!"
                    else:
                        msg2 = "Error during deletion..."
                    return render_template("result2.html",msg2 = msg2)
                except:
                    msg2 = "Error during deletion..."
                    return render_template("result2.html",msg2 = msg2)
            else:
                msg2 = "Error during deletion..."
                return render_template("result2.html",msg2 = msg2)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        return redirect(url_for('n1'))




#___________________________________________________________________________________

    @app.route('/adminseller')
    def adminseller():
        if g.admin:
            return render_template("adminseller.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/showsellers')
    def showsellers():
        if g.admin:
            conn = lite.connect('data.db')
            conn.row_factory = lite.Row

            cur = conn.cursor()
            cur.execute("select * from seller")

            rows = cur.fetchall();
            return render_template("showsellers.html",rows = rows)
            c.close
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/addseller')
    def addseller():
        if g.admin:
            return render_template("addseller.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/addse',methods = ['POST', 'GET'])
    def addse():
        if g.admin:
            if request.method == 'POST':
                try:
                    idd = request.form['sid']
                    uname = request.form['uname']
                    firstname = request.form['firstname']
                    firstname = str(firstname)
                    lastname = request.form['lastname']
                    lastname = str(lastname)
                    password = request.form['password']
                    if (password == "" or uname == "" or idd == "" or firstname == "" or lastname == ""):
                        raise ValueError
                    if (re.match("^[A-Za-z]*$", firstname) and re.match("^[A-Za-z]*$", lastname)):
                        password=pbkdf2_sha256.encrypt(password , rounds=20000 , salt_size = 16)
                        conn = lite.connect('data.db')
                        c = conn.cursor()
                        c.execute('SELECT COUNT(*) FROM seller WHERE username=?', (uname,))
                        d = c.fetchone()[0]
                        if (d==1):
                            msg = "Username already exists!"
                        else:
                            c.execute("INSERT INTO seller(sellerid,username,firstname,lastname,password) VALUES (?,?, ?, ?, ?)", (idd,uname, firstname, lastname, password))
                            conn.commit()
                            msg = "Seller successfully added!"
                        return render_template("result.html",msg = msg)
                    else:
                        raise ValueError
                except:
                    msg = "Error during insertion..."
                    return render_template("result.html",msg = msg)
            else:
                msg = "Error during insertion..."
                return render_template("result.html",msg = msg)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))


    @app.route('/removeseller')
    def removeseller():
        if g.admin:
            return render_template("removeseller.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/rese',methods = ['POST', 'GET'])
    def rese():
        if g.admin:
            if request.method == 'POST':
                try:
                    iddd = request.form['id2']

                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT COUNT(*) FROM seller WHERE sellerid=?', (iddd,))
                    d = c.fetchone()[0]
                    if (d==1):
                        c.execute('DELETE FROM seller WHERE sellerid=?', (iddd,))
                        conn.commit()
                        msg2 = "Seller successfully removed!"
                    else:
                        msg2 = "Error during deletion!"
                    return render_template("result2.html",msg2 = msg2)
                except:
                    msg2 = "Error during deletion..."
                    return render_template("result2.html",msg2 = msg2)
            else:
                msg2 = "Error during deletion..."
                return render_template("result2.html",msg2 = msg2)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))




#_________________________________________________________________________________


    @app.route('/adminprogram')
    def adminprogram():
        if g.admin:
            return render_template("adminprogram.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))


    @app.route('/add')
    def add():
        if g.admin:
            return render_template("add.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/addrec',methods = ['POST', 'GET'])
    def addrec():
        if g.admin:
            if request.method == 'POST':
                try:
                    idd = request.form['id']
                    name = request.form['name']
                    cpc = request.form['cpc']
                    cpc = int(cpc)
                    if (name == "" or cpc == ""  or idd == ""):
                        raise ValueError

                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT COUNT(*) FROM program WHERE programname=?', (name,))
                    d = c.fetchone()[0]
                    if (d==1):
                        msg = "There is already a program with that name!"
                    else:
                        c.execute("INSERT INTO program(programid,programname,costpercall) VALUES (?, ?, ?)", (idd, name,cpc))
                        conn.commit()
                        msg = "Program successfully added!"
                    return render_template("result.html",msg = msg)
                except:
                    msg = "Error during insertion..."
                    return render_template("result.html",msg = msg)
            else:
                msg = "Error during insertion..."
                return render_template("result.html",msg = msg)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))
    @app.route('/addrecc',methods = ['POST', 'GET'])
    def addrecc():
        if g.admin:
            if request.method == 'POST':
                try:
                    iddd = request.form['id2']

                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT COUNT(*) FROM program WHERE programid=?', (iddd,))
                    d = c.fetchone()[0]
                    if (d==1):
                        c.execute('DELETE FROM program WHERE programid=?', (iddd,))
                        conn.commit()
                        msg2 = "Program succesfully deleted!"
                    else:
                        msg2 = "Error during deletion..."
                    return render_template("result2.html",msg2 = msg2)
                except:
                    msg2 = "Error during deletion..."
                    return render_template("result2.html",msg2 = msg2)
            else:
                msg2 = "Error during deletion..."
                return render_template("result2.html",msg2 = msg2)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))





    @app.route('/remove')
    def remove():
        if g.admin:
            return render_template("remove.html")
        return redirect(url_for('n1'))
    @app.route('/show')
    def show():
        if g.admin:
            conn = lite.connect('data.db')
            conn.row_factory = lite.Row

            cur = conn.cursor()
            cur.execute("select * from program")

            rows = cur.fetchall();
            return render_template("show.html",rows = rows)
            c.close
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    @app.route('/seller')
    def sel():
        if g.seller:
            return render_template("seller.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        return redirect(url_for('n1'))
#_____________________________________________________________

    @app.route('/billcheck')
    def billcheck():
        if g.seller:
            return render_template("billcheck.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        return redirect(url_for('n1'))


    @app.route('/billch',methods = ['POST', 'GET'])
    def billch():
        if g.seller:
            if request.method == 'POST':
                try:
                    idd = request.form['id']
                    idd = int(idd)
                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT COUNT(*) FROM customer WHERE customerid=?', (idd,))
                    a = c.fetchone()[0]
                    if (a==1):
                        c.execute('SELECT COUNT(*) FROM calls WHERE customerid=?', (idd,))
                        calls = c.fetchone()[0]
                        c.execute('SELECT programid FROM customer WHERE customerid=?', (idd,))
                        prog = c.fetchone()[0]
                        c.execute('SELECT costpercall FROM program WHERE programid=?', (prog,))
                        cost = c.fetchone()[0]
                        bill = cost*calls
                        msg1 = "This client need to pay"
                        msg2 = "euro(s)!"
                        return render_template("billresult.html",msg1 = msg1,bill=bill,msg2=msg2)
                    else:
                        msg = "There is no such client!"
                        return render_template("result.html",msg = msg)
                except:
                    msg = "Error!"
                    return render_template("result.html",msg = msg)
            else:
                msg = "Error"
                return render_template("result.html",msg = msg)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        return redirect(url_for('n1'))
#_____________________________________________________________________________

    @app.route('/changeprogram',methods = ['POST', 'GET'])
    def changeprogramm():
        if g.seller:
            return render_template("chprog.html")
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        return redirect(url_for('n1'))


    @app.route('/proch',methods = ['POST', 'GET'])
    def proch():
        if g.seller:
            if request.method == 'POST':
                try:
                    conn = lite.connect('data.db')
                    c = conn.cursor()
                    idd = request.form['id']
                    idd = int(idd)
                    prid = request.form['prid']
                    prid = int(prid)
                    if (idd == "" or prid == ""):
                        raise ValueError
                    c.execute('SELECT COUNT(*) FROM program WHERE programid=?', (prid,))
                    d1 = c.fetchone()[0]
                    c.execute('SELECT COUNT(*) FROM customer WHERE customerid=?', (idd,))
                    d = c.fetchone()[0]
                    if (d1!=1):
                        msg ="There is no such program!"
                    elif (d!=1):
                        msg ="There is no such client!"
                    else:
                        c.execute("UPDATE customer SET programid=? WHERE customerid=?", (prid, idd))
                        conn.commit()
                        msg = "Database updated"
                    return render_template("result.html",msg = msg)
                except:
                    msg2 = "Error during the update!"
                    return render_template("result2.html",msg2 = msg2)
        if g.client:
            flash("")
            return redirect(url_for('cl'))
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        return redirect(url_for('n1'))




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @app.route('/client')
    def cl():
        if g.client:
            return render_template("client.html")
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))

        return redirect(url_for('n1'))



    @app.route('/billcheckcl')
    def billcheckcl():
        if g.client:
            try:
                conn = lite.connect('data.db')
                c = conn.cursor()
                c.execute("SELECT customerid FROM customer WHERE username = ?",(g.client,))
                clientid = c.fetchone()[0]
                c.execute('SELECT COUNT(*) FROM calls WHERE customerid=?', (clientid,))
                calls = c.fetchone()[0]
                c.execute('SELECT programid FROM customer WHERE customerid=?', (clientid,))
                prog = c.fetchone()[0]
                c.execute('SELECT costpercall FROM program WHERE programid=?', (prog,))
                cost = c.fetchone()[0]
                bill = cost*calls
                msg1 = "You need to pay"
                msg2 = "euro(s)!"
                return render_template("billpay.html",msg1 = msg1,bill=bill,msg2=msg2)
            except:
                msg = "Error!"
                return render_template("result.html",msg = msg)
        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))

    @app.route('/billpay' ,methods = ['POST', 'GET'])
    def billpay():
        if g.client:
            if request.method == 'POST':
                try:
                    number = request.form['number']
                    number = int(number)
                    expm = request.form['expm']
                    expm = int(expm)
                    expy = request.form['expy']
                    expy = int(expy)
                    code = request.form['code']
                    code = int(code)
                    if (len(str(number))==16 and expm>0 and expm<13 and expy>2015 and expy<3000 and len(str(code))==3 ):
                        msg = "Your bill has been payed. Thank you!"
                        conn = lite.connect('data.db')
                        c = conn.cursor()
                        c.execute("SELECT customerid FROM customer WHERE username = ?",(g.client,))
                        clientid = c.fetchone()[0]
                        c.execute('DELETE FROM calls WHERE customerid=?', (clientid,))
                        conn.commit()
                        return render_template("result.html",msg = msg)
                    else:
                        msg = "Invalid Credentials!"
                        return render_template("result.html",msg = msg)
                except:
                    msg = "Error!"
                    return render_template("result.html",msg = msg)
            else:
                msg = "Error!"
                return render_template("result.html",msg = msg)




            if g.admin:
                flash("")
                return redirect(url_for('adm'))
            if g.seller:
                flash("")
                return redirect(url_for('sel'))
            return redirect(url_for('n1'))


    @app.route('/callhistory')
    def callhistory():
        if g.client:
            try:
                conn = lite.connect('data.db')
                conn.row_factory = lite.Row
                cur = conn.cursor()
                cur.execute("SELECT customerid FROM customer WHERE username = ?",(g.client,))
                clientid = cur.fetchone()[0]
                cur.execute("SELECT * FROM calls WHERE customerid = ?",(clientid,))
                rows = cur.fetchall();
                return render_template("showcalls.html",rows = rows)
                c.close
            except:
                msg = "Error!"
                return render_template("result.html",msg = msg)

        if g.admin:
            flash("")
            return redirect(url_for('adm'))
        if g.seller:
            flash("")
            return redirect(url_for('sel'))
        return redirect(url_for('n1'))


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    if __name__ == "__main__":
            app.run(debug=True)
