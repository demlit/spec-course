#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sqlite3 as db
import os

contentdir = '../database/'
createDB = open(contentdir+'createDB', 'r')
fillDB = open(contentdir+'fillDB', 'r')

def CreateDB():
	os.popen("/usr/bin/rm ../database/db.db")
	os.popen("/usr/bin/touch ../database/db.db")
	conn=db.connect(contentdir+'db.db')
	cur=conn.cursor()
	cur.executescript(createDB.read())
	cur.executescript(fillDB.read())
	conn.commit()
	cur.close()
	conn.close()

if __name__=='__main__':
	CreateDB()
