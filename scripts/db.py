#!/usr/bin/python
#_*_coding:utf-8_*_
import sqlite3 as db
import date
from datetime import datetime, timedelta, date, time as dt_time

database = '../database/db.db'
conn = db.connect(database)
cur = conn.cursor()


def Answer(fio):
	cur.execute("SELECT id FROM Answers WHERE fio=?", (fio))
	row =  cur.fetchone()
	if row != None:
		return False
	else:
		d = datetime.now()
		cur.execute("INSERT INTO Answers (fio,date) VALUES(?,?);", (fio, d.date()))
		cur.execute("SELECT id FROM Answers WHERE fio=? ORDER BY id DESC;", (fio,))
		row = cur.fetchone()
		return row[0]

def GetQuestions():
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
	return questlist

def GetCountQuestions():
	cur.execute("SELECT COUNT(*) FROM Question;")
	count = cur.fetchone()
	return int(count[0])

def SetDataInDB(data, user_id):
	cur.execute("SELECT id,id_type FROM Question;")
	questions = cur.fetchall()
	cur.execute("SELECT * FROM AnswerValues;")
	answers = cur.fetchall()
	content = "<p>Результаты теста:\n"
	
	for q in questions:
		if q[1] == 1:
			cur.execute("SELECT Value FROM AnswerValues WHERE id_Question=?",(q[0],))
			ans = cur.fetchall()[int(self.get_body_argument("ans%s" % str(q[0]))) - 1]
			self.write("Choice one answer: %s<br>" % ans)
		if q[1] == 2:
			cur.execute("SELECT Value FROM AnswerValues WHERE id_Question=?",(q[0],))
			ans = ''
			abc = cur.fetchall()
			for i in self.get_body_arguments("ans%s" % str(q[0])):
				ab = abc[int(i)-1]
				ans = ans+ab[0]+' '
			self.write("Choice many answers: %s<br>" % ans)
		if q[1] == 3:
			ans = self.get_body_argument("ans%s" % str(q[0]))
			self.write("Input answer: %s<br>" % ans)
		cur.execute("INSERT INTO AnswerDetails(id_Answer,id_Question,Answers) VALUES (?,?,?);", (id_Answer, id, ans[0]))
	conn.commit()



cur.close()
conn.close()
