# -*- coding: utf-8 -*-
#Todo: mstat, more speed(alg3, 4), sort_adjudicators, type of adjudicators(trainee , panel , chair), adjudicators exchange de adj no basho kawaru
#judge points distribution on team-win/lose, teamscore -adj ranking, adjscore -debater ranking, teamscore-teamranking, role-score distribution, power_pairing_strong, 
from system.modules.internal_modules import *
from system.modules.io_modules import *
from system.modules.classes import *
from system.modules import interaction_modules
"""KOYAMAs
from system.modules.mstat_modules import *
import system.modules.plot_modules as plt
import numpy as np
"""
try:
	import readline
except:
	interaction_modules.progress("readline module is recommended thou this program can work without it")
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
	interaction_modules.progress("usage: python main.py [mode] #modes are: "+str(list(STYLE_CFGS.keys())))
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
	
def prompt(selected_grid_lists_with_info, tournament, grid_list, round_num, fnames, debater_num_per_team, teamnum, style_cfg):
	while True:
		save(tournament, fnames, style_cfg)
		f_names = fnames["workfolder"].split("/")
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

				for team in tournament["team_list"]:
					if team.name == data[1]:
						team_a = team
					elif team.name == data[2]:
						team_b = team

				if team_a is None or team_b is None:
					interaction_modules.warn("Please write valid team name")
					continue

				new_matchups = copy.deepcopy(selected_grid_lists_with_info[data[0]-1])

				exchange_teams(new_matchups[0], team_a, team_b)
				#for grid in new_matchups[0]:
				#	if grid.warnings != []:
				#		print grid.warnings
				#print
				new_matchups[1] = return_grid_list_info(new_matchups[0], tournament, round_num, "revised", teamnum)
				new_matchups[1].matchups_no = len(selected_grid_lists_with_info)+1
				export_matchups(new_matchups[0], str(len(selected_grid_lists_with_info)+1)+"team", round_num, fnames["workfolder"])
				selected_grid_lists_with_info.append(new_matchups)
				show_matchups_by_grid(new_matchups, round_num)

			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
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
						interaction_modules.warn("please raw_input a valid matchup_no")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_grid(selected_grid_lists_with_info[num-1], round_num)
			
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'teams', a):
			show_teams(tournament["team_list"])
		elif re.match(r'venues', a):
			show_venues(tournament["venue_list"])
		elif re.match(r'results', a):
			interaction_modules.commandline("-------------------------------------result-----------------------------------------")
			show_debater_scores(tournament["team_list"])
			show_teams_scores(tournament["team_list"], teamnum)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(tournament["adjudicator_list"])
		else:
			interaction_modules.commandline("exchange [matchup No.], [team1 name], [team2 name]: exchange these teams and create new matchup")
			interaction_modules.commandline("choose [matchup No.]: choose the matchup")
			interaction_modules.commandline("show [matchup No.]: see again the matchup you selected")
			interaction_modules.commandline("teams")
			interaction_modules.commandline("venues")
			interaction_modules.commandline("results")

def prompt_adj(selected_lattice_lists_with_info, tournament, lattice_list, round_num, fnames, constants_of_adj, style_cfg):
	teamnum = style_cfg["team_num"]
	while True:
		save(tournament, fnames, style_cfg)
		f_names = fnames["workfolder"].split("/")
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
				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == data[1]:
						adjudicator1 = adjudicator
					if adjudicator.name == data[2]:
						adjudicator2 = adjudicator
				if adjudicator1 is None or adjudicator2 is None or adjudicator1 == adjudicator2:
					interaction_modules.warn("please write a valid adjudicator name")
					continue

				new_allocations = copy.deepcopy(selected_lattice_lists_with_info[num-1])

				exchange_adj(new_allocations, adjudicator1, adjudicator2)
				new_allocations[1] = return_lattice_list_info(new_allocations[0], tournament, constants_of_adj, round_num, "revised", teamnum)
				new_allocations[1].allocation_no = len(selected_lattice_lists_with_info)+1
				export_allocations(new_allocations[0], str(len(selected_lattice_lists_with_info)+1)+"adj", round_num, fnames["workfolder"])
				selected_lattice_lists_with_info.append(new_allocations)
				show_matchups_by_lattice(new_allocations, round_num, constants_of_adj)
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
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
						interaction_modules.progress("allocation No."+str(num)+" was chosen successfully")
						return selected_lattice_list_with_info
					else:
						interaction_modules.warn("please raw_input a valid allocation_No")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_lattice(selected_lattice_lists_with_info[num-1], round_num, constants_of_adj)
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(tournament["adjudicator_list"])
		else:
			interaction_modules.commandline("exchange [allocation No.], [adj name], [adj name]: exchange these adjudicators and create new matchup")
			interaction_modules.commandline("choose [allocation No.]: choose the matchup")
			interaction_modules.commandline("show [allocation No.]: see again the matchup you selected")
			interaction_modules.commandline("adjudicators: see all the adjudicators")

