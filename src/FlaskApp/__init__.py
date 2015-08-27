from flask import Flask, send_from_directory, render_template
from information import static_lol
import os

info = static_lol()
champion_list = info.get_champion_list()
champ_names = info.get_champion_names()
black_market_list = info.get_black_market_items()
all_item_list = info.get_all_items()
ironback_stats = info.get_merc_info("ironbacks")
ocklepods_stats = info.get_merc_info("ocklepods")
plundercrabs_stats = info.get_merc_info("plundercrabs")
razorfins_stats = info.get_merc_info("razorfins")

app = Flask(__name__, static_folder='static/', static_url_path='')

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/black_market")
def black_market_page():
    return render_template('black_market.html', items=black_market_list, all_items=all_item_list)

@app.route("/brawlers")
def brawlers_page():
    return render_template('brawlers.html', ironback_stats=ironback_stats, ocklepods_stats=ocklepods_stats, plundercrabs_stats=plundercrabs_stats, razorfins_stats=razorfins_stats)

@app.route("/champion")
def champion_info_page():
    return render_template('champion_info.html', champion_list=champion_list)

@app.route("/champion/<champion>")
def champion_page(champion=None):
    if str(champion) in champ_names:
      stats = info.get_specific_champ(champion)[0]
      pre_items = info.get_specific_champ_items(champion)[0]
      items = []
      for item in pre_items:
        items.append(str(item))
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