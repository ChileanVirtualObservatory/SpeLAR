import MySQLdb

num_selected_sets = 1
num_lines_per_set = 10
noise_lines_per_spectum = 10
selected_set_support = 0.5


db = MySQLdb.connect(host='localhost', user='molar', passwd='molar', db='splatalogue')
cur = db.cursor()
