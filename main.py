# -*- coding: utf-8 -*-
#Todo: mstat, more speed(alg3, 4), sort_adjudicators
#judge points distribution on team-win/lose, teamscore -adj ranking, adjscore -debater ranking, teamscore-teamranking, role-score distribution, power_pairing_strong, 
from modules.internal_modules import *
from modules.io_modules import *
from modules.classes import *
try:
	import readline
except:
	print "readline module is recommended thou this program can work without it"
import re
import copy
import sys
argvs = sys.argv

#MORE THAN THIS YOU NEED TO PREPARE teams.csv FOR EACH MODE
DEBATER_NUM_PER_TEAM = None
TEAMNUM2 = True
try:
	MODE = argvs[1]
except:
	print "usage: python main.py [mode] #modes are: ACADEMIC, NA, PDA, ASIAN, BP, NAFA"
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
	print "usage: python main.py [mode] #modes are: ACADEMIC, NA, PDA, ASIAN, BP, NAFA"
	sys.exit()


ROUND_NUM = 4
FILENAME_SETTINGS = "cfg/config.csv"
FILENAME_SETTINGS_OF_ADJ = "cfg/constants_of_adj.csv"

################### DO NOT CHANGE THIS ADDRESS ###################
FILENAME_VENUES = "dat/venues.csv"
FILENAME_TEAMS = "dat/teams.csv"
FILENAME_ADJUDICATORS = "dat/adjudicators.csv"
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
#       |           |_bit
#       |           |_property
#       | 
#       |_ io_for
#       |   |_bit
#       |   |_property
#       |   |_classes
#       |   |_io
#       |      |_bit
#       |      |_property
#       |      |_classes
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



########### FOR OTHER 2 SIDES STYLE YOU NEED TO FIX THESE FUNCTIONS ###########
#
# main:
# internal:
# io: 
# io_for: read_results, read_and_process_result, export_random_result, read_teams, export_results, export_teams, save, load, check_results
# classes:
# property:
# commandline:
# filter:
# select:
# bit:
#

########### FOR OTHER 4 SIDES STYLE YOU NEED TO FIX THESE FUNCTIONS ###########
#
# main: prompt
# internal: initial check, create_lattice_list, create_grid_list, return_selected_grid_lists, set_panel, exchange_teams, create_filter_lists, create_filter_of_adj_lists, check_team_list2, cmp_allocations, grid_list_errors
#         : grid_check_power_pairing, grid_check_one_sided, grid_check_past_opponent, grid_check_same_institution, lattice_check_conflict, lattice_check_bubble_round, lattice_check_same_round
# io: read_results, read_and_process_result, export_random_result, read_teams, read_constants, export_matchups, export_allocations, export_official_ballot, export_results, export_teams, save, load, check_results, export_dummy_results_adj
# classes:
# property:calc_power_pairing_indicator, is_one_sided, team_gov_percentage, calc_str_str_indicator, calc_deleting_effect, seen_num
# commandline:show_matchups(_), show_teams_score
# filter:power_pairing, random_pairing, prevent(_), prioritize_bubble_round
# select:disavail_grids, select_grids, refresh_grids_for_adopt, select_alg3, select_alg4
# bit:
#


#cfg/config.csv
#past_opponent, strong power pairing

def finish_round_debug(allocations, round_num):
	export_random_result_adj(allocations, round_num)
	export_random_result(allocations, round_num)
	
def prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, round_num, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 2] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
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
					print "Please write valid team name"
					continue

				new_matchups = copy.deepcopy(selected_grid_lists_with_info[data[0]-1])

				exchange_teams(new_matchups[0], team_a, team_b)
				#for grid in new_matchups[0]:
				#	if grid.warnings != []:
				#		print grid.warnings
				#print
				new_matchups[1] = return_grid_list_info(new_matchups[0], team_list, round_num)
				new_matchups[1].matchups_no = len(selected_grid_lists_with_info)+1
				export_matchups(new_matchups[0], str(len(selected_grid_lists_with_info)+1)+"team", round_num)
				selected_grid_lists_with_info.append(new_matchups)
				show_matchups_by_grid(new_matchups, round_num)

			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		
		elif re.match(r'choose', a):
			try:
				d = raw_input("Are you sure to proceed?(y/n) > ")
				if re.match(r'y', d):
					a = a.replace("choose", "")
					a = a.replace("(", "")
					a = a.replace(")", "")
					a = a.replace(" ", "")
					num = int(a)

					if num <= len(selected_grid_lists_with_info):
						return selected_grid_lists_with_info[num-1]
					else:
						print "please input a valid matchup_no"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_grid(selected_grid_lists_with_info[num-1], round_num)
			
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		else:
			print "exchange(matchup_no, team1_name, team2_name): exchange these teams and create new matchup"
			print "choose(matchup_no): choose the matchup"
			print "show(matchup_no): see again the matchup you selected"

def prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, lattice_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 3] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
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
					print "please write a valid adjudicator name"
					continue

				new_allocations = copy.deepcopy(selected_lattice_lists_with_info[num-1])

				exchange_adj(new_allocations, adjudicator1, adjudicator2)
				new_allocations[1] = return_lattice_list_info(new_allocations[0], adjudicator_list, constants_of_adj, round_num)
				new_allocations[1].allocation_no = len(selected_lattice_lists_with_info)+1
				export_allocations(new_allocations[0], str(len(selected_lattice_lists_with_info)+1)+"adj", round_num)
				selected_lattice_lists_with_info.append(new_allocations)
				show_matchups_by_lattice(new_allocations, round_num, constants_of_adj)
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'choose', a):
			try:
				d = raw_input("Are you sure to proceed?(y/n) > ")
				if re.match(r'y', d):
					a = a.replace("choose", "")
					a = a.replace("(", "")
					a = a.replace(")", "")
					a = a.replace(" ", "")
					num = int(a)

					if num <= len(selected_lattice_lists_with_info):
						selected_lattice_list_with_info = selected_lattice_lists_with_info[num-1]
						print "allocation No."+str(num)+" was chosen successfully"
						return selected_lattice_list_with_info
					else:
						print "please input a valid allocation_No"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'show', a):
			try:
				a = a.replace("show", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.replace(" ", "")
				num = int(a)

				show_matchups_by_lattice(selected_lattice_lists_with_info[num-1], round_num, constants_of_adj)
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		else:
			print "exchange(allocation_No, adj_name, adj_name): exchange these adjudicators and create new matchup"
			print "choose(allocation_No): choose the matchup"
			print "show(allocation_No): see again the matchup you selected"
			print "adjudicators: see all the adjudicators"

def prompt_panel(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, constants_of_adj, filename_venues, filename_adjudicators):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 4] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
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
					print "please write a valid adjudicator name"
					continue
				exchange_adj(allocations, adjudicator1, adjudicator2)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num)
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue

		elif re.match(r'delete', a):
			try:
				a = a.replace("delete", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()
				panel = None
				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						panel = adjudicator
						break

				if panel is None:
					print "please write a valid adjudicator name"
					continue

				delete_adj(allocations, panel)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num)

			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'add', a):
			try:
				a = a.replace("add", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
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
					print "please write a valid panel name"
					continue

				add_adj(allocations, data[0], panel)
				allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, round_num)
				show_matchups_by_lattice(allocations, round_num, constants_of_adj)
				export_allocations(allocations[0], "panel", round_num)
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'proceed', a):
			d = raw_input("Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'set panel', a):
			set_panel(allocations, adjudicator_list)
			show_matchups_by_lattice(allocations, round_num, constants_of_adj)
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		else:
			print "exchange(panel_name, panel_name): exchange these panels and create new matchup"
			print "proceed: proceed to next step"
			print "set panel: set panels"
			print "adjudicators: see all the adjudicators"
			print "delete(panel_name):"
			print "add(chair_name, panel_name):"

def prompt_venue(allocations, team_list, venue_list, adjudicator_list, round_num, filename_teams, filename_venues, filename_adjudicators):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 5] > ")

		if re.match(r'exchange', a):
			try:
				a = a.replace("exchange", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
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
					print "please write a valid venue name"
					continue

				for lattice in allocations[0]:
					if lattice.venue == venue1:
						lattice.venue = venue2
					elif lattice.venue == venue2:
						lattice.venue = venue1

				show_matchups_by_venue(allocations[0], venue_list, round_num)
				export_allocations(allocations[0], "venue", round_num)
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'proceed', a):
			d = raw_input("Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				return allocations
		elif re.match(r'venues', a):
			show_venues(venue_list)
		elif re.match(r'set venue', a):
			set_venue(allocations[0], venue_list)
			show_matchups_by_venue(allocations[0], venue_list, round_num)
		else:
			print "exchange(venue_name, venue_name): exchange these venues and create new matchup"
			print "proceed: proceed to next step"
			print "venues: see all the venues"
			print "set venue: set venues"

def prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum2):
	while True:
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 1] > ")

		if re.match(r'proceed', a):
			d = raw_input("Are you sure to proceed?(y/n) > ")
			if re.match(r'y', d):
				break
		elif re.match(r'absent', a):
			try:
				a = a.replace("absent", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for team in team_list:
					if team.name == a:
						team.available = False
						print team.name + " was set absent successfully"
						break
				else:
					print "Please write a valid team name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'add team', a):####################################################################
			try:
				new_team_name = raw_input("new team name > ")
				debater1 = raw_input("member 1 > ")
				debater2 = raw_input("member 2 > ")
				debater3 = raw_input("member 3 > ")
				#debater4 = raw_input("member 4 > ")
				debater1 = debater1.strip()
				debater2 = debater2.strip()
				debater3 = debater3.strip()
				#debater4 = debater4.strip()
				debater_names = [debater1, debater2, debater3, debater4]
				institutions_raw = raw_input("institutions (,separation) > ")
				institutions = institutions_raw.split(",")
				new_institutions = []
				for institution in institutions:
					new_institutions.append(institution.strip())
				team_list.append(Team(len(team_list), new_team_name, debater_names, "large", new_institutions))
				print new_team_name + "was added to team list successfully"

			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'delete team', a):
			try:
				a = raw_input("Are you sure you want to delete a team? (y/n) > ")
				if a != "y":continue
				team_name = raw_input("team name > ")
				team_name = team_name.strip()

				for team in team_list:
					if team.name == team_name:
						team_list.remove(team)
						print team_name + " was deleted from team list successfully"
						break
				else:
					print "please write a valid adjudicator name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'present', a):
			try:
				a = a.replace("present", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for team in team_list:
					if team.name == a:
						team.available = True
						print team.name + " was set present successfully"
						break
				else:
					print "Please write a valid team name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'roomnotavailable', a):
			try:
				a = a.replace("roomnotavailable", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for venue in venue_list:
					if venue.name == a:
						venue.available = False
						print venue.name + " was set not available successfully"
						break
				else:
					print "Please write a valid venue name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'roomavailable', a):
			try:
				a = a.replace("roomavailable", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for venue in venue_list:
					if venue.name == a:
						venue.available = True
						print venue.name + " was set available successfully"
						break
				else:
					print "Please write a valid venue name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'adjabsent', a):
			try:
				a = a.replace("adjabsent", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						adjudicator.absent = True
						print adjudicator.name + " was set absent successfully"
						break
				else:
					print "Please write a valid adjudicator name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'adjpresent', a):
			try:
				a = a.replace("adjpresent", "")
				a = a.replace("(", "")
				a = a.replace(")", "")
				a = a.strip()

				for adjudicator in adjudicator_list:
					if adjudicator.name == a:
						adjudicator.absent = False
						print adjudicator.name + " was set present successfully"
						break
				else:
					print "Please write a valid adjudicator name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'adjudicators', a):
			show_adjudicators(adjudicator_list)
		elif re.match(r'add venue', a):
			try:
				venue_name = raw_input("venue name > ")
				venue_name = venue_name.strip()
				priority = int(raw_input("venue priority [1, 3] > "))

				venue_list.append(Venue(venue_name, priority))
				print venue_name + " was added to venues successfully(priority:"+str(priority)+")"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue

		elif re.match(r'delete venue', a):
			try:
				venue_name = raw_input("venue name > ")
				venue_name = venue_name.strip()

				for venue in venue_list:
					if venue.name == venue_name:
						venue_list.remove(venue)
						print venue_name + " was deleted from venues successfully"
						break
				else:
					print "please write a valid venue name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'add adjudicator', a):
			try:
				adjudicator_name = raw_input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()
				if adjudicator_name in [adjudicator.name for adjudicator in adjudicator_list]:
					print "the adjudicator already exists in adjudicator list"
					continue
				if adjudicator_name == "":
					print "please type a valid name"
					continue
				reputation = int(raw_input("reputation[0, 10] > "))
				judge_test = int(raw_input("judge test[0, 10] > "))
				institutions_raw = raw_input("institutions (,separation) > ")
				institutions = institutions_raw.split(",")
				new_institutions = []
				for institution in institutions:
					new_institutions.append(institution.strip())
				conflict_teams_raw = raw_input("conflict teams (,separation) > ")
				conflict_teams = conflict_teams_raw.split(",")
				new_conflict_teams = []
				for conflict_team in conflict_teams:
					new_conflict_teams.append(conflict_team.strip())
				adjudicator_list.append(Adjudicator(adjudicator_name, reputation, judge_test, new_institutions, new_conflict_teams))

				print adjudicator_name + " was added to adjudicator list successfully"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'delete adjudicator', a):
			try:
				adjudicator_name = raw_input("adjudicator name > ")
				adjudicator_name = adjudicator_name.strip()

				for adjudicator in adjudicator_list:
					if adjudicator.name == adjudicator_name:
						adjudicator_list.remove(adjudicator)
						print adjudicator_name + " was deleted from adjudicator list successfully"
						break
				else:
					print "please write a valid adjudicator name"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				continue
		elif re.match(r'teams', a):
			show_teams(team_list)
		elif re.match(r'venues', a):
			show_venues(venue_list)
		elif re.match(r'results', a):
			print "-------------------------------------result-----------------------------------------"
			show_debater_scores(team_list)
			show_teams_scores(team_list, teamnum2)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(adjudicator_list)

		else:
			print "proceed: see the matchups for next round"
			print "absent(team_name): set the team as absent"
			print "present(team_name): set the absent team as present"
			print "adjabsent(adj_name): set the adjudicator as absent"
			print "adjpresent(adj_name): set the absent adjudicator as present"
			print "roomnotavailable(room_name): set the room as absent"
			print "roomavailable(room_name): set the absent room as present"
			print "teams: see all participating teams"
			print "venues: see all available venues"
			print "adjudicators: see all available venues"
			print "resuls: see all available venues"
			print "add team: add a team"
			print "add venue: add a venue"
			print "delete venue: delete a venue"
			print "add adjudicator: add an adjudicator"
			print "delete adjudicator: delete an adjudicator"

def create_matchups(grid_list, round_num, team_list, filter_lists):
	progress("[creating matchups for round "+str(round_num)+"]")
	progress("filtering grid list")
	filtration(grid_list, round_num, team_list, filter_lists)
	progress("adding priority to grids")
	addpriority(grid_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	progress("selecting grids")
	selected_grid_lists_with_info = return_selected_grid_lists(grid_list, round_num, team_list)

	for k, selected_grid_list_with_info in enumerate(selected_grid_lists_with_info):
		export_matchups(selected_grid_list_with_info[0], str(k)+"team", round_num)
		selected_grid_list_with_info[1].matchups_no = k+1

	return selected_grid_lists_with_info

def create_allocations(adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, round_num, filter_lists, constants_of_adj):
	progress("[creating allocations for round "+str(round_num)+"]")
	progress("filtering lattice list")
	lattice_filtration(adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, round_num, filter_lists)
	progress("adding priority to grids")
	addpriority(lattice_list)
	#show_adoptness1(grid_list, team_list)
	#print
	#show_adoptness2(grid_list, team_list)
	progress("selecting lattices")
	selected_lattice_lists_with_info = return_selected_lattice_lists(lattice_list, round_num, team_list, adjudicator_list, constants_of_adj)
	for k, selected_lattice_list_with_info in enumerate(selected_lattice_lists_with_info):
		export_allocations(selected_lattice_list_with_info[0], str(k)+"adj", round_num)
		selected_lattice_list_with_info[1].allocation_no = k+1

	return selected_lattice_lists_with_info

def preparation(filename_teams, filename_venues, filename_adjudicators, filename_settings, filename_settings_of_adj):
	team_list = read_teams(filename_teams)
	venue_list = read_venues(filename_venues)
	check_team_list(team_list)
	adjudicator_list = read_adjudicators(filename_adjudicators)
	check_adjudicator_list(adjudicator_list)

	constants, orders1 = read_constants(filename_settings)
	filter_lists = create_filter_lists(orders1)
	constants_of_adj, orders2 = read_constants_of_adj(filename_settings_of_adj)
	filter_of_adj_lists = create_filter_of_adj_lists(orders2)

	return team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj

def main_demo(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	for i in range(rounds):
		evaluate_adjudicator(adjudicator_list, constants_of_adj)
		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum2)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = selected_grid_lists_with_info[-1]

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=8, round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = selected_lattice_lists_with_info[-1]

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1)
		set_panel(allocations, adjudicator_list)
		export_allocations(allocations[0], "panel", i+1)
		
		set_venue(allocations[0], venue_list)
		export_allocations(allocations[0], "venue", i+1)

		export_official_ballot(allocations[0], i+1)
		export_blank_results(allocations[0], i+1)
		export_blank_results_of_adj(allocations[0], i+1)
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1)
		read_and_process_result(round_num=i+1, team_list=team_list)
		read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum2=teamnum2)

		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		show_debater_scores(team_list)
		show_teams_scores(team_list, teamnum2)
		#show_evaluation(adjudicator_list)
		show_adjudicator_score(adjudicator_list)
		#finish_round_debug(grid_list=grid_list, matchups=matchups, round_num=1)
		check_team_list2(team_list, i+1, teamnum2)
	
	export_results(team_list, adjudicator_list)

def main_no_adj_feedback(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	for i in range(rounds):
		prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum2)
		evaluate_adjudicator(adjudicator_list, constants_of_adj)
		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum2)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team)

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=8, round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1)
		prompt_panel(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)
		export_allocations(allocations[0], "panel", i+1)

		prompt_venue(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, filename_venues, filename_adjudicators)
		export_allocations(allocations[0], "venue", i+1)

		export_official_ballot(allocations[0], i+1)
		export_blank_results(allocations[0], i+1)
		export_blank_results_of_adj(allocations[0], i+1)
		show_matchups(allocations, i+1)

		#finish_round_debug(allocations=allocations[0], round_num=i+1)
		export_dummy_results_adj(allocations, i+1)
		while True:
			a = raw_input("read results of round {0}? (y/n) > ".format(i+1))
			if re.match(r'y', a):
				try:
					read_and_process_result(round_num=i+1, team_list=team_list)
					break
				except:
					progress("failed to read results")
					continue
			elif re.match(r'n', a):
				break
		try:
			read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum2=teamnum2)
		except:
			print "warning: results_of_adj file broken"
			print "you can still use this program but cannot use the '(adjudicators) avoid watched teams' feature"
			pass

		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		show_debater_scores(team_list)
		show_teams_scores(team_list, teamnum2)
		#show_evaluation(adjudicator_list)
		show_adjudicator_score(adjudicator_list)
		#finish_round_debug(grid_list=grid_list, matchups=matchups, round_num=1)
		check_team_list2(team_list, i+1, teamnum2)
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
	
	export_results(team_list, adjudicator_list)

