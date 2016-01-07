# team_list, teamnum -> {gov:[1, 0, 0, 1, 0], opp:[]}
from scipy import stats
import numpy as np
import math

def get_ttest_text(data1, data2):
	t, p = stats.ttest_rel(data1, data2)
	text_list = ["t value: {0:.2f}".format(t), "p value: {0:.2f}".format(p)]

	if p < 0.05:
		text_list+=["there's a meaningful difference(5%  rejection)"]
	else:
		text_list+=['no meaningful difference(5%  rejection)']

	if p < 0.10:
		text_list+=["there's a meaningful difference(10%  rejection)"]
	else:
		text_list+=['no meaningful difference(10%  rejection)']

	return text_list

def gini(data):
	def get_avrsubt(data):
		subt = []
		for i in range(0, len(data)-1):
			for j in range(i+1, len(data)):
				subt.append(np.abs(data[i]-data[j]))
		if len(data) == 0:
			return 0
		else:
			return float(sum(subt))*2/(len(data)**2)
	avrsubt = get_avrsubt(data)
	gini = avrsubt/(2*np.mean(data))
	return gini

def std_2_distri(data):
	if len(data) != 0:
		Xbar = np.mean(data)
		return math.sqrt(Xbar*(1-Xbar)/float(len(data)))
	else:
		return 0

def get_wins_by_side(team_list, teamnum, round_num):
	if teamnum == 2:
		sides = ["gov", "opp"]
	else:
		sides = ["og", "oo", "cg", "co"]
	wins = {side:[] for side in sides}
	wins['n/a'] = []
	for team in team_list:
		wins[team.past_sides_sub[round_num-1]].append(team.wins_sub[round_num-1])
	return wins

def get_scores_by_side(team_list, teamnum, round_num):
	if teamnum == 2:
		sides = ["gov", "opp"]
	else:
		sides = ["og", "oo", "cg", "co"]
	scores = {side:[] for side in sides}
	scores['n/a'] = []
	for team in team_list:
		scores[team.past_sides_sub[round_num-1]].append(team.scores_sub[round_num-1])
	return scores

def get_win_percentage(wins, side):
	np_wins = np.array(wins[side])
	return np.mean(np_wins)