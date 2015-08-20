#!/usr/bin/python

import json
import sys
import os
import sqlite3

sys.path.insert(0, '../lib/riotwatcher')
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
from riotwatcher import error_429
from riotwatcher import error_500
from riotwatcher import error_503

def get_file(file):
	## opens a file called api.key which contains my api key
	keyfile = open(file,"r")
	return keyfile.read()

def static_get_champion_list(rw):
	tries = 5
	while tries != 0:
		try:
			return rw.static_get_champion_list(champ_data="all")
		except LoLException as e:
			if e.error not in [error_429, error_503, error_500]:
				print "error from server"
				return
			if 'Retry-After' in e.response.headers:
				time.sleep(int(e.response.headers['Retry-After']))
			else:
				if e.error in [error_500,error_503]:
					time.sleep(30)
				else:
					time.sleep(1)
				tries -= 1

def static_get_item_list(rw):
	tries = 5
	while tries != 0:
		try:
			return rw.static_get_item_list()
		except LoLException as e:
			if e.error not in [error_429, error_503, error_500]:
				print "error from server"
				return
			if 'Retry-After' in e.response.headers:
				time.sleep(int(e.response.headers['Retry-After']))
			else:
				if e.error in [error_500,error_503]:
					time.sleep(30)
				else:
					time.sleep(1)
				tries -= 1

def print_champion_info(rw):
	champ_list =  static_get_champion_list(rw)

	dir_location = "../info/BILGEWATER_DATASET/BILGEWATER"
	files_dir = os.listdir(dir_location)

	
	champions = {}
	champions_stats = {}
	file_count = 0
	for file in files_dir:
		if "_info.json" in file:
			file_count += 1
			with open(dir_location + "/" + file, 'r') as data_file:
				count = 0;
				for line in data_file:
					clean_line = ""
					if count == 0:
						clean_line = line[1:len(line)-2]
					elif count == 9999:
						clean_line = line[:len(line)-1]
					else:
						clean_line = line[:len(line)-2]
					count += 1
					
					print file + ": " + str(count)

					match = json.loads(clean_line)

					for team in match['teams']:
						if "bans" in team:
							for bans in team['bans']:
								champion = str(bans['championId'])
								if champion in champions_stats:
									new_b = champions_stats[champion]['bans'] + 1
									champions_stats[champion].update({"bans":new_b})
								else:
									champions_stats[champion] = {"kills":0,"deaths":0,"assists":0,"minionsKilled":0,"goldEarned":0, "games_won":0,"totalDamageDealt":0,"totalDamageTaken":0,"bans":1,"items":{}}

					for participant in match['participants']:
						champion = str(participant['championId'])
						if champion in champions:
							champions[champion] += 1
						else:
							champions[champion] = 1

						if champion in champions_stats:
							kills = participant['stats']['kills']
							old_kills = champions_stats[champion]['kills']

							deaths = participant['stats']['deaths']
							old_deaths = champions_stats[champion]['deaths']

							assists = participant['stats']['assists']
							old_assists = champions_stats[champion]['assists']

							gold = participant['stats']['goldEarned']
							old_gold = champions_stats[champion]['goldEarned']

							minions = participant['stats']['minionsKilled'] + participant['stats']['neutralMinionsKilled']
							old_minions = champions_stats[champion]['minionsKilled']

							totalDamageTaken = participant['stats']['totalDamageTaken']
							old_totalDamageTaken = champions_stats[champion]['totalDamageTaken']

							totalDamageDealt = participant['stats']['totalDamageDealt']
							old_totalDamageDealt = champions_stats[champion]['totalDamageDealt']

							games_won = champions_stats[champion]['games_won']
							if participant['stats']['winner']:
								games_won += 1

							items = champions_stats[champion]['items']
							for item in [participant['stats']['item0'],participant['stats']['item1'], participant['stats']['item2'],participant['stats']['item3'],participant['stats']['item4'],participant['stats']['item5'],participant['stats']['item6']]:
								if str(item) in items:
									old_item_count = items[str(item)]
									items[str(item)] = old_item_count + 1

								else:
									items[str(item)] = 1

							champions_stats[champion].update({'kills':old_kills + kills,'deaths':old_deaths + deaths,'assists':old_assists + assists,'minionsKilled':old_minions + minions,'goldEarned':old_gold + gold,"games_won":games_won,"totalDamageDealt":old_totalDamageDealt + totalDamageDealt,"totalDamageTaken":old_totalDamageTaken + totalDamageTaken, "items":items})
							
						else:
							kills = participant['stats']['kills']
							deaths = participant['stats']['deaths']
							assists = participant['stats']['assists']
							minions = participant['stats']['minionsKilled'] + participant['stats']['neutralMinionsKilled']
							gold = participant['stats']['goldEarned']
							totalDamageTaken = participant['stats']['totalDamageTaken']
							totalDamageDealt = participant['stats']['totalDamageDealt']
							games_won = 0
							if participant['stats']['winner']:
								games_won += 1
							champions_stats[champion] = {"kills":kills,"deaths":deaths,"assists":assists,"minionsKilled":minions,"goldEarned":gold, "games_won":games_won,"totalDamageDealt":totalDamageDealt,"totalDamageTaken":totalDamageTaken,"bans":0,"items":{}}
	drop_db()
	make_db()

	for champion in champ_list['data']:
		p_champ = str(champ_list['data'][champion]['id'])
		p_champ_title = str(champ_list['data'][champion]['title'])
		if p_champ in champions:
			games_num = champions[p_champ]
			parcent = (float(games_num) / (10000*file_count)) * 100
			display_name = champ_list['data'][champion]['name']
			real_name = champion[0] + champion[1:].lower()
			kills = float("{0:.2f}".format(float(champions_stats[p_champ]['kills'])/games_num))
			deaths = float("{0:.2f}".format(float(champions_stats[p_champ]['deaths'])/games_num))
			assists = float("{0:.2f}".format(float(champions_stats[p_champ]['assists'])/games_num))
			kda = float("{0:.2f}".format(float(kills + assists) / deaths))
			avg_minion_score = float("{0:.2f}".format(float(champions_stats[p_champ]['minionsKilled'])/games_num))
			avg_gold = float("{0:.2f}".format(float(champions_stats[p_champ]['goldEarned'])/games_num))
			win_rate = float("{0:.2f}".format(float(champions_stats[p_champ]['games_won'])/games_num*100))
			avg_dmg_delt = int(float(champions_stats[p_champ]['totalDamageDealt'])/games_num)
			avg_dmg_taken = int(float(champions_stats[p_champ]['totalDamageTaken'])/games_num)
			position = champ_list['data'][champion]['tags'][0]
			ban_rate = float("{0:.2f}".format((float(champions_stats[p_champ]['bans']) / (10000*file_count)) * 100))

			item_list = []

			for del_item in ['0','3340','3341','3342','3361','3362','3363','3364']:
				if del_item in champions_stats[p_champ]['items']:
					del champions_stats[p_champ]['items'][del_item]
			for item, value in champions_stats[p_champ]['items'].iteritems():
				item_list.append((item, value))

			sorted_list = sorted(item_list, key=lambda tup: tup[1], reverse=True)
			new_sorted = []
			for new_item in sorted_list[:9]:
				(key,value) = new_item
				new_sorted.append(key)

			insert_db(p_champ, real_name, display_name, pick_rate=parcent, num_games=games_num, title=p_champ_title, avg_kills=kills,avg_deaths=deaths,avg_assists=assists, avg_kda=kda, avg_minion_score=avg_minion_score, avg_gold=avg_gold, win_rate=win_rate, avg_dmg_taken=avg_dmg_taken, avg_dmg_delt=avg_dmg_delt,position=position,ban_rate=ban_rate,fav_items=new_sorted)

