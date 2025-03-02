import sqlite3
import datetime

# This is primarily a testing file, but I'll leave it set to call database for testing purposes

def insertDispatch(units, callType, location, timeout):
    con = sqlite3.connect("records.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE dispatches(units, callType, location, timeout)")
    except:
        pass

    cur.execute(f"""
        INSERT INTO dispatches VALUES
        ('{units}', '{callType}', '{location}', '{timeout}')
    """)

    con.commit()

    con.close()

def getAllDispatches():
    con = sqlite3.connect("records.db")

    cur = con.cursor()

    res = cur.execute("SELECT * FROM dispatches")

    print(res.fetchall())

#insertDispatch('Engine 21', 'Test Incident', '61st & Indianola', datetime.datetime.now())
getAllDispatches()