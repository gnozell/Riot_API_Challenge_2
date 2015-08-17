from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static/', static_url_path='')

@app.route("/")
def index_page():
    stats = {}
    return render_template('index.html', stats=stats)

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/black_market")
def black_market_page():
    stats = {}
    return render_template('black_market.html', stats=stats)

@app.route("/brawlers")
def brawlers_page():
    stats = {}
    return render_template('brawlers.html', stats=stats)

@app.route("/champion_info")
def champion_info_page():
    champion_list = []
    stats = {}
    return render_template('champion_info.html', stats=stats, champion_list=champion_list)

@app.route("/champion/<champion>")
def champion_page(champion=None):
    if str(champion) in ["Aatrox","Ahri"]:
      stats = {"pickrate" : 49, "winrate": 49, "kills":1, "deaths":2, "assists":1 ,"kda":3, "primaryroll":"Top"}
      items = ['1001','1001','1001','1001','1001','1001','1001','1001','1001']
      return render_template('champion.html', champion=champion, items=items, stats=stats)
    else:
      return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()