def prompt_panel(allocations, tournament, round_num, fnames, constants_of_adj, style_cfg):
	teamnum = style_cfg["team_num"]
	while True:
		save(tournament, fnames, style_cfg)
		f_names = fnames["workfolder"].split("/")
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
				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == data[0]:
						adjudicator1 = adjudicator
					if adjudicator.name == data[1]:
						adjudicator2 = adjudicator
				if adjudicator1 is None or adjudicator2 is None or adjudicator1 == adjudicator2:
					interaction_modules.warn("please write a valid adjudicator name")
					continue
				exchange_adj(allocations, adjudicator1, adjudicator2)
				allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, fnames["workfolder"])
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue

		elif re.match(r'delete', a):
			try:
				a = a.replace("delete", "")
				a = a.strip()
				panel = None
				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == a:
						panel = adjudicator
						break

				if panel is None:
					interaction_modules.warn("please write a valid adjudicator name")
					continue

				delete_adj(allocations, panel)
				allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, fnames["workfolder"])

			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'add', a):
			try:
				a = a.replace("add", "")
				b = a.split(",")
				data = []
				for ele in b:
					data.append(ele.strip())
				panel = None

				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == data[1]:
						panel = adjudicator
						break

				if panel is None:
					interaction_modules.warn("please write a valid panel name")
					continue

				add_adj(allocations, data[0], panel)
				allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, round_num, "revised", teamnum)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num, fnames["workfolder"])
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'proceed', a):
			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'set panel', a):
			set_panel(allocations, tournament["adjudicator_list"])
			show_matchups_by_lattice(allocations, round_num, constants_of_adj)
		elif re.match(r'adjudicators', a):
			show_adjudicators(tournament["adjudicator_list"])
		else:
			interaction_modules.commandline("exchange [panel name 1], [panel name 2]: exchange these panels and create new matchup")
			interaction_modules.commandline("proceed: proceed to next step")
			interaction_modules.commandline("set panel: set panels")
			interaction_modules.commandline("adjudicators: see all the adjudicators")
			interaction_modules.commandline("delete [panel name]: delete panel of '[panel name]'")
			interaction_modules.commandline("add [chair name], [panel_name]: add panel to the debate where [chair name] do a chair")

def prompt_venue(allocations, tournament, round_num, fnames, style_cfg):
	while True:
		save(tournament, fnames, style_cfg)
		f_names = fnames["workfolder"].split("/")
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
				for venue in tournament["venue_list"]:
					if venue.name == data[0]:
						venue1 = venue
					elif venue.name == data[1]:
						venue2 = venue
				if venue1 is None or venue2 is None or venue1 == venue2:
					interaction_modules.warn("please write a valid venue name")
					continue

				for lattice in allocations[0]:
					if lattice.venue == venue1:
						lattice.venue = venue2
					elif lattice.venue == venue2:
						lattice.venue = venue1

				show_matchups_by_venue(allocations[0], tournament["venue_list"], round_num)
				export_allocations(allocations[0], "venue", round_num, fnames["workfolder"])
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'proceed', a):
			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				return allocations
		elif re.match(r'venues', a):
			show_venues(tournament["venue_list"])
		elif re.match(r'set venue', a):
			set_venue(allocations[0], tournament["venue_list"])
			show_matchups_by_venue(allocations[0], tournament["venue_list"], round_num)
		else:
			interaction_modules.commandline("exchange [venue name 1], [venue name 2]: exchange these venues and create new matchup")
			interaction_modules.commandline("proceed: proceed to next step")
			interaction_modules.commandline("venues: see all the venues")
			interaction_modules.commandline("set venue: set venues")

