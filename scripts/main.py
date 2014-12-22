#!/usr/bin/python
#_*_coding:utf-8_*_
import sqlite3 as db
import time
from datetime import datetime, timedelta, date, time as dt_time
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import sys
import pagemaker as page
import db

id_Answer = ''

database = '../database/db.db'
staticdir = '../static/'

class WelcomeHandler(tornado.web.RequestHandler):
	def get(self):
		cookie = self.get_cookie("user.opros",default=None)
		if cookie == None:
			if self.get_query_argument("err", default = False):
				self.write(page.makepage('newuser', 'incorrectdata'))
			else:
				self.write(page.makepage('newuser'))
		else:
			self.write(page.makepage('continue'))

class BeginTestHandler(tornado.web.RequestHandler):
	def post(self):
		if self.get_query_argument("err", default = False):
			self.write(page.makepage('questions', 'incorrectdata'))
		elif self.get_body_argument("new", default = False):
			print 'ping'
			self.Start()
		else:
			print 'pong'
			fio = self.CorrectName()
			if fio == 'ERROR':
				self.redirect('/?err=1')
			elif db.Answer(fio) == False:
				self.write(page.makepage('answerexist'))
			else:
				user_id = db.Answer(fio)
#				self.set_cookie("user.opros", (str(user_id)))
				self.Start()

	def get(self):
		cookie = self.get_cookie("user.opros",default=None)
		if cookie == None:
			self.redirect('/')
		self.Start()

	def CorrectName(self):
		name1 = self.get_body_argument("name1")
		name2 = self.get_body_argument("name2")
		name3 = self.get_body_argument("name3")
#		global id_Answer
		for name in name1, name2, name3:
			if name.istitle() != True:
				return 'ERROR'
			for char in name:
				if (char.isalpha() != True) and (char != ' '):
					return 'ERROR'
		return "%s %s %s" % (name1, name2, name3)			


#	def Welcome(self,fio):
#		conn = db.connect(database)
#		cur = conn.cursor()
#		self.write("Добро пожаловать на самый бессмысленный тест в вашей жизни.<br>")
#		d = datetime.now()
#		cur.execute("INSERT INTO Answers (fio,date) VALUES(?,?);", (fio, d.date()))
#		cur.execute("SELECT id FROM Answers WHERE fio=? ORDER BY id DESC;", (fio,))
#		row = cur.fetchone()

#		id_Answer = row[0]
#		conn.commit()
#		cur.close()
#		conn.close()
#		return id_Answer

#	def GetQuestions(self):
#		conn = db.connect(database)
#		cur = conn.cursor()
#		cur.execute("SELECT COUNT(*) FROM Question;")
#		row = cur.fetchone()
#		count = row[0]
#		self.write("<form action='/endtest' method='POST'>")
#		for question in range(1, count+1):
#			self.Quest(question, cur)
#		self.write("<br><input type='submit'></form>")
#		conn.commit()
#		cur.close()
#		conn.close()

	def Start(self):
		questlist = db.GetQuestions()
		content = "<p>Добро пожаловать на самый бессмысленный тест в вашей жизни.\n<form action='/endtest' method='POST'>\n"
		for question in questlist:
#			print type(content), type(question), type(questlist[question]), type(page.makequestion(question, questlist[question]))
			print page.makequestion(question, questlist[question])
			content = "".join([content, unicode(str(page.makequestion(question, questlist[question])), 'utf-8')])
		content = content + "<br><input type='submit'></form>"
		quest = open(staticdir + "questions", 'w')
		quest.write(content)
		quest.close()
		self.write(page.makepage('questions'))

#	def Quest(self, id, cur):
#		cur.execute("SELECT * FROM Question WHERE id=?;" , (id,))
#		quest=cur.fetchall()
#		for q in quest:
#			self.write( "<br><br>%s. %s<br>" % (q[0], q[1]))
#			if q[2] == 1:	#only one choise
#					cur.execute("SELECT * FROM AnswerValues WHERE id_Question=?;", (id,))
#					num=0
#					for a in cur.fetchall():
#						num=num+1
#						self.write("<input type='radio' name='ans%s' value='%s'>%s<br>" % (a[1], num, a[2]))
#			if q[2] == 2:	#many choises
#					cur.execute("SELECT * FROM AnswerValues WHERE id_Question=?;", (id,))
#					num = 0
#					for a in cur.fetchall():
#						num = num + 1
#						self.write("<input type='checkbox' name='ans%s' value='%s'>%s<br>" % (a[1], num, a[2]))
#			if q[2] == 3:
#					self.write("<p>Введите ответ: <input type='text' name='ans%s'><br>" % q[0])

class EndTestHandler(tornado.web.RequestHandler):
	def post(self):
		data = self.CorrectData()
		if data == 'ERROR':
			self.redirect('/begintest?err=1')
		else:
			printable = db.SetDataInDB(data, user_id)
			result = open(staticdir + "result", 'w')
			result.write(printable)
			result.close()
			self.write(page.makepage('result'))

	def CorrectData(self):
		count = db.GetCountQuestions()
		data = {}
		for num in range(1, count + 1):
			if self.get_body_argument("ans%s" % num) == None:
				return 'ERROR'
			else:
				data[num] = self.get_body_arguments("ans%s" % num)
		return data

#	def post(self):
#		conn = db.connect(database)
#		cur = conn.cursor()
#		cur.execute("SELECT COUNT(*) FROM Question;")
#		row = cur.fetchone()
#		count = row[0]
#		for id in range(1, count+1):
#			cur.execute("SELECT * FROM Question WHERE id=?;",(id,))
#			q = cur.fetchone()
#			if q[2] == 1:
#				cur.execute("SELECT Value FROM AnswerValues WHERE id_Question=?",(q[0],))
#				ans = cur.fetchall()[int(self.get_body_argument("ans%s" % str(q[0]))) - 1]
#				self.write("Choice one answer: %s<br>" % ans)
#			if q[2] == 2:
#				cur.execute("SELECT Value FROM AnswerValues WHERE id_Question=?",(q[0],))
#				ans = ''
#				abc = cur.fetchall()
#				for i in self.get_body_arguments("ans%s" % str(q[0])):
#					ab = abc[int(i)-1]
#					ans = ans+ab[0]+' '
#				self.write("Choice many answers: %s<br>" % ans)
#			if q[2] == 3:
#				ans = self.get_body_argument("ans%s" % str(q[0]))
#				self.write("Input answer: %s<br>" % ans)
#			cur.execute("INSERT INTO AnswerDetails(id_Answer,id_Question,Answers) VALUES (?,?,?);", (id_Answer, id, ans[0]))
#		conn.commit()
#		cur.close()
#		conn.close()

	def get(self):
		cookie = self.get_cookie("user.opros",default=None)
		if cookie == None:
			self.redirect('/')
		else:
			self.write("Test was completed")

application = tornado.web.Application([
	(r"/", WelcomeHandler),
	(r"/begintest", BeginTestHandler),
	(r"/endtest", EndTestHandler),
])

if __name__=='__main__':
	if sys.argv[1] == 'newDB':
		from createdb import CreateDB
		CreateDB()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
