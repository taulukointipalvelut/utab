#import csv
#from numpy.random import beta
import numpy as np
#import scipy as sp
import math
import matplotlib.pyplot as plt
from . import mstat_modules as mstat
import matplotlib.cm as cm
#import random
#import itertools

def bar_sd2(gov_percentage_list, std_list):
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

def bar_sd3(percentage_list, std_list, teamnum):
	if teamnum == 2:
		N = len(percentage_list)
		opp_percentage_list = [100-num for num in percentage_list]
		ind = np.arange(N)    # the x locations for the groups
		width = 0.25       # the width of the bars: can also be len(x) sequence

		p1 = plt.bar(ind, percentage_list, width, color='b', yerr=std_list)
		p3 = plt.bar(ind, percentage_list, width, color='r')
		p2 = plt.bar(ind, opp_percentage_list, width, color='w', bottom=percentage_list)

		plt.ylabel('percentages')
		plt.title('Motion fairness by gov/opp')
		plt.xticks(ind + width/2., ['R'+str(i+1) for i in range(N)])
		plt.yticks(np.arange(0, 110, 10))
		plt.legend((p3[0], p2[0]), ('Gov', 'Opp'))

		plt.show()
	else:
		print("nomodasfjpo;adsj")

def hist(data_list):
	plt.style.use('bmh')
	for data in data_list:
		plt.hist(data, histtype="stepfilled", bins=abs(math.sqrt(len(data))), alpha=0.5, normed=False)
	#plt.hist(scores2, histtype="stepfilled", bins=abs(math.sqrt(len(scores2))), alpha=0.5, normed=False)
	#plt.hist(data, histtype="stepfilled", bins=abs(math.log(len(data))/math.log(2)+1), alpha=0.5, normed=False)
	plt.show()

def line_graph_1d(data):
	plt.plot([i+1 for i in range(len(data))], data)
	plt.show()

def bar_1d(data):
	#plt.plot([i for i in range(len(data))], data)
	plt.bar([i+1 for i in range(len(data))], data)
	plt.show()

def bar_2d(data1, data2):
	#plt.plot([i for i in range(len(data))], data)
	plt.bar(data1, data2)
	plt.show()

def plot_gini(data):
	pass

def plot_ira(f1, f2, g, adjudicator_list, team_list, rounds, teamnum):
	adjudicator_ira_judge_indicator_dict = mstat.get_ira_judge_indicator_dict(f1, g, adjudicator_list, team_list, rounds, teamnum)
	adjudicator_and_ira_list = []
	for adjudicator in adjudicator_list:
		ira_judge_indicators = adjudicator_ira_judge_indicator_dict[adjudicator]
		adjudicator_and_ira_list.append([adjudicator.name, ira_judge_indicators[0], ira_judge_indicators[1]])

	adjudicator_and_ira_list.sort(key=lambda sub_list: sub_list[1], reverse=True)
	#plt.bar_2d([sub_list[0] for sub_list in adjudicator_and_ira_list], [sub_list[1] for sub_list in adjudicator_and_ira_list])
	#plt.bar_2d([sub_list[0] for sub_list in adjudicator_and_ira_list], [sub_list[1] for sub_list in adjudicator_and_ira_list])
	ira_list = [f2(sub_list[1]) for sub_list in adjudicator_and_ira_list]
	std_list = [sub_list[2] for sub_list in adjudicator_and_ira_list]
	adj_list = [sub_list[0] for sub_list in adjudicator_and_ira_list]
	print(adj_list)
	#bar_1d(ira_list)
	#print ira_list
	#print std_list
	plot_data_with_sd(ira_list, std_list)
	#plt.bar_1d(std_list)

def plot_ira_abs(adjudicator_list, team_list, rounds, teamnum):
	f1 = lambda lists: [(abs(sub_list[0]-sub_list[1])) for sub_list in lists]
	identical = lambda x: x
	plot_ira(f1, identical, identical, adjudicator_list, team_list, rounds, teamnum)

def plot_ira_pm(adjudicator_list, team_list, rounds, teamnum):
	f2 = lambda lists: [(sub_list[0]-sub_list[1]) for sub_list in lists]
	identical = lambda x: x
	plot_ira(f2, identical, identical, adjudicator_list, team_list, rounds, teamnum)

def plot_ira_sd(adjudicator_list, team_list, rounds, teamnum):
	f3 = lambda lists: [(sub_list[0]-sub_list[1])**2 for sub_list in lists]
	plot_ira(f3, math.sqrt, math.sqrt, adjudicator_list, team_list, rounds, teamnum)

"""
def plot_ira_3(adjudicator_list, team_list, rounds, teamnum):
	f3 = lambda lists: [(sub_list[0]-sub_list[1])**3 for sub_list in lists]
	g = lambda x: x**(1/float(3))
	plot_ira(f3, g, adjudicator_list, team_list, rounds, teamnum)
"""

"""
def plot_bar_data(bbax, bbay, bap, adj, adjl, adjr):
	dataset = {'dat1':(y1+y2+y3+y4+y5), 
	           'dat2':(y2+y3+y4+y5), 
	           'dat3':(y3+y4+y5), 
	           'dat4':(y4+y5), 
	           'dat5':y5}

	colors = [cm.RdBu(0.85), cm.RdBu(0.7), cm.PiYG(0.7), cm.Spectral(0.38), cm.Spectral(0.25)]
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 5))

    ax1.bar(x, dataset['dat1'], color=colors[0], edgecolor='w', align='center', label='Data1')
    ax1.bar(x, dataset['dat2'], color=colors[1], edgecolor='w', align='center', label='Data2')
    ax1.bar(x, dataset['dat3'], color=colors[2], edgecolor='w', align='center', label='Data3')
    ax1.bar(x, dataset['dat4'], color=colors[3], edgecolor='w', align='center', label='Data4')
    ax1.bar(x, dataset['dat5'], color=colors[4], edgecolor='w', align='center', label='Data5')

    if bap == 999:
        ax1.legend(bbox_to_anchor=(bbax, bbay))
    else:
        ax1.legend(bbox_to_anchor=(bbax, bbay), borderaxespad=bap)

    if adj != 0:
        plt.subplots_adjust(left = adjl, right = adjr)

    plt.plot()
"""

def plot_data_with_sd(data, sd_list):
	x = np.array([i+1 for i in range(len(data))])

	plt.bar(x, data, align = "center", yerr = sd_list, ecolor = "black")
	plt.show()

if __name__ == "__main__":
	bar2([23, 24], [5, 5])
	bar3([23, 24], [5, 5], 2)
	hist([[1,2,3,2,3,2,3], [2,3,3,4,2,2,3,3,3]])
	plot_1d([1,3,2,2,1,3,4,23,12,1])