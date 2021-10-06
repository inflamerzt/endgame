import sqlite3
if __name__ != '__main__':
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
    params = (dmethod, durl, dparams, drbody, drheader, dstatus, dresponse)
    #print(params)
    cursor.execute(sql, params)
    db.commit()
    db.close()


def h_load(columns=False, id=False, cnt=False):
    global dbname
    global tablename
    try:
        db = sqlite3.connect(dbname)
    except sqlite3.Error as e:
        # log.err(f"Database error: {e}")
        return
    cursor = db.cursor()
    if isinstance(columns, tuple):
        # select where id =
        query = f'SELECT '

        for item in columns:
            query += item + ', '
        query = query[:-2]

        query += f' FROM {tablename}'

        #cursor.execute(f"""SELECT FROM {tablename} WHERE id = {id}""")

    else:
        # select all
        query = f'SELECT * FROM {tablename}'

    if id: query += f' WHERE id = {id}'
    if cnt: query += f' ORDER BY id DESC LIMIT {cnt}'
    if __name__ == '__main__': print(query)

    cursor.execute(query)
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


if __name__ == '__main__':

    print(
        h_load(('id', 'method', 'url', 'params', 'rbody', 'rheader', 'status',
                'response'), 1))

    #print(h_load(0, 0, 1))

    for string in reversed(h_load(('id', 'method', 'url', 'status'), 0, 2)):
        print(string)
