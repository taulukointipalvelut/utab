# -*- coding: utf-8 -*-
from .classes import *
from .bit_modules import *
from .property_modules import *
from datetime import datetime
import random
import shutil
import csv
import sys
import os
import math
import copy
import re
import itertools
try:
	import readline
except:
	pass

def round_str2float(ele, m):
	if ele == 'n/a':
		return 'n/a'
	else:
		return round(ele, m)
	
def export_blank_results(allocations, round_num, style_cfg, filename):
	if os.path.exists(filename):
		print("the file", filename, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename, "w") as g:
		writer = csv.writer(g)
		if style_cfg["team_num"] == 4:
			win_text = "Win-points[0, 1, 2, 3]"
			position_text = "Position[og, oo, cg, co]"
			sides = ["og", "oo", "cg", "co"]
		else:
			win_text = "Win[0:lose, 1:win]"
			position_text = "Side[gov, opp]"
			sides = ["gov", "opp"]
		writer.writerow(["team_name", "name"]+["R"+str(round_num)+"-"+str(i+1) for i in range(len(style_cfg["score_weight"]))]+[win_text]+["Opponent"+str(i+1) for i in range(style_cfg["team_num"]-1)]+[position_text])

		for lattice in allocations:
			for k, team in enumerate(lattice.grid.teams):
				for member in team.debaters:
					writer.writerow([team.name, member.name]+[0 for i in range(len(style_cfg["score_weight"]))]+[""]+list(set([t.name for t in lattice.grid.teams])-set(team.name))+[sides[k]])

def read_results(filename, style_cfg):
	f = open(filename, 'r')#style_cfg => [[1, 1], [1, 1], [1, 1], [1, 1]]
	reader = csv.reader(f)
	header = next(reader)
	positions = len(style_cfg["score_weight"])
	team_num = style_cfg["team_num"]
	results = []
	for row in reader:
		results.append([row[0], row[1]]+[float(row[2+i]) for i in range(positions)]+[int(row[2+positions])]+[row[3+positions+j] for j in range(team_num-1)]+[row[2+team_num+positions]])
	return results

def read_and_process_result(round_num, team_list, style_cfg, filename_results):
	teamnum = style_cfg["team_num"]
	if check_results(filename_results, style_cfg):
		print("Results file broken")
		raise NameError('Results file broken')
	results_list = read_results(filename_results, style_cfg)
	team_list_temp = []
	debater_list_temp = []
	debater_num_per_team = style_cfg["debater_num_per_team"]
	positions = len(style_cfg["score_weight"])
	score_weight = style_cfg["score_weight"]
	team_num = style_cfg["team_num"]
	for i in range(int(len(results_list)/debater_num_per_team)):#results=>[team name, name, R[i] 1st, R[i] 2nd, R[i] rep, win?lose?, opponent name, gov?opp?]
		for team in team_list:
			if team.name == results_list[debater_num_per_team*i][0]:
				member_names = [results_list[debater_num_per_team*i+j][1] for j in range(debater_num_per_team)]
				member_score_lists = [results_list[debater_num_per_team*i+j][2:2+positions] for j in range(debater_num_per_team)]
				side = results_list[debater_num_per_team*i][2+positions+team_num]
				win = results_list[debater_num_per_team*i][2+positions]
				for debater in team.debaters:
					for member_name, member_score_list in zip(member_names, member_score_lists):
						if debater.name == member_name:
							score = 0
							sum_weight = 0
							for sc, weight in zip(member_score_list, score_weight):
								score += sc
								sum_weight += weight
							if sum_weight == 0:
								print("error: Results file(Results"+str(round_num)+".csv) broken")
							else:
								score = score/float(sum_weight)
								debater.finishing_process(member_score_list, score)
								debater_list_temp.append(debater)
								break
					else:
						print("error: Results file(Results"+str(round_num)+".csv) broken")

				if team_num == 4:
					margin = 0
				else:
					opp_team_score = 0
					for results in results_list:
						if results[0] == results_list[debater_num_per_team*i][3+positions]:
							opp_team_score += sum(results[2:2+positions])
					margin = sum([sum(member_score_list) for member_score_list in member_score_lists])-opp_team_score
				team.finishing_process(opponent=[results_list[debater_num_per_team*i][3+positions+j] for j in range(team_num-1)], score=sum([sum(member_score_list) for member_score_list in member_score_lists]), side=side, win=win, margin=margin)
				team_list_temp.append(team)

	all_debater_list = [d for t in team_list for d in t.debaters]
	ranking = 1
	for debater in all_debater_list:
		debater.rankings.append(ranking)
		debater.rankings_sub.append(ranking)
		ranking += 1
	rest_debater_list = [d for d in all_debater_list if d not in debater_list_temp]
	for debater in rest_debater_list:
		debater.score_lists_sub.append(['n/a']*positions)
		debater.scores_sub.append('n/a')
		debater.rankings_sub.append('n/a')

	for team in team_list:
		if team.name not in [results[0] for results in results_list]:
			if team.available:
				print("team: {0:15s} not in results: {1}".format(team.name, filename_results))

	for team in team_list:
		for debater in team.debaters:
			if debater.name not in [results[1] for results in results_list]:
				if team.available:
					print("debater: {0:15s} not in results: {1}".format(debater.name, filename_results))

	rest_team_list = [t for t in team_list if t not in team_list_temp]
	for team in rest_team_list:
		team.dummy_finishing_process(team_num)

