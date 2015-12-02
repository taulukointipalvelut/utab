# -*- coding: utf-8 -*-
FILENAME_TEAMS = 'dat/teams.csv'
FILENAME_ADJUDICATORS = 'dat/adjudicators.csv'
ROUND_NUM = 4
ROUND_NUM_ADJ = 2

import csv
from numpy.random import beta
import numpy as np
import scipy as sp
import math
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools

from modules.classes import *
from modules.internal_modules import *
from modules.commandline_modules import *

import readline
import sys
argvs = sys.argv
#MORE THAN THIS YOU NEED TO PREPARE teams.csv FOR EACH MODE
DEBATER_NUM_PER_TEAM = None
SPEAKING_NUM_PER_TEAM = None
TEAMNUM2 = True
try:
	MODE = argvs[1]
except:
	print "usage: python mstat.py [mode] #modes are: ACADEMIC, NA, PDA, ASIAN, BP, NAFA"
	sys.exit()
if MODE == "ACADEMIC":
	from modules.io_modules_for_academic import *
	DEBATER_NUM_PER_TEAM = 4
elif MODE == "NA":
	from modules.io_modules_for_na import *
	DEBATER_NUM_PER_TEAM = 2
elif MODE == "NAFA":
	from modules.io_modules_for_nafa import *
	DEBATER_NUM_PER_TEAM = 2
elif MODE == "PDA":
	from modules.io_modules_for_pda import *
	DEBATER_NUM_PER_TEAM = 3
elif MODE == "ASIAN":
	from modules.io_modules_for_asian import *
	DEBATER_NUM_PER_TEAM = 3
elif MODE == "BP":
	from modules.io_modules_for_bp import *
	DEBATER_NUM_PER_TEAM = 2
	TEAMNUM2 = False
else:
	print "usage: python mstat.py [mode] #modes are: ACADEMIC, NA, PDA, ASIAN, BP, NAFA"
	sys.exit()

class Team2(Team):
	def __init__(self, code, name, debater_names, institution_scale, institutions):
		Team.__init__(self, code, name, debater_names, institution_scale, institutions)
		self.watched_adjudicators = []

class Adjudicator2(Adjudicator):
	def __init__(self, name, reputation, judge_test, institutions, conflict_teams):
		Adjudicator.__init__(self, name, reputation, judge_test, institutions, conflict_teams)
		self.gave_points = []

def ret_scores_by_side(team_list, i, teamnum2):
	if teamnum2:
		scores_by_gov = []
		scores_by_opp = []
		for team in team_list:
			if i <= len(team.wins):
				if team.past_sides[i-1] == "gov":
					scores_by_gov.append(team.scores[i-1])
				else:
					scores_by_opp.append(team.scores[i-1])
		return [scores_by_gov, scores_by_opp]
	else:
		scores_by_og = []
		scores_by_oo = []
		scores_by_cg = []
		scores_by_co = []
		for team in team_list:
			if i <= len(team.wins):
				if team.past_sides[i-1] == "og":
					scores_by_og.append(team.scores[i-1])
				elif team.past_sides[i-1] == "oo":
					scores_by_oo.append(team.scores[i-1])
				elif team.past_sides[i-1] == "cg":
					scores_by_cg.append(team.scores[i-1])
				elif team.past_sides[i-1] == "co":
					scores_by_co.append(team.scores[i-1])
		return [scores_by_og, scores_by_oo, scores_by_cg, scores_by_co]

def ret_wins_by_side(team_list, i, teamnum2):
	if teamnum2:
		gov_wins, opp_wins = 0, 0
		for team in team_list:
			if i <= len(team.wins):
				if team.past_sides[i-1] == "gov":
					if team.wins[i-1] == 1:
						gov_wins += 1
				else:
					if team.wins[i-1] == 1:
						opp_wins += 1
		return [gov_wins, opp_wins]
	else:
		og_wins, oo_wins, cg_wins, co_wins = 0, 0, 0, 0
		for team in team_list:
			if i <= len(team.wins):
				if team.past_sides[i-1] == "og":
					og_wins += team.wins[i-1]
				elif team.past_sides[i-1] == "oo":
					oo_wins += team.wins[i-1]
				elif team.past_sides[i-1] == "cg":
					cg_wins += team.wins[i-1]
				elif team.past_sides[i-1] == "co":
					co_wins += team.wins[i-1]
		return [og_wins, oo_wins, cg_wins, co_wins]

