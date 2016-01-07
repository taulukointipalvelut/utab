#import csv
#from numpy.random import beta
import numpy as np
#import scipy as sp
import math
import matplotlib.pyplot as plt
#import random
#import itertools

def bar2(gov_percentage_list, std_list):
	arr_percentages = np.array(gov_percentage_list)
	arr_sds = np.array(std_list)
	arr_100s = np.array([100]*len(std_list))
	#percentages = [43, 23, 55, 32, 31]
	#sds = [12, 15, 13, 9, 10]
	data = [(arr_percentages-arr_sds).tolist(), (arr_sds).tolist(), (arr_sds).tolist(), (arr_100s-arr_sds-arr_percentages).tolist()]

	#data.append([100-num for num in percentages])

	columns = ['R'+str(i+1) for i in range(len(gov_percentage_list))]
	rows = ['%s' % x for x in ("opp", "opp-sd", "gov-sd", "gov")]

	values = np.arange(0, 110, 10)
	value_increment = 1

	# Get some pastel shades for the colors
	colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
	n_rows = len(data)

	index = np.arange(len(columns)) + 0.3
	bar_width = 0.4

	# Initialize the vertical-offset for the stacked bar chart.
	y_offset = np.array([0.0] * len(columns))

	# Plot bars and create text labels for the table
	cell_text = []
	for row in range(n_rows):
	    plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
	    y_offset = y_offset + data[row]
	    cell_text.append(['%1.1f' % (x) for x in y_offset])
	# Reverse colors and text labels to display the last value at the top.
	colors = colors[::-1]
	cell_text.reverse()

	# Add a table at the bottom of the axes
	the_table = plt.table(cellText=cell_text,
	                      rowLabels=rows,
	                      rowColours=colors,
	                      colLabels=columns,
	                      loc='bottom')

	# Adjust layout to make room for the table:
	plt.subplots_adjust(left=0.2, bottom=0.2)

	plt.ylabel("percentage")
	plt.yticks(values * value_increment, ['%d' % val for val in values])
	plt.xticks([])
	plt.title('Percentage for gov-win')

	plt.show()

def bar3(percentage_list, sd_list, teamnum):
	if teamnum == 2:
		N = len(percentage_list)
		opp_percentage_list = [100-num for num in percentage_list]
		ind = np.arange(N)    # the x locations for the groups
		width = 0.25       # the width of the bars: can also be len(x) sequence

		p1 = plt.bar(ind, percentage_list, width, color='b', yerr=sd_list)
		p3 = plt.bar(ind, percentage_list, width, color='r')
		p2 = plt.bar(ind, opp_percentage_list, width, color='w', bottom=percentage_list)

		plt.ylabel('percentages')
		plt.title('Motion fairness by gov/opp')
		plt.xticks(ind + width/2., ['R'+str(i+1) for i in range(N)])
		plt.yticks(np.arange(0, 110, 10))
		plt.legend((p3[0], p2[0]), ('Gov', 'Opp'))

		plt.show()
	else:
		print "nomodasfjpo;adsj"

def hist(data_list):
	plt.style.use('bmh')
	for data in data_list:
		plt.hist(data, histtype="stepfilled", bins=abs(math.sqrt(len(data))), alpha=0.5, normed=False)
	#plt.hist(scores2, histtype="stepfilled", bins=abs(math.sqrt(len(scores2))), alpha=0.5, normed=False)
	#plt.hist(data, histtype="stepfilled", bins=abs(math.log(len(data))/math.log(2)+1), alpha=0.5, normed=False)
	plt.show()

if __name__ == "__main__":
	bar2([23, 24], [5, 5])
	bar3([23, 24], [5, 5], 2)
	hist([[1,2,3,2,3,2,3], [2,3,3,4,2,2,3,3,3]])