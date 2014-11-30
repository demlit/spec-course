#!/usr/bin/python
#_*_coding:utf-8_*_
import sqlite3 as db

contentdir = '../database/'
createDB = open(contentdir+'createDB', 'r')
fillDB = open(contentdir+'fillDB', 'r')

def CreateDB():
	conn=db.connect(contentdir+'db.db')
	cur=conn.cursor()
	cur.executescript(createDB.read())
	cur.executescript(fillDB.read())
	conn.commit()
	cur.close()
	conn.close()

if __name__=='__main__':
	CreateDB()
