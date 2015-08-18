

class static_lol:
	def __init__(self):
		self.champion_list = ["Aatrox","Ahri","Akali","Alistar","Amumu","Anivia","Annie",
								"Ashe","Azir","Bard","Blitzcrank","Brand","Braum","Caitlyn",
								"Cassiopeia","Chogath","Corki","Darius","Diana","Drmundo","Draven",
								"Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz",
								"Galio","Gangplank","Garen","Gnar","Gragas","Graves","Hecarim",
								"Heimerdinger","Irelia","Janna","Jarvaniv","Jax","Jayce","Jinx",
								"Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kennen",
								"Khazix","Kogmaw","Leblanc","Leesin","Leona","Lissandra","Lucian",
								"Lulu","Lux","Malphite","Malzahar","Maokai","Masteryi","Missfortune",
								"Mordekaiser","Morgana","Nami","Nasus","Nautilus","Nidalee","Nocturne",
								"Nunu","Olaf","Orianna","Pantheon","Poppy","Quinn","Rammus",
								"Reksai","Renekton","Rengar","Riven","Rumble","Ryze","Sejuani",
								"Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner",
								"Sona","Soraka","Swain","Syndra","Tahmkench","Talon","Taric",
								"Teemo","Thresh","Tristana","Trundle","Tryndamere","Twistedfate","Twitch",
								"Udyr","Urgot","Varus","Vayne","Veigar","Velkoz","Vi",
								"Viktor","Vladimir","Volibear","Warwick","Monkeyking","Xerath","Xinzhao",
								"Yasuo","Yorick","Zac","Zed","Ziggs","Zilean","Zyra"]
		self.champion_dict = {}
		self.black_market_list = ["3433","3430","3431","3434","3911","3742","3844","3841","3840","3652","3829","3924","3744","3745","3150","1338"]
		
	def get_champion_list(self):
		return self.champion_list
	
	def get_champion_dict(self):
		return self.champion_dict
		
	def get_black_market_items(self):
		return self.black_market_list