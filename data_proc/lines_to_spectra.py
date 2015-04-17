#This file is part of ChiVO, the Chilean Virtual Observatory
#A project sponsored by FONDEF (D11I1060)
#Copyright (C) 2015 Universidad Tecnica Federico Santa Maria Mauricio Solar
#                                                            Marcelo Mendoza
#                   Universidad de Chile                     Diego Mardones
#                   Pontificia Universidad Catolica          Karim Pichara
#                   Universidad de Concepcion                Ricardo Contreras
#                   Universidad de Santiago                  Victor Parada
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import argparse
import csv
import sys


parser = argparse.ArgumentParser()
parser.add_argument("in_file", help="CSV input file")
parser.add_argument("out_file", help="CSV input file")
parser.add_argument("-u", "--unidentified", action='store_true', help="Just spectra that has at least one unidentified line")
args = parser.parse_args()

in_csv = args.in_file
out_csv = args.out_file

UNID_COUNT = 0
SPECTRA_COUNT = 0

with open(in_csv, 'r') as in_file:
	reader = csv.DictReader(in_file)

	with open(out_csv, 'w') as out_file:
		writer = csv.writer(out_file)

		this_spec_obj_id = False
		has_unidentified = False
		this_spectrum = []
		for row in reader:
			if row['specObjID'] != this_spec_obj_id:
				if this_spec_obj_id:
					if args.unidentified:
						if has_unidentified:
							writer.writerow(this_spectrum)
							SPECTRA_COUNT += 1
					else:	
						writer.writerow(this_spectrum)
						SPECTRA_COUNT += 1
					this_spectrum = []
					has_unidentified = False
				this_spectrum.append(row['specObjID'])
				this_spectrum.append(row['specClass'])
			if row['calcLineID'] != row['lineID']:
				has_unidentified = True
				UNID_COUNT += 1

			this_line_id = row['calcLineID']

			"""
			if this_line_id != row['lineID']:
				if 3990 <= this_line_id <= 4060:
					this_line_id = 4032
				elif 4080 <= this_line_id <= 4100:
					this_line_id = 4090
				elif 4660 <= this_line_id <= 4670:
					this_line_id = 4662
				elif 4940 <= this_line_id <= 4955:
					this_line_id = 4949
				elif 5440 <= this_line_id <= 5450:
					this_line_id = 5442
				elif 5796 <= this_line_id <= 5810:
					this_line_id = 5803
				elif 6520 <= this_line_id <= 6548:
					this_line_id = 6536
				elif 7020 <= this_line_id <= 7060:
					this_line_id = 7045
				elif 7490 <= this_line_id <= 7510:
					this_line_id = 7501
				elif 7540 <= this_line_id <= 7570:
					this_line_id = 7555
				elif 7615 <= this_line_id <= 7630:
					this_line_id = 7621
				else:
					this_spec_obj_id = row['specObjID']
					continue
			"""

			this_spectrum.append(this_line_id)
			this_spec_obj_id = row['specObjID']

print "Number of spectra: ", SPECTRA_COUNT
print "Unidentified lines: ", UNID_COUNT