def main_complete(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	for i in range(rounds):
		prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum2)
		evaluate_adjudicator(adjudicator_list, constants_of_adj)
		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum2)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team)

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=8, round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1)
		prompt_panel(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)
		export_allocations(allocations[0], "panel", i+1)

		prompt_venue(allocations, team_list, venue_list, adjudicator_list, i+1, filename_teams, filename_venues, filename_adjudicators)
		export_allocations(allocations[0], "venue", i+1)

		export_official_ballot(allocations[0], i+1)
		export_blank_results(allocations[0], i+1)
		export_blank_results_of_adj(allocations[0], i+1)
		show_matchups(allocations, i+1)

		#finish_round_debug(allocations=allocations[0], round_num=i+1)
		#export_dummy_results_adj(allocations, i+1)
		while True:
			a = raw_input("read results of round {0}? (y/n) > ".format(i+1))
			if re.match(r'y', a):
				try:
					read_and_process_result(round_num=i+1, team_list=team_list)
					break
				except:
					progress("failed to read results")
					continue
			elif re.match(r'n', a):
				break
		while True:
			a = raw_input("read results_of_adj of round {0}? (y/n) > ".format(i+1))
			if re.match(r'y', a):
				try:
					read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum2=teamnum2)
					break
				except:
					progress("failed to read results of adjs")
					continue 
			elif re.match(r'n', a):
				break

		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		show_debater_scores(team_list)
		show_teams_scores(team_list, teamnum2)
		#show_evaluation(adjudicator_list)
		show_adjudicator_score(adjudicator_list)
		#finish_round_debug(grid_list=grid_list, matchups=matchups, round_num=1)
		check_team_list2(team_list, i+1, teamnum2)
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
	
	export_results(team_list, adjudicator_list)

