import sqlite3 as sql

### Interface between sqlite3 and python. Used by db manager ###

def insertNewJob(title, isNew, company, companyLogoUrl, timePosted, timeExpired, salary, located, preDescription, fullDescription, keywords, applications, jobUrl):
    con = sql.connect("database/jobs.db")
    cur = con.cursor()
    cur.execute("INSERT INTO jobs (title,isNew,company,companyLogoUrl,timePosted,timeExpired,salary,located,preDescription,fullDescription,keywords,applications,jobUrl) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (title, isNew,company, companyLogoUrl, timePosted, timeExpired, salary, located, preDescription, fullDescription, keywords, applications, jobUrl))
    con.commit()
    con.close()

def retrieve():
    con = sql.connect("database/jobs.db")
    cur = con.cursor()
    cur.execute("SELECT title, isNew, company, companyLogoUrl, timePosted, timeExpired, salary, located, preDescription, fullDescription, keywords, applications, jobUrl FROM jobs")
    allRows = cur.fetchall()
    con.close()
    return allRows

def retrieveOldUrl():
    con = sql.connect("database/jobs.db")
    cur = con.cursor()
    cur.execute("SELECT jobUrl FROM jobs")
    links = cur.fetchall()
    con.close()
    return links

def deleteRow(url):
    con = sql.connect("database/jobs.db")
    cur = con.cursor()
    cur.execute("DELETE from jobs where jobUrl = '{}'".format(url))
    con.commit()
    con.close()