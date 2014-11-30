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
	for line in  template.readlines():
		if line == '%content%\n':
			line = insert
		page = page+line
	con.close()
	template.close()
	return page

if __name__=='__main__':
	print makepage('newuser', 'continue')

