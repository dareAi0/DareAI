
import os
import sqlite3
from flask import request

def sql_injection():
    uid = request.args.get('id')
    q = "SELECT * FROM users WHERE id = '" + uid + "'"
    sqlite3.connect("db.sqlite").execute(q)

def xss_issue():
    name = request.args.get("name")
    return "<h1>" + name + "</h1>"

def command_injection():
    cmd = request.args.get("cmd")
    os.system(cmd)

def hardcoded_pw():
    password = "admin123"
    return password
