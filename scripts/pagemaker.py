#!/usr/bin/python
#_*_coding:utf-8_*_

contentdir = '../static/'


def makepage(*content):
	insert = ''
	page = ''
	for con in content:
		con = open(contentdir+con, 'r')
		insert = insert + con.read()
	template = open(contentdir+'template', 'r')
	stylesheet = open(contentdir+'style.css', 'r')
	for line in  template.readlines():
		if line == '%content%\n':
			line = insert
		if line == '%stylesheet%\n':
			line = stylesheet.read()
		page = page+line
	con.close()
	template.close()
	stylesheet.close()
	return page

def makequestion(q, ans):
	content = "<br><br>%s. %s<br>\n" % (q[0], q[1])
	if q[2] == 1:
		num = 0
		for a in ans:
			num = num + 1
			content = content + "<input type='radio' name='ans%s' value='%s'>%s<br>\n" % (a[1], num, a[2])) 
	if q[2] == 2:
		num = 0
		for a in ans:
			num = num + 1
			content = content + "<input type='checkbox' name='ans%s' value='%s'>%s<br>\n" % (a[1], num, a[2])) 
	if q[2] == 3:
		content = content + "<p>Введите ответ: <input type='text' name='ans%s'><br>\n" % q[0]
	return content

if __name__=='__main__':
	print makepage('newuser', 'continue')

