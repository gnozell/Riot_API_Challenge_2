from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static/', static_url_path='')

@app.route("/")
@app.route("/index.html")
def homepage():
    return render_template('index.html')

@app.route("/about.html")
def about_page():
    return render_template('about.html')

@app.route("/black_market.html")
def black_market_page():
    return render_template('black_market.html')

@app.route("/brawlers.html")
def brawlers_page():
    return render_template('brawlers.html')

@app.route("/champion.html")
def champion_page():
    return render_template('champion.html')

@app.route("/champion_info.html")
def champion_info_page():
    return render_template('champion_info.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()