def ret_scores(team_list, i):
	scores = []
	for team in team_list:
		if i <= len(team.scores):
			scores.append(team.scores[i-1])
	return scores

def avrsubt(data):
	subt = []
	for i in range(0, len(data)-1):
		for j in range(i+1, len(data)):
			subt.append(np.abs(data[i]-data[j]))
	if len(data) == 0:
		return 0
	else:
		return float(sum(subt))*2/(len(data)**2)

def gini(avrsubt, data):
	gini = avrsubt/(2*np.mean(data))
	return "{0:.3f}".format(gini)

def wins_analysis(gov_wins, opp_wins):
	if gov_wins+opp_wins == 0:
		Xbar = 0
		sd = 0
	else:
		Xbar = gov_wins / float(opp_wins+gov_wins)
		sd = math.sqrt(Xbar*(1-Xbar)/float(opp_wins+gov_wins))
	return Xbar, sd

def ttest_by_scores(scores_by_gov, scores_by_opp):
	t, p = stats.ttest_rel(scores_by_gov, scores_by_opp)

	if p < 0.10:
		return ["t value: {0:.2f}".format(t), "p value: {0:.2f}".format(p), "there's a meaningful difference(10%  rejection)"]
	else:
		return ["t value: {0:.2f}".format(t), "p value: {0:.2f}".format(p), 'no meaningful difference(10%  rejection)']

def strength_analysis(team):
	if len(team.scores) == 0:
		Xbar = 0
		sd = 0
	else:
		Xbar = sum(team.scores)/float(len(team.scores))
		if len(team.scores) == 1:
			sd = 0
		else:
			sd = math.sqrt((len(team.scores)/(len(team.scores)-1))*np.var(team.scores)/float(len(team.scores)))
	alpha, beta = Xbar-1.96*sd, Xbar+1.96*sd
	#print team.name+"'s real points exist in ["+str(alpha)+","+str(beta)+"] by 95%, ", Xbar, "+-", sd
	return "{0:20s} real points exist in [{1:.2f} ,{2:.2f}] by 95%, {3:.2f}+-{4:.2f}".format(team.name+'\'s', alpha, beta, Xbar, sd)

def export(export_rows):
	export_filename = "private/statistics.csv"
	with open(export_filename, "w") as g:
		writer = csv.writer(g)
		for export_row in export_rows:
			writer.writerow([export_row])

def show(export_rows):
	for export_row in export_rows:
		print export_row

def read_matchups(filename_matchups):






def barcode():
	# the bar
	x = np.where(np.random.rand(100) > 0.7, 1.0, 0.0)
	print x

	axprops = dict(xticks=[], yticks=[])
	barprops = dict(aspect='auto', cmap=plt.cm.binary, interpolation='nearest')

	fig = plt.figure()

	# a vertical barcode -- this is broken at present
	x.shape = len(x), 1
	ax = fig.add_axes([0.1, 0.3, 0.1, 0.6], **axprops)
	ax.imshow(x, **barprops)


	plt.show()

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

def bar3(percentage_list, sd_list, teamnum2):
	if teamnum2:
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
	"""
	scores_by_opp1 = [43.0, 35.0, 36.0, 32.0, 24.0, 34.0, 38.0]
	scores_by_gov1 = [30.0, 36.0, 32.0, 30.0, 31.0, 28.0, 33.0]
	scores_by_opp2 = [35.0, 34.0, 29.0, 30.0, 33.0, 30.0, 38.0]
	scores_by_gov2 = [32.0, 38.0, 39.0, 29.0, 25.0, 43.0, 31.0]
	scores_by_opp3 = [22.0, 30.0, 49.0, 32.0, 32.0, 33.0, 34.0]
	scores_by_gov3 = [31.0, 30.0, 37.0, 35.0, 21.0, 35.0, 37.0]
	scores_by_gov = scores_by_gov1+scores_by_gov2+scores_by_gov3
	scores_by_opp = scores_by_opp1+scores_by_opp2+scores_by_opp3
	scores = scores_by_gov+scores_by_opp

	scores_by_gov = [random.randint(1, 100) for i in range(1000)]
	scores_by_opp = [random.randint(1, 100) for i in range(1000)]
	scores_by_gov = beta(10, 3, size=50)
	scores_by_opp = beta(12, 7, size=50)
	"""
	for data in data_list:
		plt.hist(data, histtype="stepfilled", bins=abs(math.sqrt(len(data))), alpha=0.5, normed=False)
	#plt.hist(scores2, histtype="stepfilled", bins=abs(math.sqrt(len(scores2))), alpha=0.5, normed=False)
	#plt.hist(data, histtype="stepfilled", bins=abs(math.log(len(data))/math.log(2)+1), alpha=0.5, normed=False)
	plt.show()

