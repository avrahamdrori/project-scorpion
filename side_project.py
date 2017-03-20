import os,sys
import json
class Upfile():
	
	def __init__(self, email, file_name, originame, downloads_left):
		self.email = email
		self.file_name = file_name
		self.originame = originame
		self.downloads_left = downloads_left
		#self.newfilename = newfilename
		print self.email
		self.servername = "http://localhost:8080/"
	
	def generate_link(self):
		self.link = self.servername, 'download/', self.file_name
		return self.link

class list_of_files():
	def __init___(self):
		self.listoffiles = {}
