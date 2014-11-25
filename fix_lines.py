import csv
import sys
from bisect import bisect_left

NEW_LINES = 0
ID_LINES = 0
ids_dict = dict()

def identify_line(calc_rest_wave, wave_err, line_ids):
	global NEW_LINES
	global ID_LINES 
	global ids_dict

	if wave_err < 1:
		wave_err = 1

	calc_rest_wave = round(calc_rest_wave)

	pos = bisect_left(line_ids, calc_rest_wave)
	if pos == 0:
		ret_val = line_ids[0]
	elif pos == len(line_ids):
		ret_val = line_ids[-1]
	else:
		before = line_ids[pos-1]
		after = line_ids[pos]
		if after - calc_rest_wave == calc_rest_wave - before:
			ret_val = calc_rest_wave + wave_err + 1
		elif after - calc_rest_wave < calc_rest_wave - before:
			ret_val = after
		else:
			ret_val = before
	if abs(calc_rest_wave - ret_val) <= wave_err:

		ID_LINES += 1
		ids_dict[ret_val] = ids_dict.get(ret_val, 0) + 1

		return ret_val
	else:

		NEW_LINES += 1

		new_id = int(round(calc_rest_wave))

		ids_dict[new_id] = ids_dict.get(new_id, 0) + 1

		line_ids.insert(pos, new_id)
		return new_id

def main():

	lines_in_path = sys.argv[1]
	lines_id_in_path = sys.argv[2]
	lines_out_path = sys.argv[3]

	with open(lines_id_in_path, 'r') as lines_id_in_file:

		line_ids = []

		csv_reader = csv.DictReader(lines_id_in_file)
		for row in csv_reader:
			line_ids.append(row['value'])
		line_ids = map(int, line_ids)
		line_ids.sort()

	#import ipdb;ipdb.set_trace()

	with open(lines_in_path, 'r') as lines_in_file:
		with open(lines_out_path, 'w') as lines_out_file:

			csv_reader = csv.DictReader(lines_in_file)

			out_fieldnames = csv_reader.fieldnames + ['calcLineID']

			csv_writer = csv.DictWriter(lines_out_file, out_fieldnames)
			csv_writer.writeheader()

			i = 0
			for row in csv_reader:

				if abs(float(row['specObjZ']) - float(row['specLineZ'])) < 0.0001:
					row['calcLineID'] = row['lineID']
				else:
					calc_rest_wave = float(row['calcRestWave'])
					wave_err = float(row['waveErr'])
					this_id = identify_line(calc_rest_wave, wave_err, line_ids)
					row['calcLineID'] = this_id

				csv_writer.writerow(row)

				#i += 1
				#if i > 10000:
				#	break
			
	print "\nNumber of IDs: %d\nNew IDs: %d\nIdentified existing: %d\n" % (len(line_ids), NEW_LINES, ID_LINES)
	w = csv.writer(open("data/line_ids_new.csv", "w"))
	sorted_ids_dict = sorted(ids_dict.items(), key=lambda x: x[1], reverse=True)
	for key, val in sorted_ids_dict:
	    w.writerow([key, val])

if __name__ == '__main__':
    main()



	
