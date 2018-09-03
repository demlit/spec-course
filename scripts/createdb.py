#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sqlite3 as db
import os

contentdir = '../database/'
createDB = open(contentdir+'createDB', 'r', encoding="utf8")
fillDB = open(contentdir+'fillDB', 'r', encoding="utf8")

def CreateDB():
#	os.popen("/usr/bin/rm ../database/db.db")
#	os.popen("/usr/bin/touch ../database/db.db")
	try:
		os.remove("../database/db.db")
	except:
		pass
	database = os.open("../database/db.db", os.O_CREAT)
	os.close(database)
	conn = db.connect(contentdir+'db.db')
	cur = conn.cursor()
	cur.executescript(createDB.read())
	cur.executescript(fillDB.read())
	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	CreateDB()