def print_items_info(rw):
	item_list = static_get_item_list(rw)

	for item in item_list['data']:
		print "id: " + item
		print "   name: " + item_list['data'][item]['name']

def drop_db():
	if os.path.isfile('FlaskApp/yarhahar.db'):
		os.remove("FlaskApp/yarhahar.db")

def make_db():
	conn = sqlite3.connect('FlaskApp/yarhahar.db')
	c = conn.cursor()

	# Create table

	c.execute('''CREATE TABLE `merc` (
		  `id` INTEGER NULL DEFAULT NULL,
		  `display_name` VARCHAR NULL DEFAULT NULL,
		  `win_rate` INTEGER NULL DEFAULT NULL,
		  `games_played` INTEGER NULL DEFAULT NULL,
		  `ability_rank` INTEGER NULL DEFAULT NULL,
		  `offense_rank` INTEGER NULL DEFAULT NULL,
		  `defense_rank` INTEGER NULL DEFAULT NULL,
		  PRIMARY KEY (`id`)
		)''')

	c.execute('''CREATE TABLE `items` (
		  `id` INTEGER NULL DEFAULT NULL,
		  `display_name` VARCHAR NULL DEFAULT NULL,
		  `buy_rate` INTEGER NULL DEFAULT NULL,
		  `win_rate` INTEGER NULL DEFAULT NULL,
		  `num_games` INTEGER NULL DEFAULT NULL,
		  PRIMARY KEY (`id`)
		)''')

	c.execute('''CREATE TABLE `champion` (
		  `id` INTEGER NOT NULL DEFAULT NULL,
		  `name` VARCHAR NOT NULL DEFAULT 'NULL',
		  `display_name` VARCHAR NOT NULL DEFAULT 'NULL',
		  `avg_kills` INTEGER NULL DEFAULT NULL,
		  `avg_deaths` INTEGER NULL DEFAULT NULL,
		  `avg_assists` INTEGER NULL DEFAULT NULL,
		  `avg_kda` INTEGER NULL DEFAULT NULL,
		  `avg_minion_score` INTEGER NULL DEFAULT NULL,
		  `avg_dmg_delt` INTEGER NULL DEFAULT NULL,
		  `avg_dmg_taken` INTEGER NULL DEFAULT NULL,
		  `avg_kraken` INTEGER NULL DEFAULT NULL,
		  `avg_gold` INTEGER NULL DEFAULT NULL,
		  `pick_rate` INTEGER NULL DEFAULT NULL,
		  `ban_rate` INTEGER NULL DEFAULT NULL,
		  `position` INTEGER NULL DEFAULT NULL,
		  `num_games` INTEGER NULL DEFAULT NULL,
		  `fav_merc` INTEGER NULL DEFAULT NULL,
		  `fav_item0` INTEGER NULL DEFAULT NULL,
		  `fav_item1` INTEGER NULL DEFAULT NULL,
		  `fav_item2` INTEGER NULL DEFAULT NULL,
		  `fav_item3` INTEGER NULL DEFAULT NULL,
		  `fav_item4` INTEGER NULL DEFAULT NULL,
		  `fav_item5` INTEGER NULL DEFAULT NULL,
		  `fav_item6` INTEGER NULL DEFAULT NULL,
		  `fav_item7` INTEGER NULL DEFAULT NULL,
		  `fav_item8` INTEGER NULL DEFAULT NULL,

		  `win_rate` INTEGER NULL DEFAULT NULL,
		  `title` VARCHAR NULL DEFAULT NULL,
		  PRIMARY KEY (`id`, `fav_merc`)
		);''')

	# Insert a row of data
	#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def read_db():
	conn = sqlite3.connect('FlaskApp/yarhahar.db')
	c = conn.cursor()
	for row in c.execute('SELECT display_name, ban_rate FROM champion ORDER BY ban_rate'):
		#print row
		pass
	conn.close()

