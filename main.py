#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import cgitb
cgitb.enable()
import os, sys
from side_project import Upfile, list_of_files
import uuid
import json
'''TODO 
1. change name of uploaded file
2. make qr code
3. send qr to email
4. translate qr to url and send file
'''
PORT_NUMBER = 8080
upload_path = os.path.join(os.curdir,'files')



	
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path.startswith("/download"):
			uuidfilename = self.path[9,]
			print uuidfilename
			return 
			
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
			

	#Handler for the POST requests
	def do_POST(self):
		
		if self.path=="/upload":
			form = cgi.FieldStorage(
			
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
		if not form.has_key('upfile'):
			print "no file form"
			return

		fileitem = form["upfile"]
		#print fileitem
		if not fileitem.file: 
			print "no fileitem"
			return
		#print  fileitem.filename
		#give file a new name	
		newfilename = uuid.uuid1()
		print newfilename
		fout = file (os.path.join(upload_path, str(newfilename)), 'w')
		while True:
			chunk = fileitem.file.read(100000)
			if not chunk: break
			fout.write(chunk)
			
			newfile = Upfile(form["Email"].value,newfilename, fileitem.filename,form['downNum'])
			list_of_files.listoffiles[newfilename]=newfile
		fout.close()
		with open('kistoffiles.json', 'w') as f:
			json.dump(list_of_files, f)
		upf=list_of_files.listoffiles[newfilename]
		print upf.file_name
		print "saved in %s" % os.path.join(upload_path, fileitem.filename)
		print "Your name is: %s" % form["Email"].value
		print "downNum is: %s" % form["downNum"].value
		
		self.send_response(200)
		self.end_headers()
		self.wfile.write("Thanks %s !" % form["Email"].value)
		
			
	
	
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
