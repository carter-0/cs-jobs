import sqlite3 as sql

### Interface between sqlite3 and python. Used by webserver for login details [hashed with bcrypt] ###

def pwInsert(usr,email,passwrd):
    con = sql.connect("database/LoginData.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (usr,email,passwrd) VALUES (?,?,?)", (usr,email,passwrd))
    con.commit()
    con.close()

def pwRetrieve():
	con = sql.connect("database/LoginData.db")
	cur = con.cursor()
	cur.execute("SELECT usr, email, passwrd FROM users")
	users = cur.fetchall()
	con.close()
	return users

def pwRetrieveNames():
    con = sql.connect("database/LoginData.db")
    cur = con.cursor()
    cur.execute("SELECT usr FROM users")
    names = cur.fetchall()
    con.close()
    return names

def pwRetrieveEmails():
    con = sql.connect("database/LoginData.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM users")
    emails = cur.fetchall()
    con.close()
    return emails
