# -*- coding: utf-8 -*-
from classes import *
from bit_modules import *
from property_modules import *
from io_modules import *
import time
import random
import shutil
import csv
import sys
import os
import math
import copy
import re
try:
	import readline
except:
	pass
	
def export_blank_results(allocations, round_num):
	with open("blankresults/Results"+str(round_num)+".csv", "w") as g:
		writer = csv.writer(g)
		writer.writerow(["team_name", "name", "R"+str(round_num)+" 1st", "R"+str(round_num)+" 2nd", "R"+str(round_num)+" 3rd", "R"+str(round_num)+" reply", "Win[0, 1]", "Opponent", "Gov Opp[gov, opp]"])

		for lattice in allocations:
			gov_members = copy.copy(lattice.grid.teams[0].debaters)
			opp_members = copy.copy(lattice.grid.teams[1].debaters)

			writer.writerow([lattice.grid.teams[0].name, gov_members[0].name, 0, 0, 0, 0, "", lattice.grid.teams[1].name, ""])
			writer.writerow([lattice.grid.teams[0].name, gov_members[1].name, 0, 0, 0, 0, "", lattice.grid.teams[1].name, ""])
			writer.writerow([lattice.grid.teams[0].name, gov_members[2].name, 0, 0, 0, 0, "", lattice.grid.teams[1].name, ""])
			writer.writerow([lattice.grid.teams[1].name, opp_members[0].name, 0, 0, 0, 0, "", lattice.grid.teams[0].name, ""])
			writer.writerow([lattice.grid.teams[1].name, opp_members[1].name, 0, 0, 0, 0, "", lattice.grid.teams[0].name, ""])
			writer.writerow([lattice.grid.teams[1].name, opp_members[2].name, 0, 0, 0, 0, "", lattice.grid.teams[0].name, ""])
		
def read_results(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	results = []
	for raw_row in reader:
		row = [raw_one.strip() for raw_one in raw_row]
		results.append([row[0], row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6]), row[7], row[8]])
	return results

def read_and_process_result(round_num, team_list):
	filename_results = "private/Results"+str(round_num)+".csv"
	if check_results(filename_results):
		print "Results file broken"
		raise NameError('Results file broken')
	results_list = read_results(filename_results)
	for i in range(int(len(results_list)/3)):#results=>[team name, name, R[i] 1st, R[i] 2nd, R[i] rep, win?lose?, opponent name, gov?opp?]
		for team in team_list:
			if team.name == results_list[3*i][0]:
				member1_name = results_list[3*i][1]
				member2_name = results_list[3*i+1][1]
				member3_name = results_list[3*i+2][1]
				member1_score_list = results_list[3*i][2:6]
				member2_score_list = results_list[3*i+1][2:6]
				member3_score_list = results_list[3*i+2][2:6]
				side = results_list[3*i][8]
				win = results_list[3*i][6]
				for debater in team.debaters:
					if debater.name == member1_name:
						debater.score_lists.append(member1_score_list)
						if member1_score_list.count(0) == 3:
							debater.scores.append(sum(member1_score_list))
						elif member1_score_list.count(0) == 2:
							debater.scores.append(sum(member1_score_list)*2/3)
					elif debater.name == member2_name:
						debater.score_lists.append(member2_score_list)
						if member2_score_list.count(0) == 3:
							debater.scores.append(sum(member2_score_list))
						elif member2_score_list.count(0) == 2:
							debater.scores.append(sum(member2_score_list)*2/3)
					elif debater.name == member3_name:
						debater.score_lists.append(member3_score_list)
						if member3_score_list.count(0) == 3:
							debater.scores.append(sum(member3_score_list))
						elif member3_score_list.count(0) == 2:
							debater.scores.append(sum(member3_score_list)*2/3)
					else:
						print "error: Results file(Results"+str(round_num)+".csv) broken"

				opp_team_score = 0
				for results in results_list:
					if results[0] == results_list[3*i][7]:
						opp_team_score += sum(results[2:6])

				team.finishing_process(opponent=[results_list[3*i][6]], score=sum(member1_score_list)+sum(member2_score_list)+sum(member3_score_list), side=side, win=win, margin=sum(member1_score_list)+sum(member2_score_list)+sum(member3_score_list)-opp_team_score)

	for team in team_list:
		if team.name not in [results[0] for results in results_list]:
			if team.available:
				print "team: {0:15s} not in results: {1}".format(team.name, filename_results)

	for team in team_list:
		for debater in team.debaters:
			if debater.name not in [results[1] for results in results_list]:
				if team.available:
					print "debater: {0:15s} not in results: {1}".format(debater.name, filename_results)