def prompt_before(tournament, fnames, teamnum, debater_num_per_team, style_cfg, round_num):
	while True:
		save(tournament, fnames, style_cfg)
		f_names = fnames["workfolder"].split("/")
		f_name = f_names[1]
		a = input("["+f_name+"]Please type a command(you can see commands by typing 'help') [step 1] > ")

		if re.match(r'proceed', a):
			if not checks_before_creation(tournament, teamnum): continue

			d = input("["+f_name+"]Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'absent', a):
			try:
				a = a.replace("absent", "")
				a = a.strip()

				for team in tournament["team_list"]:
					if team.name == a:
						team.available = False
						interaction_modules.progress(team.name + " was set absent successfully")
						break
				else:
					interaction_modules.warn("Please write a valid team name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
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
				scales_raw = input("institution scale (a, b, c) > ")
				scales = institutions_raw.split(",")
				new_scales = [scale.strip() for scale in scales]
				if list(set(new_scales)-set(["a", "b", "c"])): continue
				for new_institution, scale in zip(new_institutions, new_scales):
					institutions_list.append(Institution(len(institutions_list), new_institution, scale))
				institutions = [insti for insti in institutions_list if insti.name in new_institutions]
				team = Team(len(tournament["team_list"]), new_team_name, debater_names, institutions)

				score_list = ['n/a']*len(style_cfg["score_weight"])
				score = ['n/a']
				for i in range(round_num-1):
					team.dummy_finishing_process()
					for debater in team.debaters:
						debater.score_lists_sub.append(score_list)
						debater.scores_sub.append(score)
				tournament["team_list"].append(team)
				interaction_modules.progress(new_team_name + "was added to team list successfully")

			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'delete team', a):
			try:
				team_name = input("team name > ")
				team_name = team_name.strip()
				a = input("["+f_name+"]Are you sure you want to delete a team '"+team_name+"' ? (y/n) > ")
				if a != "y":continue

				for team in tournament["team_list"]:
					if team.name == team_name:
						tournament["team_list"].remove(team)
						interaction_modules.progress(team_name + " was deleted from team list successfully")
						break
				else:
					interaction_modules.warn("please write a valid team name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'present', a):
			try:
				a = a.replace("present", "")
				a = a.strip()

				for team in tournament["team_list"]:
					if team.name == a:
						team.available = True
						interaction_modules.progress(team.name + " was set present successfully")
						break
				else:
					interaction_modules.warn("Please write a valid team name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'roomnotavailable', a):
			try:
				a = a.replace("roomnotavailable", "")
				a = a.strip()

				for venue in tournament["venue_list"]:
					if venue.name == a:
						venue.available = False
						interaction_modules.progress(venue.name + " was set not available successfully")
						break
				else:
					interaction_modules.warn("Please write a valid venue name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'roomavailable', a):
			try:
				a = a.replace("roomavailable", "")
				a = a.strip()

				for venue in tournament["venue_list"]:
					if venue.name == a:
						venue.available = True
						interaction_modules.progress(venue.name + " was set available successfully")
						break
				else:
					interaction_modules.warn("Please write a valid venue name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjabsent', a):
			try:
				a = a.replace("adjabsent", "")
				a = a.strip()

				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == a:
						adjudicator.absent = True
						interaction_modules.progress(adjudicator.name + " was set absent successfully")
						break
				else:
					interaction_modules.warn("Please write a valid adjudicator name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjpresent', a):
			try:
				a = a.replace("adjpresent", "")
				a = a.strip()

				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == a:
						adjudicator.absent = False
						interaction_modules.progress(adjudicator.name + " was set present successfully")
						break
				else:
					interaction_modules.warn("Please write a valid adjudicator name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(tournament["adjudicator_list"])
		elif re.match(r'add venue', a):
			try:
				venue_name = input("venue name > ")
				venue_name = venue_name.strip()
				priority = int(input("venue priority [1, 3] > "))

				tournament["venue_list"].append(Venue(venue_name, priority))
				interaction_modules.progress(venue_name + " was added to venues successfully(priority:"+str(priority)+")")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue

		elif re.match(r'delete venue', a):
			try:
				venue_name = input("venue name > ")
				venue_name = venue_name.strip()

				for venue in tournament["venue_list"]:
					if venue.name == venue_name:
						tournament["venue_list"].remove(venue)
						interaction_modules.progress(venue_name + " was deleted from venues successfully")
						break
				else:
					interaction_modules.warn("please write a valid venue name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'add adjudicator', a):
			try:
				adjudicator_name = input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()
				if adjudicator_name in [adjudicator.name for adjudicator in tournament["adjudicator_list"]]:
					interaction_modules.warn("the adjudicator already exists in adjudicator list")
					continue
				if adjudicator_name == "":
					interaction_modules.warn("please type a valid name")
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
				adjudicator = Adjudicator(len(tournament["adjudicator_list"]), adjudicator_name, reputation, judge_test, new_institutions, new_conflict_teams)
				for i in range(round_num-1):
					adjudicator.dummy_finishing_process()
					adjudicator.watched_debate_ranks_sub.append('n/a')
				tournament["adjudicator_list"].append(adjudicator)

				interaction_modules.progress(adjudicator_name + " was added to adjudicator list successfully")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'delete adjudicator', a):
			try:
				adjudicator_name = input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()

				a = input("["+f_name+"]Are you sure you want to delete a team '"+adjudicator_name+"' ? (y/n) > ")
				if a != "y":continue

				for adjudicator in tournament["adjudicator_list"]:
					if adjudicator.name == adjudicator_name:
						tournament["adjudicator_list"].remove(adjudicator)
						interaction_modules.progress(adjudicator_name + " was deleted from adjudicator list successfully")
						break
				else:
					interaction_modules.warn("please write a valid adjudicator name")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'teams', a):
			show_teams(tournament["team_list"])
		elif re.match(r'venues', a):
			show_venues(tournament["venue_list"])
		elif re.match(r'results', a):
			interaction_modules.commandline("-------------------------------------result-----------------------------------------")
			show_debater_scores(tournament["team_list"])
			show_teams_scores(tournament["team_list"], teamnum)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(tournament["adjudicator_list"])

		else:
			interaction_modules.commandline("proceed: see the matchups for next round")
			interaction_modules.commandline("absent [team name]: set the team as absent")
			interaction_modules.commandline("present [team name]: set the absent team as present")
			interaction_modules.commandline("adjabsent [adj name]: set the adjudicator as absent")
			interaction_modules.commandline("adjpresent [adj_name]: set the absent adjudicator as present")
			interaction_modules.commandline("roomnotavailable [room name]: set the room as absent")
			interaction_modules.commandline("roomavailable [room name]: set the absent room as present")
			interaction_modules.commandline("teams: see all participating teams")
			interaction_modules.commandline("venues: see all available venues")
			interaction_modules.commandline("adjudicators: see all available venues")
			interaction_modules.commandline("resuls: see all available venues")
			interaction_modules.commandline("add team: add a team")
			interaction_modules.commandline("delete team: delete a team(irreversible!)")
			interaction_modules.commandline("add venue: add a venue")
			interaction_modules.commandline("delete venue: delete a venue(irreversible!)")
			interaction_modules.commandline("add adjudicator: add an adjudicator")
			interaction_modules.commandline("delete adjudicator: delete an adjudicator(irreversible!)")

def create_matchups(grid_list, round_num, tournament, filter_lists, teamnum, workfolder_name):
	interaction_modules.progress("[creating matchups for round "+str(round_num)+"]")
	interaction_modules.progress("filtering grid list")
	filtration(grid_list, round_num, tournament, filter_lists)
	interaction_modules.progress("adding priority to grids")
	addpriority(grid_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	interaction_modules.progress("selecting grids")
	selected_grid_lists_with_info = return_selected_grid_lists(grid_list, round_num, tournament, teamnum)

	for k, selected_grid_list_with_info in enumerate(selected_grid_lists_with_info):
		export_matchups(selected_grid_list_with_info[0], str(k)+"team", round_num, workfolder_name)
		selected_grid_list_with_info[1].matchups_no = k+1

	return selected_grid_lists_with_info

def create_allocations(tournament, selected_grid_list, lattice_list, break_team_num, round_num, filter_lists, constants_of_adj, teamnum, workfolder_name):
	interaction_modules.progress("[creating allocations for round "+str(round_num)+"]")
	interaction_modules.progress("filtering lattice list")
	lattice_filtration(tournament, selected_grid_list, lattice_list, break_team_num, round_num, filter_lists)
	interaction_modules.progress("adding priority to grids")
	addpriority(lattice_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	interaction_modules.progress("selecting lattices")
	selected_lattice_lists_with_info = return_selected_lattice_lists(lattice_list, round_num, tournament, constants_of_adj, teamnum)
	for k, selected_lattice_list_with_info in enumerate(selected_lattice_lists_with_info):
		export_allocations(selected_lattice_list_with_info[0], str(k)+"adj", round_num, workfolder_name)
		selected_lattice_list_with_info[1].allocation_no = k+1

	return selected_lattice_lists_with_info

def preparation(fnames, style_cfg):
	tournament = {}
	tournament["institution_list"] = read_institutions(fnames["institutions"])
	tournament["team_list"] = read_teams(fnames["teams"], style_cfg, tournament["institution_list"])
	tournament["venue_list"] = read_venues(fnames["venues"])
	check_team_list(tournament["team_list"])
	tournament["adjudicator_list"] = read_adjudicators(fnames["adjudicators"])
	check_adjudicator_list(tournament["adjudicator_list"])

	constants, orders1 = read_constants(fnames["settings"])
	filter_lists = create_filter_lists(orders1)
	constants_of_adj, orders2, break_team_nums = read_constants_of_adj(fnames["adjsettings"])
	filter_of_adj_lists = create_filter_of_adj_lists(orders2)

	return tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, break_team_nums




def arrange_data(tournament, constants_of_adj):
	evaluate_adjudicator(tournament["adjudicator_list"], constants_of_adj)
	sort_adjudicator_list_by_score(tournament["adjudicator_list"])
	sort_team_list_by_score(tournament["team_list"])

def export_info(tournament, round_num, style_cfg, workfolder_name):
	export_results(tournament, workfolder_name+"private/round_info/Results_of_adjudicators_by_R"+str(round_num)+".csv", workfolder_name+"private/round_info/Results_of_debaters_by_R"+str(round_num-1)+".csv", workfolder_name+"private/round_info/Results_of_teams_by_R"+str(round_num-1)+".csv", style_cfg)
	export_adj_info(tournament["adjudicator_list"], workfolder_name+"private/round_info/Adjudicators_info_by_R"+str(round_num)+".csv")

def show_data(tournament, teamnum):
	sort_adjudicator_list_by_score(tournament["adjudicator_list"])
	sort_team_list_by_score(tournament["team_list"])

	show_debater_scores(tournament["team_list"])
	show_teams_scores(tournament["team_list"], teamnum)
	#show_evaluation(adjudicator_list)
	show_adjudicator_score(tournament["adjudicator_list"])

def return_imported_allocations(constants_of_adj, grid_list, tournament, teamnum, round_num, break_team_num, workfolder_name):
	selected_lattice_list = import_matchup(workfolder_name+"matchups_imported/matchups_for_round_"+str(round_num)+".csv", grid_list, tournament, teamnum)
	selected_grid_list = [lattice.grid for lattice in selected_lattice_list]
	selected_grid_list_info = return_grid_list_info(selected_grid_list, tournament["team_list"], round_num, "", teamnum)
	selected_grid_list_info.matchup_no = 0
	selected_grid_list_with_info = [selected_grid_list, selected_grid_list_info]
	prioritize_bubble_round(round_num, tournament["adjudicator_list"], selected_grid_list, tournament["team_list"], selected_lattice_list, break_team_num, 0)
	selected_lattice_list_info = return_lattice_list_info(selected_lattice_list, tournament, constants_of_adj, round_num, "", teamnum)
	selected_lattice_list_info.allocation_no = 1
	allocations = [selected_lattice_list, selected_lattice_list_info]
	return allocations, selected_grid_list_with_info

def main_demo(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	if not checks_before_creation(tournament, teamnum): sys.exit(4)
	for i in range(rounds):
		#export_info(adjudicator_list, team_list, i+1, style_cfg, fnames["workfolder"])
		arrange_data(tournament, constants_of_adj)

		interaction_modules.progress("creating grid list")

		grid_list = create_grid_list(tournament["team_list"], teamnum)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, tournament=tournament, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=fnames["workfolder"])
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = selected_grid_lists_with_info[-1]
		export_matchups(matchups[0], "matchups_without_adj", i+1, fnames["workfolder"])

		lattice_list = create_lattice_list(matchups[0], tournament["adjudicator_list"])
		selected_lattice_lists_with_info = create_allocations(tournament=tournament, selected_grid_list=matchups[0], lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=fnames["workfolder"])
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = selected_lattice_lists_with_info[-1]

		allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, i+1, "chosen", teamnum)
		set_panel(allocations, tournament["adjudicator_list"])
		export_allocations(allocations[0], "panel", i+1, fnames["workfolder"])

		set_venue(allocations[0], tournament["venue_list"])
		export_allocations(allocations[0], "venue", i+1, fnames["workfolder"])

		export_official_matchups(allocations[0], i+1, fnames["workfolder"])
		export_blank_results(allocations[0], i+1, style_cfg, fnames["workfolder"]+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, fnames["workfolder"]+"blankresults/Results_of_adj"+str(i+1)+".csv")
		export_dummy_results_adj(allocations[0], i+1, style_cfg, fnames["workfolder"])
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1, style_cfg=style_cfg, workfolder_name=fnames["workfolder"])
		read_and_process_result(round_num=i+1, tournament=tournament, style_cfg=style_cfg, filename_results = fnames["workfolder"]+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"private/Results_of_adj"+str(i+1)+".csv")

		show_data(tournament, teamnum)
		export_info(tournament, i+1, style_cfg, fnames["workfolder"])
		check_team_list2(tournament["team_list"], i+1, teamnum)
	
	export_results(tournament, fnames["workfolder"]+"private/final_result/Results_of_adjudicators.csv", fnames["workfolder"]+"private/final_result/Results_of_debaters.csv", fnames["workfolder"]+"private/final_result/Results_of_teams.csv", style_cfg)

def main_complete(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, no_adj, style_cfg):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	for i in range(rounds):
		save(tournament, fnames, style_cfg)
		interaction_modules.progress("-----------------Round "+str(i+1)+"-----------------")
		#export_info(adjudicator_list, team_list, i+1, style_cfg, fnames["workfolder"])
		prompt_before(tournament, fnames, teamnum, debater_num_per_team, style_cfg, i+1)
		arrange_data(tournament, constants_of_adj)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, fnames["workfolder"])
		interaction_modules.progress("creating grid list")
		grid_list = create_grid_list(tournament["team_list"], teamnum)

		fn_match = "matchups_imported/matchups_for_round_"+str(i+1)+".csv"
		fn = "private/Results"+str(i+1)+".csv"
		fn_adj = "private/Results_of_adj"+str(i+1)+".csv"
		results_read = False
		matchups_read = False
		allocations = None

		while True:
			if os.path.exists(fnames["workfolder"]+fn):
				root, ext = os.path.splitext(fnames["workfolder"]+fn)
				a = input("The Results file already exists in private folder. Do you want to read the result '"+root+ext+"'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							read_and_process_result(round_num=i+1, tournament=tournament, style_cfg=style_cfg, filename_results = fnames["workfolder"]+"private/Results"+str(i+1)+".csv")
							interaction_modules.progress("processed results of round "+str(i+1))
							results_read = True
							break
						except:
							interaction_modules.warn("failed to read Results file")
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
			if os.path.exists(fnames["workfolder"]+fn_adj):
				root, ext = os.path.splitext(fnames["workfolder"]+fn_adj)
				a = input("The Results file already exists in private folder. Do you want to read the result '"+root+ext+"'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"private/Results_of_adj"+str(i+1)+".csv")
							interaction_modules.progress("processed results_of_adj of round "+str(i+1))
							results_read = True
							break
						except:
							interaction_modules.warn("failed to read Results of adj file")
							a = input("Do you still want to read the result '"+root+ext+"'? (y/n) > ")
							if re.match(r'y', a):
								continue
							elif re.match(r'n', a):
								try:
									read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"dummyresults/Results_of_adj"+str(i+1)+".csv")
								except:
									interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
								break
					break
				elif re.match(r'n', a):
					try:
						read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"dummyresults/Results_of_adj"+str(i+1)+".csv")
					except:
						interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
					break
				else:
					continue
				break
			else:
				break

		if results_read:
			continue

		while True:
			if os.path.exists(fnames["workfolder"]+fn_match):
				root, ext = os.path.splitext(fnames["workfolder"]+fn_match)
				a = input("Read imported matchup 'matchups_imported/matchups_for_round_"+str(i+1)+".csv'? (y/n) > ")
				if re.match(r'y', a):
					while True:
						try:
							allocations = edit_revised_matchups(constants_of_adj, grid_list, tournament, teamnum, i+1, break_team_nums[i], fnames, debater_num_per_team, style_cfg)
							matchups_read = True
							break
						except:
							interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
							interaction_modules.warn("failed to read matchups file")
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
			selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, tournament=tournament, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=fnames["workfolder"])
			for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_grid(selected_grid_list_with_info, i+1)
			matchups = prompt(selected_grid_lists_with_info, tournament, grid_list, i+1, fnames, debater_num_per_team, teamnum, style_cfg)
			export_matchups(matchups[0], "matchups_without_adj", i+1, fnames["workfolder"])

			prompt_before(tournament, fnames, teamnum, debater_num_per_team, style_cfg, i+1)

			lattice_list = create_lattice_list(matchups[0], tournament["adjudicator_list"])
			selected_lattice_lists_with_info = create_allocations(tournament=tournament, selected_grid_list=matchups[0], lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=fnames["workfolder"])
			for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
			allocations = prompt_adj(selected_lattice_lists_with_info, tournament, grid_list, i+1, fnames, constants_of_adj, style_cfg)

			allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, i+1, "chosen", teamnum)
			prompt_panel(allocations, tournament, i+1, fnames, constants_of_adj, style_cfg)
			export_allocations(allocations[0], "panel", i+1, fnames["workfolder"])

			prompt_venue(allocations, tournament, i+1, fnames, style_cfg)
			export_allocations(allocations[0], "venue", i+1, fnames["workfolder"])

			while True:
				interaction_modules.progress("generated matchups in 'public'")
				a = input("read revised matchup 'matchups_imported/matchups_for_round_"+str(i+1)+".csv'? (y/n) > ")
				if re.match(r'y', a):
					try:
						allocations, selected_grid_list_with_info = return_imported_allocations(constants_of_adj, grid_list, tournament, teamnum, i+1, break_team_nums[i], fnames["workfolder"])
						break
					except Exception as inst:
						interaction_modules.warn(inst)
						continue
				elif re.match(r'n', a):
					break

		export_official_matchups(allocations[0], i+1, fnames["workfolder"])
		export_blank_results(allocations[0], i+1, style_cfg, fnames["workfolder"]+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, fnames["workfolder"]+"blankresults/Results_of_adj"+str(i+1)+".csv")
		show_matchups(allocations, i+1)

		export_dummy_results_adj(allocations[0], i+1, style_cfg, fnames["workfolder"])

		while True:
			a = input("read results of round {0}? (y/n) > ".format(i+1))
			if re.match(r'y', a):
				try:
					read_and_process_result(round_num=i+1, tournament=tournament, style_cfg=style_cfg, filename_results = fnames["workfolder"]+"private/Results"+str(i+1)+".csv")
					break
				except:
					interaction_modules.warn("failed to read results")
					continue
			elif re.match(r'n', a):
				break
		if no_adj:
			try:
				read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"dummyresults/Results_of_adj"+str(i+1)+".csv")
			except:
				interaction_modules.warn("warning: results_of_adj file broken")
				interaction_modules.warn("you can still use this program but cannot use the '(adjudicators) avoid watched teams' feature")
				pass
		else:
			while True:
				a = input("read results_of_adj of round {0}? (y/n) > ".format(i+1))
				if re.match(r'y', a):
					try:
						read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"private/Results_of_adj"+str(i+1)+".csv")
						break
					except:
						interaction_modules.warn("failed to read results of adjs")
						continue 
				elif re.match(r'n', a):
					break

		show_data(tournament, teamnum)
		check_team_list2(tournament["team_list"], i+1, teamnum)
		export_info(tournament, i+1, style_cfg, fnames["workfolder"])
	
	export_results(tournament, fnames["workfolder"]+"private/final_result/Results_of_adjudicators.csv", fnames["workfolder"]+"private/final_result/Results_of_debaters.csv", fnames["workfolder"]+"private/final_result/Results_of_teams.csv", style_cfg)

def main_quick_debug(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	for i in range(rounds):
		save(tournament, fnames, style_cfg)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, fnames["workfolder"])
		prompt_before(tournament, fnames, teamnum, debater_num_per_team, style_cfg, i+1)
		arrange_data(tournament, constants_of_adj)
		#export_info(adjudicator_list, team_list, i+1, style_cfg, fnames["workfolder"])

		interaction_modules.progress("creating grid list")
		grid_list = create_grid_list(tournament["team_list"], teamnum)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, tournament=tournament, filter_lists=filter_lists, teamnum=teamnum, workfolder_name=fnames["workfolder"])
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = prompt(selected_grid_lists_with_info, tournament, grid_list, i+1, fnames, debater_num_per_team, teamnum, style_cfg)
		export_matchups(matchups[0], "matchups_without_adj", i+1, fnames["workfolder"])

		lattice_list = create_lattice_list(matchups[0], tournament["adjudicator_list"])
		selected_lattice_lists_with_info = create_allocations(tournament=tournament, selected_grid_list=matchups[0], lattice_list=lattice_list, break_team_num=break_team_nums[i], round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj, teamnum=teamnum, workfolder_name=fnames["workfolder"])
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = prompt_adj(selected_lattice_lists_with_info, tournament, grid_list, i+1, fnames, constants_of_adj, style_cfg)

		allocations[1] = return_lattice_list_info(allocations[0], tournament, constants_of_adj, i+1, "chosen", teamnum)
		set_panel(allocations, tournament["adjudicator_list"])
		export_allocations(allocations[0], "panel", i+1, fnames["workfolder"])
		
		set_venue(allocations[0], tournament["venue_list"])
		export_allocations(allocations[0], "venue", i+1, fnames["workfolder"])

		export_official_matchups(allocations[0], i+1, fnames["workfolder"])
		export_blank_results(allocations[0], i+1, style_cfg, fnames["workfolder"]+"blankresults/Results"+str(i+1)+".csv")
		export_blank_results_of_adj(allocations[0], i+1, fnames["workfolder"]+"blankresults/Results_of_adj"+str(i+1)+".csv")
		export_dummy_results_adj(allocations[0], i+1, style_cfg, fnames["workfolder"])
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1, style_cfg=style_cfg, workfolder_name=fnames["workfolder"])
		read_and_process_result(round_num=i+1, tournament=tournament, style_cfg=style_cfg, filename_results = fnames["workfolder"]+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"private/Results_of_adj"+str(i+1)+".csv")
	
		show_data(tournament, teamnum)
		check_team_list2(tournament["team_list"], i+1, teamnum)
		export_info(tournament, i+1, style_cfg, fnames["workfolder"])
	
	export_results(tournament, fnames["workfolder"]+"private/final_result/Results_of_adjudicators.csv", fnames["workfolder"]+"private/final_result/Results_of_debaters.csv", fnames["workfolder"]+"private/final_result/Results_of_teams.csv", style_cfg)