def main_quick_debug(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	for i in range(rounds):
		prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum2)
		evaluate_adjudicator(adjudicator_list, constants_of_adj)
		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		progress("creating grid list")
		grid_list = create_grid_list(team_list, teamnum2)
		selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+1, team_list=team_list, filter_lists=filter_lists)
		for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_grid(selected_grid_list_with_info, i+1)
		matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team)

		lattice_list = create_lattice_list(matchups[0], adjudicator_list)
		selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=8, round_num=i+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj)
		for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
			show_matchups_by_lattice(selected_lattice_list_with_info, i+1, constants_of_adj)
		allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

		allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+1)
		set_panel(allocations, adjudicator_list)
		export_allocations(allocations[0], "panel", i+1)
		
		set_venue(allocations[0], venue_list)
		export_allocations(allocations[0], "venue", i+1)

		export_official_ballot(allocations[0], i+1)
		export_blank_results(allocations[0], i+1)
		export_blank_results_of_adj(allocations[0], i+1)
		show_matchups(allocations, i+1)

		finish_round_debug(allocations=allocations[0], round_num=i+1)
		read_and_process_result(round_num=i+1, team_list=team_list)
		read_and_process_result_adj(round_num=i+1, team_list=team_list, adjudicator_list=adjudicator_list, teamnum2=teamnum2)
	
		sort_adjudicator_list_by_score(adjudicator_list)
		sort_team_list_by_score(team_list)

		show_debater_scores(team_list)
		show_teams_scores(team_list, teamnum2)
		#show_evaluation(adjudicator_list)
		show_adjudicator_score(adjudicator_list)
		#finish_round_debug(grid_list=grid_list, matchups=matchups, round_num=1)
		check_team_list2(team_list, i+1, teamnum2)
		save(adjudicator_list, venue_list, team_list, filename_teams, filename_venues, filename_adjudicators)
	
	export_results(team_list, adjudicator_list)

