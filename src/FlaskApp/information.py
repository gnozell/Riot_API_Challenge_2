import sqlite3

class static_lol:
	def __init__(self):
		self.champion_list = self.gen_champ_list()
		self.champion_names = self.gen_champ_display_name()
		self.black_market_list = ["3433","3430","3431","3434","3911","3742","3844","3841","3840","3652","3829","3924","3744","3745","3150","1338"]
		

	def gen_champ_list(self):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		champs = []
		for row in c.execute('SELECT display_name, name, pick_rate, win_rate, ban_rate, position FROM champion ORDER BY display_name'):
			champs.append(row)
		conn.close()
		return champs

	def gen_champ_display_name(self):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		champs = []
		for row in c.execute('SELECT name FROM champion ORDER BY display_name'):
			champs.append(row[0])
		conn.close()
		return champs

	def get_specific_champ(self, champion_name):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		champs = []
		params = [champion_name]
		for row in c.execute('SELECT pick_rate, win_rate, avg_kills, avg_deaths, avg_assists, avg_kda, position, avg_kraken, fav_merc, num_games, avg_minion_score, avg_dmg_delt, avg_dmg_taken, display_name, title FROM champion WHERE name=?',params):
			champs.append(row)
		conn.close()
		return champs

	def get_specific_champ_items(self, champion_name):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		champs = []
		params = [champion_name]
		for row in c.execute('SELECT fav_item0, fav_item1, fav_item2, fav_item3, fav_item4, fav_item5, fav_item6, fav_item7, fav_item8 FROM champion WHERE name=?',params):
			champs.append(row)
		conn.close()
		return champs

	def get_champion_names(self):
		return self.champion_names

	def get_champion_list(self):
		return self.champion_list
		
	def get_black_market_items(self):
		return self.black_market_list