def main_graph(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg):
	teamnum = style_cfg["team_num"]
	debater_num_per_team = style_cfg["debater_num_per_team"]
	"""
	for i in range(rounds):
		read_and_process_result(round_num=i+1, tournament=tournament, style_cfg=style_cfg, filename_results = fnames["workfolder"]+"private/Results"+str(i+1)+".csv")
		read_and_process_result_adj(round_num=i+1, tournament=tournament, teamnum=teamnum, filename_results_of_adj=fnames["workfolder"]+"private/Results_of_adj"+str(i+1)+".csv")
	
		show_data(tournament, teamnum)
		check_team_list2(tournament["team_list"], i+1, teamnum)
	
	export_results(tournament, fnames["workfolder"]+"private/final_result/Results_of_adjudicators.csv", fnames["workfolder"]+"private/final_result/Results_of_debaters.csv", fnames["workfolder"]+"private/final_result/Results_of_teams.csv", style_cfg)
	mstat(tournament, teamnum, rounds)
	"""

def edit_revised_matchups(constants_of_adj, grid_list, tournament, teamnum, round_num, break_team_num, fnames, debater_num_per_team, style_cfg):
	try:
		allocations, selected_grid_list_with_info = return_imported_allocations(constants_of_adj, grid_list, tournament, teamnum, round_num, break_team_num, fnames["workfolder"])
	except Exception as inst:
		interaction_modules.warn(inst)
		raise Exception("could not read imported matchups")

	selected_grid_list_with_info[1].matchups_no = 1
	show_matchups_by_grid(selected_grid_list_with_info, round_num)

	matchups = prompt([selected_grid_list_with_info], tournament, grid_list, round_num, fnames, debater_num_per_team, teamnum, style_cfg)
	export_matchups(matchups[0], "matchups_without_adj", round_num, fnames["workfolder"])

	lattice_list = create_lattice_list(matchups[0], tournament["adjudicator_list"])

	allocations = merge_matchups_and_allocations(matchups, allocations, lattice_list, round_num, tournament, constants_of_adj, teamnum)

	show_matchups_by_lattice(allocations, round_num, constants_of_adj)
	allocations = prompt_adj([allocations], tournament, grid_list, round_num, fnames, constants_of_adj, style_cfg)

	prompt_panel(allocations, tournament, round_num, fnames, constants_of_adj, style_cfg)
	export_allocations(allocations[0], "panel", round_num, fnames["workfolder"])

	prompt_venue(allocations, tournament, round_num, fnames, style_cfg)
	export_allocations(allocations[0], "venue", round_num, fnames["workfolder"])

	return allocations

