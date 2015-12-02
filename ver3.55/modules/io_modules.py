# -*- coding: utf-8 -*-
from classes import *
from bit_modules import *
from property_modules import *
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

	adjudicator_list = []
	for row in csv_data:
		if row[0] != '':
			adjudicator_list.append(Adjudicator(row[0], float(row[1]), float(row[2]), row[3:13], row[13:]))

	return adjudicator_list

def read_results_of_adj(filename, teamnum2):
	if teamnum2:
		f = open(filename, 'r')
		reader = csv.reader(f)
		header = next(reader)
		results = []
		for row in reader:
			results.append([row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), row[6], row[7]])
		return results
	else:
		f = open(filename, 'r')
		reader = csv.reader(f)
		header = next(reader)
		results = []
		for row in reader:
			results.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11])])
		return results

def read_and_process_result_adj(round_num, team_list, adjudicator_list, teamnum2):
	if teamnum2:
		filename_results_of_adj = "private/Results_of_adj"+str(round_num)+".csv"
		if check_results_of_adj(filename_results_of_adj, teamnum2):
			print "Results of adj file broken"
			raise NameError('Results file broken')
		results_of_adj_list = read_results_of_adj(filename_results_of_adj, teamnum2)

		adjudicator_temp = []
		for results_of_adj in results_of_adj_list:
			for adjudicator in adjudicator_list:
				if adjudicator.name == results_of_adj[0]:
					if results_of_adj[1:6].count(0) == 5:
						score = 0
					else:
						score = float(sum(results_of_adj[1:6]))/(5-results_of_adj[1:6].count(0))
					team1, team2 = None, None
					for team in team_list:
						if team.name == results_of_adj[6]:
							team1 = team
						if team.name == results_of_adj[7]:
							team2 = team
					if team1 is None or team2 is None:
						print "results_of_adj file broken", str(team1), str(team2)
						break
					else:
						if results_of_adj[5] == 0:
							adjudicator.finishing_process(score=score, teams=[team1, team2], watched_debate_score=team1.score+team2.score, chair=True)
						else:
							adjudicator.finishing_process(score=score, teams=[team1, team2], watched_debate_score=team1.score+team2.score, chair=False)
						adjudicator_temp.append(adjudicator)

		adjudicator_temp.sort(key=lambda adjudicator: adjudicator.watched_debate_score, reverse=True)
		for k, adjudicator in enumerate(adjudicator_temp):
			adjudicator.watched_debate_ranks.append(k+1)
	else:
		filename_results_of_adj = "private/Results_of_adj"+str(round_num)+".csv"
		if check_results_of_adj(filename_results_of_adj, teamnum2):
			print "Results of adj file broken"
			raise NameError('Results file broken')
		results_of_adj_list = read_results_of_adj(filename_results_of_adj, teamnum2)

		adjudicator_temp = []
		for results_of_adj in results_of_adj_list:
			for adjudicator in adjudicator_list:
				if adjudicator.name == results_of_adj[0]:
					if results_of_adj[1:8].count(0) == 7:
						score = 0
					else:
						score = float(sum(results_of_adj[1:8]))/(7-results_of_adj[1:8].count(0))
					team1, team2, team3, team4 = None, None, None, None
					for team in team_list:
						if team.name == results_of_adj[8]:
							team1 = team
						if team.name == results_of_adj[9]:
							team2 = team
						if team.name == results_of_adj[10]:
							team3 = team
						if team.name == results_of_adj[11]:
							team4 = team
					if team1 is None or team2 is None or team3 is None or team4 is None:
						print "results_of_adj file broken", str(team1), str(team2), str(team3), str(team4)
						break
					else:
						if results_of_adj[7] == 0:
							adjudicator.finishing_process(score=score, teams=[team1, team2, team3, team4], watched_debate_score=team1.score+team2.score+team3.score+team4.score, chair=True)
						else:
							adjudicator.finishing_process(score=score, teams=[team1, team2, team3, team4], watched_debate_score=team1.score+team2.score+team3.score+team4.score, chair=False)
						adjudicator_temp.append(adjudicator)

		adjudicator_temp.sort(key=lambda adjudicator: adjudicator.watched_debate_score, reverse=True)
		for k, adjudicator in enumerate(adjudicator_temp):
			adjudicator.watched_debate_ranks.append(k+1)
	
def export_random_result_adj(allocations, round_num):
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
	
