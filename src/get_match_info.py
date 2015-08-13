#!/usr/bin/python

import ast
import json
import os
import sys
import time
sys.path.insert(0, '../lib/riotwatcher')
from riotwatcher import RiotWatcher
from riotwatcher import LoLException
from riotwatcher import error_429
from riotwatcher import error_500
from riotwatcher import error_503

####
#
# By: Griffin Nozell
# Summoner: DrSunshine
# 
# This program takes the information provided by the Riot API Challenge 2
# Bilgewater set of MatchIDs and pulls down the matches and stores them into
# _info.json files located in the same directory as the information files.
#
# WARNING: using the developer keys this can take a long time to pull down all the matches
# so please dont expect this to be done in the blink of an eye. ~3.5 hours PER file
#
# Also for this program to work it requires a file called "api.key" with your API Key located 
# the file in text
#
####


def get_file(file):
	## opens a file called api.key which contains my api key
	keyfile = open(file,"r")
	return keyfile.read()

def wait(rw):
	# used to control on user side the frequency of API calls
    while not rw.can_make_request():
        time.sleep(1)
	
def main():
	# gets key from file
	api_key = get_file("api.key")

	# location of the matchIDs if you want AP_ITEM_DATASET change to
	# the appropriate directory
	dir_location = "../info/BILGEWATER_DATASET/BILGEWATER"
	#files_dir = os.listdir(dir_location)
	files_dir = ["BR.json"]

	for file in files_dir:
		# For every file that doesn't end in _info.json loop through it
		# expecting a list of MatchIDs and then preform API calls to get the match info
		# and then write to a file with ending "_info.json"
		if "_info.json" not in file:
			## init RiotWatcher
			rw = RiotWatcher(api_key,default_region=file.replace(".json","").lower())

			new_file_name = file.replace(".json","_info.json")

			print "Generating %s"%(new_file_name)
			print_file = open(dir_location + "/" + new_file_name ,"w+")

			# opens the file and reads contents
			file_info = get_file(dir_location + "/" + file)

			# turns the string representation of a list of MatchIDs
			# into an actual list of MatchIDs
			match_list = ast.literal_eval(file_info)

			# variables to display progress in processing MatchIDs
			count = 1
			match_len = len(match_list)

			# Begins writing the output file with beginning of the list
			print_file.write("[")

			# For every MatchId in the MatchList
			for matchID in match_list:

				# Sets default value for match_info
				match_info = {}

				# used to gauge 429 responses later on
				gotitbool = False

				# Loops until gotitbool is found
				while not gotitbool:
					try:
						# checks if queue is clear if not waits until it is
						wait(rw)

						# attempts to get the match information given MatchID
						match_info = rw.get_match(matchID)

						# if it got this far it successful and gotitbool is set to True
						gotitbool = True

					except LoLException as e:
						# This trips if an LoLException is raised from RiotWatcher

						print e.error

						# If this is not a 429 error then it can't wait a time span
						# to find a solution to it

						if e.error not in [error_429, error_503, error_500]:
							# a 400, 401, 404 error
							print "error from server: %s"%(e.error)
							return

						# Prints out all the applicable headers used for debugging
						for header in e.response.headers:
							if header not in ['access-control-allow-headers','content-encoding','transfer-encoding','x-newrelic-app-data','server','connection','cache-control','date','access-control-allow-origin','access-control-allow-methods','content-type','content-length']:
								print "headers: %s"%(header)

						if 'Retry-After' in e.response.headers:
							# If the client receives a Rate Limit Exceeded response the client 
							# should process this response and halt future API calls for the duration, 
							# in seconds, indicated by the Retry-After header
							time.sleep(int(e.response.headers['Retry-After']))
						else:
							# Else if no Retry-After header wait a reasonable time (1sec)
							# and then try agian

							if e.error in [error_500,error_503]:
								time.sleep(30)
							else:
								time.sleep(1)
							
					except Exception as e:
						# An error occured that was not anticipated
						print str(e)
						return 

				# Dumps the json information into the output file
				print_file.write(str(json.dumps(match_info)))

				# If not the end of the file adds a ",\n" which is 
				# needed to properly process the file later
				if count != match_len:
					print_file.write(",\n")

				# Prints progress in processing the file
				print "%s: %s/%s"%(str(file), count, match_len)

				# Moves counter up by 1
				count += 1

			# closing off the list of matches
			print_file.write("]")
			print_file.close()

if __name__ == "__main__":
	# If this is ran file then use function main
    main()