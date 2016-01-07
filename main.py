# -*- coding: utf-8 -*-
#Todo: mstat, more speed(alg3, 4), sort_adjudicators, type of adjudicators(trainee , panel , chair), adjudicators exchange de adj no basho kawaru
#judge points distribution on team-win/lose, teamscore -adj ranking, adjscore -debater ranking, teamscore-teamranking, role-score distribution, power_pairing_strong, 
from system.modules.internal_modules import *
from system.modules.io_modules import *
from system.modules.classes import *
"""KOYAMAs
from system.modules.mstat_modules import *
import system.modules.plot_modules as plt
import numpy as np
"""
try:
	import readline
except:
	print("readline module is recommended thou this program can work without it")
import re
import copy
import sys
from datetime import datetime
import os.path
import math
import shutil

ROUND_NUM = 4

argvs = sys.argv

STYLE_CFGS = {# => {style name, debater num per team, team num, [score weight], reply indexes}
	"ACADEMIC":{"style": "ACADEMIC", "debater_num_per_team":4, "team_num":2, "score_weight":[1, 1, 1, 1], "reply":[], "num_of_reply":0},
	"NA":{"style": "NA", "debater_num_per_team":2, "team_num":2, "score_weight":[1, 1, 0.5], "reply":[1], "num_of_reply":0},
	"NAFA":{"style": "NAFA", "debater_num_per_team":2, "team_num":2, "score_weight":[1, 1, 1, 1], "reply":[], "num_of_reply":0},
	"PDA":{"style": "PDA", "debater_num_per_team":3, "team_num":2, "score_weight":[1, 1, 1], "reply":[], "num_of_reply":0},
	"ASIAN":{"style": "ASIAN", "debater_num_per_team":3, "team_num":2, "score_weight":[1, 1, 1, 0.5], "reply":[0, 1], "num_of_reply":1},
	"BP":{"style": "BP", "debater_num_per_team":2, "team_num":4, "score_weight":[1, 1], "reply":[], "num_of_reply":0},
	"SMALLBP":{"style": "SMALLBP", "debater_num_per_team":1, "team_num":4, "score_weight":[1], "reply":[], "num_of_reply":0},
	"SMALL":{"style": "SMALL", "debater_num_per_team":1, "team_num":2, "score_weight":[1, 0.5], "reply":[0], "num_of_reply":1}
	}

#MORE THAN THIS YOU NEED TO PREPARE teams.csv FOR EACH MODE
try:
	MODE = argvs[1]
	STYLE_CFG = STYLE_CFGS[MODE]
except:
	print("usage: python main.py [mode] #modes are: "+str(list(STYLE_CFGS.keys())))
	sys.exit()
	


##################################################################


#################### ROLE OF EACH MODULE ####################
# main: wrappers
# internal: functions for iternal process of grids/lattices
# io: export and import data
# classes: classes
# commandline: commandline manipulation functions
# property: extract information from grids/lattices
# filter: functions to add adoptness for grids/lattices
# select: functions to choose best grids/lattices
# bit: wrappers for bit calculation on adoptness
# mstat: functions to analyze results
#
# main---- internal
#       |      |_bit
#       |      |_commandline
#       |      |    |_property
#       |      |    |_bit
#       |      |
#       |      |_property
#       |      |_classes
#       |      |_select
#       |      |    |_property
#       |      |    |_quick
#       |      |
#       |      |_filter
#       |      |    |_bit
#       |      |    |_property
#       |      |
#       |      |_  io
#       |           |_bit
#       |           |_property
#       | 
#       |_ classes
#
#
# mstat---- internal
#       |      |_bit
#       |      |_commandline
#       |      |    |_property
#       |      |    |_bit
#       |      |
#       |      |_property
#       |      |_classes
#       |      |_select
#       |      |    |_property
#       |      |
#       |      |_filter
#       |           |_bit
#       |           |_property
#       | 
#       |_ classes
#       |
#       |_ commandline
#


#cfg/config.csv
#past_opponent, strong power pairing

def finish_round_debug(allocations, round_num, style_cfg, workfolder_name):
	export_random_result_adj(allocations, round_num, style_cfg, workfolder_name+"private/Results_of_adj"+str(round_num)+".csv")
	export_random_result(allocations, round_num, style_cfg, workfolder_name+"private/Results"+str(round_num)+".csv")
	
def prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, round_num, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum, style_cfg, workfolder_name):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		f_names = workfolder_name.split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 2] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				team_a, team_b = None, None
				data[0] = int(data[0])

				for team in team_list:
					if team.name == data[1]:
						team_a = team
					elif team.name == data[2]:
						team_b = team

				if team_a is None or team_b is None:
					print("Please write valid team name")
					continue

				new_matchups = copy.deepcopy(selected_grid_lists_with_info[data[0]-1])

				exchange_teams(new_matchups[0], team_a, team_b)
				#for grid in new_matchups[0]:
				#	if grid.warnings != []:
				#		print grid.warnings
				#print
				new_matchups[1] = return_grid_list_info(new_matchups[0], team_list, round_num, "revised", teamnum)
				new_matchups[1].matchups_no = len(selected_grid_lists_with_info)+1
				export_matchups(new_matchups[0], str(len(selected_grid_lists_with_info)+1)+"team", round_num, workfolder_name)
				selected_grid_lists_with_info.append(new_matchups)
				show_matchups_by_grid(new_matchups, round_num)

			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		
		elif re.match(r'choose', a):
			try:
				d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
				if re.match(r'y', d):
					a = a.replace("choose", "")
					a = a.replace(" ", "")
					num = int(a)

					if num <= len(selected_grid_lists_with_info):
						return selected_grid_lists_with_info[num-1]
					else:
						print("please input a valid matchup_no")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_grid(selected_grid_lists_with_info[num-1], round_num)
			
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'teams', a):
			show_teams(team_list)
		elif re.match(r'venues', a):
			show_venues(venue_list)
		elif re.match(r'results', a):
			print("-------------------------------------result-----------------------------------------")
			show_debater_scores(team_list)
			show_teams_scores(team_list, teamnum)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(adjudicator_list)
		else:
			print("exchange [matchup No.], [team1 name], [team2 name]: exchange these teams and create new matchup")
			print("choose [matchup No.]: choose the matchup")
			print("show [matchup No.]: see again the matchup you selected")
			print("teams")
			print("venues")
			print("results")

def prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, lattice_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		f_names = workfolder_name.split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 3] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				num = int(data[0])
				adjudicator1, adjudicator2 = None, None
				for adjudicator in adjudicator_list:
					if adjudicator.name == data[1]:
						adjudicator1 = adjudicator
					if adjudicator.name == data[2]:
						adjudicator2 = adjudicator
				if adjudicator1 is None or adjudicator2 is None or adjudicator1 == adjudicator2:
					print("please write a valid adjudicator name")
					continue

				new_allocations = copy.deepcopy(selected_lattice_lists_with_info[num-1])

				exchange_adj(new_allocations, adjudicator1, adjudicator2)
				new_allocations[1] = return_lattice_list_info(new_allocations[0], adjudicator_list, constants_of_adj, round_num, "revised", teamnum)
				new_allocations[1].allocation_no = len(selected_lattice_lists_with_info)+1
				export_allocations(new_allocations[0], str(len(selected_lattice_lists_with_info)+1)+"adj", round_num, workfolder_name)
				selected_lattice_lists_with_info.append(new_allocations)
				show_matchups_by_lattice(new_allocations, round_num, constants_of_adj)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'choose', a):
			try:
				d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
				if re.match(r'y', d):
					a = a.replace("choose", "")
					a = a.replace(" ", "")
					num = int(a)

					if num <= len(selected_lattice_lists_with_info):
						selected_lattice_list_with_info = selected_lattice_lists_with_info[num-1]
						print("allocation No."+str(num)+" was chosen successfully")
						return selected_lattice_list_with_info
					else:
						print("please input a valid allocation_No")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_lattice(selected_lattice_lists_with_info[num-1], round_num, constants_of_adj)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		else:
			print("exchange [allocation No.], [adj name], [adj name]: exchange these adjudicators and create new matchup")
			print("choose [allocation No.]: choose the matchup")
			print("show [allocation No.]: see again the matchup you selected")
			print("adjudicators: see all the adjudicators")

def prompt_panel(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		f_names = workfolder_name.split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 4] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				adjudicator1, adjudicator2 = None, None
				for adjudicator in adjudicator_list:
					if adjudicator.name == data[0]:
						adjudicator1 = adjudicator
					if adjudicator.name == data[1]:
						adjudicator2 = adjudicator
				if adjudicator1 is None or adjudicator2 is None or adjudicator1 == adjudicator2:
					print("please write a valid adjudicator name")
					continue
				exchange_adj(allocations, adjudicator1, adjudicator2)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, workfolder_name)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue

		elif re.match(r'delete', a):
			try:
				a = a.replace("delete", "")
				a = a.strip()
				panel = None
				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						panel = adjudicator
						break

				if panel is None:
					print("please write a valid adjudicator name")
					continue

				delete_adj(allocations, panel)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, workfolder_name)

			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'add', a):
			try:
				a = a.replace("add", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				panel = None

				for adjudicator in adjudicator_list:
					if adjudicator.name == data[1]:
						panel = adjudicator
						break

				if panel is None:
					print("please write a valid panel name")
					continue

				add_adj(allocations, data[0], panel)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, workfolder_name)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'proceed', a):
			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'set panel', a):
			set_panel(allocations, adjudicator_list)
			show_matchups_by_lattice(allocations, round_num, constants_of_adj)
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		else:
			print("exchange [panel name 1], [panel name 2]: exchange these panels and create new matchup")
			print("proceed: proceed to next step")
			print("set panel: set panels")
			print("adjudicators: see all the adjudicators")
			print("delete [panel name]: delete panel of '[panel name]'")
			print("add [chair name], [panel_name]: add panel to the debate where [chair name] do a chair")

def prompt_venue(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		f_names = workfolder_name.split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 5] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				venue1, venue2 = None, None
				for venue in venue_list:
					if venue.name == data[0]:
						venue1 = venue
					elif venue.name == data[1]:
						venue2 = venue
				if venue1 is None or venue2 is None or venue1 == venue2:
					print("please write a valid venue name")
					continue

				for lattice in allocations[0]:
					if lattice.venue == venue1:
						lattice.venue = venue2
					elif lattice.venue == venue2:
						lattice.venue = venue1

				show_matchups_by_venue(allocations[0], venue_list, round_num)
				export_allocations(allocations[0], "venue", round_num, workfolder_name)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'proceed', a):
			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				return allocations
		elif re.match(r'venues', a):
			show_venues(venue_list)
		elif re.match(r'set venue', a):
			set_venue(allocations[0], venue_list)
			show_matchups_by_venue(allocations[0], venue_list, round_num)
		else:
			print("exchange [venue name 1], [venue name 2]: exchange these venues and create new matchup")
			print("proceed: proceed to next step")
			print("venues: see all the venues")
			print("set venue: set venues")

def prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum, debater_num_per_team, style_cfg, round_num, workfolder_name):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		f_names = workfolder_name.split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 1] > ")

		if re.match(r'proceed', a):
			if not checks_before_creation(adjudicator_list, venue_list, team_list, teamnum): continue

			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'absent', a):
			try:
				a = a.replace("absent", "")
				a = a.strip()

				for team in team_list:
					if team.name == a:
						team.available = False
						print(team.name + " was set absent successfully")
						break
				else:
					print("Please write a valid team name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'add team', a):####################################################################
			try:
				new_team_name = input("new team name > ")
				debaters = [input("member "+str(i+1)+" > ") for i in range(debater_num_per_team)]
				debater_names = [debater.strip() for debater in debaters]
				#debater4 = debater4.strip()
				institutions_raw = input("institutions (,separation) > ")
				institutions = institutions_raw.split(",")
				new_institutions = []
				for institution in institutions:
					new_institutions.append(institution.strip())
				scale_raw = input("institution scale (a, b, c) > ")
				scale = scale_raw.strip()
				if scale not in ["a", "b", "c"]: continue
				team = Team(len(team_list), new_team_name, debater_names, scale, new_institutions)
				score_list = ['n/a']*len(style_cfg["score_weight"])
				score = ['n/a']
				for i in range(round_num-1):
					team.dummy_finishing_process()
					for debater in team.debaters:
						debater.score_lists_sub.append(score_list)
						debater.scores_sub.append(score)
				team_list.append(team)
				print(new_team_name + "was added to team list successfully")

			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'delete team', a):
			try:
				team_name = input("team name > ")
				team_name = team_name.strip()
				a = input("["+f_name+"]Are you sure you want to delete a team '"+team_name+"' ? (y/n) > ")
				if a != "y":continue

				for team in team_list:
					if team.name == team_name:
						team_list.remove(team)
						print(team_name + " was deleted from team list successfully")
						break
				else:
					print("please write a valid team name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'present', a):
			try:
				a = a.replace("present", "")
				a = a.strip()

				for team in team_list:
					if team.name == a:
						team.available = True
						print(team.name + " was set present successfully")
						break
				else:
					print("Please write a valid team name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'roomnotavailable', a):
			try:
				a = a.replace("roomnotavailable", "")
				a = a.strip()

				for venue in venue_list:
					if venue.name == a:
						venue.available = False
						print(venue.name + " was set not available successfully")
						break
				else:
					print("Please write a valid venue name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'roomavailable', a):
			try:
				a = a.replace("roomavailable", "")
				a = a.strip()

				for venue in venue_list:
					if venue.name == a:
						venue.available = True
						print(venue.name + " was set available successfully")
						break
				else:
					print("Please write a valid venue name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjabsent', a):
			try:
				a = a.replace("adjabsent", "")
				a = a.strip()

				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						adjudicator.absent = True
						print(adjudicator.name + " was set absent successfully")
						break
				else:
					print("Please write a valid adjudicator name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjpresent', a):
			try:
				a = a.replace("adjpresent", "")
				a = a.strip()

				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						adjudicator.absent = False
						print(adjudicator.name + " was set present successfully")
						break
				else:
					print("Please write a valid adjudicator name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		elif re.match(r'add venue', a):
			try:
				venue_name = input("venue name > ")
				venue_name = venue_name.strip()
				priority = int(input("venue priority [1, 3] > "))

				venue_list.append(Venue(venue_name, priority))
				print(venue_name + " was added to venues successfully(priority:"+str(priority)+")")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue

		elif re.match(r'delete venue', a):
			try:
				venue_name = input("venue name > ")
				venue_name = venue_name.strip()

				for venue in venue_list:
					if venue.name == venue_name:
						venue_list.remove(venue)
						print(venue_name + " was deleted from venues successfully")
						break
				else:
					print("please write a valid venue name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'add adjudicator', a):
			try:
				adjudicator_name = input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()
				if adjudicator_name in [adjudicator.name for adjudicator in adjudicator_list]:
					print("the adjudicator already exists in adjudicator list")
					continue
				if adjudicator_name == "":
					print("please type a valid name")
					continue
				reputation = int(input("reputation[0, 10] > "))
				judge_test = int(input("judge test[0, 10] > "))
				institutions_raw = input("institutions (,separation) > ")
				institutions = institutions_raw.split(",")
				new_institutions = []
				for institution in institutions:
					new_institutions.append(institution.strip())
				conflict_teams_raw = input("conflict teams (,separation) > ")
				conflict_teams = conflict_teams_raw.split(",")
				new_conflict_teams = []
				for conflict_team in conflict_teams:
					new_conflict_teams.append(conflict_team.strip())
				adjudicator = Adjudicator(len(adjudicator_list), adjudicator_name, reputation, judge_test, new_institutions, new_conflict_teams)
				for i in range(round_num-1):
					adjudicator.dummy_finishing_process()
					adjudicator.watched_debate_ranks_sub.append('n/a')
				adjudicator_list.append(adjudicator)

				print(adjudicator_name + " was added to adjudicator list successfully")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'delete adjudicator', a):
			try:
				adjudicator_name = input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()

				a = input("["+f_name+"]Are you sure you want to delete a team '"+adjudicator_name+"' ? (y/n) > ")
				if a != "y":continue

				for adjudicator in adjudicator_list:
					if adjudicator.name == adjudicator_name:
						adjudicator_list.remove(adjudicator)
						print(adjudicator_name + " was deleted from adjudicator list successfully")
						break
				else:
					print("please write a valid adjudicator name")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'teams', a):
			show_teams(team_list)
		elif re.match(r'venues', a):
			show_venues(venue_list)
		elif re.match(r'results', a):
			print("-------------------------------------result-----------------------------------------")
			show_debater_scores(team_list)
			show_teams_scores(team_list, teamnum)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(adjudicator_list)

		else:
			print("proceed: see the matchups for next round")
			print("absent [team name]: set the team as absent")
			print("present [team name]: set the absent team as present")
			print("adjabsent [adj name]: set the adjudicator as absent")
			print("adjpresent [adj_name]: set the absent adjudicator as present")
			print("roomnotavailable [room name]: set the room as absent")
			print("roomavailable [room name]: set the absent room as present")
			print("teams: see all participating teams")
			print("venues: see all available venues")
			print("adjudicators: see all available venues")
			print("resuls: see all available venues")
			print("add team: add a team")
			print("delete team: delete a team(irreversible!)")
			print("add venue: add a venue")
			print("delete venue: delete a venue(irreversible!)")
			print("add adjudicator: add an adjudicator")
			print("delete adjudicator: delete an adjudicator(irreversible!)")

def create_matchups(grid_list, round_num, team_list, filter_lists, teamnum, workfolder_name):
	progress("[creating matchups for round "+str(round_num)+"]")
	progress("filtering grid list")
	filtration(grid_list, round_num, team_list, filter_lists)
	progress("adding priority to grids")
	addpriority(grid_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	progress("selecting grids")
	selected_grid_lists_with_info = return_selected_grid_lists(grid_list, round_num, team_list, teamnum)

	for k, selected_grid_list_with_info in enumerate(selected_grid_lists_with_info):
		export_matchups(selected_grid_list_with_info[0], str(k)+"team", round_num, workfolder_name)
		selected_grid_list_with_info[1].matchups_no = k+1

	return selected_grid_lists_with_info

def create_allocations(adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, round_num, filter_lists, constants_of_adj, teamnum, workfolder_name):
	progress("[creating allocations for round "+str(round_num)+"]")
	progress("filtering lattice list")
	lattice_filtration(adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, round_num, filter_lists)
	progress("adding priority to grids")
	addpriority(lattice_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	progress("selecting lattices")
	selected_lattice_lists_with_info = return_selected_lattice_lists(lattice_list, round_num, team_list, adjudicator_list, constants_of_adj, teamnum)
	for k, selected_lattice_list_with_info in enumerate(selected_lattice_lists_with_info):
		export_allocations(selected_lattice_list_with_info[0], str(k)+"adj", round_num, workfolder_name)
		selected_lattice_list_with_info[1].allocation_no = k+1

	return selected_lattice_lists_with_info

def preparation(filename_teams, filename_venues, filename_adjudicators, filename_settings, filename_settings_of_adj, style_cfg):
	team_list = read_teams(filename_teams, style_cfg)
	venue_list = read_venues(filename_venues)
	check_team_list(team_list)
	adjudicator_list = read_adjudicators(filename_adjudicators)
	check_adjudicator_list(adjudicator_list)

	constants, orders1 = read_constants(filename_settings)
	filter_lists = create_filter_lists(orders1)
	constants_of_adj, orders2, break_team_nums = read_constants_of_adj(filename_settings_of_adj)
	filter_of_adj_lists = create_filter_of_adj_lists(orders2)

	return team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, break_team_nums




def arrange_data(adjudicator_list, constants_of_adj, team_list):
	evaluate_adjudicator(adjudicator_list, constants_of_adj)
	sort_adjudicator_list_by_score(adjudicator_list)
	sort_team_list_by_score(team_list)

def export_info(adjudicator_list, team_list, round_num, style_cfg, workfolder_name):
	export_results(team_list, adjudicator_list, workfolder_name+"private/round_info/Results_of_adjudicators_by_R"+str(round_num)+".csv", workfolder_name+"private/round_info/Results_of_debaters_by_R"+str(round_num-1)+".csv", workfolder_name+"private/round_info/Results_of_teams_by_R"+str(round_num-1)+".csv", style_cfg)
	export_adj_info(adjudicator_list, workfolder_name+"private/round_info/Adjudicators_info_by_R"+str(round_num)+".csv")

def show_data(adjudicator_list, team_list, teamnum):
	sort_adjudicator_list_by_score(adjudicator_list)
	sort_team_list_by_score(team_list)

	show_debater_scores(team_list)
	show_teams_scores(team_list, teamnum)
	#show_evaluation(adjudicator_list)
	show_adjudicator_score(adjudicator_list)

def return_imported_allocations(constants_of_adj, grid_list, team_list, adjudicator_list, venue_list, teamnum, round_num, break_team_num, workfolder_name):
	selected_lattice_list = import_matchup(workfolder_name+"matchups_imported/matchups_for_round_"+str(round_num)+".csv", grid_list, team_list, adjudicator_list, venue_list, teamnum)
	selected_grid_list = [lattice.grid for lattice in selected_lattice_list]
	selected_grid_list_info = return_grid_list_info(selected_grid_list, team_list, round_num, "", teamnum)
	selected_grid_list_info.matchup_no = 0
	selected_grid_list_with_info = [selected_grid_list, selected_grid_list_info]
	prioritize_bubble_round(round_num, adjudicator_list, selected_grid_list, team_list, selected_lattice_list, break_team_num, 0)
	selected_lattice_list_info = return_lattice_list_info(selected_lattice_list, adjudicator_list, constants_of_adj, round_num, "", teamnum)
	selected_lattice_list_info.allocation_no = 1
	allocations = [selected_lattice_list, selected_lattice_list_info]
	return allocations, selected_grid_list_with_info

def main_demo(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	if not checks_before_creation(adjudicator_list, venue_list, team_list, teamnum): sys.exit(4)
	for i in range(rounds):
		#export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
		arrange_data(adjudicator_list, constants_of_adj, team_list)

		progress("creating grid list")

		grid_list = create_grid_list(team_list, teamnum)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=workfolder_name)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = selected_grid_lists_with_info[-1]
		export_matchups(matchups[0], "matchups_without_adj", i+1, workfolder_name)

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=workfolder_name)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = selected_lattice_lists_with_info[-1]

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1, "chosen", teamnum)
		set_panel(allocations, adjudicator_list)
		export_allocations(allocations[0], "panel", i+1, workfolder_name)

		set_venue(allocations[0], venue_list)
		export_allocations(allocations[0], "venue", i+1, workfolder_name)

		export_official_matchups(allocations[0], i+1, workfolder_name)
		export_blank_results(allocations[0], i+1, style_cfg, workfolder_name+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, workfolder_name+"blankresults/Results_of_adj"+str(i+1)+".csv")
		export_dummy_results_adj(allocations[0], i+1, style_cfg, workfolder_name)
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1, style_cfg=style_cfg, workfolder_name=workfolder_name)
		read_and_process_result(round_num=i+1, team_list=team_list, style_cfg=style_cfg, filename_results = workfolder_name+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"private/Results_of_adj"+str(i+1)+".csv")

		show_data(adjudicator_list, team_list, teamnum)
		export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
		check_team_list2(team_list, i+1, teamnum)
	
	export_results(team_list, adjudicator_list, workfolder_name+"private/final_result/Results_of_adjudicators.csv", workfolder_name+"private/final_result/Results_of_debaters.csv", workfolder_name+"private/final_result/Results_of_teams.csv", style_cfg)

def main_complete(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, no_adj, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	for i in range(rounds):
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		print("-----------------Round "+str(i+1)+"-----------------")
		#export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
		prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum, debater_num_per_team, style_cfg, i+1, workfolder_name)
		arrange_data(adjudicator_list, constants_of_adj, team_list)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum)

		fn_match = "matchups_imported/matchups_for_round_"+str(i+1)+".csv"
		fn = "private/Results"+str(i+1)+".csv"
		fn_adj = "private/Results_of_adj"+str(i+1)+".csv"
		results_read = False
		matchups_read = False
		allocations = None

		while True:
			if os.path.exists(workfolder_name+fn):
				root, ext = os.path.splitext(workfolder_name+fn)
				a = input("The Results file already exists in private folder. Do you want to read the result '"+root+ext+"'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							read_and_process_result(round_num=i+1, team_list=team_list, style_cfg=style_cfg, filename_results = workfolder_name+"private/Results"+str(i+1)+".csv")
							progress("processed results of round "+str(i+1))
							results_read = True
							break
						except:
							print("failed to read Results file")
							a = input("Do you still want to read the result '"+root+ext+"'? (y/n) > ")
							if re.match(r'y', a):
								continue
							elif re.match(r'n', a):
								break
					break
				elif re.match(r'n', a):
					break
				else:
					continue
				break
			else:
				break

		while True:
			if os.path.exists(workfolder_name+fn_adj):
				root, ext = os.path.splitext(workfolder_name+fn_adj)
				a = input("The Results file already exists in private folder. Do you want to read the result '"+root+ext+"'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"private/Results_of_adj"+str(i+1)+".csv")
							progress("processed results_of_adj of round "+str(i+1))
							results_read = True
							break
						except:
							print("failed to read Results of adj file")
							a = input("Do you still want to read the result '"+root+ext+"'? (y/n) > ")
							if re.match(r'y', a):
								continue
							elif re.match(r'n', a):
								try:
									read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"dummyresults/Results_of_adj"+str(i+1)+".csv")
								except:
									print("Unexpected error:", sys.exc_info()[0])
								break
					break
				elif re.match(r'n', a):
					try:
						read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"dummyresults/Results_of_adj"+str(i+1)+".csv")
					except:
						print("Unexpected error:", sys.exc_info()[0])
					break
				else:
					continue
				break
			else:
				break

		if results_read:
			continue

		while True:
			if os.path.exists(workfolder_name+fn_match):
				root, ext = os.path.splitext(workfolder_name+fn_match)
				a = input("Read imported matchup 'matchups_imported/matchups_for_round_"+str(i+1)+".csv'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							allocations = edit_revised_matchups(constants_of_adj, grid_list, team_list, adjudicator_list, venue_list, teamnum, i+1, break_team_nums[i], workfolder_name, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, style_cfg)
							matchups_read = True
							break
						except:
							print("Unexpected error:", sys.exc_info()[0])
							print("failed to read matchups file")
							a = input("Do you still want to read the matchups '"+root+ext+"'? (y/n) > ")
							if re.match(r'y', a):
								continue
							elif re.match(r'n', a):
								break
					break
				elif re.match(r'n', a):
					break
				else:
					continue
				break
			else:
				break

		if not matchups_read:
			selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=workfolder_name)
			for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_grid(selected_grid_list_with_info, i+1)
			matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum, style_cfg, workfolder_name)
			export_matchups(matchups[0], "matchups_without_adj", i+1, workfolder_name)

			prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum, debater_num_per_team, style_cfg, i+1, workfolder_name)

			lattice_list = create_lattice_list(matchups[0], adjudicator_list)
			selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=workfolder_name)
			for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
			allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name)

			allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1, "chosen", teamnum)
			prompt_panel(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
			export_allocations(allocations[0], "panel", i+1, workfolder_name)

			prompt_venue(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
			export_allocations(allocations[0], "venue", i+1, workfolder_name)

			while True:
				print("generated matchups in 'public'")
				a = input("read revised matchup 'matchups_imported/matchups_for_round_"+str(i+1)+".csv'? (y/n) > ")
				if re.match(r'y', a):
					try:
						allocations, selected_grid_list_with_info = return_imported_allocations(constants_of_adj, grid_list, team_list, adjudicator_list, venue_list, teamnum, i+1, break_team_nums[i], workfolder_name)
						break
					except Exception as inst:
						print(inst)
						continue
				elif re.match(r'n', a):
					break

		export_official_matchups(allocations[0], i+1, workfolder_name)
		export_blank_results(allocations[0], i+1, style_cfg, workfolder_name+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, workfolder_name+"blankresults/Results_of_adj"+str(i+1)+".csv")
		show_matchups(allocations, i+1)

		export_dummy_results_adj(allocations[0], i+1, style_cfg, workfolder_name)

		while True:
			a = input("read results of round {0}? (y/n) > ".format(i+1))
			if re.match(r'y', a):
				try:
					read_and_process_result(round_num=i+1, team_list=team_list, style_cfg=style_cfg, filename_results = workfolder_name+"private/Results"+str(i+1)+".csv")
					break
				except:
					progress("failed to read results")
					continue
			elif re.match(r'n', a):
				break
		if no_adj:
			try:
				read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"dummyresults/Results_of_adj"+str(i+1)+".csv")
			except:
				print("warning: results_of_adj file broken")
				print("you can still use this program but cannot use the '(adjudicators) avoid watched teams' feature")
				pass
		else:
			while True:
				a = input("read results_of_adj of round {0}? (y/n) > ".format(i+1))
				if re.match(r'y', a):
					try:
						read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"private/Results_of_adj"+str(i+1)+".csv")
						break
					except:
						progress("failed to read results of adjs")
						continue 
				elif re.match(r'n', a):
					break

		show_data(adjudicator_list, team_list, teamnum)
		check_team_list2(team_list, i+1, teamnum)
		export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
	
	export_results(team_list, adjudicator_list, workfolder_name+"private/final_result/Results_of_adjudicators.csv", workfolder_name+"private/final_result/Results_of_debaters.csv", workfolder_name+"private/final_result/Results_of_teams.csv", style_cfg)

