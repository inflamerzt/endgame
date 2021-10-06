import sqlite3
import modules.logger as log

dbname = "history.db"
tablename = "history"
isinit = False

# table # method url params request_body  status response


def h_init():
    global dbname
    global tablename
    try:
        db = sqlite3.connect(dbname)
    except sqlite3.Error as e:
        log.err(f"Database error: {e}")
        return
    cursor = db.cursor()
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {tablename}(id INTEGER PRIMARY KEY AUTOINCREMENT,method TEXT,url TEXT,params TEXT,rbody TEXT,rheader TEXT,status INTEGER,response TEXT)"""
    )

    db.commit()
    db.close()


def h_save(**data):
    global dbname
    global tablename
    try:
        db = sqlite3.connect(dbname)
    except sqlite3.Error as e:
        log.err(f"Database error: {e}")
        return

    cursor = db.cursor()

    if "method" in data.keys():
        dmethod = data["method"]
    else:
        dmethod = ""
    if "url" in data.keys():
        durl = data["url"]
    else:
        durl = ""
    if "params" in data.keys():
        dparams = data["params"]
    else:
        dparams = ""
    if "rbody" in data.keys():
        drbody = data["rbody"]
    else:
        drbody = ""
    if "rheader" in data.keys():
        drheader = data["rheader"]
    else:
        drheader = ""

    if "status" in data.keys():
        dstatus = data["status"]
    else:
        dstatus = 0
    if "response" in data.keys():
        dresponse = data["response"]
    else:
        dresponse = ""

    sql = f"""INSERT INTO {tablename} (method,url,params,rbody,rheader,status,response) VALUES(?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (dmethod, durl, dparams, drbody,
                   drheader, dstatus, dresponse))
    db.commit()
    db.close()


def h_load(id=None):
    global dbname
    global tablename
    try:
        db = sqlite3.connect(dbname)
    except sqlite3.Error as e:
        # log.err(f"Database error: {e}")
        return
    cursor = db.cursor()
    if id:
        # select where id =
        cursor.execute(f"""SELECT FROM {tablename} WHERE id = {id}""")
        data = cursor.fetchall()
        db.close()
        return data

    else:
        # select all
        cursor.execute(f"""SELECT * FROM {tablename}""")
        data = cursor.fetchall()
        db.close()
        return data


def h_clear():
    global dbname
    global tablename
    try:
        db = sqlite3.connect(dbname)
    except sqlite3.Error as e:
        log.err(f"Database error: {e}")
        return
    cursor = db.cursor()
    cursor.execute(f"""DROP TABLE IF EXISTS {tablename}""")
    db.commit()
    db.close()
    h_init()
