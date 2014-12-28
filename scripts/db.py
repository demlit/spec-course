#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sqlite3 as db
#from datetime import datetime, timedelta, date, time as dt_time
from datetime import datetime, date

database = '../database/db.db'


def Answer(fio):
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT id FROM Answers WHERE fio=?", (fio,))
	row =  cur.fetchone()
	if row != None:
		return False
	else:
		d = datetime.now()
		cur.execute("INSERT INTO Answers (fio,date) VALUES(?,?);", (fio, d.date()))
		conn.commit()
		cur.execute("SELECT id FROM Answers WHERE fio=? ORDER BY id DESC;", (fio,))
		row = cur.fetchone()
		return row[0]
	cur.close()
	conn.close()

def FindAnswer(fio):
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT id FROM Answers WHERE fio=? ORDER BY id DESC;", (fio,))
	count = cur.fetchone()
	cur.close()
	conn.close()
	return int(count[0])

def GetQuestions():
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT * FROM Question;")
	questions = cur.fetchall()
	cur.execute("SELECT * FROM AnswerValues")
	answers = cur.fetchall()
	questlist = {}
	for question in questions:
		if question[2] == 3:
			questlist[question] = None
		else:
			anslist = []
			for answer in answers:
				if answer[1] == question[0]:
					anslist.append(answer)
			questlist[question] = anslist
	cur.close()
	conn.close()
	return questlist

def GetCountQuestions():
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT COUNT(*) FROM Question;")
	count = cur.fetchone()
	cur.close()
	conn.close()
	return int(count[0])

def SetDataInDB(data, user_id):
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT * FROM Question;")
	questions = cur.fetchall()
	cur.execute("SELECT * FROM AnswerValues;")
	answers = cur.fetchall()
	content = "<p>Результаты:<br>\n"
	for q in questions:
		if q[2] == 1:
			value = []
			for v in answers:
				if v[1] == q[0]:
					value.append(v[2])
			ans = str(value[int(data[q[0]][0])-1])
			content = content + "%s - %s<br>" % (q[1],ans)

		if q[2] == 2:
			value = []
			ans = ''
			for v in answers:
				if v[1] == q[0]:
					value.append(v[2])
			for i in data[q[0]]:
				ans = ans + str(value[int(i)-1]) + ' '
			content = content + "%s - %s<br>" % (q[1],ans)

		if q[2] == 3:
			ans = data[q[0]]
			ans = str(ans[0])
			content = content + "%s - %s<br>" % (q[1],ans)
		cur.execute("INSERT OR REPLACE INTO AnswerDetails(id_Answer,id_Question,Answers) VALUES (?,?,?);", (user_id, q[0], str(ans)))
	content = content + '<form action="/?new=1" method="GET"><input type="submit" value="Заново"></form>'
	conn.commit()
	cur.close()
	conn.close()
	return content

def GetResults(user_id):
	conn = db.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT * FROM AnswerDetails WHERE id_Answer=?", (user_id,))
	answers = cur.fetchall()
	cur.execute("SELECT * FROM Question")
	questions = cur.fetchall()
	count = int(GetCountQuestions())
	content = "<p>Результаты:<br>\n"
	c = 0
	for a in answers:
		if c%count == 0:
			content = content + "<br><br>Тест №%s:<br><br>" % int(c/count+1)
		c = c + 1
		type = questions[a[2]-1]
		if type[2] == 1:
			content = content + "%s - %s<br>" % (type[1],a[3]) 
		if type[2] == 2:
			content = content + "%s - %s<br>" % (type[1],a[3]) 
		if type[2] == 3:
			content = content + "%s - %s<br>" % (type[1],a[3]) 
	content = content + '<form action="/?new=1" method="GET"><input type="submit" value="Заново"></form>'
	cur.close()
	conn.close()
	return content

