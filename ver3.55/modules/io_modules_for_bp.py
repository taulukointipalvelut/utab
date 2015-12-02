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
		writer.writerow(["team_name", "name", "R"+str(round_num)+" 1st", "R"+str(round_num)+" 2nd", "Win-points[0, 1, 2, 3]", "Opponent1", "Opponent2", "Opponent3", "Position[og, oo, cg, co]"])

		for lattice in allocations:
			og_members = copy.copy(lattice.grid.teams[0].debaters)
			oo_members = copy.copy(lattice.grid.teams[1].debaters)
			cg_members = copy.copy(lattice.grid.teams[2].debaters)
			co_members = copy.copy(lattice.grid.teams[3].debaters)

			writer.writerow([lattice.grid.teams[0].name, og_members[0].name, 0, 0, "", lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[0].name, og_members[1].name, 0, 0, "", lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[1].name, oo_members[0].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[1].name, oo_members[1].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[2].name, cg_members[0].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[2].name, cg_members[1].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[3].name, ""])
			writer.writerow([lattice.grid.teams[3].name, co_members[0].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, ""])
			writer.writerow([lattice.grid.teams[3].name, co_members[1].name, 0, 0, "", lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, ""])

def read_results(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	results = []
	for row in reader:
		results.append([row[0], row[1], float(row[2]), float(row[3]), int(row[4]), row[5], row[6], row[7], row[8]])
	return results

def read_and_process_result(round_num, team_list):
	filename_results = "private/Results"+str(round_num)+".csv"
	if check_results(filename_results):
		print "Results file broken"
		raise NameError('Results file broken')
	results_list = read_results(filename_results)
	for i in range(int(len(results_list)/2)):#results=>[team name, name, R[i] 1st, R[i] 2nd, R[i] rep, win?lose?, opponent name, gov?opp?]
		for team in team_list:
			if team.name == results_list[2*i][0]:
				member1_name = results_list[2*i][1]
				member2_name = results_list[2*i+1][1]
				member1_score_list = results_list[2*i][2:4]
				member2_score_list = results_list[2*i+1][2:4]
				side = results_list[2*i][8]
				win = results_list[2*i][4]
				for debater in team.debaters:
					if debater.name == member1_name:
						debater.score_lists.append(member1_score_list)
						debater.scores.append(sum(member1_score_list))
					elif debater.name == member2_name:
						debater.score_lists.append(member2_score_list)
						debater.scores.append(sum(member2_score_list))
					else:
						print "error: Results file(Results"+str(round_num)+".csv) broken"

				team.finishing_process(opponent=[results_list[2*i][5], results_list[2*i][6], results_list[2*i][7]], score=sum(member1_score_list)+sum(member2_score_list), side=side, win=win, margin=0)

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
		writer.writerow(["team_name", "name", "R"+str(round_num)+" 1st", "R"+str(round_num)+" 2nd", "Win-points", "Opponent1", "Opponent2", "Opponent3", "Position"])

		for lattice in allocations:
			oga_base_score = random.randint(73, 77)
			ogb_base_score = random.randint(73, 77)
			ooa_base_score = random.randint(73, 77)
			oob_base_score = random.randint(73, 77)
			cga_base_score = random.randint(73, 77)
			cgb_base_score = random.randint(73, 77)
			coa_base_score = random.randint(73, 77)
			cob_base_score = random.randint(73, 77)
			og_members = copy.copy(lattice.grid.teams[0].debaters)
			oo_members = copy.copy(lattice.grid.teams[1].debaters)
			cg_members = copy.copy(lattice.grid.teams[2].debaters)
			co_members = copy.copy(lattice.grid.teams[3].debaters)
			random.shuffle(og_members)
			random.shuffle(oo_members)
			random.shuffle(cg_members)
			random.shuffle(co_members)

			teams_dict = {"og": oga_base_score+ogb_base_score, "oo": ooa_base_score+oob_base_score, "cg": cga_base_score+cgb_base_score, "co": coa_base_score+cob_base_score}
			teams_dict_sorted = sorted(teams_dict.items(), key=lambda x:x[1])
			for i, k in enumerate(teams_dict_sorted):
				teams_dict[k[0]] = i

			oga_score_from_panel1 = oga_base_score + random.randint(-2,+2)
			oga_score_from_panel2 = oga_base_score + random.randint(-2,+2)
			oga_score_from_chair = oga_base_score + random.randint(-2,+2)
			ogb_score_from_panel1 = ogb_base_score + random.randint(-2,+2)
			ogb_score_from_panel2 = ogb_base_score + random.randint(-2,+2)
			ogb_score_from_chair = ogb_base_score + random.randint(-2,+2)
			ooa_score_from_panel1 = ooa_base_score + random.randint(-2,+2)
			ooa_score_from_panel2 = ooa_base_score + random.randint(-2,+2)
			ooa_score_from_chair = ooa_base_score + random.randint(-2,+2)
			oob_score_from_panel1 = oob_base_score + random.randint(-2,+2)
			oob_score_from_panel2 = oob_base_score + random.randint(-2,+2)
			oob_score_from_chair = oob_base_score + random.randint(-2,+2)
			cga_score_from_panel1 = cga_base_score + random.randint(-2,+2)
			cga_score_from_panel2 = cga_base_score + random.randint(-2,+2)
			cga_score_from_chair = cga_base_score + random.randint(-2,+2)
			cgb_score_from_panel1 = cgb_base_score + random.randint(-2,+2)
			cgb_score_from_panel2 = cgb_base_score + random.randint(-2,+2)
			cgb_score_from_chair = cgb_base_score + random.randint(-2,+2)
			coa_score_from_panel1 = coa_base_score + random.randint(-2,+2)
			coa_score_from_panel2 = coa_base_score + random.randint(-2,+2)
			coa_score_from_chair = coa_base_score + random.randint(-2,+2)
			cob_score_from_panel1 = cob_base_score + random.randint(-2,+2)
			cob_score_from_panel2 = cob_base_score + random.randint(-2,+2)
			cob_score_from_chair = cob_base_score + random.randint(-2,+2)

			if len(lattice.panel) == 2:
				oga_score = (oga_score_from_panel1+oga_score_from_panel2+oga_score_from_chair)/3.0
				ogb_score = (ogb_score_from_panel1+ogb_score_from_panel2+ogb_score_from_chair)/3.0
				ooa_score = (ooa_score_from_panel1+ooa_score_from_panel2+ooa_score_from_chair)/3.0
				oob_score = (oob_score_from_panel1+oob_score_from_panel2+oob_score_from_chair)/3.0
				cga_score = (cga_score_from_panel1+cga_score_from_panel2+cga_score_from_chair)/3.0
				cgb_score = (cgb_score_from_panel1+cgb_score_from_panel2+cgb_score_from_chair)/3.0
				coa_score = (coa_score_from_panel1+coa_score_from_panel2+coa_score_from_chair)/3.0
				cob_score = (cob_score_from_panel1+cob_score_from_panel2+cob_score_from_chair)/3.0
			elif len(lattice.panel) == 1:
				oga_score = (oga_score_from_panel1+oga_score_from_chair)/2.0
				ogb_score = (ogb_score_from_panel1+ogb_score_from_chair)/2.0
				ooa_score = (ooa_score_from_panel1+ooa_score_from_chair)/2.0
				oob_score = (oob_score_from_panel1+oob_score_from_chair)/2.0
				cga_score = (cga_score_from_panel1+cga_score_from_chair)/2.0
				cgb_score = (cgb_score_from_panel1+cgb_score_from_chair)/2.0
				coa_score = (coa_score_from_panel1+coa_score_from_chair)/2.0
				cob_score = (cob_score_from_panel1+cob_score_from_chair)/2.0
			else:
				oga_score = oga_score_from_chair
				ogb_score = ogb_score_from_chair
				ooa_score = ooa_score_from_chair
				oob_score = oob_score_from_chair
				cga_score = cga_score_from_chair
				cgb_score = cgb_score_from_chair
				coa_score = coa_score_from_chair
				cob_score = cob_score_from_chair

			writer.writerow([lattice.grid.teams[0].name, og_members[0].name, oga_score, 0, teams_dict["og"], lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, "og"])
			writer.writerow([lattice.grid.teams[0].name, og_members[1].name, 0, ogb_score, teams_dict["og"], lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, "og"])
			writer.writerow([lattice.grid.teams[1].name, oo_members[0].name, ooa_score, 0, teams_dict["oo"], lattice.grid.teams[0].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, "oo"])
			writer.writerow([lattice.grid.teams[1].name, oo_members[1].name, 0, oob_score, teams_dict["oo"], lattice.grid.teams[0].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name, "oo"])
			writer.writerow([lattice.grid.teams[2].name, cg_members[0].name, cga_score, 0, teams_dict["cg"], lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[3].name, "cg"])
			writer.writerow([lattice.grid.teams[2].name, cg_members[1].name, 0, cgb_score, teams_dict["cg"], lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[3].name, "cg"])
			writer.writerow([lattice.grid.teams[3].name, co_members[0].name, coa_score, 0, teams_dict["co"], lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, "co"])
			writer.writerow([lattice.grid.teams[3].name, co_members[1].name, 0, cob_score, teams_dict["co"], lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, "co"])

def read_teams(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	teams = []
	for code, raw_row in enumerate(reader):
		row = [raw_one.strip() for raw_one in raw_row]
		if row[0] != '':
			teams.append(Team(code, row[0], [row[1], row[2]], row[3], row[4:]))#=>code, name, member_names
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
				row.extend(score_list2)
				row.append(round(sum(score_list), 2))
				sum_score += sum(score_list)
			if len(debater.score_lists) == 0:
				average_score = 0
			else:
				for score_list in debater.score_lists:
					average_score += sum(score_list)
				average_score = round(average_score/(len(debater.score_lists)), 2)
				
			row.append(average_score)

			for score_list in debater.score_lists:
				sd += (sum(score_list)-average_score)**2
			if len(debater.score_lists) != 0:
				sd /= len(debater.score_lists)
				sd = math.sqrt(sd)
			row.append(round(sum_score, 2))
			row.append(round(sd, 2))
			individual_score_rows.append(row)

	for i in range(int((len(individual_score_rows[0])-3)/3)):
		header.extend(["round"+str(i+1)+" 1st", "round"+str(i+1)+" 2nd", "round"+str(i+1)+" average"])

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
		score_rows.append(row)

	for i in range((len(score_rows[0])-4)):
		header.append("round"+str(i+1))
	header.extend(["sum", "win-points"])

	score_rows.sort(key=lambda row: (row[-1], row[-2]), reverse=True)

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
		writer.writerow(["team name", "name1", "mame2", "scale", "institution"])
		for team in team_list:
			export_row = [team.name, team.debaters[0].name, team.debaters[1].name, team.institution_scale]
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
		results_lists.append([row[0], row[1], float(row[2]), float(row[3]), int(row[4]), row[5], row[6], row[7], row[8]])

	for i in range(int(len(results_lists)/2)):
		if results_lists[2*i][0] != results_lists[2*i+1][0]:
			print("error in team name column, row:"+str(2*i+3))
			return True

	multi2 = {results_list[1]:0 for results_list in results_lists}

	for results_list in results_lists:
		multi2[results_list[1]] += 1

	for k, v in multi2.items():
		if v > 1:
			print("warning in debater name column, row(appears twice):"+str(i+3)+":"+k)

	for i, results_list in enumerate(results_lists):
		if results_list[2:4].count(0) == 0 or results_list[2:4].count(0) == 2:
			print("error in debater score column, row:"+str(i+3))
			return True

	fst = 0
	snd = 0
	trd = 0
	fth = 0
	for results_list in results_lists:
		if results_list[4] == 3:
			fst += 1
		elif results_list[4] == 2:
			snd += 1
		elif results_list[4] == 1:
			trd += 1
		elif results_list[4] == 0:
			fth += 1

	if fst != snd or fst != trd or fst != fth or snd != trd or snd != fth or trd != fth:
		print("error in win column")
		return True

	og = 0
	oo = 0
	cg = 0
	co = 0
	for results_list in results_lists:
		if results_list[8] == "og":
			og += 1
		elif results_list[8] == "oo":
			oo += 1
		elif results_list[8] == "cg":
			cg += 1
		elif results_list[8] == "co":
			co += 1

	if og != oo or og != cg or og != co or oo != cg or oo != co or cg != co:
		print("error in side column")
		return True

	opponents1, opponents2, opponents3, opponents4 = [], [], [], []
	for results_list in results_lists:
		opponents1.extend([results_list[5], results_list[6], results_list[7]])
		opponents2.extend([results_list[0], results_list[6], results_list[7]])
		opponents3.extend([results_list[0], results_list[5], results_list[7]])
		opponents4.extend([results_list[0], results_list[5], results_list[6]])
	if set(opponents1) != set(opponents2) or set(opponents1) != set(opponents3) or set(opponents1) != set(opponents4) or set(opponents2) != set(opponents3) or set(opponents2) != set(opponents4) or set(opponents3) != set(opponents4):
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
				new_team = Team(len(team_list), row[0], [row[2], row[3]], row[4], row[5:])
				new_team.available = True if int(row[1]) == 1 else False
				team_list.append(new_team)
	except:
		pass


pass