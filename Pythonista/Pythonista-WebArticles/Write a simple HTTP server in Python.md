# Write a simple HTTP server in Python

_Captured: 2015-10-02 at 16:43 from [www.acmesystems.it](http://www.acmesystems.it/python_httpd)_

![](http://www.acmesystems.it/www/pubblicita/arietta_fiat500_tux.jpg)

  * [1](http://www.acmesystems.it/python_httpd)
  * [2](http://www.acmesystems.it/python_httpd)

The default Python distribution has a built-in support to the HTTP protocol that you can use to make a simple stand-alone Web server.

Visit also:

The Python module that provides this support is called [BaseFTTPServer](http://docs.python.org/library/basehttpserver.html) and can be used in our programs just including it in our sources:
    
    
    fromBaseHTTPServerimportBaseHTTPRequestHandler,HTTPServer

## Hello world !

Let's start with the first basic example. It just return "Hello World !" on the web browser.

[example1.py ](https://github.com/tanzilli/playground/blob/master/python/httpserver/example1.py)
    
    
    #!/usr/bin/pythonfromBaseHTTPServerimportBaseHTTPRequestHandler,HTTPServer
    
    PORT_NUMBER =8080#This class will handles any incoming request from#the browser class myHandler(BaseHTTPRequestHandler):#Handler for the GET requestsdef do_GET(self):self.send_response(200)self.send_header('Content-type','text/html')self.end_headers()# Send the html messageself.wfile.write("Hello World !")returntry:#Create a web server and define the handler to manage the#incoming request
    	server =HTTPServer(('', PORT_NUMBER), myHandler)print'Started httpserver on port ', PORT_NUMBER
    	
    	#Wait forever for incoming htto requests
    	server.serve_forever()exceptKeyboardInterrupt:print'^C received, shutting down the web server'
    	server.socket.close()

Run it by typing:
    
    
    debarm:~/playground/python/httpserver# python example1.py
    

Then open your web browser on this URL: **http://fox_ip_address:8080**.

"Hello World !" will appear on your browser and two log messages on the FOX console:
    
    
    Started httpserver on port  8080
    10.55.98.7 - - [30/Jan/2012 15:40:52] "GET / HTTP/1.1" 200 -
    10.55.98.7 - - [30/Jan/2012 15:40:52] "GET /favicon.ico HTTP/1.1" 200 -
    

## Serve static files

Let's try an example that shows how to serve static files like index.html, style.css, javascript code and images:

[example2.py ](https://github.com/tanzilli/playground/blob/master/python/httpserver/example2.py)
    
    
    #!/usr/bin/pythonfromBaseHTTPServerimportBaseHTTPRequestHandler,HTTPServerfrom os import curdir, sep
    
    PORT_NUMBER =8080#This class will handles any incoming request from#the browser class myHandler(BaseHTTPRequestHandler):#Handler for the GET requestsdef do_GET(self):ifself.path=="/":self.path="/index_example2.html"try:#Check the file extension required and#set the right mime type
    
    			sendReply =Falseifself.path.endswith(".html"):
    				mimetype='text/html'
    				sendReply =Trueifself.path.endswith(".jpg"):
    				mimetype='image/jpg'
    				sendReply =Trueifself.path.endswith(".gif"):
    				mimetype='image/gif'
    				sendReply =Trueifself.path.endswith(".js"):
    				mimetype='application/javascript'
    				sendReply =Trueifself.path.endswith(".css"):
    				mimetype='text/css'
    				sendReply =Trueif sendReply ==True:#Open the static file requested and send it
    				f = open(curdir + sep +self.path)self.send_response(200)self.send_header('Content-type',mimetype)self.end_headers()self.wfile.write(f.read())
    				f.close()returnexceptIOError:self.send_error(404,'File Not Found: %s'%self.path)try:#Create a web server and define the handler to manage the#incoming request
    	server =HTTPServer(('', PORT_NUMBER), myHandler)print'Started httpserver on port ', PORT_NUMBER
    	
    	#Wait forever for incoming htto requests
    	server.serve_forever()exceptKeyboardInterrupt:print'^C received, shutting down the web server'
    	server.socket.close()

This new example:

  * check the extension of the file requested file 
  * set the right mime type to give back to the browser
  * open the static file requested
  * send it back to the browser

Run it by typing:
    
    
    debarm:~/playground/python/httpserver# python example2.py
    

then open your web browser on this URL: **http://fox_ip_address:8080**.

An HTML home page will appear on your browser.

## Read data from a form

Now explore how to read incoming data from an HTML form.

[example3.py ](https://github.com/tanzilli/playground/blob/master/python/httpserver/example3.py)
    
    
    #!/usr/bin/pythonfromBaseHTTPServerimportBaseHTTPRequestHandler,HTTPServerfrom os import curdir, sep
    import cgi
    
    PORT_NUMBER =8080#This class will handles any incoming request from#the browser class myHandler(BaseHTTPRequestHandler):#Handler for the GET requestsdef do_GET(self):ifself.path=="/":self.path="/index_example3.html"try:#Check the file extension required and#set the right mime type
    
    			sendReply =Falseifself.path.endswith(".html"):
    				mimetype='text/html'
    				sendReply =Trueifself.path.endswith(".jpg"):
    				mimetype='image/jpg'
    				sendReply =Trueifself.path.endswith(".gif"):
    				mimetype='image/gif'
    				sendReply =Trueifself.path.endswith(".js"):
    				mimetype='application/javascript'
    				sendReply =Trueifself.path.endswith(".css"):
    				mimetype='text/css'
    				sendReply =Trueif sendReply ==True:#Open the static file requested and send it
    				f = open(curdir + sep +self.path)self.send_response(200)self.send_header('Content-type',mimetype)self.end_headers()self.wfile.write(f.read())
    				f.close()returnexceptIOError:self.send_error(404,'File Not Found: %s'%self.path)#Handler for the POST requestsdef do_POST(self):ifself.path=="/send":
    			form = cgi.FieldStorage(
    				fp=self.rfile, 
    				headers=self.headers,
    				environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})print"Your name is: %s"% form["your_name"].value
    			self.send_response(200)self.end_headers()self.wfile.write("Thanks %s !"% form["your_name"].value)returntry:#Create a web server and define the handler to manage the#incoming request
    	server =HTTPServer(('', PORT_NUMBER), myHandler)print'Started httpserver on port ', PORT_NUMBER
    	
    	#Wait forever for incoming htto requests
    	server.serve_forever()exceptKeyboardInterrupt:print'^C received, shutting down the web server'
    	server.socket.close()

Run this example:
    
    
    debarm:~/playground/python/httpserver# python example3.py
    

and type your name in the "Your name" label.

  * Python documentation: [BaseHTTPServer](http://docs.python.org/library/basehttpserver.html)

  
  
  


ARM9 Linux Embedded Module (128MB) 

Arietta G25 is a small and low-cost multi-chip module that integrates:

  * up to 3 USB 2.0 host ports
  * 20x2 pads for strip pitch 2.54mm (100mil) 

Basic Version with no strips mounted

  
| [Product description...](http://www.acmesystems.it/arietta) |

  
  
  


Acqua A5 + 4.3 inch TFT LCD evaluation kit 

Basic kit to evaluate the Acqua A25 SoM with TFT LCD 4.3 inch

Parts included:

  * A bootable microSD with Debian Linux preinstalled
  * Wall adapter 5 volt @ 1A switching power supply (Code PS-5V1A-EU-MUSB)

**Acme Systems srl**   
Via Aldo Moro 53 - 00055 Ladispoli (RM) - Italy   
Partita IVA / Codice Fiscale 08114831004 - **Tel +39.06.99.12.187** \- Fax +39.06.622.765.31 - email: **info@acmesystems.it** pec: acmesystemssrl@pec.it   
Iscritta al Registro delle Imprese di Roma al n. 08114831004