def export_random_result(allocations, round_num):
	with open("private/Results"+str(round_num)+".csv", "w") as g:
		writer = csv.writer(g)
		writer.writerow(["team_name", "name", "R"+str(round_num)+" 1st", "R"+str(round_num)+" 2nd", "R"+str(round_num)+" 3rd", "R"+str(round_num)+" reply", "Win", "Opponent", "Gov Opp"])

		for lattice in allocations:
			ga_base_score = random.randint(73, 77)
			gb_base_score = random.randint(73, 77)
			gc_base_score = random.randint(73,77)
			gd_base_score = random.randint(73,77)/2.0
			oa_base_score = random.randint(73, 77)
			ob_base_score = random.randint(73, 77)
			oc_base_score = random.randint(73,77)
			od_base_score = random.randint(73,77)/2.0
			gov_members = copy.copy(lattice.grid.teams[0].debaters)
			opp_members = copy.copy(lattice.grid.teams[1].debaters)
			random.shuffle(gov_members)
			random.shuffle(opp_members)
			team1_win = 1 if sum([ga_base_score, gb_base_score, gc_base_score, gd_base_score]) > sum([oa_base_score, ob_base_score, oc_base_score, od_base_score]) else 0

			ga_score_from_panel1 = ga_base_score + random.randint(-2,+2)
			ga_score_from_panel2 = ga_base_score + random.randint(-2,+2)
			ga_score_from_chair = ga_base_score + random.randint(-2,+2)
			gb_score_from_panel1 = gb_base_score + random.randint(-2,+2)
			gb_score_from_panel2 = gb_base_score + random.randint(-2,+2)
			gb_score_from_chair = gb_base_score + random.randint(-2,+2)
			gc_score_from_panel1 = gc_base_score + random.randint(-2,+2)
			gc_score_from_panel2 = gc_base_score + random.randint(-2,+2)
			gc_score_from_chair = gc_base_score + random.randint(-2,+2)
			gd_score_from_panel1 = gd_base_score + random.randint(-2,+2)/2.0
			gd_score_from_panel2 = gd_base_score + random.randint(-2,+2)/2.0
			gd_score_from_chair = gd_base_score + random.randint(-2,+2)/2.0
			oa_score_from_panel1 = oa_base_score + random.randint(-2,+2)
			oa_score_from_panel2 = oa_base_score + random.randint(-2,+2)
			oa_score_from_chair = oa_base_score + random.randint(-2,+2)
			ob_score_from_panel1 = ob_base_score + random.randint(-2,+2)
			ob_score_from_panel2 = ob_base_score + random.randint(-2,+2)
			ob_score_from_chair = ob_base_score + random.randint(-2,+2)
			oc_score_from_panel1 = oc_base_score + random.randint(-2,+2)
			oc_score_from_panel2 = oc_base_score + random.randint(-2,+2)
			oc_score_from_chair = oc_base_score + random.randint(-2,+2)
			od_score_from_panel1 = od_base_score + random.randint(-2,+2)/2.0
			od_score_from_panel2 = od_base_score + random.randint(-2,+2)/2.0
			od_score_from_chair = od_base_score + random.randint(-2,+2)/2.0

			if len(lattice.panel) == 2:
				ga_score = (ga_score_from_panel1+ga_score_from_panel2+ga_score_from_chair)/3.0
				gb_score = (gb_score_from_panel1+gb_score_from_panel2+gb_score_from_chair)/3.0
				gc_score = (gc_score_from_panel1+gc_score_from_panel2+gc_score_from_chair)/3.0
				gd_score = (gd_score_from_panel1+gd_score_from_panel2+gd_score_from_chair)/3.0
				oa_score = (oa_score_from_panel1+oa_score_from_panel2+oa_score_from_chair)/3.0
				ob_score = (ob_score_from_panel1+ob_score_from_panel2+ob_score_from_chair)/3.0
				oc_score = (oc_score_from_panel1+oc_score_from_panel2+oc_score_from_chair)/3.0
				od_score = (od_score_from_panel1+od_score_from_panel2+od_score_from_chair)/3.0
			elif len(lattice.panel) == 1:
				ga_score = (ga_score_from_panel1+ga_score_from_chair)/2.0
				gb_score = (gb_score_from_panel1+gb_score_from_chair)/2.0
				gc_score = (gc_score_from_panel1+gc_score_from_chair)/2.0
				gd_score = (gd_score_from_panel1+gd_score_from_chair)/2.0
				oa_score = (oa_score_from_panel1+oa_score_from_chair)/2.0
				ob_score = (ob_score_from_panel1+ob_score_from_chair)/2.0
				oc_score = (oc_score_from_panel1+oc_score_from_chair)/2.0
				od_score = (od_score_from_panel1+od_score_from_chair)/2.0
			else:
				ga_score = ga_score_from_chair
				gb_score = gb_score_from_chair
				gc_score = gc_score_from_chair
				gd_score = gd_score_from_chair
				oa_score = oa_score_from_chair
				ob_score = ob_score_from_chair
				oc_score = oc_score_from_chair
				od_score = od_score_from_chair

			if random.choice([True, False]):
				writer.writerow([lattice.grid.teams[0].name, gov_members[0].name, ga_score, 0, 0, gd_score, team1_win, lattice.grid.teams[1].name, "gov"])
				writer.writerow([lattice.grid.teams[0].name, gov_members[1].name, 0, gb_score, 0, 0, team1_win, lattice.grid.teams[1].name, "gov"])
				writer.writerow([lattice.grid.teams[0].name, gov_members[2].name, 0, 0, gc_score, 0, team1_win, lattice.grid.teams[1].name, "gov"])
			else:
				writer.writerow([lattice.grid.teams[0].name, gov_members[0].name, ga_score, 0, 0, 0, team1_win, lattice.grid.teams[1].name, "gov"])
				writer.writerow([lattice.grid.teams[0].name, gov_members[1].name, 0, gb_score, 0, gd_score, team1_win, lattice.grid.teams[1].name, "gov"])
				writer.writerow([lattice.grid.teams[0].name, gov_members[2].name, 0, 0, gc_score, 0, team1_win, lattice.grid.teams[1].name, "gov"])

			if random.choice([True, False]):
				writer.writerow([lattice.grid.teams[1].name, opp_members[0].name, oa_score, 0, 0, od_score, 1-team1_win, lattice.grid.teams[0].name, "opp"])
				writer.writerow([lattice.grid.teams[1].name, opp_members[1].name, 0, ob_score, 0, 0, 1-team1_win, lattice.grid.teams[0].name, "opp"])
				writer.writerow([lattice.grid.teams[1].name, opp_members[2].name, 0, 0, oc_score, 0, 1-team1_win, lattice.grid.teams[0].name, "opp"])
			else:
				writer.writerow([lattice.grid.teams[1].name, opp_members[0].name, oa_score, 0, 0, 0, 1-team1_win, lattice.grid.teams[0].name, "opp"])
				writer.writerow([lattice.grid.teams[1].name, opp_members[1].name, 0, ob_score, 0, od_score, 1-team1_win, lattice.grid.teams[0].name, "opp"])
				writer.writerow([lattice.grid.teams[1].name, opp_members[2].name, 0, 0, oc_score, 0, 1-team1_win, lattice.grid.teams[0].name, "opp"])

