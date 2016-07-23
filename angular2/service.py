import time
import BaseHTTPServer
import json
import cgi
import os
import urlparse

HOST_NAME = 'localhost'
PORT_NUMBER = 8020 
    
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to a GET request."""
        if self.path == "/get_all_images":
            response = {}
            counter = 0
            image_path = "images"
            mtime = lambda f: os.stat(os.path.join(image_path, f)).st_mtime
            for file in list(sorted(os.listdir(image_path), key=mtime)):
                response[counter] = file
                counter+=1
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
            self.end_headers()
            self.wfile.write(json.dumps(response))
            
        
    def do_POST(self):
        """Respond to a POST request."""
        if self.path == "/":
            content_length = int(self.headers['Content-Length'])
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            newFile = open ("./images/%s" % form['name'].value, "wb")
            newFile.write(form['file'].value)
            # Respond with 200 OK           
            self.send_response(200, form['name'].value)
            self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
            self.end_headers()
        elif self.path == "/remove_images":
            content_length = int(self.headers['Content-Length'])
            file_content = self.rfile.read(content_length)
            data = json.loads(file_content)
            image_path = "images"
            for filename in data:                
                if os.path.isfile("%s/%s" % (image_path, filename)):
                    os.remove("%s/%s" % (image_path, filename))
            # Respond with 200 OK            
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
            self.end_headers()
   
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)