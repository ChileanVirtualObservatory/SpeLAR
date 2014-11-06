import csv
import sys

in_csv = sys.argv[1]
out_csv = sys.argv[2]

with open(in_csv, 'r') as in_file:
	reader = csv.DictReader(in_file)

	with open(out_csv, 'w') as out_file:
		writer = csv.writer(out_file)

		this_spec_obj_id = False
		this_spectrum = []
		for row in reader:
			if this_spec_obj_id and row['specObjID'] != this_spec_obj_id:
				writer.writerow(this_spectrum)
				this_spectrum = []
			this_spectrum.append(row['calcLineID'])
			this_spec_obj_id = row['specObjID']