def convertTeam2Team2(team_list_origin):
	team_list = []
	for team in team_list_origin:
		team2 = Team2(team.code, team.name, [], "", team.institutions)
		team_list.append(team2)
	return team_list

def convertAdjudicator2Adjudicator2(adjudicator_list_origin):
	adjudicator_list = []
	for adjudicator in adjudicator_list_origin:
		adjudicator2 = Adjudicator2(adjudicator.name, adjudicator.reputation, adjudicator.judge_test, adjudicator.institutions, adjudicator.conflict_teams)
		adjudicator_list.append(adjudicator2)
	return adjudicator_list_origin

def adjudicator_points_by_wins(adjudicator_list, TEAMNUM2):
	if TEAMNUM2:
		adj_scores_from_win_team = []
		adj_scores_from_lose_team = []
		for adjudicator in adjudicator_list:
			for i in range(len(adjudicator.watched_teams)):
				if adjudicator.watched_teams[2*i].wins[i] == 1:
					adj_scores_from_win_team.append(adjudicator.scores[i])
				else:
					adj_scores_from_lose_team += 1

def add_adjudicator_to_watched_adjudicators(results_of_adj, results, teamnum2, team_list, adjudicator_list):
	if teamnum2:
		team_adj_list_origin = []
		for result_of_adj in results_of_adj:
			team_adj_list_origin.extend([[result_of_adj[6], result_of_adj[0]], [result_of_adj[7], result_of_adj[0]]])
		team_adj_list = []
		for team_adj_origin in team_adj_list_origin:
			for team_adj in team_adj_list:
				if team_adj[0] == team_adj_origin[0] or team_adj[0] == team_adj_origin[0]:
					break
			else:
				team_adj_list.append(team_adj_origin)

		for team_adj in team_adj_list:
			team = None
			adj = None
			for team2 in team_list:
				if team2.name == team_adj[0]:
					team == team2
					break
			for adj2 in adjudicator_list:
				if adj2.name == team_adj[1]:
					adj = adj2
					break
			if team == None:
				print("no team named "+team_adj[0])
				break
			if team == None:
				print("no adjudicator named "+team_adj[1])
				break

			team.watched_adjudicators.append(adjudicator)

def add_points_to_gave_points(results_of_adj, results, adjudicator_list, team_list):
	

