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
			return rw.static_get_champion_list()
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
	champion_template = {"name":"", "":"", "":"", "":"", "":"", 
							"":"","":"","":"","":"","":"",
							"":"","":"","":"","":"","":"",
							"":"","":"","":"","":"","":"",
							"":"","":"","":"","":"","":"",
							"":"","":""}
	for file in files_dir:
		if "_info.json" in file:
			with open(dir_location + "/" + file) as data_file:    
				data = json.load(data_file)
				for match in data:
					for participant in match['participants']:
						champion = str(participant['championId'])
						if champion in champions:
							champions[champion] += 1
						else:
							champions[champion] = 1
	
	
	for champion in champ_list['data']:
		p_champ = str(champ_list['data'][champion]['id'])
		if p_champ in champions:
			games_num = champions[p_champ]
			parcent = (float(games_num) / 10000) * 100
			display_name = champ_list['data'][champion]['name']
			print "id: " + str(p_champ)
			print "    name: " + str(champion)
			print "    display_name: " + str(display_name)
			print "    total games: " + str(games_num)
			print "    parcent: " + str(parcent) + "%"

def print_items_info(rw):
	item_list = static_get_item_list(rw)

	for item in item_list['data']:
		print "id: " + item
		print "   name: " + item_list['data'][item]['name']

def drop_db():
	if os.path.isfile('example.db'):
		os.remove("example.db")

def insert_db():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()

	# Create table
	c.execute('''CREATE TABLE stocks
	             (date text, trans text, symbol text, qty real, price real)''')

	# Insert a row of data
	c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def read_db():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	for row in c.execute('SELECT * FROM stocks ORDER BY price'):
		print row
	conn.close()

def main():
	api_key = get_file("api.key")

	## init RiotWatcher
	rw = RiotWatcher(api_key)
	#print static_get_champion_list(rw)
	#print_champion_info(rw)
	#print_items_info(rw)
	drop_db()
	insert_db()
	read_db()

if __name__ == "__main__":
	# If this is ran file then use function main
    main()