def prompt_beginning(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, debater_num_per_team, style_cfg):
	while True:
		a = input("Please type a command(you can see commands by typing 'help') [step 0] > ")

		if a == 'demo':
			main_demo(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg)
		elif a == 'no_adj_feedback':
			main_complete(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, True, style_cfg)
		elif a == 'run':
			main_complete(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, False, style_cfg)
		elif a == 'debug':
			main_quick_debug(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg)
		elif a == 'graph':
			main_graph(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, fnames, break_team_nums, style_cfg)
		else:
			interaction_modules.commandline("run: start this program")
			interaction_modules.commandline("no_adj_feedback: start this program without team2adj feedback")
			interaction_modules.commandline("debug: debug this program with adj (may change the Results files)")
			interaction_modules.commandline("demo: see demo of this program automatically (may change the Results files)")
			interaction_modules.commandline("helper: help other tabulation program (read matchups from other tabulation program)")
			interaction_modules.commandline("graph: plot graph")

			continue
		break

def mstat(tournament, teamnum, rounds):
	plt.plot_ira_abs(tournament["adjudicator_list"], tournament["team_list"], rounds, teamnum)
	plt.plot_ira_pm(tournament["adjudicator_list"], tournament["team_list"], rounds, teamnum)
	plt.plot_ira_sd(tournament["adjudicator_list"], tournament["team_list"], rounds, teamnum)
	#plt.plot_ira_3(adjudicator_list, tournament["team_list"], rounds, teamnum)

	"""
	all_debaters = [debater for team in tournament["team_list"] for debater in team.debaters]
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
		wins_all.append(get_wins_by_side(tournament["team_list"], teamnum, i+1))
		scores_all.append(get_scores_by_side(tournament["team_list"], teamnum, i+1))
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
	plt.bar_1d(sorted(get_debater_score(tournament["team_list"]), reverse=True))
	plt.line_graph_1d(sorted(get_debater_score(tournament["team_list"]), reverse=True))
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
		#print str(a)
		if re.match(r'choose', a):
			fn = a.replace("choose", "")
			fn = fn.strip()
			br = False
			if re.match(r'^_', fn):
				interaction_modules.warn("error: the workfolder ", fn, "is an unsubstantial workfolder to generate substantial workfolder")
				continue
			if br: continue
			fn = "workfolders/"+fn
			if os.path.exists(fn):
				workfolder_name = fn
				interaction_modules.progress("the workfolder "+fn+" was selected successfully")
				break
			else:
				interaction_modules.warn("Please write a valid workfolder name")
		elif re.match(r'create', a):
			try:
				fn = a.replace("create", "")
				fn = fn.strip()
				fn = "workfolders/_"+fn

				if not os.path.exists(fn):
					os.mkdir(fn)
					for folder_name in folder_names:
						os.mkdir(fn+"/"+folder_name)
					interaction_modules.progress("the workfolder "+fn+" was created successfully")
				else:
					interaction_modules.warn("the workfolder you want to create already exists")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
			"""
			elif re.match(r'backup', a):
				try:
					fn = a.replace("backup", "")
					fn = fn.strip()
					fn = "workfolders/"+fn
					datetimenow = datetime.now()
					nowtime = datetimenow.strftime('%m')+datetimenow.strftime('%d')+datetimenow.strftime('%H')+datetimenow.strftime('%M')+datetimenow.strftime('%S')
					shutil.copytree(fn, fn+"_backup"+nowtime)
					interaction_modules.progress("the workfolder "+fn+"_backup"+nowtime+" was created successfully")
				except:
					interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
					continue
			"""
		elif re.match(r'delete', a):
			try:
				if not interaction_modules.areyousure("Are you sure to delete the workfolder?", "warning"):
					continue
				fn = a.replace("delete", "")
				fn = fn.strip()
				fn = "workfolders/"+fn
				shutil.rmtree(fn)
				interaction_modules.progress("the workfolder "+fn+" was deleted successfully")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
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
							interaction_modules.progress("the workfolder "+fns[1]+" was created successfully")
							break
						else:
							interaction_modules.warn("the workfolder already exists")
							break
				else:
					interaction_modules.warn("the workfolder "+fns[0]+" does not exist")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		elif re.match(r'init', a):
			try:
				fn = a.replace("init", "")
				fn = fn.strip()
				fns = fn.split(" ")
				fn_from = "workfolders/"+fns[0].strip()
				fn_to = "workfolders/"+fns[1].strip()+fns[0].strip()
				fns = [fn.strip() for fn in fns]

				if os.path.exists(fn_from):
					while True:
						if not os.path.exists(fns[1]):
							datetimenow = datetime.now()
							fn_to = fn_to+"_"+datetimenow.strftime('%m')+datetimenow.strftime('%d')+"-"+datetimenow.strftime('%H')+datetimenow.strftime('%M')
							#folder_name = datetimenow.strftime('%m')+datetimenow.strftime('%d')+datetimenow.strftime('%H')+datetimenow.strftime('%M')+datetimenow.strftime('%S')
							shutil.copytree(fn_from, fn_to)
							reset_except_dat_cfg(fn_to+"/")
							interaction_modules.progress("the workfolder "+fn_to+" was created successfully")
							break
						else:
							interaction_modules.warn("the workfolder "+fn_to+" already exists")
							break
				else:
					interaction_modules.warn("the workfolder "+fn_from+" does not exist")
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
		elif re.match(r'show', a):
			try:
				workfolder_names = os.listdir("workfolders/")
				string = ""
				for name in workfolder_names:
					string = string + name + ", "
				interaction_modules.commandline(string)
			except:
				interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
				continue
		else:
			interaction_modules.commandline("choose [workfolder name]: select the workfolder")
			interaction_modules.commandline("create [workfolder name]: create a workfolder named [workfolder name]")
			interaction_modules.commandline("copy [workfolder name from] [workfolder name to]: copy a workfolder named [workfolder name from] to [workfolder name to]")
			interaction_modules.commandline("init [workfolder name from] [workfolder name to]: initialize a workfolder named [workfolder name from] to [workfolder name to] only take over the dat,cfg folders")
			interaction_modules.commandline("backup [workfolder name]: backup a workfolder named [workfolder name]")
			interaction_modules.commandline("delete [workfolder name]: delete a workfolder named [workfolder name] (irreversible!)")
			interaction_modules.commandline("show: show all workfolders")

	return workfolder_name+"/"

if __name__ == "__main__":
	#show_logo_random_fade()
	#show_logo_star()
	WORKFOLDER_NAME = get_workfolder()

	################### DO NOT CHANGE THIS ###################
	FNAMES = {
		"venues": WORKFOLDER_NAME+"dat/venues.csv",
		"teams": WORKFOLDER_NAME+"dat/teams.csv",
		"adjudicators": WORKFOLDER_NAME+"dat/adjudicators.csv",
		"institutions": WORKFOLDER_NAME+"dat/institutions.csv",
		"settings": WORKFOLDER_NAME+"cfg/config.csv",
		"adjsettings": WORKFOLDER_NAME+"cfg/constants_of_adj.csv",
		"export_filename_tm": WORKFOLDER_NAME+"temp/tm.csv",
		"export_filename_aj": WORKFOLDER_NAME+"temp/aj.csv",
		"export_filename_vn": WORKFOLDER_NAME+"temp/vn.csv",
		"export_filename_is": WORKFOLDER_NAME+"temp/is.csv",
		"workfolder": WORKFOLDER_NAME
	}
	
	tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, break_team_nums = preparation(FNAMES, STYLE_CFG)
	initial_check(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, STYLE_CFG)
	load(tournament, STYLE_CFG, FNAMES)
	prompt_beginning(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, ROUND_NUM, FNAMES, break_team_nums, STYLE_CFG)

pass