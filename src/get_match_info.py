import sys
sys.path.insert(0, '../lib/riotwatcher')
from riotwatcher import RiotWatcher

rw = RiotWatcher('<key here>')
champs = rw.get_all_champions()
print champs