def insert_db(id=1, name=1, display_name=1, avg_kills=1, avg_deaths=1, avg_assists=1, avg_kda=1, avg_minion_score=1, avg_dmg_delt=1, avg_dmg_taken=1, avg_kraken=1, avg_gold=1, pick_rate=1, ban_rate=1, position=1, num_games=1, fav_merc=1, fav_item_list=1, win_rate=1, title=1, fav_items=[1,1,1,1,1,1,1,1,1]):
	conn = sqlite3.connect('FlaskApp/yarhahar.db')
	fav_item0 = fav_items[0]
	fav_item1 = fav_items[1]
	fav_item2 = fav_items[2]
	fav_item3 = fav_items[3]
	fav_item4 = fav_items[4]
	fav_item5 = fav_items[5]
	fav_item6 = fav_items[6]
	fav_item7 = fav_items[7]
	fav_item8 = fav_items[8]

	params = (id, name, display_name, avg_kills, avg_deaths, avg_assists, 
		avg_kda, avg_minion_score, avg_dmg_delt, avg_dmg_taken, avg_kraken,
		 avg_gold, pick_rate, ban_rate, position, num_games, fav_merc, win_rate, title,
		 fav_item0, fav_item1, fav_item2, fav_item3, fav_item4, fav_item5, fav_item6, fav_item7, fav_item8)
	c = conn.cursor()
	call = '''INSERT INTO `champion` (`id`,`name`,`display_name`,
					`avg_kills`,`avg_deaths`,`avg_assists`,`avg_kda`,`avg_minion_score`,
					`avg_dmg_delt`,`avg_dmg_taken`,`avg_kraken`,`avg_gold`,`pick_rate`,
					`ban_rate`,`position`,`num_games`,`fav_merc`,`win_rate`,`title`,
					`fav_item0`,`fav_item1`,`fav_item2`,`fav_item3`,`fav_item4`,`fav_item5`,
					`fav_item6`,`fav_item7`,`fav_item8`) VALUES

					(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
					'''
	c.execute(call,params)

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def main():
	api_key = get_file("api.key")

	## init RiotWatcher
	rw = RiotWatcher(api_key)

	print_champion_info(rw)

	#read_db()

if __name__ == "__main__":
	# If this is ran file then use function main
    main()