if __name__ == "__main__":
	team_list_origin = read_teams(FILENAME_TEAMS)
	adjudicator_list = read_adjudicators(FILENAME_ADJUDICATORS)

	team_list = convertTeam2Team2(team_list_origin)

	for k in range(ROUND_NUM):
		read_and_process_result(k+1, team_list)
	for k in range(ROUND_NUM_ADJ):
		read_and_process_result_adj(k+1, team_list, adjudicator_list, TEAMNUM2)

	for j in range(min(ROUND_NUM, ROUND_NUM_ADJ)):
		results = read_results('private/Results{0}.csv'.format(j+1))
		results_of_adj = read_results_of_adj('private/Results_of_adj{0}.csv'.format(j+1), TEAMNUM2)
		add_adjudicator_to_watched_adjudicators(results_of_adj, results, TEAMNUM2, team_list, adjudicator_list)
		add_points_to_gave_points(results_of_adj, results, adjudicator_list, team_list)

	#show_teams_scores(team_list, False)
	sort_team_list_by_score(team_list)
	sort_adjudicator_list_by_score(adjudicator_list)


	all_wins_by_side = []
	wins_by_side_list = []
	all_scores_by_side = []
	scores_by_side_list = []
	#all_percentage_list = []
	#all_std_list = []
	export_rows = []
	Xbar_list = []
	sd_list = []

	for i in range(ROUND_NUM):
		export_rows.append("-----------------------round {0:1d}-----------------------".format(i+1))
		scores = ret_scores(team_list, i+1)
		scores_by_side = ret_scores_by_side(team_list, i+1, TEAMNUM2)
		wins_by_side = ret_wins_by_side(team_list, i+1, TEAMNUM2)
		wins_by_side_list.append(wins_by_side)
		scores_by_side_list.append(scores_by_side)

		#print wins_by_side
		hist(scores_by_side)

		combinations_of_scores = list(itertools.combinations(scores_by_side, 2))
		combinations_of_wins = list(itertools.combinations(wins_by_side, 2))

		#percentage_list = []
		#if teamnum2:
		#	for team in team_list:
		#	percentage_list = [team.count(1)]
		#	#percentage_list.append(win_pair[0]/float(win_pair[0]+win_pair[1])*100)
		#	#std_list.append(np.std(win_pair[0]))


		#percentage_list = []
		#std_list = []

		for win_pair, score_pair, vs in zip(combinations_of_wins, combinations_of_scores, ["team1:team2", "team1:team3", "team1:team4", "team2:team3", "team2:team4", "team3:team4"]):
			export_rows.append(vs)
			export_rows.append("--t test--")
			export_rows.extend(ttest_by_scores(score_pair[0], score_pair[1]))
			export_rows.append("--wins analysis--")
			Xbar, sd = wins_analysis(win_pair[0], win_pair[1])
			Xbar_list.append(Xbar*100)
			sd_list.append(sd*100)
			export_rows.append("real win-point exist in [{0:.2f} ,{1:.2f}] by 95%, {2:.2f}+-{3:.2f}".format(Xbar-1.96*sd, Xbar+1.96*sd, Xbar, sd))

		export_rows.append("--gini index--")
		export_rows.append(gini(avrsubt(scores), scores))

	all_wins_by_side = wins_by_side_list[0]
	all_scores_by_side = scores_by_side_list[0]
	for i in range(len(scores_by_side_list)-1):
		for j in range(len(all_wins_by_side)):
			all_wins_by_side[j]+=wins_by_side_list[i+1][j]
			all_scores_by_side[j]+=scores_by_side_list[i+1][j]
	hist(all_scores_by_side)
	bar2(Xbar_list, sd_list)
	bar3(Xbar_list, sd_list, TEAMNUM2)

	export_rows.append("-----------------------overall-----------------------".format(i+1))
	export_rows.append("--t test--")
	for win_pair, score_pair, vs in zip(combinations_of_wins, combinations_of_scores, ["team1:team2", "team1:team3", "team1:team4", "team2:team3", "team2:team4", "team3:team4"]):
		export_rows.append(vs)
		export_rows.extend(ttest_by_scores(score_pair[0], score_pair[1]))
		export_rows.append("--wins analysis--")
		export_rows.append(wins_analysis(win_pair[0], win_pair[1]))
		export_rows.append("\n")

	export_rows.append("")
	for team in team_list:
		export_rows.append(strength_analysis(team))

	export(export_rows)
	show(export_rows)
	show_teams_scores(team_list, TEAMNUM2)
	sort_team_list_by_score(team_list)

	scores = []
	for team in team_list:
		if len(team.scores) != 0:
			scores.append(float(sum(team.scores))/len(team.scores))
		else:
			scores.append(0)
	rankings = [j+1 for j in range(len(scores))]
	plt.plot(rankings, scores)
	plt.show()

	team_list.sort(key=lambda team: sum(team.scores), reverse=True)

	scores = []
	for team in team_list:
		if len(team.scores) != 0:
			scores.append(float(sum(team.scores))/len(team.scores))
		else:
			scores.append(0)
	rankings = [j+1 for j in range(len(scores))]
	plt.plot(rankings, scores)
	plt.show()

	adjudicator_list.sort(key);kaldjsf;lakdsfupoiadsufoijdsaopu32-q948udoasfjopijopad

	scores = []
	for adjudicator in adjudicator_list:
		if len(adjudicator.scores) != 0:
			scores.append(float(sum(adjudicator.scores))/len(adjudicator.scores))
		else:
			scores.append(0)
	rankings = [j+1 for j in range(len(scores))]
	plt.plot(rankings, scores)
	plt.show()

pass
