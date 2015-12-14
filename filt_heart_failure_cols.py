# This is to get TF, DF and TF/DF
from __future__ import division
import csv

dp_range = range(2,1107) + range(1128,3179)


# counters set to 0
heart_failure_yes_count = 0
diag_yes_count = {}
heart_failure_diag_count = {}
for i in dp_range:
	diag_yes_count[i] = 0
	heart_failure_diag_count[i] = 0
total_diag_count = 0



with open('pvecs.csv', 'r') as fin, open('filt_heart_failure_cols.csv', 'w') as fout:
	writer = csv.writer(fout, delimiter=',')
	# to ignore headers
	has_header = csv.Sniffer().has_header(fin.read(1024))
	fin.seek(0)
	incsv = csv.reader(fin)


	if has_header:
		next(incsv)
	for row in csv.reader(fin, delimiter=','):
		total_diag_count += 1
		if row[1113] == 'y':
			heart_failure_yes_count += 1

		for i in dp_range:
			if row[i] == '1':
				diag_yes_count[i] += 1
				if row[1113] == 'y':
					heart_failure_diag_count[i] += 1


col_count = 0
p_count = 0
column_indices = []

for i in range (1108,1126):
	column_indices.append(i)

for i in range(2,1107):
	top = heart_failure_diag_count[i]/heart_failure_yes_count
	bottom = diag_yes_count[i]/total_diag_count
	# if top > 0.7:
	# 	col_count += 1
	# 	column_indices.append(i)
	if bottom:
		ratio = top/bottom
		if ratio >= 1 and top > 0.3:
			col_count += 1
			column_indices.append(i)

for i in range(1128,3179):
	top = heart_failure_diag_count[i]/heart_failure_yes_count
	bottom = diag_yes_count[i]/total_diag_count
	if bottom:
		ratio = top/bottom
		if ratio > 1 and top > 0.03:
			p_count += 1
			column_indices.append(i)


with open('pvecs.csv', 'r') as fin, open('filt_heart_failure_cols.csv', 'w') as fout:
	writer = csv.writer(fout, delimiter=',')
	for row in csv.reader(fin, delimiter=','):
		if row[1113] == 'y' or row[1113] == "info__chronic_heart_failure":
			temp_row = []
			for i in column_indices:
				temp_row.append(row[i])
			writer.writerow(temp_row)




ind = 1203

print "heart_failure_diag_count:"
print heart_failure_diag_count[ind]
# for i in range(2,1107):
# 	if heart_failure_diag_count[i] > 0:
# 		print diag_yes_count[i]
print "heart_failure yes count: ", heart_failure_yes_count
print "diag_yes_count:"
print diag_yes_count[ind]
# for i in range(2,1107):
# 	if diag_yes_count[i] > 0:
# 		print diag_yes_count[i]
print "total_diag_count: ", total_diag_count
#print heart_failure_diag_count

print "col_count: ", col_count
print "p_count:", p_count
#print "column_indices", column_indices