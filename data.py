from sqlalchemy import schema, types
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete,join
from passlib.hash import pbkdf2_sha256
from sqlalchemy import *


engine = create_engine('sqlite:///data.db', echo=True)
connection=engine.connect()



#password=pbkdf2_sha256.encrypt("123" , rounds=20000 , salt_size = 16)
#idd=1
#f="Stelios"
#l="Arxo"
#u="admin1"

#password1=pbkdf2_sha256.encrypt("123" , rounds=20000 , salt_size = 16)
#idd1=2
#f1="Manos"
#l1="Fwkas"
#u1="admin2"

#password2=pbkdf2_sha256.encrypt("123" , rounds=20000 , salt_size = 16)
#idd2=3
#f2="Mixalis"
#l2="Koutzos"
#u2="admin3"




with engine.begin() as conn:
#    conn.execute("INSERT INTO admin(adminid,username,firstname,lastname,password) VALUES (?,?, ?, ?, ?)", (idd,u, f, l, password))
#    conn.execute("INSERT INTO admin(adminid,username,firstname,lastname,password) VALUES (?,?, ?, ?, ?)", (idd1,u1, f1, l1, password1))
#    conn.execute("INSERT INTO admin(adminid,username,firstname,lastname,password) VALUES (?,?, ?, ?, ?)", (idd2,u2, f2, l2, password2))
    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (1,1, 1)")
    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (2,1,2)")
    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (3,1, 3)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (4,2, 1)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (5,2,2)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (6,2, 3)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (7,3, 1)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (8,3,2)")
#    conn.execute("INSERT INTO calls(callid,customerid,duration) VALUES (9,3, 3)")




connection.execute()
connection.close()

#import sqlite3 as lite
#con = lite.connect('data.db')
#cur = con.cursor()
#cur.execute('select * from customer')
#users = cur.fetchall()
#print users