def export_random_result(allocations, round_num, style_cfg, filename):
	if os.path.exists(filename):
		print("the file", filename, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename, "w") as g:
		writer = csv.writer(g)
		if style_cfg["team_num"] == 4:
			win_text = "Win-points[0, 1, 2, 3]"
			position_text = "Position[og, oo, cg, co]"
			sides = ["og", "oo", "cg", "co"]
		else:
			win_text = "Win[0:lose, 1:win]"
			position_text = "Side[gov, opp]"
			sides = ["gov", "opp"]
		writer.writerow(["team_name", "name"]+["R"+str(round_num)+"-"+str(i+1) for i in range(len(style_cfg["score_weight"]))]+[win_text]+["Opponent"+str(i+1) for i in range(style_cfg["team_num"]-1)]+[position_text])

		for lattice in allocations:
			teams_score_lists_raw = []
			for i in range(style_cfg["team_num"]):
				teams_score_lists_raw.append([random.randint(73, 77)*float(w) for w in style_cfg["score_weight"]])
			teams_member_lists_raw = [copy.copy(lattice.grid.teams[i].debaters) for i in range(style_cfg["team_num"])]
			teams_member_lists = [random.shuffle(team_member_list) for team_member_list in teams_member_lists_raw]

			teams_score_lists_all_info = []#=>[[ [a_1, a_2, a_3], [] ],[],[],[]]
			for team_score_list_raw in teams_score_lists_raw:
				team_score_list_all_info = []
				for score in team_score_list_raw:
					team_score_list_all_info.append([score + random.randint(-2,+2), score + random.randint(-2,+2), score + random.randint(-2,+2)])
				teams_score_lists_all_info.append(team_score_list_all_info)

			teams_score_lists_averaged = []
			for team_score_list_all_info in teams_score_lists_all_info:
				team_score_list_averaged = []
				for score_list in team_score_list_all_info:
					team_score_list_averaged.append(sum(score_list[0:len(lattice.panel)+1])/(len(lattice.panel)+1))
				teams_score_lists_averaged.append(team_score_list_averaged)

			if style_cfg["team_num"] == 4:
				sides = ["og", "oo", "cg", "co"]
			else:
				sides = ["gov", "opp"]
			teams_dict = {side: sum(team_score_list_raw) for side, team_score_list_raw in zip(sides, teams_score_lists_raw)}
			teams_dict_sorted = sorted(list(teams_dict.items()), key=lambda x:x[1])
			for i, k in enumerate(teams_dict_sorted):
				teams_dict[k[0]] = i

			win_points = [teams_dict[side] for side in sides]

			teams_score_lists_each = []

			if style_cfg["reply"]:
				reply_indexes = style_cfg["reply"]
				random.shuffle(reply_indexes)
				reply_indexes_chosen = reply_indexes[:style_cfg["num_of_reply"]]
				for team_score_list_averaged in teams_score_lists_averaged:
					team_score_lists_each = []
					for k in range(len(team_score_list_averaged)-1):
						team_score_list_each = [0 for i in range(len(style_cfg["score_weight"]))]
						team_score_list_each[k] = team_score_list_averaged[k]
						if k in reply_indexes_chosen:
							team_score_list_each[-1] = team_score_list_averaged[-1]
						team_score_lists_each.append(team_score_list_each)
					teams_score_lists_each.append(team_score_lists_each)
			else:
				for team_score_list_averaged in teams_score_lists_averaged:
					team_score_lists_each = []
					for k, score in enumerate(team_score_list_averaged):
						team_score_list_each = [0 for i in range(len(style_cfg["score_weight"]))]
						team_score_list_each[k] = score
						team_score_lists_each.append(team_score_list_each)
					teams_score_lists_each.append(team_score_lists_each)

			for k, team_score_list_each in enumerate(teams_score_lists_each):
				for j, score_list in enumerate(team_score_list_each):
					writer.writerow([lattice.grid.teams[k].name, lattice.grid.teams[k].debaters[j].name]+score_list+[win_points[k]]+list(set([t.name for t in lattice.grid.teams])-set([lattice.grid.teams[k].name]))+[sides[k]])					

def read_teams(filename, style_cfg):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	debater_num_per_team = style_cfg["debater_num_per_team"]
	teams = []
	for code, raw_row in enumerate(reader):
		row = [raw_one.strip() for raw_one in raw_row]
		if row[0] != '':
			teams.append(Team(code, row[0], [row[1+i] for i in range(debater_num_per_team)], row[1+debater_num_per_team], row[2+debater_num_per_team:]))#=>code, name, member_names
	return teams