def main_quick_debug(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	for i in range(rounds):
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
		prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum, debater_num_per_team, style_cfg, i+1, workfolder_name)
		arrange_data(adjudicator_list, constants_of_adj, team_list)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)

		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=workfolder_name)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum, style_cfg, workfolder_name)
		export_matchups(matchups[0], "matchups_without_adj", i+1, workfolder_name)

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=workfolder_name)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name)

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1, "chosen", teamnum)
		set_panel(allocations, adjudicator_list)
		export_allocations(allocations[0], "panel", i+1, workfolder_name)
		
		set_venue(allocations[0], venue_list)
		export_allocations(allocations[0], "venue", i+1, workfolder_name)

		export_official_matchups(allocations[0], i+1, workfolder_name)
		export_blank_results(allocations[0], i+1, style_cfg, workfolder_name+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, workfolder_name+"blankresults/Results_of_adj"+str(i+1)+".csv")
		export_dummy_results_adj(allocations[0], i+1, style_cfg, workfolder_name)
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1, style_cfg=style_cfg, workfolder_name=workfolder_name)
		read_and_process_result(round_num=i+1, team_list=team_list, style_cfg=style_cfg, filename_results = workfolder_name+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"private/Results_of_adj"+str(i+1)+".csv")
	
		show_data(adjudicator_list, team_list, teamnum)
		check_team_list2(team_list, i+1, teamnum)
		export_info(adjudicator_list, team_list, i+1, style_cfg, workfolder_name)
	
	export_results(team_list, adjudicator_list, workfolder_name+"private/final_result/Results_of_adjudicators.csv", workfolder_name+"private/final_result/Results_of_debaters.csv", workfolder_name+"private/final_result/Results_of_teams.csv", style_cfg)