def export_blank_results_of_adj(allocations, round_num):
	if len(allocations[0].grid.teams) == 2:
		with open("blankresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
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
		with open("blankresults/Results_of_adj"+str(round_num)+".csv", "w") as g:
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
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	csv_data = map(list, zip(*csv_data))
	csv_data.pop(0)
	
	orders = []
	for row in csv_data:
		new_row = []
		row.pop(7)
		row = map(int, row)
		orders.append(row[:7])
		max_in_row = max(row)

		for value in row[:7]:### convert order into desirability#[1,2,0]=>[2,1,0]
			if value != 0:
				new_row.append(max_in_row-value+1)
			else:
				new_row.append(0)
		for value in row[7:]:
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

	return constants, orders

def read_constants(filename):
	constants = []
	f = open(filename, 'r')
	reader = csv.reader(f)
	header = next(reader)
	csv_data = []

	for row in reader:
		csv_data.append(row)

	csv_data = map(list, zip(*csv_data))
	csv_data.pop(0)
	
	orders = []
	for row in csv_data:
		new_row = []
		row = map(int, row)
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

def export_matchups(matchups, exportcode, round_num):
	if len(matchups[0].teams) == 2:
		export_filename = "temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["Gov", "Opp", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for grid in matchups:
				export_row = [grid.teams[0].name, grid.teams[1].name, "", "", "", ""]
				export_row.extend(grid.warnings)
				writer.writerow(export_row)
	else:
		export_filename = "temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
		with open(export_filename, "w") as g:
			writer = csv.writer(g)
			writer.writerow(["OG", "OO", "CG", "CO", "Chair", "Panel1", "Panel2", "Venue", "Warnings"])
			for grid in matchups:
				export_row = [grid.teams[0].name, grid.teams[1].name, grid.teams[2].name, grid.teams[3].name, "", "", "", ""]
				export_row.extend(grid.warnings)
				writer.writerow(export_row)


def export_allocations(allocations, exportcode, round_num):
	if len(allocations[0].grid.teams) == 2:
		export_filename = "temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
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
		export_filename = "temp/matchups_for_round_"+str(round_num)+"_"+str(exportcode)+".csv"
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


def export_official_ballot(allocations, round_num):
	if len(allocations[0].grid.teams) == 2:
		export_filename = "public/ballot_for_round_"+str(round_num)+".csv"
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
		export_filename = "public/ballot_for_round_"+str(round_num)+".csv"
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

def export_dummy_results_adj(allocations, round_num):
	if len(allocations[0].grid.teams):
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
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
		with open("private/Results_of_adj"+str(round_num)+".csv", "w") as g:
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
	
def reset():
	filename_list = ['temp/tm.csv', 'temp/vn.csv', 'temp/aj.csv', 'private/Results_of_adjudicators.csv', 'private/Results_of_debaters.csv', 'private/Results_of_teams.csv']
	filename_list.extend(['private/Results'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['private/Results_of_adj'+str(i)+'.csv' for i in range(50)])
	filename_list.extend(['public/ballot_for_round_'+str(i)+'.csv' for i in range(50)])
	to_folder = 'backups/'+str(int(time.time()))+'/'
	os.mkdir(to_folder)
	for filename in filename_list:
		try:
			shutil.move(filename, to_folder)
		except:
			continue
	filename_list = ['backups/dat/teams.csv', 'backups/dat/adjudicators.csv', 'backups/dat/venues.csv']
	to_file_list = ['dat/teams.csv', 'dat/adjudicators.csv', 'dat/venues.csv']
	for filename, to_file in zip(filename_list, to_file_list):
		#try:
			shutil.copyfile(filename, to_file)
		#except:
		#	continue
	print "successfully moved files"

def backup_data():
	filename_list = ['dat/teams.csv', 'dat/adjudicators.csv', 'dat/venues.csv']
	to_folder = 'backups/dat'
	for filename in filename_list:
		try:
			shutil.copy(filename, to_folder)
		except:
			continue

def check_results_of_adj(filename, teamnum2):
	if teamnum2:
		f = open(filename, 'r')
		reader = csv.reader(f)
		header = next(reader)
		regexp = re.compile(r'^[0-9A-Za-z. ¥-]+$')

		results_lists = []

		for row in reader:
			for ele in row:
				hit = regexp.search(ele)
				if hit is None:
					print("warning: results of adj file is using unknown character(fullwidth forms or other symbols)", ele)
			results_lists.append([row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), row[6], row[7]])

		multi2 = {results_list[0]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[0]] += 1

		for k, v in multi2.items():
			if v > 1:
				print("error in adjudicator name column, row(appears twice):"+k)
				return True

		teams = {results_list[6]:results_list[7] for results_list in results_lists}

		for results_list in results_lists:
			if teams[results_list[6]] != results_list[7]:
				print("error in team columns:"+str(results_list[6]))
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
				print("error in team columns:"+team)
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
					print("warning: results of adj file is using unknown character(fullwidth forms or other symbols)", ele)
			results_lists.append([row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), row[8], row[9], row[10], row[11]])

		multi2 = {results_list[0]:0 for results_list in results_lists}

		for results_list in results_lists:
			multi2[results_list[0]] += 1

		for k, v in multi2.items():
			if v > 1:
				print("error in adjudicator name column, row(appears twice):"+k)
				time.sleep(5)
				#return True

		teams = {results_list[8]:[results_list[9], results_list[10], results_list[11]] for results_list in results_lists}

		for results_list in results_lists:
			if teams[results_list[8]] != [results_list[9], results_list[10], results_list[11]]:
				print("error in team columns:"+str(results_list[8]))
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
				print("error in team columns:"+team)
				time.sleep(5)
				#return True

		return False


pass