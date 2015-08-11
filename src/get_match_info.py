import sys
import ast
import os
import json
import time
sys.path.insert(0, '../lib/riotwatcher')
from riotwatcher import RiotWatcher



def get_file(file):
	## opens a file called api.key which contains my api key
	keyfile = open(file,"r")
	return keyfile.read()

def main():
	## gets key from file
	api_key = get_file("api.key")

	dir_location = "../info/BILGEWATER_DATASET/BILGEWATER"
	#files_dir = os.listdir(dir_location)
	files_dir = ["NA.json"]
	for file in files_dir:
		if "_info.json" not in file:
			## init RiotWatcher
			rw = RiotWatcher(api_key,default_region=file.replace(".json","").lower())

			new_file_name = file.replace(".json","_info.json")

			print "Generating %s"%(new_file_name)
			print_file = open(dir_location + "/" + new_file_name ,"w+")

			file_info = get_file(dir_location + "/" + file)
			match_list = ast.literal_eval(file_info)

			count = 1
			match_len = len(match_list)
			print_file.write("[")
			for matchID in match_list:
				try:

					while not rw.can_make_request():
						time.sleep(1)

					match_info = rw.get_match(matchID)
					
					print_file.write(str(json.dumps(match_info)))

					if count != match_len:
						print_file.write(",\n")

					print "%s/%s"%(count, match_len)

				except Exception as e:

					print "error @ %s/%s"%(count, match_len)
					print (e)
					break
				count += 1
			print_file.write("]")

			print_file.close()

if __name__ == "__main__":
    main()