def main_graph(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	"""
	for i in range(rounds):
		read_and_process_result(round_num=i+1, team_list=team_list, style_cfg=style_cfg, filename_results = workfolder_name+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum=teamnum, filename_results_of_adj=workfolder_name+"private/Results_of_adj"+str(i+1)+".csv")
	
		show_data(adjudicator_list, team_list, teamnum)
		check_team_list2(team_list, i+1, teamnum)
	
	export_results(team_list, adjudicator_list, workfolder_name+"private/final_result/Results_of_adjudicators.csv", workfolder_name+"private/final_result/Results_of_debaters.csv", workfolder_name+"private/final_result/Results_of_teams.csv", style_cfg)
	mstat(adjudicator_list, team_list, teamnum, rounds)
	"""

def edit_revised_matchups(constants_of_adj, grid_list, team_list, adjudicator_list, venue_list, teamnum, round_num, break_team_num, workfolder_name, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, style_cfg):
	try:
		allocations, selected_grid_list_with_info = return_imported_allocations(constants_of_adj, grid_list, team_list, adjudicator_list, venue_list, teamnum, round_num, break_team_num, workfolder_name)
	except Exception as inst:
		print(inst)
		raise Exception("could not read imported matchups")

	selected_grid_list_with_info[1].matchups_no = 1
	show_matchups_by_grid(selected_grid_list_with_info, round_num)

	matchups = prompt([selected_grid_list_with_info], team_list, venue_list, adjudicator_list, grid_list, round_num, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum, style_cfg, workfolder_name)
	export_matchups(matchups[0], "matchups_without_adj", round_num, workfolder_name)

	lattice_list = create_lattice_list(matchups[0], adjudicator_list)

	allocations = merge_matchups_and_allocations(matchups, allocations, lattice_list, round_num, adjudicator_list, constants_of_adj, teamnum)

	show_matchups_by_lattice(allocations, round_num, constants_of_adj)
	allocations = prompt_adj([allocations], team_list, venue_list, adjudicator_list, grid_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name)

	prompt_panel(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
	export_allocations(allocations[0], "panel", round_num, workfolder_name)

	prompt_venue(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, filename_venues, filename_adjudicators, style_cfg, workfolder_name)
	export_allocations(allocations[0], "venue", round_num, workfolder_name)

	return allocations

def prompt_beginning(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, style_cfg, workfolder_name):
	while True:
		a = input("Please type a command(you can see commands by typing 'help') [step 0] > ")

		if a == 'demo':
			main_demo(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name)
		elif a == 'no_adj_feedback':
			main_complete(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, True, style_cfg, workfolder_name)
		elif a == 'run':
			main_complete(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, False, style_cfg, workfolder_name)
		elif a == 'debug':
			main_quick_debug(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name)
		elif a == 'graph':
			main_graph(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, break_team_nums, style_cfg, workfolder_name)
		else:
			print("run: start this program")
			print("no_adj_feedback: start this program without team2adj feedback")
			print("debug: debug this program with adj (may change the Results files)")
			print("demo: see demo of this program automatically (may change the Results files)")
			print("helper: help other tabulation program (read matchups from other tabulation program)")
			print("graph: plot graph")

			continue
		break

def mstat(adjudicator_list, team_list, teamnum, rounds):
	plt.plot_ira_abs(adjudicator_list, team_list, rounds, teamnum)
	plt.plot_ira_pm(adjudicator_list, team_list, rounds, teamnum)
	plt.plot_ira_sd(adjudicator_list, team_list, rounds, teamnum)
	#plt.plot_ira_3(adjudicator_list, team_list, rounds, teamnum)

	"""
	all_debaters = [debater for team in team_list for debater in team.debaters]
	for debater, k in zip(all_debaters, range(6)):
		scores = [debater.scores_sub[i] for i in range(4)]
		rankings = [debater.rankings_sub[i] for i in range(4)]
		print  scores, rankings
		plt.line_graph_1d(scores)
		plt.line_graph_1d(rankings)
	wins_all = []
	scores_all = []
	if teamnum == 2:
		sides = ["gov", "opp"]
	else:
		sides = ["og", "oo", "cg", "co"]
	for i in range(ROUND_NUM):
		wins_all.append(get_wins_by_side(team_list, teamnum, i+1))
		scores_all.append(get_scores_by_side(team_list, teamnum, i+1))
	print wins_all
	print scores_all
	for i in range(len(wins_all)):
		print "round "+str(i+1)
		for side in sides:
			print side, get_win_ratio(wins_all[i], side), std_2_distri(wins_all[i][side])
			print wins_all[i][side]
			print scores_all[i][side]
		if teamnum == 2:
			print "win-percentages t test", get_ttest_text(wins_all[i]["gov"], wins_all[i]["opp"])
			print "scores t test", get_ttest_text(scores_all[i]["gov"], scores_all[i]["opp"])
		plt.hist([scores_all[i]["gov"], scores_all[i]["opp"]])
	plt.hist([[score for scores in scores_all for score in scores["gov"]], [score for scores in scores_all for score in scores["opp"]]])

	percentage_list = []
	std_list = []
	for i in range(len(wins_all)):
		percentage_list.append(100*get_win_ratio(wins_all[i], "gov"))
		std_list.append(100*std_2_distri(wins_all[i]["gov"]))

	#plt.bar_1d(sorted(scores_all[0]["gov"], reverse=True))
	plt.bar_1d(sorted(get_debater_score(team_list), reverse=True))
	plt.line_graph_1d(sorted(get_debater_score(team_list), reverse=True))
	#print percentage_list, std_list
	plt.bar_sd2(percentage_list, std_list)
	plt.bar_sd3(percentage_list, std_list, teamnum)
	#plt.hist([scores["gov"] for scores in scores_all]+[scores["opp"] for scores in scores_all])
	#plt.hist([wins["gov"] for wins in wins_all]+[wins["opp"] for wins in wins_all])
	"""

def get_workfolder():
	workfolder_name = ""
	folder_names = ["dat", "cfg", "public", "private", "private/final_result", "private/round_info", "matchups_imported", "blankresults", "dummyresults", "temp"]
	while True:
		a = input("Please type a command(you can see commands by typing 'help') [step -1] > ")
		if re.match(r'choose', a):
			fn = a.replace("choose", "")
			fn = fn.strip()
			br = False
			if re.match(r'^_', fn):
				print("the workfolder ", fn, "is an unsubstantial workfolder to generate substantial workfolder")
				while True:
					b = input("Are you sure to choose the workfolder and treat it as substantial? (y/n) > ")
					if b == "y":
						break
					elif b == 'n':
						br = True
						break
			if br: continue
			fn = "workfolders/"+fn
			if os.path.exists(fn):
				workfolder_name = fn
				print("the workfolder "+fn+" was selected successfully")
				break
			else:
				print("Please write a valid workfolder name")
		elif re.match(r'create', a):
			try:
				fn = a.replace("create", "")
				fn = fn.strip()
				fn = "workfolders/"+fn

				if not os.path.exists(fn):
					os.mkdir(fn)
					for folder_name in folder_names:
						os.mkdir(fn+"/"+folder_name)
					print("the workfolder "+fn+" was created successfully")
				else:
					print("the workfolder you want to create already exists")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'backup', a):
			try:
				fn = a.replace("backup", "")
				fn = fn.strip()
				fn = "workfolders/"+fn
				datetimenow = datetime.now()
				nowtime = datetimenow.strftime('%m')+datetimenow.strftime('%d')+datetimenow.strftime('%H')+datetimenow.strftime('%M')+datetimenow.strftime('%S')
				shutil.copytree(fn, fn+"_backup"+nowtime)
				print("the workfolder "+fn+"_backup"+nowtime+" was created successfully")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'delete', a):
			try:
				fn = a.replace("delete", "")
				fn = fn.strip()
				fn = "workfolders/"+fn
				shutil.rmtree(fn)
				print("the workfolder "+fn+" was deleted successfully")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'copy', a):
			try:
				fn = a.replace("copy", "")
				fn = fn.strip()
				fns = fn.split(" ")
				fns = ["workfolders/"+fn.strip() for fn in fns]

				if os.path.exists(fns[0]):
					while True:
						if not os.path.exists(fns[1]):
							shutil.copytree(fns[0], fns[1])
							break
					print("the workfolder "+fns[1]+" was created successfully")
				else:
					print("the workfolder "+fns[0]+" does not exist")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'init', a):
			try:
				fn = a.replace("init", "")
				fn = fn.strip()
				fns = fn.split(" ")
				fns = ["workfolders/"+fn.strip() for fn in fns]

				if os.path.exists(fns[0]):
					while True:
						if not os.path.exists(fns[1]):
							datetimenow = datetime.now()
							folder_name = datetimenow.strftime('%m')+datetimenow.strftime('%d')+datetimenow.strftime('%H')+datetimenow.strftime('%M')+datetimenow.strftime('%S')
							shutil.copytree(fns[0], fns[1])
							reset_except_dat_cfg(fns[1]+"/")
							print("the workfolder "+fns[1]+" was created successfully")
							break
						else:
							print("the workfolder "+fns[1]+" already exists")
							break
				else:
					print("the workfolder "+fns[0]+" does not exist")
			except:
				print("Unexpected error:", sys.exc_info()[0])
		elif re.match(r'show', a):
			try:
				workfolder_names = os.listdir("workfolders/")
				string = ""
				for name in workfolder_names:
					string = string + name + ", "
				print(string)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue
		else:
			print("choose [workfolder name]: select the workfolder")
			print("create [workfolder name]: create a workfolder named [workfolder name]")
			print("copy [workfolder name from] [workfolder name to]: copy a workfolder named [workfolder name from] to [workfolder name to]")
			print("init [workfolder name from] [workfolder name to]: initialize a workfolder named [workfolder name from] to [workfolder name to] only take over the dat,cfg folders")
			print("backup [workfolder name]: backup a workfolder named [workfolder name]")
			print("delete [workfolder name]: delete a workfolder named [workfolder name] (irreversible!)")
			print("show: show all workfolders")

	return workfolder_name+"/"

