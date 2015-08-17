from flask import Flask, send_from_directory
import os
app = Flask(__name__,static_folder='../rel',static_url_path='')

@app.route("/")
def main():
    return app.send_static_file('index.html')
	


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)