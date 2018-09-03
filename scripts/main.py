#!/usr/bin/python3
#-*- coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import sys
import pagemaker as page
import db

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
			self.Start()
		else:
			fio = self.CorrectName()
			if fio == 'ERROR':
				self.redirect('/?err=1')
			else:
				user_id = db.Answer(fio)
				if user_id == False:
					user_id = db.FindAnswer(fio)
					self.set_cookie("user.opros", (str(user_id)))
					self.write(page.makepage('answerexist'))
				else:
					self.set_cookie("user.opros", (str(user_id)))
					self.Start()

	def get(self):
		cookie = self.get_cookie("user.opros",default=None)
		if cookie == None:
			self.redirect('/')
		elif self.get_query_argument("err", default = False):
			self.post()
		else:
			self.Start()

	def CorrectName(self):
		name1 = self.get_body_argument("name1")
		name2 = self.get_body_argument("name2")
		name3 = self.get_body_argument("name3")
		for name in name1, name2, name3:
			if name.istitle() != True:
				return 'ERROR'
			for char in name:
				if (char.isalpha() != True) and (char != ' '):
					return 'ERROR'
		return "%s %s %s" % (name1, name2, name3)

	def Start(self):
		questlist = db.GetQuestions()
		content = "<p>Начинаем самый бессмысленный тест в твоей жизни!\n<form action='/endtest' method='POST'>\n"
		for question in sorted(questlist):
			content = content + page.makequestion(question, questlist[question])
		content = content + "<br><input type='submit'></form>"
		quest = open(staticdir + "questions", 'w', encoding="utf8")
		quest.write(content)
		quest.close()
		self.write(page.makepage('questions'))


class EndTestHandler(tornado.web.RequestHandler):
	def post(self):
		cookie = self.get_cookie("user.opros",default=None)
		user_id = cookie
		data = self.CorrectData()
		if data == 'ERROR':
			self.redirect('/begintest?err=1')
		else:
			printable = db.SetDataInDB(data, user_id)
			result = open(staticdir + "result", 'w', encoding="utf8")
			result.write(printable)
			result.close()
			self.write(page.makepage('result'))
			self.clear_cookie("user.opros")

	def CorrectData(self):
		count = db.GetCountQuestions()
		data = {}
		for num in range(1, count + 1):
			if self.get_body_argument("ans%s" % num, default = None) == None:
				return 'ERROR'
			else:
				data[num] = self.get_body_arguments("ans%s" % num)
		return data

	def get(self):
		cookie = self.get_cookie("user.opros",default=None)
		try:
			user_id = int(cookie)
		except:
			self.redirect('/')
		if self.get_argument("results", default=False):
			printable = db.GetResults(user_id)
			results = open(staticdir + "results", 'w', encoding="utf8")
			results.write(printable)
			results.close()
			self.write(page.makepage('results'))
			self.clear_cookie("user.opros")
		else:
			self.redirect('/')





application = tornado.web.Application([
	(r"/", WelcomeHandler),
	(r"/begintest", BeginTestHandler),
	(r"/endtest", EndTestHandler),
])

if __name__ == '__main__':
	try:
		sys.argv[1]
	except:
		pass
	else:
		if sys.argv[1] == 'newDB':
			from createdb import CreateDB
			CreateDB()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