if __name__ == "__main__":
	#show_logo_random_fade()
	#show_logo_star()
	WORKFOLDER_NAME = get_workfolder()
	FILENAME_SETTINGS = WORKFOLDER_NAME+"cfg/config.csv"
	FILENAME_SETTINGS_OF_ADJ = WORKFOLDER_NAME+"cfg/constants_of_adj.csv"

	################### DO NOT CHANGE THIS ###################
	FILENAME_VENUES = WORKFOLDER_NAME+"dat/venues.csv"
	FILENAME_TEAMS = WORKFOLDER_NAME+"dat/teams.csv"
	FILENAME_ADJUDICATORS = WORKFOLDER_NAME+"dat/adjudicators.csv"
	
	team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, break_team_nums = preparation(FILENAME_TEAMS, FILENAME_VENUES, FILENAME_ADJUDICATORS, FILENAME_SETTINGS, FILENAME_SETTINGS_OF_ADJ, STYLE_CFG)
	initial_check(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, STYLE_CFG)
	load(adjudicator_list, venue_list, team_list, STYLE_CFG, WORKFOLDER_NAME)
	prompt_beginning(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, ROUND_NUM, FILENAME_TEAMS, FILENAME_VENUES, FILENAME_ADJUDICATORS, break_team_nums, STYLE_CFG, WORKFOLDER_NAME)

pass