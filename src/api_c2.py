import time
import BaseHTTPServer


HOST_NAME = 'localhost' 
PORT_NUMBER = 80

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
	
        s.wfile.write(make_page(s))
	
		
def make_page(s):

	returnstring = "<html><head><title>Riot API Challenge 2</title></head>"
	returnstring += "<body><p>This is a super basic web server to possibly use later</p>"
	if str(s.path) == "/league":
		returnstring += "<p>path: %s</p>" % vars(s)

	returnstring +=	"</body></html>"
		
	return returnstring

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