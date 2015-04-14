"""
This file is part of ChiVO
Copyright (C) Nicolas Miranda

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import MySQLdb

num_selected_sets = 1
num_lines_per_set = 10
noise_lines_per_spectum = 10
selected_set_support = 0.5


db = MySQLdb.connect(host='localhost', user='molar', passwd='molar', db='splatalogue')
cur = db.cursor()
