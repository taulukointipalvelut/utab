# team_list, teamnum -> {gov:[1, 0, 0, 1, 0], opp:[]}
from scipy import stats
import numpy as np
import math
from .property_modules import *
import copy

def get_ttest_text(data1, data2):
	t, p = stats.ttest_rel(data1, data2)
	text_list = ["mean of data1: {0:.2f}, mean of data2: {1:.2f}".format(np.mean(data1), np.mean(data2)), "t value: {0:.2f}".format(t), "p value: {0:.2f}".format(p)]

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

def std(data):
	return np.std(data)

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

def get_(team_list, name):
	for team in team_list:
		for debater in team.debaters:
			if debater.name:
				pass

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

def get_scores_by_half(team_list, teamnum, round_num):
	if teamnum == 4:
		#scores = {half:[] for half in ["opening", "closing", "government", "opposition"]}
		scores_by_side = get_scores_by_side(team_list, teamnum, round_num)
		scores["opening"] = scores_by_side["og"]+scores_by_side["oo"]
		scores["closing"] = scores_by_side["cg"]+scores_by_side["co"]
		scores["government"] = scores_by_side["og"]+scores_by_side["cg"]
		scores["opposition"] = scores_by_side["oo"]+scores_by_side["co"]

		return scores

def ira_judge(adjudicator_list, team_list, rounds, teamnum):
	ira_judge_list = []
	adjudicator_and_score_dict = get_adjudicator_and_score_dict(adjudicator_list, team_list, teamnum, rounds)
	score_and_average_dict = convert_adjudicator_and_score_dict2score_and_average_dict(adjudicator_list, team_list, adjudicator_and_score_dict)
	#print score_and_average_dict

	adjudicator_list_cp = copy.copy(adjudicator_list)
	adjudicator_list_cp.sort(key=lambda adjudicator: adjudicator.average(), reverse=True)
	adjudicator_ranking_dict = {adjudicator:i for i, adjudicator in enumerate(adjudicator_list_cp)}#ranking is available

	return score_and_average_dict

def get_ira_judge_indicator_dict(f, g, adjudicator_list, team_list, rounds, teamnum):
	score_and_average_dict = ira_judge(adjudicator_list, team_list, rounds, teamnum)
	diff_dict = {adjudicator:f(score_and_average_dict[adjudicator]) for adjudicator in adjudicator_list}

	#print diff2_list
	adjudicator_ira_judge_indicator_dict = {adjudicator:None for adjudicator in adjudicator_list}
	for adjudicator in adjudicator_list:
		if len(diff_dict[adjudicator]) != 0:
			adjudicator_ira_judge_indicator_dict[adjudicator] = [np.mean(diff_dict[adjudicator]), g(np.std(diff_dict[adjudicator]))]
			#print adjudicator.name
			#print diff_dict[adjudicator]
			#print adjudicator_ira_judge_indicator_dict[adjudicator]
		else:
			adjudicator_ira_judge_indicator_dict[adjudicator] = [0, 0]

	return adjudicator_ira_judge_indicator_dict
	
def convert_adjudicator_and_score_dict2score_and_average_dict(adjudicator_list, team_list, adjudicator_and_score_dict):
	score_and_average_dict = {adjudicator:[] for adjudicator in adjudicator_list}
	for adjudicator in adjudicator_list:
		for key, values_list in list(adjudicator_and_score_dict.items()):
			for values in values_list:
				if values[0] == adjudicator:
					score_and_average_dict[values[0]].append([values[1], key.average()])

	return score_and_average_dict

def get_adjudicator_and_score_dict(adjudicator_list, team_list, teamnum, rounds):#=>{team(instance):[[adjudicator(instance), scoreByAdjudicator]]}
	adjudicator_by_team_dict = {team:[] for team in team_list}
	for i in range(rounds):
		for adjudicator in adjudicator_list:
			#print adjudicator.watched_teams_sub
			for j in range(teamnum):
				watched_team = adjudicator.watched_teams_sub[i*teamnum+j]
				if watched_team == 'n/a':
					continue
				adjudicator_by_team_dict[watched_team].append([adjudicator, watched_team.scores_sub[i]])

	return adjudicator_by_team_dict

def get_debater_score(team_list):
	debater_list = [debater for team in team_list for debater in team.debaters]

	return [sum(debater.scores) for debater in debater_list]

def get_win_ratio(wins, side):
	np_wins = np.array(wins[side])
	return np.mean(np_wins)