def read_teams(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	teams = []
	for code, raw_row in enumerate(reader):
		row = [raw_one.strip() for raw_one in raw_row]
		if row[0] != '':
			teams.append(Team(code, row[0], [row[1], row[2], row[3]], row[4], row[5:]))#=>code, name, member_names
	return teams

def export_results(team_list, adjudicator_list):
	header = ["ranking", "name", "team name"]
	individual_score_rows = []
	for team in team_list:
		for debater in team.debaters:
			row = [debater.name, team.name]
			sum_score = 0
			sd = 0
			average_score = 0
			for score_list in debater.score_lists:
				score_list2 = [round(score, 2) for score in score_list]
				if score_list.count(0) == 3:
					row.extend(score_list2)
					row.append(round(sum(score_list), 2))
					sum_score += sum(score_list)
				elif score_list.count(0) == 2:
					row.extend(score_list2)
					row.append(round(sum(score_list)*2/3, 2))
					sum_score += sum(score_list)*2/3
			if len(debater.score_lists) == 0:
				average_score = 0
			else:
				for score_list in debater.score_lists:
					if score_list.count(0) == 3:
						average_score += sum(score_list)
					elif score_list.count(0) == 2:
						average_score += sum(score_list)*2/3
				average_score = round(average_score/(len(debater.score_lists)), 2)

			row.append(average_score )

			for score_list in debater.score_lists:
				sd += (sum(score_list)-average_score)**2
			if len(debater.score_lists) != 0:
				sd /= len(debater.score_lists)
				sd = math.sqrt(sd)
			row.append(round(sum_score, 2))
			row.append(round(sd, 2))
			individual_score_rows.append(row)

	for i in range(int((len(individual_score_rows[0])-2)/5)):
		header.extend(["round"+str(i+1)+" 1st", "round"+str(i+1)+" 2nd", "round"+str(i+1)+" 3rd", "round"+str(i+1)+" reply", "round"+str(i+1)+" average"])

	header.extend(["average", "sum", "sd"])

	individual_score_rows.sort(key=lambda row: row[-2], reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(individual_score_rows)-1):
		if individual_score_rows[k][-1] != individual_score_rows[k+1][-1]:
			individual_score_rows[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			individual_score_rows[k].insert(0, ranking)
			stay += 1
	individual_score_rows[-1].insert(0, ranking)

	with open("private/Results_of_debaters.csv", "w") as g:
		writer = csv.writer(g)
		writer.writerow(header)
		for row in individual_score_rows:
			writer.writerow(row)

	score_rows = []
	header = ["ranking", "team name"]
	for team in team_list:
		row = [team.name]
		scores2 = [round(score, 2) for score in team.scores]

		row.extend(scores2)
		row.append(round(sum(team.scores), 2))
		row.append(sum(team.wins))
		row.append(round(team.margin, 2))
		score_rows.append(row)

	for i in range((len(score_rows[0])-4)):
		header.append("round"+str(i+1))
	header.extend(["sum", "wins", "margin"])

	score_rows.sort(key=lambda row: (row[-2], row[-3], row[-1]), reverse=True)

	ranking = 1
	stay = 0
	for k in range(len(score_rows)-1):
		if score_rows[k][-2] != score_rows[k+1][-2] or score_rows[k][-3] != score_rows[k+1][-3] or score_rows[k][-1] or score_rows[k+1][-1]:
			score_rows[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			score_rows[k].insert(0, ranking)
			stay += 1
	score_rows[-1].insert(0, ranking)

	with open("private/Results_of_teams.csv", "w") as g:
		writer = csv.writer(g)
		writer.writerow(header)
		for row in score_rows:
			writer.writerow(row)
	
	adjudicator_score_rows = []
	header = ["ranking", "name", "average"]
	for adjudicator in adjudicator_list:
		if len(adjudicator.scores) != 0:
			adjudicator_score_rows.append([adjudicator.name, round(sum(adjudicator.scores)/len(adjudicator.scores), 2)])
		else:
			adjudicator_score_rows.append([adjudicator.name, 0])

	ranking = 1
	stay = 0
	for k in range(len(adjudicator_score_rows)-1):
		if adjudicator_score_rows[k][-1] != adjudicator_score_rows[k+1][-1]:
			adjudicator_score_rows[k].insert(0, ranking)
			ranking += 1 + stay
			stay = 0
		else:
			adjudicator_score_rows[k].insert(0, ranking)
			stay += 1
	adjudicator_score_rows[-1].insert(0, ranking)

	with open("private/Results_of_adjudicators.csv", "w") as g:
		writer = csv.writer(g)
		writer.writerow(header)
		for row in adjudicator_score_rows:
			writer.writerow(row)

def export_teams(filename_teams, team_list):
	with open(filename_teams, "w") as g:
		writer = csv.writer(g)
		writer.writerow(["team name", "name1", "mame2", "name3", "scale", "institution"])
		for team in team_list:
			export_row = [team.name, team.debaters[0].name, team.debaters[1].name, team.debaters[2].name, team.institution_scale]
			export_row.extend(team.institutions)
			writer.writerow(export_row)
			
def check_results(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)

	header = next(reader)
	regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

	results_lists = []

	for row in reader:
		for ele in row:
			hit = regexp.search(ele)
			if hit is None:
				print("warning: results file is using unknown character(fullwidth forms or other symbols)", ele)
		results_lists.append([row[0], row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6]), row[7], row[8]])

	for i in range(int(len(results_lists)/3)):
		if results_lists[3*i][0] != results_lists[3*i+1][0] or results_lists[3*i+1][0] != results_lists[3*i+2][0] or results_lists[3*i][0] != results_lists[3*i+2][0]:
			print("error in team name column, row:"+str(3*i+3))
			return True

	multi2 = {results_list[1]:0 for results_list in results_lists}

	for results_list in results_lists:
		multi2[results_list[1]] += 1

	for k, v in multi2.items():
		if v > 1:
			print("warning in debater name column, row(appears twice):"+str(i+3)+":"+k)

	for i, results_list in enumerate(results_lists):
		if results_list[2:6].count(0) == 0 or results_list[2:6].count(0) == 4:
			print("error in debater score column, row:"+str(i+3))
			return True

	win = 0
	lose = 0
	for results_list in results_lists:
		if results_list[6] == 1:
			win += 1
		else:
			lose += 1

	if win != lose:
		print("error in win column")
		return True

	gov = 0
	opp = 0
	for results_list in results_lists:
		if results_list[8] == "gov":
			gov += 1
		else:
			opp += 1

	if gov != opp:
		print("error in gov column")
		return True

	opponents = {results_list[0]:results_list[7] for results_list in results_lists}
	opponents2 = {results_list[7]:results_list[0] for results_list in results_lists}

	if opponents != opponents2:
		print("error in team and the opponent column")
		return True

	return False

def save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators):
	export_filename_aj = "temp/aj.csv"
	export_filename_vn = "temp/vn.csv"
	export_filename_tm = "temp/tm.csv"
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
	export_teams(filename_teams, team_list)
	export_venues(filename_venues, venue_list)
	export_adjudicators(filename_adjudicators, adjudicator_list)

def load(adjudicator_list, venue_list, team_list):
	export_filename_aj = "temp/aj.csv"
	export_filename_vn = "temp/vn.csv"
	export_filename_tm = "temp/tm.csv"
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
				new_team = Team(len(team_list), row[0], [row[2], row[3], row[4]], row[5], row[6:])
				new_team.available = True if int(row[1]) == 1 else False
				team_list.append(new_team)
	except:
		pass


pass