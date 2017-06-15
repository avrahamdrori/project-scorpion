import sqlite3 as sql

def insert_file(email,originalFileName,uuidName,numOfTimes):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO entries (email,originalFileName,uuidName,numOfTimes) VALUES (?,?,?,?)", (email,originalFileName,uuidName,numOfTimes))
        con.commit()
def getFileList(email):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select originalFileName,uuidName,numOfTimes from entries where email like ?", (email,))
        rows = cur.fetchall();
        return rows
def getFilenamyByUuid(fileuuid):
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select originalFileName from entries where uuidName like ?", (fileuuid,))
        filename = cur.fetchone()
        return filename