def create_rows_for_results_of_debaters(team_list, style_cfg):
	individual_score_rows = []
	score_weight = style_cfg["score_weight"]
	for team in team_list:
		for debater in team.debaters:
			row = [debater.name, team.name]
			for i, score_list in enumerate(debater.score_lists_sub):
				row.extend([round_str2float(score, 2) for score in score_list])
				row.append(round(debater.average_in_round(i+1, style_cfg), 2))
				
			row.insert(2, round(debater.average(style_cfg), 2))

			row.insert(2, round(debater.sum_scores(style_cfg), 2))
			row.insert(4, round(debater.sd(style_cfg), 2))
			individual_score_rows.append(row)

	header = ["ranking", "name", "team name", "sum", "average", "sd"]
	for i in range(int(len(individual_score_rows[0])-5)//(len(style_cfg["score_weight"])+1)):
		header.extend(["Round"+str(i+1)+"-"+str(j+1) for j in range(len(style_cfg["score_weight"]))]+["round"+str(i+1)+" average"])

	return [header]+individual_score_rows
	
def insert_ranking_for_results_of_debaters(individual_score_rows):
	individual_score_rows_cp = copy.copy(individual_score_rows)
	header = individual_score_rows_cp.pop(0)
	individual_score_rows_cp.sort(key=lambda row: (row[2], -row[4]), reverse=True)
	ranking = 1
	stay = 0
	for k in range(len(individual_score_rows_cp)-1):
		if individual_score_rows_cp[k][2] != individual_score_rows_cp[k+1][2]:
			individual_score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			individual_score_rows_cp[k].insert(0, ranking)
			stay += 1
	individual_score_rows_cp[-1].insert(0, ranking)

	return [header] + individual_score_rows_cp

def create_rows_for_results_of_teams(team_list, style_cfg):
	score_rows = []
	for team in team_list:
		row = [team.name]
		scores2_sub = [round_str2float(score, 2) for score in team.scores_sub]

		row.append(team.sum_wins())
		row.append(round(team.sum_scores(), 2))
		row.append(round(team.margin, 2))
		row.append(round(team.average(), 2))
		row.append(round(team.sd(), 2))
		row.extend(scores2_sub)
		score_rows.append(row)

	if style_cfg["team_num"] == 2:
		win_text = "wins"
	else:
		win_text = "win-points"
	header = ["ranking", "team name"]+[win_text]+["sum", "margin", "average", "sd"]
	for i in range(len(score_rows[0])-6):
		header.append("round"+str(i+1))

	return [header]+score_rows

def insert_ranking_for_results_of_teams(score_rows, style_cfg):
	score_rows_cp = copy.copy(score_rows)
	header = score_rows_cp.pop(0)
	score_rows_cp.sort(key=lambda row: (row[1], row[2], row[3], -row[5]), reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(score_rows_cp)-1):
		if score_rows_cp[k][2] != score_rows_cp[k+1][2] or score_rows_cp[k][1] != score_rows_cp[k+1][1] or score_rows_cp[k][3] != score_rows_cp[k+1][3]:
			score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			score_rows_cp[k].insert(0, ranking)
			stay += 1
	score_rows_cp[-1].insert(0, ranking)

	return [header] + score_rows_cp

def create_rows_for_results_of_adjudicators(adjudicator_list):
	adjudicator_score_rows = []
	for adjudicator in adjudicator_list:
		row = [adjudicator.name, round(adjudicator.average(), 2), round(adjudicator.sd(), 2)] + [round_str2float(ele, 2) for ele in adjudicator.scores_sub]#->[name, average_score, scores]
		adjudicator_score_rows.append(row)

	header = ["ranking", "name", "average", "sd"]
	header += ["R"+str(i+1)+" average" for i in range(len(adjudicator_score_rows[0])-3)]

	return [header] + adjudicator_score_rows

def insert_ranking_for_results_of_adjudicators(adjudicator_score_rows):
	adjudicator_score_rows_cp = copy.copy(adjudicator_score_rows)
	header = adjudicator_score_rows_cp.pop(0)
	adjudicator_score_rows_cp.sort(key=lambda row: (row[1], -row[2]), reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(adjudicator_score_rows_cp)-1):
		if adjudicator_score_rows_cp[k][1] != adjudicator_score_rows_cp[k+1][1]:
			adjudicator_score_rows_cp[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			adjudicator_score_rows_cp[k].insert(0, ranking)
			stay += 1

	adjudicator_score_rows_cp[-1].insert(0, ranking)

	return [header] + adjudicator_score_rows_cp

def create_rows_for_adj_info(adjudicator_list):
	adjudicator_score_rows = []
	for adjudicator in adjudicator_list:
		institutions_text = ""
		watched_teams_text = ""
		conflict_teams_text  = ""
		watched_teams = list(set(adjudicator.watched_teams))
		for institution in adjudicator.institutions:
			institutions_text += institution + ", "
		for watched_team in watched_teams:
			watched_teams_text += watched_team.name + ", "
		for conflict_team in adjudicator.conflict_teams:
			conflict_teams_text += conflict_team + ", "
		adjudicator_score_rows.append([str(adjudicator.active_num_as_chair), str(adjudicator.active_num-adjudicator.active_num_as_chair), institutions_text, conflict_teams_text, watched_teams_text])

	header = ["chair", "panel", "institutions", "conflict", "watched teams"]

	return [header]+adjudicator_score_rows

def export_adj_info(adjudicator_list, filename_adj_info):
	adjudicator_score_rows1 = create_rows_for_results_of_adjudicators(adjudicator_list)
	adjudicator_score_rows2 = create_rows_for_adj_info(adjudicator_list)
	adjudicator_score_rows = [row1+row2 for row1, row2 in zip(adjudicator_score_rows1, adjudicator_score_rows2)]

	adjudicator_score_rows_with_ranking = insert_ranking_for_results_of_adjudicators(adjudicator_score_rows)

	if os.path.exists(filename_adj_info):
		print("the file", filename_adj_info, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename_adj_info, "w") as g:
		writer = csv.writer(g)
		for row in adjudicator_score_rows_with_ranking:
			writer.writerow(row)

def export_results(team_list, adjudicator_list, filename_adj_res, filename_deb_res, filename_tm_res, style_cfg):
	individual_score_rows = create_rows_for_results_of_debaters(team_list, style_cfg)
	individual_score_rows = insert_ranking_for_results_of_debaters(individual_score_rows)

	if os.path.exists(filename_adj_res):
		print("the file", filename_adj_res, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename_deb_res, "w") as g:
		writer = csv.writer(g)
		for row in individual_score_rows:
			writer.writerow(row)

	score_rows = create_rows_for_results_of_teams(team_list, style_cfg)
	score_rows = insert_ranking_for_results_of_teams(score_rows, style_cfg)

	if os.path.exists(filename_tm_res):
		print("the file", filename_tm_res, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename_tm_res, "w") as g:
		writer = csv.writer(g)
		for row in score_rows:
			writer.writerow(row)
	
	adjudicator_score_rows = create_rows_for_results_of_adjudicators(adjudicator_list)
	adjudicator_score_rows = insert_ranking_for_results_of_adjudicators(adjudicator_score_rows)

	if os.path.exists(filename_adj_res):
		print("the file", filename_adj_res, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename_adj_res, "w") as g:
		writer = csv.writer(g)
		for row in adjudicator_score_rows:
			writer.writerow(row)

def export_teams(filename_teams, team_list, style_cfg):
	with open(filename_teams, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["team name"]+["name" for i in range(style_cfg["debater_num_per_team"])]+["scale", "institution1", "institution2", "institution3", "institution4", "institution5", "institution6"])
		for team in team_list:
			export_row = [team.name]+[d.name for d in team.debaters]+[team.institution_scale]
			export_row.extend(team.institutions)
			writer.writerow(export_row)
			
def check_results(filename, style_cfg):
	f = open(filename, 'r')
	reader = csv.reader(f)

	header = next(reader)
	regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

	results_lists = []

	positions = len(style_cfg["score_weight"])
	team_num = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	for row in reader:
		for ele in row:
			hit = regexp.search(ele)
			if hit is None:
				print(("warning: results file is using unknown character(fullwidth forms or other symbols)", ele))
		results_lists.append([row[0], row[1]]+[float(row[2+i]) for i in range(positions)]+[int(row[2+positions])]+[row[3+positions+j] for j in range(team_num-1)]+[row[2+positions+team_num]])

	if team_num == 4:
		for i in range(int(len(results_lists)/debater_num_per_team)):
			team_names = [results_lists[debater_num_per_team*i+j][0] for j in range(debater_num_per_team)]
			teams_name_pairs = list(itertools.combinations(team_names, 2))
			for teams_name_pair in teams_name_pairs:
				if teams_name_pair[0] != teams_name_pair[1]:
					print(("error in team name column, row:"+str(debater_num_per_team*i+3)))
					return True

		multi2 = {results_list[1]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[1]] += 1

		for k, v in list(multi2.items()):
			if v > 1:
				print(("warning in debater name column, row(appears twice):"+k))

		for i, results_list in enumerate(results_lists):
			if results_list[2:2+positions].count(0) == 0:
				print(("warning in debater score column, row:"+str(i+3)))
			elif results_list[2:2+positions].count(0) == positions:
				print(("warning in debater score column, row:"+str(i+3)))

		wins = [0 for i in range(team_num)]
		try:
			for i, results_list in enumerate(results_lists):
				wins[results_list[2+positions]] += 1
		except:
			print(("error in win column, unexpected value, row:")+str(i+3))
			print("Unexpected error:", sys.exc_info()[0])
			return True

		wins_pairs = list(itertools.combinations(wins, 2))
		for wins_pair in wins_pairs:
			if wins_pair[0] != wins_pair[1]:
				print("error in win column")
				return True

		if team_num == 4:
			sides = {"og":0, "oo":0, "cg":0, "co":0}
		else:
			sides = {"gov":0, "opp":0}

		try:
			for i, results_list in enumerate(results_lists):
				sides[results_list[2+positions+team_num]] += 1
		except:
			print(("error in side column, unexpected value, row:")+str(i+3))
			print("Unexpected error:", sys.exc_info()[0])
			return True

		sides_pairs = list(itertools.combinations(list(sides.values()), 2))
		for sides_pair in sides_pairs:
			if sides_pair[0] != sides_pair[1]:
				print("error in side column")
				return True

		if team_num == 4:
			opponents1, opponents2, opponents3, opponents4 = [], [], [], []
			for results_list in results_lists:
				opponents1.extend([results_list[3+positions], results_list[4+positions], results_list[5+positions]])
				opponents2.extend([results_list[0], results_list[4+positions], results_list[5+positions]])
				opponents3.extend([results_list[0], results_list[3+positions], results_list[5+positions]])
				opponents4.extend([results_list[0], results_list[3+positions], results_list[4+positions]])
			if set(opponents1) != set(opponents2) or set(opponents1) != set(opponents3) or set(opponents1) != set(opponents4) or set(opponents2) != set(opponents3) or set(opponents2) != set(opponents4) or set(opponents3) != set(opponents4):
				print("error in team and the opponent column")
				return Trueaa
		else:
			opponents = {results_list[0]:results_list[3+positions] for results_list in results_lists}
			opponents2 = {results_list[3+positions]:results_list[0] for results_list in results_lists}

			if opponents != opponents2:
				print("error in team and the opponent column")
				return True

		return False

def save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name):
	export_filename_aj = workfolder_name+"temp/aj.csv"
	export_filename_vn = workfolder_name+"temp/vn.csv"
	export_filename_tm = workfolder_name+"temp/tm.csv"
	with open(export_filename_aj, "w") as g:
		writer = csv.writer(g)
		for adjudicator in adjudicator_list:
			tf = 1 if adjudicator.absent else 0
			export_row = [adjudicator.name, tf]
			writer.writerow(export_row)
	with open(export_filename_vn, "w") as g:
		writer = csv.writer(g)
		for venue in venue_list:
			tf = 1 if venue.available else 0
			export_row = [venue.name, tf, venue.priority]
			writer.writerow(export_row)
	with open(export_filename_tm, "w") as g:
		writer = csv.writer(g)
		for team in team_list:
			tf = 1 if team.available else 0
			export_row = [team.name, tf]
			export_row.extend([debater.name for debater in team.debaters])
			export_row.append(team.institution_scale)
			export_row.extend(team.institutions)
			writer.writerow(export_row)
	export_teams(filename_teams, team_list, style_cfg)
	export_venues(filename_venues, venue_list)
	export_adjudicators(filename_adjudicators, adjudicator_list)

def load(adjudicator_list, venue_list, team_list, style_cfg, workfolder_name):
	export_filename_aj = workfolder_name+"temp/aj.csv"
	export_filename_vn = workfolder_name+"temp/vn.csv"
	export_filename_tm = workfolder_name+"temp/tm.csv"
	debater_num_per_team = style_cfg["debater_num_per_team"]
	try:
		f = open(export_filename_aj, 'r')
		reader = csv.reader(f)
		for row in reader:
			for adjudicator in adjudicator_list:
				if row[0] == adjudicator.name:
					if int(row[1]) == 1:
						adjudicator.absent = True
					else:
						adjudicator.absent = False
		f = open(export_filename_vn, 'r')
		reader = csv.reader(f)
		for row in reader:
			for venue in venue_list:
				if row[0] == venue.name:
					if int(row[1]) == 1:
						venue.available = True
					else:
						venue.available = False
					venue.priority = int(row[2])
					break
			else:
				new_venue = Venue(row[0], row[2])
				new_venue.available = True if int(row[1]) == 1 else False
				venue_list.append(new_venue)
		f = open(export_filename_tm, 'r')
		reader = csv.reader(f)
		for row in reader:
			for team in team_list:
				if row[0] == team.name:
					if int(row[1]) == 1:
						team.available = True
					else:
						team.available = False
					break
			else:
				new_team = Team(len(team_list), row[0], [row[2+i] for i in range(debater_num_per_team)], row[2+debater_num_per_team], row[3+debater_num_per_team:])
				new_team.available = True if int(row[1]) == 1 else False
				team_list.append(new_team)
	except:
		pass
		"""
		print "Unexpected error:", sys.exc_info()[0]
		print "load failed"
		"""






def read_matchup(filename_matchup, teamnum):
	f = open(filename_matchup, 'r')
	reader = csv.reader(f)
	header = next(reader)
	raw_data_rows = []
	for row in reader:
		raw_data_rows.append([row[i] for i in range(4+teamnum)])
	return raw_data_rows

def str2float(ele):
	if ele == "n":
		return 0
	else:
		return float(ele)

def read_venues(filename):
	venue_list = []
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	for row in reader:
		venue_list.append(Venue(row[0], int(row[1])))
	return venue_list

def read_adjudicators(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	code = 0
	adjudicator_list = []
	for row in csv_data:
		if row[0] != '':
			adjudicator_list.append(Adjudicator(code, row[0], float(row[1]), float(row[2]), row[3:13], row[13:]))
			code += 1

	return adjudicator_list

def read_results_of_adj(filename, teamnum):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	results = []
	for row in reader:
		data_row = [row[0]]+[str2float(row[i+1]) for i in range(3+teamnum)]+[row[i+4+teamnum] for i in range(teamnum)]
		results.append(data_row)
	return results

def read_and_process_result_adj(round_num, team_list, adjudicator_list, teamnum, filename_results_of_adj):
	if check_results_of_adj(filename_results_of_adj, teamnum):
		print("Results of adj file broken")
		raise NameError('Results file broken')
	results_of_adj_list = read_results_of_adj(filename_results_of_adj, teamnum)

	adjudicator_temp = []
	for results_of_adj in results_of_adj_list:
		for adjudicator in adjudicator_list:
			if adjudicator.name == results_of_adj[0]:
				if results_of_adj[1:4+teamnum].count(0) == 3+teamnum:
					score = 0
				else:
					score = float(sum(results_of_adj[1:4+teamnum]))/(3+teamnum-results_of_adj[1:4+teamnum].count(0))
				teams = []
				for j in range(teamnum):
					for team in team_list:
						if team.name == results_of_adj[4+teamnum+j]:
							teams.append(team)
				if len(teams) != teamnum:
					print("results_of_adj file broken", str(teams))
					break
				else:
					if results_of_adj[3+teamnum] == 0:
						adjudicator.finishing_process(score=score, teams=teams, watched_debate_score=sum([t.score for t in teams]), chair=True)
					else:
						adjudicator.finishing_process(score=score, teams=teams, watched_debate_score=sum([t.score for t in teams]), chair=False)
					adjudicator_temp.append(adjudicator)

	adjudicator_temp.sort(key=lambda adjudicator: adjudicator.watched_debate_score, reverse=True)
	for k, adjudicator in enumerate(adjudicator_temp):
		adjudicator.watched_debate_ranks.append(k+1)
		adjudicator.watched_debate_ranks_sub.append(k+1)
	rest_adjudicator_list = [adjudicator for adjudicator in adjudicator_list if adjudicator not in adjudicator_temp]
	for adj in rest_adjudicator_list:
		adj.watched_debate_ranks_sub.append('n/a')

	for adjudicator in rest_adjudicator_list:
		adjudicator.dummy_finishing_process(teamnum)
	
def export_random_result_adj(allocations, round_num, style_cfg, filename):
	teamnum = style_cfg["team_num"]
	if os.path.exists(filename):
		print("the file", filename, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(filename, "w") as g:
		writer = csv.writer(g)
		if teamnum == 4:
			sides = ["og", "oo", "cg", "co"]
		elif teamnum == 2:
			sides = ["gov", "opp"]
		writer.writerow(["name"]+["R"+str(round_num)+" "+side for side in sides]+["R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair"]+["team"+str(i+1) for i in range(teamnum)])
		
		for lattice in allocations:
			adjudicator_base_scores = [random.randint(3,8), random.randint(3,8), random.randint(3,8)]
			chair_scores_all_info = [adjudicator_base_scores[0] + random.randint(-2,+2) for i in range(teamnum+2)]
			panels_scores = [random.randint(-2,+2) + adjudicator_base_scores[1], random.randint(-2,+2) + adjudicator_base_scores[2]]

			writer.writerow([lattice.chair.name]+[chair_scores_all_info[i] for i in range(teamnum+len(lattice.panel))]+[0 for i in range(2-len(lattice.panel))]+[0]+[team.name for team in lattice.grid.teams])
			for panel in lattice.panel:
				writer.writerow([panel.name]+[0 for i in range(teamnum+2)]+[panels_scores[0]]+[team.name for team in lattice.grid.teams])

			"""
			if len(lattice.panel) == 2:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			elif len(lattice.panel) == 1:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			else:
				writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
			"""
	"""
	if len(allocations[0].grid.teams) == 2:
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" og", "R"+str(round_num)+" oo", "R"+str(round_num)+" cg", "R"+str(round_num)+" co", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2", "team3", "team4"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team3 = random.randint(-2,+2) + chair_base_score
				chair_score_from_team4 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
	"""

def export_blank_results_of_adj(allocations, round_num, filename):
	if len(allocations[0].grid.teams) == 2:

		if os.path.exists(filename):
			print("the file", filename, "already exists")
			input("Press Enter to overwrite the file > ")
		with open(filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			for lattice in allocations:
				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:

		if os.path.exists(filename):
			print("the file", filename, "already exists")
			input("Press Enter to overwrite the file > ")
		with open(filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" og", "R"+str(round_num)+" oo", "R"+str(round_num)+" cg", "R"+str(round_num)+" co", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2", "team3", "team4"])
			
			for lattice in allocations:
				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name,0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, 0, 0, 0, 0, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
	
def read_constants_of_adj(filename):
	constants = []
	break_team_nums = []
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	csv_data = list(map(list, list(zip(*csv_data))))
	csv_data.pop(0)
	
	orders = []
	for row in csv_data:
		new_row = []
		row.pop(7)
		row2 = list(map(int, row[:10]))
		orders.append(row2[:7])
		max_in_row = max(row2)

		for value in row2[:7]:### convert order into desirability#[1,2,0]=>[2,1,0]
			if value != 0:
				new_row.append(max_in_row-value+1)
			else:
				new_row.append(0)
		for value in row2[7:]:
			new_row.append(value)

		cfg_dict = {}
		cfg_dict["random_allocation"] = new_row[0]
		cfg_dict["des_strong_strong"] = new_row[1]
		cfg_dict["des_with_fair_times"] = new_row[2]
		cfg_dict["des_avoiding_conflicts"] = new_row[3]
		cfg_dict["des_avoiding_past"] = new_row[4]
		cfg_dict["des_priori_bubble"] = new_row[5]
		cfg_dict["des_chair_rotation"] = new_row[6]
		cfg_dict["judge_test_percent"] = new_row[7]
		cfg_dict["judge_repu_percent"] = new_row[8]
		cfg_dict["judge_perf_percent"] = new_row[9]
	
		constants.append(cfg_dict)
		try:
			break_team_nums.append(int(row[10]))
		except:
			break_team_nums.append(0)

	return constants, orders, break_team_nums

def read_constants(filename):
	constants = []
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	csv_data = list(map(list, list(zip(*csv_data))))
	csv_data.pop(0)
	
	orders = []
	for row in csv_data:
		new_row = []
		row = list(map(int, row))
		orders.append(row)
		max_in_row = max(row)

		for value in row:### convert order into desirability#[1,2,0]=>[2,1,0]
			if value != 0:
				new_row.append(max_in_row-value+1)
			else:
				new_row.append(0)

		cfg_dict = {}
		cfg_dict["random_pairing"] = new_row[0]
		cfg_dict["des_power_pairing"] = new_row[1]
		cfg_dict["des_w_o_same_a_insti"] = new_row[2]
		cfg_dict["des_w_o_same_b_insti"] = new_row[3]
		cfg_dict["des_w_o_same_c_insti"] = new_row[4]
		cfg_dict["des_w_o_same_opp"] = new_row[5]
		cfg_dict["des_with_fair_sides"] = new_row[6]
	
		constants.append(cfg_dict)
	
	return constants, orders

def export_matchups(matchups, exportcode, round_num, workfolder_name):
	export_filename = workfolder_name+"temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"

	if os.path.exists(export_filename):
		print("the file", export_filename, "already exists")
		input("Press Enter to overwrite the file > ")
	with open(export_filename, "w") as g:
		writer = csv.writer(g)
		if len(matchups[0].teams) == 2:
			header = ["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue", "Warnings"]
		elif len(matchups[0].teams) == 4:
			header = ["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue", "Warnings"]
		writer.writerow(header)
		for grid in matchups:
			export_row = [team.name for team in grid.teams]+["", "", "", ""]
			export_row.extend(grid.warnings)
			writer.writerow(export_row)

def export_allocations(allocations, exportcode, round_num, workfolder_name):
	export_filename = workfolder_name+"temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
	if os.path.exists(export_filename):
		print("the file", export_filename, "already exists")
		input("Press Enter to overwrite the file > ")
	if len(allocations[0].grid.teams) == 2:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""]
				export_row.extend(lattice.warnings)
				writer.writerow(export_row)
	else:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", ""]
				export_row.extend(lattice.warnings)
				writer.writerow(export_row)

def export_official_matchups(allocations, round_num, workfolder_name):
	export_filename = workfolder_name+"public/matchups_for_round_"+str(round_num)+".csv"
	if os.path.exists(export_filename):
		print("the file", export_filename, "already exists")
		input("Press Enter to overwrite the file > ")
	if len(allocations[0].grid.teams) == 2:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""]
				writer.writerow(export_row)
	else:
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue"])
			for lattice in allocations:
				if lattice.venue:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", lattice.venue.name]
				else:
					if len(lattice.panel) == 2:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""]
					elif len(lattice.panel) == 1:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, lattice.panel[0].name, "", ""]
					else:
						export_row = [lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, lattice.chair.name, "", "", ""]
				writer.writerow(export_row)

def export_venues(filename_venues, venue_list):
	with open(filename_venues, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["name", "priority"])
		for venue in venue_list:
			export_row = [venue.name, venue.priority]
			writer.writerow(export_row)

def export_adjudicators(filename_adjudicators, adjudicator_list):
	with open(filename_adjudicators, "w") as g:
		writer = csv.writer(g)
		header = ["name", "Reputation[0, 10]", "Judge test[0, 10]"]+["institution"]*10+["conflicting team"]*10
		writer.writerow(header)
		for adjudicator in adjudicator_list:
			export_row = [adjudicator.name, adjudicator.reputation, adjudicator.judge_test]
			institutions = [""]*10
			for k, institution in enumerate(adjudicator.institutions):
				institutions[k] = institution
			conflict_teams = [""]*10
			for k, conflict_team in enumerate(adjudicator.conflict_teams):
				conflict_teams[k] = conflict_team
			export_row.extend(institutions)
			export_row.extend(conflict_teams)
			writer.writerow(export_row)

def export_dummy_results_adj(allocations, round_num, style_cfg, workfolder_name):
	if len(allocations[0].grid.teams):
		with open(workfolder_name+"dummyresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = 0#random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = 0#random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = 0#random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_panel1, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, 0, 0, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name])
	else:
		with open(workfolder_name+"dummyresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
			writer = csv.writer(g)
			writer.writerow(["name", "R"+str(round_num)+" team1", "R"+str(round_num)+" team2", "R"+str(round_num)+" panel1", "R"+str(round_num)+" panel2", "R"+str(round_num)+" chair", "team1", "team2"])
			
			for lattice in allocations:
				chair_base_score = random.randint(3,8)
				chair_score_from_team1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team2 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team3 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_team4 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel1 = 0#random.randint(-2,+2) + chair_base_score
				chair_score_from_panel2 = 0#random.randint(-2,+2) + chair_base_score
				panel1_base_score = random.randint(3,8)
				panel2_base_score = random.randint(3,8)
				panel1_score_from_chair = 0#random.randint(-2,+2) + panel1_base_score
				panel2_score_from_chair = 0#random.randint(-2,+2) + panel2_base_score

				if len(lattice.panel) == 2:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[1].name, 0, 0, 0, 0, 0, 0, panel2_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				elif len(lattice.panel) == 1:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
					writer.writerow([lattice.panel[0].name, 0, 0, 0, 0, 0, 0, panel1_score_from_chair, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])
				else:
					writer.writerow([lattice.chair.name, chair_score_from_team1, chair_score_from_team2, chair_score_from_team3, chair_score_from_team4, chair_score_from_panel1, chair_score_from_panel2, 0, lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])

def reset_except_dat_cfg(workfolder_name):
	filename_list = ['temp/tm.csv', 'temp/vn.csv', 'temp/aj.csv', 'private/final_result/Results_of_adjudicators.csv', 'private/final_result/Results_of_debaters.csv', 'private/final_result/Results_of_teams.csv']
	filename_list.extend(['private/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['blankresults/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['blankresults/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['dummyresults/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['dummyresults/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['public/matchups_for_round_'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['matchups_imported/matchups_for_round_'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_debaters_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_teams_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Results_of_adjudicators_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/round_info/Adjudicators_info_by_R'+str(i)+'.csv' for i in range(50)])
	filename_list = [workfolder_name+filename for filename in filename_list]
	for filename in filename_list:
		try:
			os.remove(filename)
			#print filename
		except:
			continue

	try:
		shutil.rmtree(workfolder_name+"temp")
		os.mkdir(workfolder_name+"temp")
	except:
		pass

	#return to_folder

def check_results_of_adj(filename, teamnum):
	if teamnum == 2:
		f = open(filename, 'r')
		reader = csv.reader(f)
		header = next(reader)
		regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

		results_lists = []

		for row in reader:
			for ele in row:
				hit = regexp.search(ele)
				if hit is None:
					print(("warning: results of adj file is using unknown character(fullwidth forms or other symbols)", ele))
			results_lists.append([row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), row[6], row[7]])

		multi2 = {results_list[0]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[0]] += 1

		for k, v in list(multi2.items()):
			if v > 1:
				print(("error in adjudicator name column, row(appears twice):"+k))
				return True

		teams = {results_list[6]:results_list[7] for results_list in results_lists}

		for results_list in results_lists:
			if teams[results_list[6]] != results_list[7]:
				print(("error in team columns:"+str(results_list[6])))
				return True

		two_teams_list = []
		for results_list in results_lists:
			if [results_list[6], results_list[7]] not in two_teams_list:
				two_teams_list.append([results_list[6], results_list[7]])

		teams = []
		for two_teams in two_teams_list:
			teams.extend(two_teams)

		for team in teams:
			if teams.count(team) > 1:
				print(("error in team columns:"+team))
				return True

		return False
	else:
		f = open(filename, 'r')
		reader = csv.reader(f)
		header = next(reader)
		regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

		results_lists = []

		for row in reader:
			for ele in row:
				hit = regexp.search(ele)
				if hit is None:
					print(("warning: results of adj file is using unknown character(fullwidth forms or other symbols)", ele))
			results_lists.append([row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), row[8], row[9], row[10], row[11]])

		multi2 = {results_list[0]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[0]] += 1

		for k, v in list(multi2.items()):
			if v > 1:
				print(("error in adjudicator name column, row(appears twice):"+k))
				time.sleep(5)
				#return True

		teams = {results_list[8]:[results_list[9], results_list[10], results_list[11]] for results_list in results_lists}

		for results_list in results_lists:
			if teams[results_list[8]] != [results_list[9], results_list[10], results_list[11]]:
				print(("error in team columns:"+str(results_list[8])))
				time.sleep(5)
				#return True

		four_teams_list = []
		for results_list in results_lists:
			if [results_list[8], results_list[9], results_list[10], results_list[11]] not in four_teams_list:
				four_teams_list.append([results_list[8], results_list[9], results_list[10], results_list[11]])

		teams = []
		for four_teams in four_teams_list:
			teams.extend(four_teams)

		for team in teams:
			if teams.count(team) > 1:
				print(("error in team columns:"+team))
				time.sleep(5)
				#return True

		return False


pass