def main_restore(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	read_num = 0
	for i in range(100):
		try:
			read_and_process_result(round_num=i+1, team_list=team_list)
			progress("processed results of round "+str(i+1))
		except:
			read_num = i
			break
	for j in range(100):
		try:
			read_and_process_result_adj(round_num=j+1, team_list=team_list, adjudicator_list=adjudicator_list)
			progress("processed results_of_adj of round "+str(j+1))
		except:
			if j > read_num: read_num = j
			break

	load(adjudicator_list, venue_list, team_list)

	if rounds-read_num > 0:
		progress("start from round "+str(read_num+1))
		for i in range(rounds-read_num):
			prompt_before(team_list, venue_list, adjudicator_list, filename_teams, filename_venues, filename_adjudicators, teamnum2)
			evaluate_adjudicator(adjudicator_list, constants_of_adj)
			sort_adjudicator_list_by_score(adjudicator_list)
			sort_team_list_by_score(team_list)

			progress("creating grid list")
			grid_list = create_grid_list(team_list, teamnum2)
			selected_grid_lists_with_info = create_matchups(grid_list=grid_list, round_num=i+read_num+1, team_list=team_list, filter_lists=filter_lists)
			for selected_grid_list_with_info in selected_grid_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_grid(selected_grid_list_with_info, i+read_num+1)
			matchups = prompt(selected_grid_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+read_num+1, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team)

			lattice_list = create_lattice_list(matchups[0], adjudicator_list)
			selected_lattice_lists_with_info = create_allocations(adjudicator_list, selected_grid_list=matchups[0], team_list=team_list, lattice_list=lattice_list, break_team_num=8, round_num=i+read_num+1, filter_lists=filter_of_adj_lists, constants_of_adj=constants_of_adj)
			for selected_lattice_list_with_info in selected_lattice_lists_with_info:####selected_grid_list_with_info => [selected_grid_list, selected_grid_list_info]
				show_matchups_by_lattice(selected_lattice_list_with_info, i+read_num+1, constants_of_adj)
			allocations = prompt_adj(selected_lattice_lists_with_info, team_list, venue_list, adjudicator_list, grid_list, i+read_num+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

			allocations[1] = return_lattice_list_info(allocations[0], adjudicator_list, constants_of_adj, i+read_num+1)
			export_allocations(allocations[0], "panel", i+read_num+1)
			prompt_panel(allocations, team_list, venue_list, adjudicator_list, i+read_num+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

			export_allocations(allocations[0], "venue", i+read_num+1)
			prompt_venue(allocations, team_list, venue_list, adjudicator_list, i+read_num+1, filename_teams, constants_of_adj, filename_venues, filename_adjudicators)

			export_official_ballot(allocations[0], i+read_num+1)
			export_blank_results(allocations[0], i+read_num+1)
			export_blank_results_of_adj(allocations[0], i+1)
			show_matchups(allocations, i+read_num+1)

			export_dummy_results_adj(allocations, i+read_num+1)
			#finish_round_debug(allocations=allocations[0], round_num=i+read_num+1)
			while True:
				a = raw_input("read results of round {0}? (y/n) > ".format(i+1))
				if re.match(r'y', a):
					try:
						read_and_process_result(round_num=i+read_num+1, team_list=team_list)
						break
					except:
						progress("failed to read results")
						continue
				elif re.match(r'n', a):
					break
			while True:
				a = raw_input("read results_of_adj of round {0}? (y/n) > ".format(i+1))
				if re.match(r'y', a):
					try:
						read_and_process_result_adj(round_num=i+read_num+1, team_list=team_list, adjudicator_list=adjudicator_list)
						break
					except:
						progress("failed to read results of adjs")
						continue 
				elif re.match(r'n', a):
					break

			sort_adjudicator_list_by_score(adjudicator_list)
			sort_team_list_by_score(team_list)

			show_debater_scores(team_list)
			show_teams_scores(team_list, teamnum2)
			#show_evaluation(adjudicator_list)
			show_adjudicator_score(adjudicator_list)
			#finish_round_debug(grid_list=grid_list, matchups=matchups, round_num=1)
			check_team_list2(team_list, i+read_num+1, teamnum2)
	
	export_results(team_list, adjudicator_list)

def prompt_beginning(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2):
	while True:
		a = raw_input("Please type a command(you can see commands by typing 'help') [step 0] > ")

		#if re.match(r'restore', a):
		#	main_restore(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, filename_teams, filename_venues, filename_adjudicators)
		#elif re.match(r'start', a):
		#	main_ordinary(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators)
		if a == 'demo':
			main_demo(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2)
		elif a == 'no_adj_feedback':
			main_no_adj_feedback(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2)
		elif a == 'run':
			main_complete(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2)
		#elif re.match(r'debug', a):
		#	main_pda_test_debug(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, 4, filename_teams, filename_venues, filename_adjudicators)
		elif a == 'debug':
			main_quick_debug(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2)
		elif a == 'continue':
			main_restore(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, rounds, filename_teams, filename_venues, filename_adjudicators, debater_num_per_team, teamnum2)
		elif a == 'reset':
			reset()
			continue
		else:
			#print "restore: restore results"
			#print "start: start this program"
			print "run: start this program"
			print "no_adj_feedback: start this program without team2adj feedback"
			print "continue: restore results for pda tournament in 11/14"
			print "debug: debug this program with adj"
			print "demo: see demo of this program automatically"
			print "reset: reset data except venues/adjudicators/teams data"

			continue
		break

if __name__ == "__main__":
	backup_data()
	#show_logo_random_fade()
	#show_logo_star()
	team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj = preparation(FILENAME_TEAMS, FILENAME_VENUES, FILENAME_ADJUDICATORS, FILENAME_SETTINGS, FILENAME_SETTINGS_OF_ADJ)
	initial_check(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, TEAMNUM2)

	prompt_beginning(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, ROUND_NUM, FILENAME_TEAMS, FILENAME_VENUES, FILENAME_ADJUDICATORS, DEBATER_NUM_PER_TEAM, TEAMNUM2)

pass