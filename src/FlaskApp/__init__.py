from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
	#return render_template('404.html'), 404
	return "lol you 404"

@app.errorhandler(500)
def internal_server_error(e):
    #return render_template('500.html'), 500
    return "lol you 500"

if __name__ == "__main__":
    app.run()