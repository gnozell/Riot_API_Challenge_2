import sqlite3

class static_lol:
	def __init__(self):
		self.champion_list = self.gen_champ_list()
		self.champion_names = self.gen_champ_display_name()
		self.black_market_list = self.gen_black_market_list()
		self.item_list = self.gen_item_list()
		self.merc_ironbacks = self.gen_merc("3612")
		self.merc_ocklepods = self.gen_merc("3614")
		self.merc_plundercrabs = self.gen_merc("3613")
		self.merc_razorfins = self.gen_merc("3611")

	def gen_merc(self, type):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		for row in c.execute('SELECT win_rate, buy_rate, games_played, ability_rank, offense_rank, defense_rank  FROM merc WHERE id=?',[type]):
			return row
		conn.close()
		return ("0","0","0","0","0","0")
		
	def gen_item_list(self):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		items = []
		for row in c.execute('SELECT id, display_name, buy_rate, win_rate, num_games FROM items  ORDER BY display_name'):
			(id,name,buy_r, win_r, games) = row
			# remove all items that are not on summoners rift / consumable / champion related
			if str(id) not in ["3007","3902","3624","3625","3626","2054","3154","3090","3122","3290","3185",
								"3073","3345","3048","3181","3029","1062","2047","3112","3084","3613","2052",
								"1063","2009","2010","3611","3903","3615","3616","3617","3170","3614","3180",
								"3623","3622","3621","1074","3184","2050","3901","3460","3159","2051","3187",
								"3348","3612","3104","3106","3008","3137","1075","1076","3241","3242","3243",
								"3240","3244","3245","2043","3196","3197","3599","2044","3200","3198","2004",
								"2003","2138","2137","2140","2139","3043","3053","3748"]:
				items.append( (str(id),name, str(buy_r), str(win_r), str(games)) )
		conn.close()
		return items

	def gen_black_market_list(self):
		conn = sqlite3.connect('FlaskApp/yarhahar.db')
		c = conn.cursor()
		items = []
		bb_list = ["3433","3430","3431","3434","3911","3742","3844","3841","3840","3652","3829","3924","3744","3745","3150","1335","1336","1337","1338","1339","1340","1341"]
		for row in c.execute('SELECT id, display_name, buy_rate, win_rate, num_games FROM items WHERE id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? OR id=? ORDER BY display_name',bb_list):
			(id,name,buy_r, win_r, games) = row
			items.append( (str(id),name, str(buy_r), str(win_r), str(games)) )
		conn.close()
		return items

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
		for row in c.execute('SELECT display_name, title, pick_rate, win_rate, ban_rate, avg_kills, avg_deaths, avg_assists, avg_kda, position, avg_gold, num_games, avg_minion_score, avg_dmg_delt, avg_dmg_taken FROM champion WHERE name=?',params):
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

	def get_all_items(self):
		return self.item_list
		
	def get_merc_info(self, merctype):
		if merctype == "ironbacks":
			return self.merc_ironbacks
		elif merctype == "ocklepods":
			return self.merc_ocklepods
		elif merctype == "plundercrabs":
			return self.merc_plundercrabs
		elif merctype == "razorfins":
			return self.merc_razorfins
		else:
			return ("error","error","error","error","error","error")