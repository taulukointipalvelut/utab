# -*- coding: utf-8 -*-
import random
import time
import itertools
import threading
import collections
from . import interaction_modules
import re
try:
	import readline
except:
	pass
import math
from .bit_modules import *
from .commandline_modules import *
from .classes import *
from .property_modules import *
from .filter_modules import *
from .select_modules import *
from .io_modules import *

def merge_matchups_and_allocations(matchups, allocations, lattice_list, round_num, tournament, constants_of_adj, teamnum):
	new_allocations = [[], None]
	for grid, lattice in zip(matchups[0], allocations[0]):
		new_lattice = find_lattice_from_lattice_list(lattice_list, grid.teams, lattice.chair)
		new_lattice.panel = lattice.panel
		new_lattice.venue = lattice.venue
		new_allocations[0].append(new_lattice)

	selected_lattice_list_info = return_lattice_list_info(new_allocations[0], tournament, constants_of_adj, round_num, "", teamnum)
	selected_lattice_list_info.allocation_no = 1
	new_allocations[1] = selected_lattice_list_info

	return new_allocations

def import_matchup(filename_matchup, grid_list, tournament, teamnum):
	selected_lattice_list = []
	try:
		raw_data_rows = read_matchup(filename_matchup, teamnum)
	except:
		interaction_modules.warn("Unexpected error:", sys.exc_info()[0])
		raise Exception("error: the matchups to import must be '"+filename_matchup+"'")

	for row in raw_data_rows:
		grid = None
		chair = None
		panels = []
		venue = None
		teams = []
		lattice = None
		for i in range(teamnum):
			for team in tournament["team_list"]:
				if team.name == row[i]:
					teams.append(team)
					break
		if len(teams) != teamnum:
			raise Exception("error: cannot read teams ["+str(row[:teamnum])+"] in matchup")

		for adjudicator in tournament["team_list"]:
			if row[teamnum] == adjudicator.name:
				chair = adjudicator
				break
		else:
			raise Exception("error: cannot read chair ["+row[teamnum]+"] in matchup")

		if row[1+teamnum]:
			for adjudicator in tournament["team_list"]:
				if row[1+teamnum] == adjudicator.name:
					panels.append(adjudicator)
					break
			else:
				raise Exception("error: cannot read panel ["+row[1+teamnum]+"] in matchup")
		if row[2+teamnum]:
			for adjudicator in tournament["team_list"]:
				if row[2+teamnum] == adjudicator.name:
					panels.append(adjudicator)
					break
			else:
				raise Exception("error: cannot read panel ["+row[2+teamnum]+"] in matchup")
		if row[3+teamnum]:
			for venue2 in tournament["venue_list"]:
				if venue2.name == row[3+teamnum]:
					venue = venue2
					break
			else:
				raise Exception("error: cannot read venue ["+row[3+teamnum]+"] in matchup")

		grid = find_grid_from_grid_list(grid_list, teams)
		if grid is None:
			raise Exception("error: failed to create lattice (maybe you have set as absent some team in "+str(teams))
			time.sleep(3)

		lattice = Lattice(grid, chair)
		lattice.panel = panels
		lattice.venue = venue

		selected_lattice_list.append(lattice)

	return selected_lattice_list

def checks_before_creation(tournament, teamnum):
	adj_available_num = len([adj for adj in tournament["adjudicator_list"] if not adj.absent])
	venue_available_num = len([venue for venue in tournament["venue_list"] if venue.available])
	team_available_num = len([team for team in tournament["team_list"] if team.available])
	interaction_modules.progress("Available Adjudicators: {0:d}, Available Venues: {1:d}, Available Teams: {2:d}".format(adj_available_num, venue_available_num, team_available_num))

	if adj_available_num < team_available_num/teamnum:
		interaction_modules.warn("need more adjudicators")
		return False
	if venue_available_num < team_available_num/teamnum:
		interaction_modules.warn("need more venues")
		return False
	if team_available_num % teamnum != 0:
		interaction_modules.warn("the number of teams is not suitable for creating matchups")
		return False

	return True

def addpriority(grid_list):
	all_len = len(grid_list)
	for p, grid in enumerate(grid_list):
		grid.set_adoptness()
		interaction_modules.progress_bar2(p+1, all_len)
	interaction_modules.progress("")

def check_adjudicator_list(adjudicator_list):
	adjudicators_names = [adjudicator.name for adjudicator in adjudicator_list]
	for adjudicator_name in adjudicators_names:
		if adjudicators_names.count(adjudicator_name) > 1:
			interaction_modules.warn("error : same adjudicator appears :", adjudicator_name)
			time.sleep(5)

def check_team_list(team_list):
	team_names = [team.name for team in team_list]
	for team_name in team_names:
		if team_names.count(team_name) > 1:
			interaction_modules.warn("error : same team appears :", team_name)
			time.sleep(5)

	for team in team_list:
		if not("c" in [insti.scale for insti in team.institutions] or "a" in [insti.scale for insti in team.institutions] or "b" in [insti.scale for insti in team.institutions]):
			interaction_modules.warn("error : team scale broken", team_name)
			time.sleep(5)

def initial_check(tournament, filter_lists, filter_of_adj_lists, constants, constants_of_adj, style_cfg):
	teamnum = style_cfg["team_num"]
	if len(constants) != len(constants_of_adj):
		interaction_modules.warn("error : settings of adjudicators and tournament don't match")
		time.sleep(1)
	if len(tournament["venue_list"]) < len(tournament["team_list"])/float(teamnum):
		interaction_modules.warn("error : few rooms")
		time.sleep(1)
	if len(tournament["team_list"])/float(teamnum) > len(tournament["adjudicator_list"]):
		interaction_modules.warn("error : few adjudicators")
		time.sleep(1)

def sort_adjudicator_list_by_score(adjudicator_list):
	adjudicator_list.sort(key=lambda adjudicator: adjudicator.evaluation, reverse=True)
	for rank, adjudicator in enumerate(adjudicator_list):
		adjudicator.ranking = rank+1

def create_lattice_list(matchups, adjudicator_list):
	lattice_list = []
	for grid in matchups:
		for chair in adjudicator_list:
			lattice_list.append(Lattice(grid, chair))

	for lattice in lattice_list:
		if (False in [t.available for t in lattice.grid.teams]) or lattice.chair.absent:
			lattice.set_not_available()
	#interaction_modules.warn(str(len(lattice_list)))#db
	return lattice_list

def return_lattice_list_info(selected_lattice_list, tournament, constants_of_adj, round_num, comment, teamnum):
	selected_lattice_list_with_info = Lattice_list_info()
	lattice_list_checks(selected_lattice_list, constants_of_adj, round_num)
	errors = lattice_list_errors(selected_lattice_list, tournament, round_num)
	selected_lattice_list_with_info.large_warnings.extend(errors)
	for lattice in selected_lattice_list:
		for warn in lattice.warnings:
			selected_lattice_list_with_info.large_warnings.append(warn.longwarning())
	selected_lattice_list_with_info.large_warnings.sort()
	selected_lattice_list_with_info.large_warnings.sort()
	selected_lattice_list_with_info.strong_strong_indicator = calc_str_str_indicator(selected_lattice_list, teamnum)
	selected_lattice_list_with_info.num_of_warnings = calc_num_of_warnings(selected_lattice_list)
	selected_lattice_list_with_info.comment = comment

	return selected_lattice_list_with_info

def return_selected_lattice_lists(lattice_list, round_num, tournament, constants_of_adj, teamnum):
	selected_lattice_lists_with_info = []
	alg_list = [select_alg_adj2, select_alg_adj11, select_alg_adj13, select_alg_adj14]
	selected_lattice_lists = []

	cp1_small = lambda g: g.adoptness1
	cp2_small = lambda g: g.adoptness2
	cp1_strict = lambda g: g.adoptness_strict1
	cp2_strict = lambda g: g.adoptness_strict2
	cp1_long = lambda g: g.adoptness1long
	cp2_long = lambda g: g.adoptness2long
	cp1_weight = lambda g: g.adoptness_weight1
	cp2_weight = lambda g: g.adoptness_weight2

	cp_pair_list = [(cp1_small, cp2_small), (cp2_small, cp1_small), (cp1_long, cp2_long), (cp2_long, cp1_long), (cp1_strict, cp2_strict), (cp2_strict, cp1_strict), (cp1_weight, cp2_weight), (cp2_weight, cp1_weight)]


	entire_length = len(alg_list) * len(cp_pair_list)
	c = 1

	def wrap(alg):
		def new_alg(es, selected_lattice_lists, pid, *args):
			selected_lattice_lists[pid] = alg(pid, *args)
			es[pid].set()
		return new_alg

	#threads = []
	new_selected_lattice_lists = [[] for i in range(len(alg_list)*len(cp_pair_list))]
	es = [threading.Event() for i in range(len(alg_list)*len(cp_pair_list))]
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			alg_wrapped = wrap(alg)
			#interaction_modules.warn(str(i*len(alg_list)+j))
			t = threading.Thread(target=alg_wrapped, args=(es, new_selected_lattice_lists, i*len(alg_list)+j, lattice_list, round_num, tournament["adjudicator_list"], cp_pair))
			t.setDaemon(True)
			t.start()
			#if i == 0 and j == 0: t.start()

	while True:
		if False not in [e.isSet() for e in es]:
			selected_lattice_lists.extend(new_selected_lattice_lists)
			break
		else:
			interaction_modules.progress_bar2([e.isSet() for e in es].count(True), entire_length)
			time.sleep(0.5)

	interaction_modules.progress("")

	for selected_lattice_list in selected_lattice_lists:
		#if len(selected_lattice_list) == 19: interaction_modules.warn("warn")#db
		selected_lattice_list.sort(key=lambda lattice: lattice.__hash__())

	selected_lattice_lists2 = []
	for selected_lattice_list in selected_lattice_lists:
		if selected_lattice_list not in selected_lattice_lists2:
			selected_lattice_lists2.append(selected_lattice_list)

	for k, selected_lattice_list in enumerate(selected_lattice_lists2):
		selected_lattice_list_with_info = return_lattice_list_info(selected_lattice_list, tournament, constants_of_adj, round_num, "", teamnum)
		selected_lattice_lists_with_info.append([selected_lattice_list, selected_lattice_list_with_info])

	selected_lattice_lists_with_info.sort(key=lambda selected_lattice_list: selected_lattice_list[1].strong_strong_indicator, reverse=True)
			
	return selected_lattice_lists_with_info

def lattice_filtration(tournament, selected_grid_list, lattice_list, break_team_num, round_num, filter_lists):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round]
	function_list = filter_lists[round_num-1]
	#random.shuffle(function_list)
	for k, function in enumerate(function_list):
		interaction_modules.progress_bar2(k+1, len(function_list))
		function(round_num, tournament, selected_grid_list, lattice_list, break_team_num, k)
		#show_adoptbits_lattice(adjudicator_list, lattice_list, k)
		#print
		#show_adoptbitslong_lattice(adjudicator_list, lattice_list, k)
	interaction_modules.progress("")

def create_grid_list_by_thread(grid_list, team_list, teamnum, flag):
	try:
		t = threading.Thread(target=cgl, args=(grid_list, team_list, teamnum, flag))
		t.setDaemon(True)
		t.start()
	except:
		interaction_modules.warn("couldn't start the sub thread")
		cgl(grid_list, team_list, teamnum, flag)
	refresh_grids_for_adopt(grid_list)

def cgl(grid_list, team_list, teamnum, flag):
	team_combinations_list = list(itertools.combinations(team_list, teamnum))
	grid_list.extend(create_grids_by_combinations_list(team_combinations_list))
	try:
		flag.set()
	except:
		pass

def add_grid_by_team(grid_list, team_list, team, teamnum):
	team_combinations_list = list(itertools.combinations(team_list, teamnum-1))
	team_combinations_list = map((lambda comb: comb+[team]), team_combinations_list)
	grid_list.extend(create_grids_by_combinations_list(team_combinations_list))

def delete_grid_by_team(grid_list, team):
	def related(grid, team):
		if team in grid.teams:
			return True
		else:
			return False
	#new_grid_list = 
	grid_list = [grid for grid in grid_list if not related(grid, team)]

def create_grids_by_combinations_list(team_combinations_list):
	grid_list = []
	for team_combinations in team_combinations_list:
		team_permutations_list = list(itertools.permutations(team_combinations))
		related_grids = [Grid(list(team_permutations)) for team_permutations in team_permutations_list]
		for grid in related_grids:
			grid.related_grids = related_grids
			if True in [not(team.available) for team in grid.teams]:
				grid.set_not_available()
		grid_list.extend(related_grids)
	return grid_list

def create_grid_list(team_list, teamnum):
	grid_list = []
	flag = False
	cgl(grid_list, team_list, teamnum, flag)
	return grid_list
	"""
	if teamnum == 2:
		grid_list = []
		pair_list = list(itertools.combinations(team_list, 2))
		for pair in pair_list:
			grid1 = Grid([pair[0], pair[1]])
			grid2 = Grid([pair[1], pair[0]])
			grid1.pair_grid = grid2
			grid2.pair_grid = grid1
			grid_list.extend([grid1, grid2])
		for team in team_list:
			grid1 = Grid([team, team])
			grid1.pair_grid = grid1
			grid_list.append(grid1)
		for grid in grid_list:
			if not(grid.teams[0].available) or not(grid.teams[1].available):
				grid.available = False

		return grid_list
	else:
		grid_list = []
		bundle_list = list(itertools.permutations(team_list, 4))
		#for team1 in team_list:
		#	for team2 in team_list:
		#		for team3 in team_list:
		#			for team4 in team_list:
		#				grid_list.append(Grid([team1, team2, team3, team4]))
		len_bundle = len(bundle_list)
		for j, bundle in enumerate(bundle_list):
			interaction_modules.progress_bar2(j+1, len_bundle)
			grid_list.append(Grid(list(bundle)))
		print

		for grid in grid_list:
			if not(grid.teams[0].available) or not(grid.teams[1].available) or not(grid.teams[2].available) or not(grid.teams[3].available):
				grid.available = False

		return grid_list
	"""
	"""
	grid_list = []
	bundle_list = list(itertools.combinations(team_list, teamnum))
	len_bundle = len(bundle_list)
	for j, bundle in enumerate(bundle_list):
		team_lists = list(itertools.permutations(bundle, teamnum))
		interaction_modules.progress_bar2(j+1, len_bundle)
		for team_list_for_grid in team_lists:
			grid_list.append(Grid(list(team_list_for_grid)))
	print

	for grid in grid_list:
		if not(grid.teams[0].available) or not(grid.teams[1].available) or not(grid.teams[2].available) or not(grid.teams[3].available):
			grid.available = False

	return grid_list
	"""

def filtration(grid_list, round_num, tournament, filter_lists):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [power_pairing, prevent_same_institution_small, prevent_same_opponent, prevent_same_institution_middle, prevent_unfair_side, prevent_same_institution_large, random_pairing]
	function_list = filter_lists[round_num-1]
	all_len = len(grid_list)
	divided_grid_list_list = [grid_list[:int(all_len/4)], grid_list[int(all_len/4):int(all_len*2/4)], grid_list[int(all_len*2/4):int(all_len*3/4)], grid_list[int(all_len*3/4):]]
	es = [threading.Event() for i in range(4)]
	#random.shuffle(function_list)
	
	def func_wrapper(func):
		def func2(i, *args):
			func(*args)
			es[i].set()
		return func2

	for i, divided_grid_list in enumerate(divided_grid_list_list):
		for k, function in enumerate(function_list):
			#interaction_modules.progress_bar2(k+1, len(function_list))
			function2 = func_wrapper(function)
			t = threading.Thread(target=function2, args=(i, divided_grid_list, round_num, tournament["team_list"], k))
			t.setDaemon(True)
			t.start()
			#print str(function)#passpass
			#show_adoptbits(team_list, grid_list, k)
			#print
			#show_adoptbitslong(team_list, grid_list, k)
		#interaction_modules.progress("")

	while True:
		if False not in [e.isSet() for e in es]:
			break
		else:
			time.sleep(0.5)
	"""
	for k, function in enumerate(function_list):
		#interaction_modules.progress_bar2(k+1, len(function_list))
		function(grid_list, round_num, tournament["team_list"], k)
		#print str(function)#passpass
		#show_adoptbits(team_list, grid_list, k)
		#print
		#show_adoptbitslong(team_list, grid_list, k)
	#interaction_modules.progress("")
	"""

def find_grid_from_grid_list(grid_list, teams):
	for grid in grid_list:
		if grid.teams == teams:
			return grid
	return None


def find_lattice_from_lattice_list(lattice_list, teams, chair):
	for lattice in lattice_list:
		if lattice.grid.teams == teams and lattice.chair == chair:
			return lattice
	return None

def multi(selected_grid_list, selected_grid_lists2):
	for selected_grid_list2 in selected_grid_lists2:
		same = True
		for grid_pair in zip(selected_grid_list, selected_grid_list2):
			if grid_pair[0] != grid_pair[1]:
				same = False
				break
		if same: return True
	return False

def return_selected_grid_lists(grid_list, round_num, tournament, teamnum):
	if len(grid_list[0].teams) == 2:
		alg_list = [select_alg2, select_alg3, select_alg4, select_alg11, select_alg13, select_alg14]
	else:
		if len(grid_list) > 25**2:
			alg_list = []
		else:
			alg_list = [select_alg2, select_alg4, select_alg11, select_alg13, select_alg14]

	cp1_small = lambda g: g.adoptness1
	cp2_small = lambda g: g.adoptness2
	cp1_strict = lambda g: g.adoptness_strict1
	cp2_strict = lambda g: g.adoptness_strict2
	cp1_long = lambda g: g.adoptness1long
	cp2_long = lambda g: g.adoptness2long
	cp1_weight = lambda g: g.adoptness_weight1
	cp2_weight = lambda g: g.adoptness_weight2

	cp_pair_list = [(cp1_small, cp2_small), (cp2_small, cp1_small), (cp1_long, cp2_long), (cp2_long, cp1_long), (cp1_strict, cp2_strict), (cp2_strict, cp1_strict), (cp1_weight, cp2_weight), (cp2_weight, cp1_weight)]

	selected_grid_lists = []
	selected_grid_lists_with_info = []

	interaction_modules.progress("creating special matchups")
	c = 1
	entire_length = 5
	if len(grid_list[0].teams) == 4:#add extra matchups
		def add_extra_matchups(pickup, divide_team_list_by_4, decide_position, comment, teamnum):
			selected_grid_list_wudc = return_selected_grid_list_wudc(grid_list, tournament["team_list"], pickup, divide_team_list_by_4, decide_position)
			selected_grid_list_info = return_grid_list_info(selected_grid_list_wudc, tournament["team_list"], round_num, comment, teamnum)
			selected_grid_list_wudc2 = side_revision(grid_list, selected_grid_list_wudc)
			selected_grid_list_info2 = return_grid_list_info(selected_grid_list_wudc2, tournament["team_list"], round_num, comment+" side-rev", teamnum)
			#selected_grid_list_wudc3 = side_revision(grid_list, selected_grid_list_wudc2)
			#selected_grid_list_info3 = return_grid_list_info(selected_grid_list_wudc3, team_list, round_num, comment+" side-rev2")
			selected_grid_lists_with_info.append([selected_grid_list_wudc, selected_grid_list_info])
			selected_grid_lists_with_info.append([selected_grid_list_wudc2, selected_grid_list_info2])
			#selected_grid_lists_with_info.append([selected_grid_list_wudc3, selected_grid_list_info3])

		add_extra_matchups(pickup_random, divide_team_list_by_4_random, decide_position_random, "WUDC RULE RANDOM", teamnum)
		interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_random, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED (For Atournament)", teamnum)
		interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_up, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED pull up", teamnum)
		interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_down, divide_team_list_by_4_score, decide_position_fair, "WUDC RULE CUSTOMIZED pull down", teamnum)
		interaction_modules.progress_bar2(c, entire_length)
		c += 1
		add_extra_matchups(pickup_pull_up, divide_team_list_by_4_half, decide_position_fair, "WUDC RULE CUSTOMIZED position", teamnum)
		interaction_modules.progress_bar2(c, entire_length)
		c += 1
	interaction_modules.progress("")

	entire_length = len(alg_list) * len(cp_pair_list)
	c = 1

	def wrap(alg):
		def new_alg(es, selected_grid_lists, pid, *args):
			selected_grid_lists[pid] = alg(pid, *args)
			es[pid].set()
		return new_alg

	#threads = []
	new_selected_grid_lists = [[] for i in range(len(alg_list)*len(cp_pair_list))]
	es = [threading.Event() for i in range(len(alg_list)*len(cp_pair_list))]
	for i, cp_pair in enumerate(cp_pair_list):
		for j, alg in enumerate(alg_list):
			alg_wrapped = wrap(alg)
			t = threading.Thread(target=alg_wrapped, args=(es, new_selected_grid_lists, i*len(alg_list)+j, grid_list, round_num, tournament["team_list"], cp_pair))
			t.setDaemon(True)
			t.start()
			#if i == 0 and j == 0: t.start()

	while True:
		if False not in [e.isSet() for e in es]:
			selected_grid_lists.extend(new_selected_grid_lists)
			break
		else:
			interaction_modules.progress_bar2([e.isSet() for e in es].count(True), entire_length)
			time.sleep(0.5)
	"""
	while True:
		#if False not in [e.isSet() for e in es]:break
		if es[0].isSet(): break
		time.sleep(0.1)
	print(new_selected_grid_lists)
	"""
	"""
	for cp_pair in cp_pair_list:
		for alg in alg_list:
			interaction_modules.progress_bar2(c, entire_length)
			c+=1
			selected_grid_lists.append(alg(grid_list, round_num, tournament["team_list"], cp_pair))
	"""
	
	interaction_modules.progress("")
	interaction_modules.progress("deleting same matchups")
	selected_grid_lists2 = []
	for selected_grid_list in selected_grid_lists:
		if selected_grid_list != None:
			selected_grid_list.sort(key=lambda g: sum([t.code for t in g.teams]))
			if not multi(selected_grid_list, selected_grid_lists2):
				selected_grid_lists2.append(selected_grid_list)

	revised_selected_grid_lists2 = [side_revision(grid_list, selected_grid_list) for selected_grid_list in selected_grid_lists2]
	#revised2_selected_grid_lists2 = [side_revision2(grid_list, selected_grid_list) for selected_grid_list in revised_selected_grid_lists2]
	#selected_grid_lists3 = selected_grid_lists2+revised_selected_grid_lists2+revised2_selected_grid_lists2
	selected_grid_lists3 = revised_selected_grid_lists2

	for selected_grid_list3 in selected_grid_lists3:
		selected_grid_list3.sort(key=lambda grid: grid.__hash__())
	interaction_modules.progress("creating more precise matchups")
	if len(grid_list[0].teams) == 2:#add more precise matchups
		selected_grid_lists4 = copy.copy(selected_grid_lists3)
		for selected_grid_list in selected_grid_lists3:
			revised_selected_grid_list = revise_selected_grid_list(selected_grid_list, grid_list)
			if not multi(revised_selected_grid_list, selected_grid_lists4):
				selected_grid_lists4.append(revised_selected_grid_list)
	else:
		selected_grid_lists4 = selected_grid_lists3
	interaction_modules.progress("adding information to matchups")
	for k, selected_grid_list in enumerate(selected_grid_lists4):#add information
		selected_grid_list_info = return_grid_list_info(selected_grid_list, tournament, round_num, "", teamnum)
		selected_grid_lists_with_info.append([selected_grid_list, selected_grid_list_info])

	##################################################################################################

	selected_grid_lists_with_info.sort(key=lambda selected_grid_list: (selected_grid_list[1].power_pairing_indicator, -selected_grid_list[1].adopt_indicator, selected_grid_list[1].same_institution_indicator), reverse=True)

	return selected_grid_lists_with_info

def side_revision(grid_list, selected_grid_list):
	selected_grid_list2 = []
	#print [[[t.name for t in g.teams] for g in gl] for gl in selected_grid_lists2]
	if len(grid_list[0].teams) == 2:
		for grid in selected_grid_list:
			if ((grid.teams[0].past_sides.count("gov")-grid.teams[0].past_sides.count("opp")+1) > 0) and ((grid.teams[1].past_sides.count("gov")-grid.teams[1].past_sides.count("opp")-1) < 0):
				selected_grid_list2.extend(list(set(grid.related_grids)-set([grid])))
			else:
				selected_grid_list2.append(grid)

		return selected_grid_list2
	else:
		for grid in selected_grid_list:
			new_grid = grid

			selected_team_list_opening = [t for t in new_grid.teams if is_one_halfed(t, "cg") == -2 or is_one_halfed(t, "co") == -2]
			selected_team_list_closing = [t for t in new_grid.teams if is_one_halfed(t, "og") == 2 or is_one_halfed(t, "oo") == 2]
			selected_team_list_neutral = list(set(new_grid.teams)-set(selected_team_list_opening)-set(selected_team_list_closing))
			selected_team_list_neutral.sort(key=lambda team: sum(team.wins), reverse=True)
			selected_team_list = selected_team_list_opening+selected_team_list_neutral+selected_team_list_closing
			selected_team_list_opening2 = selected_team_list[0:2]
			selected_team_list_closing2 = selected_team_list[2:]
			selected_team_list_opening2.sort(key=lambda team: team.past_sides.count("og")+team.past_sides.count("cg"))
			selected_team_list_closing2.sort(key=lambda team: team.past_sides.count("og")+team.past_sides.count("cg"))
			selected_team_list2 = selected_team_list_opening2+selected_team_list_closing2
			new_grid = find_grid_from_grid_list(grid_list, selected_team_list2)
			#new_grid = better_grid(grid, grid_list)
			#if new_grid != grid: print new_grid, grid
			selected_grid_list2.append(new_grid)

		return selected_grid_list2

def side_revision2(grid_list, selected_grid_list):
	selected_grid_list2 = []
	#print [[[t.name for t in g.teams] for g in gl] for gl in selected_grid_lists2]
	if len(grid_list[0].teams) == 2:
		for grid in selected_grid_list:
			if ((grid.teams[0].past_sides.count("gov")-grid.teams[0].past_sides.count("opp")+1) > 0) and ((grid.teams[1].past_sides.count("gov")-grid.teams[1].past_sides.count("opp")-1) < 0):
				selected_grid_list2.append(list(set(grid.related_grids)-set([grid])))
			else:
				selected_grid_list2.append(grid)

		return selected_grid_list2
	else:
		for grid in selected_grid_list:
			new_grid = grid
			#print [t.name for t in grid.teams]
			#while changable:
			"""
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("og")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("oo")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("og")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("oo")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("oo")+1) > 0) and ((new_grid.teams[1].past_sides.count("og")-new_grid.teams[1].past_sides.count("oo")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[2].past_sides.count("cg")-new_grid.teams[2].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("cg")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			"""
			"""#yaku tatazu
			if is_one_halfed(new_grid.teams[0], "og") == 1 and is_one_halfed(new_grid.teams[3], "co") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if is_one_halfed(new_grid.teams[2], "cg") == 1 and is_one_halfed(new_grid.teams[3], "co") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if is_one_halfed(new_grid.teams[1], "oo") == 1 and is_one_halfed(new_grid.teams[2], "cg") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[0], "og") == 1 and is_one_halfed(new_grid.teams[1], "oo") == -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[1], "oo") == 2 and is_one_halfed(new_grid.teams[2], "cg") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if is_one_halfed(new_grid.teams[0], "og") == 2 and is_one_halfed(new_grid.teams[3], "co") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if is_one_halfed(new_grid.teams[1], "oo") == 2 and is_one_halfed(new_grid.teams[3], "co") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[3], new_grid.teams[2], new_grid.teams[1]])
			if is_one_halfed(new_grid.teams[0], "og") == 2 and is_one_halfed(new_grid.teams[2], "cg") == -2:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[2], new_grid.teams[1], new_grid.teams[0], new_grid.teams[3]])
			"""
			"""
			#unnecessary revision
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("oo")+1) > 0) and ((new_grid.teams[1].past_sides.count("og")-new_grid.teams[1].past_sides.count("oo")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			if ((new_grid.teams[2].past_sides.count("cg")-new_grid.teams[2].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("cg")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("og")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("oo")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
			if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("oo")-new_grid.teams[3].past_sides.count("co")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
			if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("og")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
			"""

			"""
			team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team2_oo)*(team1_oo - team2_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team3_cg - team4_co)*(team3_co - team4_cg) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team4_co)*(team1_co - team4_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team2_oo - team3_cg)*(team2_cg - team3_oo) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team1_og - team3_cg)*(team1_cg - team3_og) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[2], new_grid.teams[1], new_grid.teams[0], new_grid.teams[3]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			if (team2_oo - team4_co)*(team2_co - team4_oo) < -1:
				new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[3], new_grid.teams[2], new_grid.teams[1]])
				team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co = pos(new_grid)
			"""

			new_grid = better_grid(grid, grid_list)
			#if new_grid != grid: print new_grid, grid
			selected_grid_list2.append(new_grid)

		return selected_grid_list2

def better_grid(grid, grid_list):
	candidate_grid_list = []
	teams = grid.teams
	candidate_team_lists = list(itertools.permutations(teams, 4))
	for candidate_team_list in candidate_team_lists:
		#print candidate_team_list
		candidate_grid_list.append(find_grid_from_grid_list(grid_list, list(candidate_team_list)))
	candidate_grid_list.sort(key=lambda grid: (sum_one_halfed(grid), var4_one_halfed(grid)))
	return candidate_grid_list[0]

def sum_one_halfed(grid):
	return abs(is_one_halfed(grid.teams[0], "og"))+abs(is_one_halfed(grid.teams[1], "oo"))+abs(is_one_halfed(grid.teams[2], "cg"))+abs(is_one_halfed(grid.teams[3], "co"))

def var4_one_halfed(grid):
	avr = (abs(is_one_halfed(grid.teams[0], "og"))+abs(is_one_halfed(grid.teams[1], "oo"))+abs(is_one_halfed(grid.teams[2], "cg"))+abs(is_one_halfed(grid.teams[3], "co")))/4.0
	return (abs(is_one_halfed(grid.teams[0], "og"))-avr)**2+(abs(is_one_halfed(grid.teams[1], "oo"))-avr)**2+(abs(is_one_halfed(grid.teams[2], "cg"))-avr)**2+(abs(is_one_halfed(grid.teams[3], "co"))-avr)**2

def pos(new_grid):
	team1_og = new_grid.teams[0].past_sides.count("og")+1
	team1_oo = new_grid.teams[0].past_sides.count("oo")
	team1_cg = new_grid.teams[0].past_sides.count("cg")
	team1_co = new_grid.teams[0].past_sides.count("co")
	team2_og = new_grid.teams[1].past_sides.count("og")
	team2_oo = new_grid.teams[1].past_sides.count("oo")+1
	team2_cg = new_grid.teams[1].past_sides.count("cg")
	team2_co = new_grid.teams[1].past_sides.count("co")
	team3_og = new_grid.teams[2].past_sides.count("og")
	team3_oo = new_grid.teams[2].past_sides.count("oo")
	team3_cg = new_grid.teams[2].past_sides.count("cg")+1
	team3_co = new_grid.teams[2].past_sides.count("co")
	team4_og = new_grid.teams[3].past_sides.count("og")
	team4_oo = new_grid.teams[3].past_sides.count("oo")
	team4_cg = new_grid.teams[3].past_sides.count("cg")
	team4_co = new_grid.teams[3].past_sides.count("co")+1

	return team1_og, team1_oo, team1_cg, team1_co, team2_og, team2_oo, team2_cg, team2_co, team3_og, team3_oo, team3_cg, team3_co, team4_og, team4_oo, team4_cg, team4_co

def pickup_random(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	random.shuffle(team_list_cp)
	return team_list_cp[0:num], team_list_cp[num:]

def pickup_pull_up(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins), reverse=True)
	return team_list_cp[0:num], team_list_cp[num:]

def pickup_pull_down(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins))
	return team_list_cp[0:num], team_list_cp[num:]

"""
def pickup_adopt(team_buffer, team_list, num, grid_list):
	team_list_cp = list(copy.copy(team_list))
	team_list_cp.sort(key=lambda team: sum(team.wins))
	other_team_lists = list(itertools.combinations(team_list, num))
	candidate_grid_list = []
	for other_team in other_team_lists:
		teams_for_grid_origin = team_buffer+list(other_team)
		teams_for_grid_list = list(itertools.permutations(teams_for_grid_origin, 4))
		for teams_for_grid in teams_for_grid_list:
			candidate_grid_list.append(find_grid_from_grid_list(grid_list, teams_for_grid))
	candidate_grid_list.sort(key=lambda grid: (grid.adoptness1long, grid.adoptness2long), reverse=True)

	return list(set(candidate_grid_list[0].teams)-set(team_buffer))
"""

def divide_team_list_by_4_random(selected_team_list, grid_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	random.shuffle(selected_team_list_cp)
	selected_team_lists = list(zip(*[iter(selected_team_list_cp)]*4))
	return [list(ts) for ts in selected_team_lists]

"""
def divide_team_list_by_4_by_adopt(selected_team_list, grid_list):
	candidate_team_lists = list(itertools.permutations(selected_team_list, 4))
	def team_list_adoptness(team_list, grid_list):
		team_4_lists = list(itertools.permutations(selected_team_list, 4))
		adoptness = 0
		for team_4_list in team_4_lists:
			grid = find_grid_from_grid_list(grid_list, list(team_list))
			adoptness += grid.adoptness2long
		return adoptness
	candidate_team_lists.sort(key=lambda team_list: team_list_adoptness(team_list, grid_list))
	return [list(ts) for ts in selected_team_lists]
"""

def divide_team_list_by_4_score(selected_team_list, grid_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	selected_team_list_cp.sort(key=lambda team: sum(team.wins), reverse=True)
	selected_team_lists = list(zip(*[iter(selected_team_list_cp)]*4))
	return [list(ts) for ts in selected_team_lists]

def divide_team_list_by_4_half(selected_team_list, grid_list):
	team_lists_by_4 = []
	selected_team_list_cp = list(copy.copy(selected_team_list))
	selected_team_list_opening = [t for t in selected_team_list_cp if is_one_halfed(t, "cg") == -2 or is_one_halfed(t, "co") == -2]
	selected_team_list_closing = [t for t in selected_team_list_cp if is_one_halfed(t, "og") == 2 or is_one_halfed(t, "oo") == 2]
	selected_team_list_opening.sort(key=lambda team: sum(team.wins), reverse=True)
	selected_team_list_closing.sort(key=lambda team: sum(team.wins), reverse=True)
	for i in range(min(int(len(selected_team_list_opening)/2), int(len(selected_team_list_closing)/2))):
		team_lists_by_4.append([selected_team_list_opening[2*i], selected_team_list_opening[2*i+1], selected_team_list_closing[2*i], selected_team_list_closing[2*i+1]])
	rest = list(set(selected_team_list)-set([inner for outer in team_lists_by_4 for inner in outer]))
	rest.sort(key=lambda team: sum(team.wins), reverse=True)
	team_lists_by_4.extend(list(zip(*[iter(selected_team_list_cp)]*4)))
	return [list(ts) for ts in team_lists_by_4]

def decide_position_random(selected_team_list):
	selected_team_list_cp = list(copy.copy(selected_team_list))
	random.shuffle(selected_team_list_cp)
	return selected_team_list_cp

def decide_position_fair(selected_team_list):
	selected_team_lists = list(itertools.permutations(selected_team_list, 4))
	selected_team_lists.sort(key=lambda selected_team_list: abs(is_one_halfed(selected_team_list[0], "og"))+abs(is_one_halfed(selected_team_list[1], "oo"))+abs(is_one_halfed(selected_team_list[2], "cg"))+abs(is_one_halfed(selected_team_list[3], "co")))
	return list(selected_team_lists[0])

def return_selected_grid_list_wudc(grid_list, team_list, pickup, divide_team_list_by_4, decide_position):
	selected_grid_list = []
	team_list_available = [team for team in team_list if team.available]

	random.shuffle(team_list_available)
	team_list_available.sort(key=lambda team: sum(team.wins), reverse=True)

	team_lists_by_same_wins = []
	highest_wins = sum(team_list_available[0].wins)
	team_list_by_same_wins = []
	for team in team_list_available:
		if sum(team.wins) == highest_wins:
			team_list_by_same_wins.append(team)
		else:
			team_lists_by_same_wins.append(list(copy.copy(team_list_by_same_wins)))
			highest_wins = sum(team.wins)
			team_list_by_same_wins = [team]
	team_lists_by_same_wins.append(team_list_by_same_wins)

	selected_team_lists = []
	nowcount = 0
	team_num_for_4division = 0
	teams_buffer = []

	#print [sum(team.wins) for team in team_list_available]

	while nowcount < len(team_lists_by_same_wins):
		#print [t.name for ts in selected_team_lists for t in ts]
		#print [sum(t.wins) for ts in selected_team_lists for t in ts]
		if teams_buffer == []:
			if len(team_lists_by_same_wins[nowcount]) % 4 == 0:
				teams_buffer = team_lists_by_same_wins[nowcount]
				nowcount += 1
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				team_num_for_4division = 0
				#print "called4"
			else:
				team_num_for_4division = 4 - len(team_lists_by_same_wins[nowcount]) % 4
				teams_buffer = team_lists_by_same_wins[nowcount]
				nowcount += 1
				#print [t.name for t in teams_buffer]
				#print team_num_for_4division
				#print "called3"
		else:
			if len(team_lists_by_same_wins[nowcount]) == team_num_for_4division:
				"""
				picked_up_teams, rest = pickup(team_lists_by_same_wins[nowcount], team_num_for_4division)
				
				
				teams_buffer.extend(picked_up_teams)
				"""
				#print [t.name for t in picked_up_teams]
				#print [t.name for t in rest]
				teams_buffer.extend(team_lists_by_same_wins[nowcount])
				nowcount += 1
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				#print "called"
				team_num_for_4division = 0
			elif len(team_lists_by_same_wins[nowcount]) > team_num_for_4division:
				#print "called1"
				picked_up_teams, rest = pickup(teams_buffer, team_lists_by_same_wins[nowcount], team_num_for_4division, grid_list)
				teams_buffer.extend(picked_up_teams)
				team_lists_by_same_wins[nowcount] = rest
				selected_team_lists.append(list(copy.copy(teams_buffer)))
				teams_buffer = []
				team_num_for_4division = 0
			else:
				#print "called2"
				#print team_num_for_4division
				team_num_for_4division -= len(team_lists_by_same_wins[nowcount])
				#print team_num_for_4division
				teams_buffer.extend(team_lists_by_same_wins[nowcount])
				nowcount += 1
				#print team_num_for_4division
				#print [t.name for t in teams_buffer]
		#print [t.name for t in teams_buffer]
		#print [[t.name for t in ts] for ts in team_lists_by_same_wins]
		#print [[t.name for t in ts] for ts in selected_team_lists]

	selected_team_lists = [list(selected_team_list) for selected_team_list in selected_team_lists]

	selected_team_lists2 = []
	for selected_team_list in selected_team_lists:
		if len(selected_team_list) / 4 != 1:
			team_lists = divide_team_list_by_4(selected_team_list, grid_list)
			selected_team_lists2.extend(team_lists)
		else:
			selected_team_lists2.append(selected_team_list)

	selected_team_lists3 = []
	for selected_team_list in selected_team_lists2:
		selected_team_lists3.append(decide_position(selected_team_list))

	if len(selected_team_lists3[-1]) != 4:
		selected_team_lists3.pop()

	for selected_team_list in selected_team_lists3:
		#print selected_team_list
		selected_grid_list.append(find_grid_from_grid_list(grid_list, selected_team_list))

	return selected_grid_list

def revise_selected_grid_list(selected_grid_list, grid_list):
	selected_grid_list2 = []
	many_gov_teams = []
	many_opp_teams = []
	for grid in selected_grid_list:
		if is_one_sided(grid.teams[0], "gov", 2) > 0: many_gov_teams.append(grid.teams[0])
		if is_one_sided(grid.teams[1], "opp", 2) < 0: many_opp_teams.append(grid.teams[1])

	for i in range(len(selected_grid_list)):
		grid = selected_grid_list[i]
		team_0_i = selected_grid_list[i].teams[0]
		team_1_i = selected_grid_list[i].teams[1]
		if i == len(selected_grid_list)-1:
			selected_grid_list2.append(grid)
			break
		team_0_in = selected_grid_list[i+1].teams[0]
		team_1_in = selected_grid_list[i+1].teams[1]
		if team_0_i in many_gov_teams and team_1_i in many_opp_teams:
			selected_grid_list2.append(find_grid_from_grid_list(grid_list, [team_1_i, team_0_i]))
		elif team_0_i in many_gov_teams and team_1_in in many_opp_teams:
			selected_grid_list2.extend([find_grid_from_grid_list(grid_list, [team_1_in, team_0_i]), find_grid_from_grid_list(grid_list, [team_0_in, team_1_i])])
		elif team_0_in in many_gov_teams and team_1_i in many_opp_teams:
			selected_grid_list2.extend([find_grid_from_grid_list(grid_list, [team_1_i, team_0_in]), find_grid_from_grid_list(grid_list, [team_0_i, team_1_in])])
		else:
			selected_grid_list2.append(grid)
	return selected_grid_list2
	"""
	for grid in selected_grid_list_cp:
		if is_one_sided(grid.teams[0], True) > 0:
			if is_one_sided(selected_grid_list[selected_grid_list.index(grid)].teams[1], False) < 0:
				new_grid = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1]])
				selected_grid_list.insert()
				selected_grid_list.remove(grid)
			elif is_one_sided(selected_grid_list[selected_grid_list.index(grid)+1].teams[1], False) < 0:
				new_grid = find_grid_from_grid_list(grid_list, [grid.teams[0], selected_grid_list[selected_grid_list.index(grid)+1].teams[1]])
	"""

def sort_team_list_by_score(team_list):
	team_list.sort(key=lambda team: (sum(team.wins), sum(team.scores), (team.margin)), reverse=True)
	for j, team in enumerate(team_list):
		team.ranking = j + 1

def return_grid_list_info(selected_grid_list, tournament, round_num, comment, teamnum):
	selected_grid_list_info = Grid_list_info()
	grid_list_checks(selected_grid_list, tournament, round_num)
	errors = grid_list_errors(selected_grid_list, tournament, round_num)
	selected_grid_list_info.large_warnings.extend(errors)
	for grid in selected_grid_list:
		for warn in grid.warnings:
			selected_grid_list_info.large_warnings.append(warn.longwarning())
	selected_grid_list_info.large_warnings.sort()
	selected_grid_list_info.power_pairing_indicator = calc_power_pairing_indicator(selected_grid_list, teamnum)
	selected_grid_list_info.same_institution_indicator = calc_same_institution_indicator(selected_grid_list)
	selected_grid_list_info.adopt_indicator, selected_grid_list_info.adopt_indicator_sd, selected_grid_list_info.adopt_indicator2 = calc_adopt_indicator(selected_grid_list)
	selected_grid_list_info.num_of_warnings = calc_num_of_warnings(selected_grid_list)
	selected_grid_list_info.scatter_indicator = calc_scatter_indicator(selected_grid_list)
	selected_grid_list_info.comment = comment

	return selected_grid_list_info

def set_venue(allocations, venue_list):
	available_venue_list = [venue for venue in venue_list if venue.available]
	random.shuffle(available_venue_list)
	available_venue_list.sort(key=lambda venue:venue.priority)
	for lattice, venue in zip(allocations, available_venue_list):
		lattice.venue = venue
	#print(len(available_venue_list))
	#print(len(allocations))
	allocations.sort(key=lambda lattice: lattice.venue.name)

def set_panel(allocations, adjudicator_list):
	if len(allocations[0][0].grid.teams) == 2:
		for lattice in allocations[0]:
			for adjudicator in adjudicator_list:
				if adjudicator.name == lattice.chair.name:
					adjudicator.active = True
					break
		allocations[1].large_warnings = []
		
		inactive_adjudicator_list = [adjudicator for adjudicator in adjudicator_list if (not(adjudicator.active) and not(adjudicator.absent))]
		inactive_adjudicator_list.sort(key=lambda adjudicator:adjudicator.evaluation, reverse=True)
		
		for lattice in allocations[0]:
			may_be_panels = []
			for panel in inactive_adjudicator_list:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(panel.institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(panel.institutions)
				if list(conflicting_insti1 | conflicting_insti2) or panel.active:
					continue
				else:
					may_be_panels.append(panel)
				if len(may_be_panels) == 2:
					break
			if len(may_be_panels) < 2:
				continue
			else:
				lattice.panel = may_be_panels
				lattice.panel[0].active = True
				lattice.panel[1].active = True
	else:
		for lattice in allocations[0]:
			for adjudicator in adjudicator_list:
				if adjudicator.name == lattice.chair.name:
					adjudicator.active = True
					break
		allocations[1].large_warnings = []
		
		inactive_adjudicator_list = [adjudicator for adjudicator in adjudicator_list if (not(adjudicator.active) and not(adjudicator.absent))]
		inactive_adjudicator_list.sort(key=lambda adjudicator:adjudicator.evaluation, reverse=True)
		
		for lattice in allocations[0]:
			may_be_panels = []
			for panel in inactive_adjudicator_list:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(panel.institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(panel.institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(panel.institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(panel.institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4) or panel.active:
					continue
				else:
					may_be_panels.append(panel)
				if len(may_be_panels) == 2:
					break
			if len(may_be_panels) < 2:
				continue
			else:
				lattice.panel = may_be_panels
				lattice.panel[0].active = True
				lattice.panel[1].active = True

def evaluate_adjudicator(adjudicator_list, constants_of_adj):
	for adjudicator in adjudicator_list:
		adjudicator.evaluation = 0
		adjudicator.evaluation += adjudicator.reputation * constants_of_adj[adjudicator.active_num]["judge_repu_percent"]/100.0
		adjudicator.evaluation += adjudicator.judge_test * constants_of_adj[adjudicator.active_num]["judge_test_percent"]/100.0

		if adjudicator.active_num != 0:
			adjudicator.evaluation += sum(adjudicator.scores) / adjudicator.active_num * constants_of_adj[adjudicator.active_num]["judge_perf_percent"]/100.0

def refresh_grids(grid_list):
	for grid in grid_list:
		grid.initialize()

def exchange_teams(grid_list, matchups, team_a, team_b):
	if len(matchups[0].teams) == 2:
		for i, grid in enumerate(matchups):
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, team_a])
				#grid.teams[0], grid.teams[1] = 
				break
			elif grid.teams[1] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, team_b])
				break
			else:
				if grid.teams[0] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1]])
				elif grid.teams[1] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a])
				elif grid.teams[1] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b])
				elif grid.teams[0] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1]])
	else:
		for i, grid in enumerate(matchups):
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				#grid.teams[0], grid.teams[1] = team_b, team_a
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, team_a, grid.teams[2], grid.teams[3]])
				break
			elif grid.teams[0] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], team_a, grid.teams[3]])
				break
			elif grid.teams[0] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], grid.teams[2], team_a])
				break
			elif grid.teams[1] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, team_b, grid.teams[2], grid.teams[3]])
				break
			elif grid.teams[1] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, team_a, grid.teams[3]])
				break
			elif grid.teams[1] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, grid.teams[2], team_a])
				break
			elif grid.teams[2] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], team_b, grid.teams[3]])
				break
			elif grid.teams[2] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, team_b, grid.teams[3]])
				break
			elif grid.teams[2] == team_a and grid.teams[3] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_b, team_a])
				break
			elif grid.teams[3] == team_a and grid.teams[0] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], grid.teams[2], team_b])
				break
			elif grid.teams[3] == team_a and grid.teams[1] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, grid.teams[2], team_b])
				break
			elif grid.teams[3] == team_a and grid.teams[2] == team_b:
				matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_a, team_b])
				break
			else:
				if grid.teams[0] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_b, grid.teams[1], grid.teams[2], grid.teams[3]])
				elif grid.teams[1] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_b, grid.teams[2], grid.teams[3]])
				elif grid.teams[2] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_b, grid.teams[3]])
				elif grid.teams[3] == team_a:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], grid.teams[2], team_b])
				elif grid.teams[0] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [team_a, grid.teams[1], grid.teams[2], grid.teams[3]])
				elif grid.teams[1] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], team_a, grid.teams[2], grid.teams[3]])
				elif grid.teams[2] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], team_a, grid.teams[3]])
				elif grid.teams[3] == team_b:
					matchups[i] = find_grid_from_grid_list(grid_list, [grid.teams[0], grid.teams[1], grid.teams[2], team_a])

def exchange_adj(allocations, adjudicator1, adjudicator2):
	for lattice in allocations[0]:
		if len(lattice.panel) == 2:
			if lattice.panel[0] == adjudicator1:
				lattice.panel[0] = adjudicator2
			elif lattice.panel[0] == adjudicator2:
				lattice.panel[0] = adjudicator1
			if lattice.panel[1] == adjudicator2:
				lattice.panel[1] = adjudicator1
			elif lattice.panel[1] == adjudicator1:
				lattice.panel[1] = adjudicator2
		elif len(lattice.panel) == 1:
			if lattice.panel[0] == adjudicator1:
				lattice.panel[0] = adjudicator2
			elif lattice.panel[0] == adjudicator2:
				lattice.panel[0] = adjudicator1

	for lattice in allocations[0]:
		if lattice.chair == adjudicator1:
			lattice.chair = adjudicator2
		elif lattice.chair == adjudicator2:
			lattice.chair = adjudicator1

def delete_adj(allocations, panel):
	for lattice in allocations[0]:
		if len(lattice.panel) == 2:
			if lattice.panel[0] == panel:
				lattice.panel.pop(0)
			elif lattice.panel[1] == panel:
				lattice.panel.pop(1)
		elif len(lattice.panel) == 1:
			if lattice.panel[0] == panel:
				lattice.panel.pop(0)

def add_adj(allocations, chair, panel):
	for lattice in allocations[0]:
		if len(lattice.panel) < 2 and lattice.chair.name == chair:
			lattice.panel.append(panel)
			break
	else:
		interaction_modules.warn("please write a valid chair name")

def create_filter_of_adj_lists(orders):#Orders=>[[1,0,0,0], [0,2,3,1]] #[rand-alloc, str-str, fair-adj, conflicts]
	functions = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round, rotation_allocation]
	function_lists = []
	for order in orders:
		function_list = []
		for i in range(8):
			if i+1 in order:
				function_list.append(functions[order.index(i+1)])
		function_lists.append(function_list)

	return function_lists

def create_filter_lists(orders):#Orders=>[[1,0,0,0,0,0,0], [0,2,3,4,5,6,1]] #[rand-par, pow-par, small-insti, middle, large, same-opp, fair]
	functions = [random_pairing, power_pairing, prevent_same_institution_a, prevent_same_institution_b, prevent_same_institution_c, prevent_same_opponent, prevent_unfair_side]
	function_lists = []
	for order in orders:
		function_list = []
		for i in range(7):
			if i+1 in order:
				function_list.append(functions[order.index(i+1)])

		function_lists.append(function_list)

	return function_lists

def check_team_list2(team_list, experienced_round_num, teamnum):
	c = 0
	for team in team_list:
		if team.available: c+=1
	if (c % teamnum) == 1:
		interaction_modules.warn("[warning]The number of teams is odd")
		time.sleep(1)
	for team in team_list:
		if len(team.past_opponents) != experienced_round_num*(teamnum-1):
			if team.available:
				interaction_modules.warn("[warning]{0:15s} : uncertain data in past_opponents, round num != len(past_opponents)    {1}".format(team.name, team.past_opponents))
				time.sleep(0.01)
		if len(team.scores) != experienced_round_num:
			if team.available:
				interaction_modules.warn("[warning]{0:15s} : uncertain data in scores, round num != len(scores)    {1}".format(team.name, team.scores))
				time.sleep(0.01)
		if len(team.past_sides) != experienced_round_num:
			if team.available:
				interaction_modules.warn("[warning]{0:15s} : uncertain data in past_sides, round num != len(past_sides)    {1}".format(team.name, team.past_sides))
				time.sleep(0.01)
		if len(team.wins) != experienced_round_num:
			if team.available:
				interaction_modules.warn("[warning]{0:15s} : uncertain data in wins, round num != len(wins)    {1}".format(team.name, team.wins))
				time.sleep(0.01)

def cmp_allocations(allocations1, allocations2):
	for lattice1 in allocations1:
		for lattice2 in allocations2:
			if lattice1.teams == lattice2.teams:
				if lattice1.chair != lattice2.chair:
					return False
				else:
					break
		else:
			return False
	return True

def grid_list_errors(grid_list, tournament, round_num):
	large_warnings = []
	multi = {team.name:0 for team in tournament["team_list"]}

	for grid in grid_list:
		for team in grid.teams:
			multi[team.name] += 1

	for k, v in list(multi.items()):
		condemned_team = None
		for team in tournament["team_list"]:
			if team.name == k:
				condemned_team = team
				break
		if v > 1:
			large_warnings.append("error : a team appears more than two times :"+str(k)+": "+str(v))
		elif v == 0:
			if condemned_team.available:
				large_warnings.append("error : a team does not exist in matchups :"+str(k))
			else:
				large_warnings.append("warning : a team is absent :"+str(k))
	for i, grid in enumerate(grid_list):
		if len(list(set(grid.teams))) != len(grid.teams):
			large_warnings.append("error : a team matching with the same team :"+str([t.name for t in grid.teams]))
		for team in grid.teams:
			if not(team.available):
				large_warnings.append("error : an absent team appears :"+str(team.name))

	return large_warnings

def grid_list_checks(grid_list, tournament, round_num):
	for grid in grid_list:
		grid.warnings = []
		grid.large_warnings = []
	grid_check_one_sided(grid_list, tournament["team_list"], round_num)
	grid_check_past_opponent(grid_list, tournament["team_list"], round_num)
	grid_check_same_institution(grid_list, tournament["team_list"], round_num)
	grid_check_power_pairing(grid_list, round_num)

def grid_check_power_pairing(grid_list, round_num):
	if len(grid_list[0].teams) == 2:
		if round_num > 1:
			for grid in grid_list:
				if abs(grid.teams[0].ranking - grid.teams[1].ranking) > int(0.3*2*len(grid_list)) or abs(sum(grid.teams[0].wins) - sum(grid.teams[1].wins)) > 1:
					difference = int(100*abs(grid.teams[0].ranking - grid.teams[1].ranking)/float(2*len(grid_list)))
					grid.warnings.append(PowerPairing(grid.teams[0], grid.teams[-1], difference))
	else:
		if round_num > 1:
			all_wins = [sum(team.wins) for grid in grid_list for team in grid.teams]
			for grid in grid_list:
				rankings = [team.ranking for team in grid.teams]
				wins = [sum(team.wins) for team in grid.teams]
				wins.sort()
				rankings.sort()
				wins_dict = {team: team.ranking for team in grid.teams}
				teams_sorted = sorted(list(wins_dict.items()), key=lambda x:x[1])
				len_teams = len(grid_list)*4
				if rankings[3]-rankings[0] > int(0.3*len_teams) or ret_wei(wins[3], all_wins, len(grid_list))-ret_wei(wins[0], all_wins, len(grid_list)) > 1:
					difference = int(100*abs(rankings[3]-rankings[0])/float(len_teams))
					grid.warnings.append(PowerPairing(teams_sorted[0][0], teams_sorted[3][0], difference))

def grid_check_one_sided(grid_list, tournament, round_num):
	if len(grid_list[0].teams) == 2:
		for i, grid in enumerate(grid_list):
			if is_one_sided(grid.teams[0], "gov", 2) != 0:
				grid.warnings.append(Sided(grid.teams[0], "gov", [grid.teams[0].past_sides.count("gov")+1, grid.teams[0].past_sides.count("opp")]))
			if is_one_sided(grid.teams[1], "opp", 2) != 0:
				grid.warnings.append(Sided(grid.teams[1], "opp", [grid.teams[0].past_sides.count("gov"), grid.teams[0].past_sides.count("opp")+1]))
			if grid.teams[0].past_sides.count("gov") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					#interaction_modules.warn("ka;dslfjadsfdddddddddddd¥n¥n¥n¥n¥n¥n¥n¥n¥nn¥¥n¥n¥n¥n¥n")
					grid.warnings.append(AllSided(grid.teams[0], "gov", len(grid.teams[0].past_sides)+1))
			if grid.teams[1].past_sides.count("opp") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[1], "opp", len(grid.teams[1].past_sides)+1))
	else:
		for i, grid in enumerate(grid_list):
			og_sided_value = is_one_halfed(grid.teams[0], "og")
			oo_sided_value = is_one_halfed(grid.teams[1], "oo")
			cg_sided_value = is_one_halfed(grid.teams[2], "cg")
			co_sided_value = is_one_halfed(grid.teams[3], "co")
			"""
			if og_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[0].name)+"("+str(grid.teams[0].past_sides.count("og")+1)+":"+str(grid.teams[0].past_sides.count("oo"))+":"+str(grid.teams[0].past_sides.count("cg"))+":"+str(grid.teams[0].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if oo_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[1].name)+"("+str(grid.teams[1].past_sides.count("og"))+":"+str(grid.teams[1].past_sides.count("oo")+1)+":"+str(grid.teams[1].past_sides.count("cg"))+":"+str(grid.teams[1].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if cg_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[2].name)+"("+str(grid.teams[2].past_sides.count("og"))+":"+str(grid.teams[2].past_sides.count("oo"))+":"+str(grid.teams[2].past_sides.count("cg")+1)+":"+str(grid.teams[2].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if co_sided_value != 0:
				grid.large_warnings.append("warning : a team's position unfair :"+str(grid.teams[3].name)+"("+str(grid.teams[3].past_sides.count("og"))+":"+str(grid.teams[3].past_sides.count("oo"))+":"+str(grid.teams[3].past_sides.count("cg"))+":"+str(grid.teams[3].past_sides.count("co")+1)+")")
				grid.warnings.append("wrn(unfair side)")
			"""
			if grid.teams[0].past_sides.count("og") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[0], "og", len(grid.teams[0].past_sides)+1))
			if grid.teams[1].past_sides.count("oo") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[1], "oo", len(grid.teams[1].past_sides)+1))
			if grid.teams[2].past_sides.count("cg") == len(grid.teams[2].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[2], "cg", len(grid.teams[2].past_sides)+1))
			if grid.teams[3].past_sides.count("co") == len(grid.teams[3].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.warnings.append(AllSided(grid.teams[3], "co", len(grid.teams[3].past_sides)+1))
			if abs(og_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[0], "government/opposition", [grid.teams[0].past_sides.count("og")+1, grid.teams[0].past_sides.count("oo"), grid.teams[0].past_sides.count("cg"), grid.teams[0].past_sides.count("co")]))
			elif abs(og_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[0], "opening/closing", [grid.teams[0].past_sides.count("og")+1, grid.teams[0].past_sides.count("oo"), grid.teams[0].past_sides.count("cg"), grid.teams[0].past_sides.count("co")]))
			if abs(oo_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[1], "government/opposition", [grid.teams[1].past_sides.count("og"), grid.teams[1].past_sides.count("oo")+1, grid.teams[1].past_sides.count("cg"), grid.teams[1].past_sides.count("co")]))
			elif abs(oo_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[1], "opening/closing", [grid.teams[1].past_sides.count("og"), grid.teams[1].past_sides.count("oo")+1, grid.teams[1].past_sides.count("cg"), grid.teams[1].past_sides.count("co")]))
			if abs(cg_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[2], "government/opposition", [grid.teams[2].past_sides.count("og"), grid.teams[2].past_sides.count("oo"), grid.teams[2].past_sides.count("cg")+1, grid.teams[2].past_sides.count("co")]))
			elif abs(cg_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[2], "opening/closing", [grid.teams[2].past_sides.count("og"), grid.teams[2].past_sides.count("oo"), grid.teams[2].past_sides.count("cg")+1, grid.teams[2].past_sides.count("co")]))
			if abs(co_sided_value) == 1:
				grid.warnings.append(Sided(grid.teams[3], "government/opposition", [grid.teams[3].past_sides.count("og"), grid.teams[3].past_sides.count("oo"), grid.teams[3].past_sides.count("cg"), grid.teams[3].past_sides.count("co")+1]))
			elif abs(co_sided_value) == 2:
				grid.warnings.append(Sided(grid.teams[3], "opening/closing", [grid.teams[3].past_sides.count("og"), grid.teams[3].past_sides.count("oo"), grid.teams[3].past_sides.count("cg"), grid.teams[3].past_sides.count("co")+1]))

def grid_check_past_opponent(grid_list, tournament, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		#past_num = 0
		for pair in pair_list:
			if pair[0].past_opponents.count(pair[1].name) > 0:
				#grid.large_warnings.append("warning : a team matching again with past opponent :"+str(pair[0].name)+"-"+str(pair[1].name))
				#past_num += 1
				grid.warnings.append(PastOpponent(pair[0], pair[1]))

def grid_check_same_institution(grid_list, tournament, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = list(set(pair[0].institutions) & set(pair[1].institutions))
			if conflicting_insti:
				for ci in conflicting_insti:
					grid.warnings.append(SameInstitution(conflicting_insti[0]))

def lattice_list_errors(selected_lattice_list, tournament, round_num):
	large_warnings = []
	multi2 = {adjudicator.name:0 for adjudicator in tournament["adjudicator_list"]}

	for lattice in selected_lattice_list:
		multi2[lattice.chair.name] += 1
		if len(lattice.panel) == 2:
			multi2[lattice.panel[0].name] += 1
			multi2[lattice.panel[1].name] += 1
		elif len(lattice.panel) == 1:
			multi2[lattice.panel[0].name] += 1

	for k, v in list(multi2.items()):
		if v > 1:
			large_warnings.append("error : an adjudicator appears more than two times :"+str(k)+": "+str(v))
		elif v == 0:
			condemned_adjudicator = None
			for adjudicator in tournament["adjudicator_list"]:
				if adjudicator.name == k:
					condemned_adjudicator = adjudicator
					break
			if not condemned_adjudicator.absent:
				large_warnings.append("warning : an adjudicator does not exist in matchups :"+str(k))
			else:
				large_warnings.append("attention : an adjudicator is absent :"+str(k))

	multi3 = {grid:0 for grid in [lattice.grid for lattice in selected_lattice_list]}

	for lattice in selected_lattice_list:
		multi3[lattice.grid] += 1

	for k, v in list(multi3.items()):
		if v > 1:
			large_warnings.append("error : a grid appears more than two times :"+str(k)+": "+str(v))
			#large_warnings.append(str(sorted([adj.code for adj in tournament["adjudicator_list"]])))

	max_active_num = 0
	for adjudicator in tournament["adjudicator_list"]:
		if adjudicator.active_num > max_active_num:
			max_active_num = adjudicator.active_num
	next_active_adjudicators = []
	for lattice in selected_lattice_list:
		next_active_adjudicators.append(lattice.chair)
		next_active_adjudicators += lattice.panel

	for adjudicator in next_active_adjudicators:
		if adjudicator.active_num > max_active_num-1:
			max_active_num = adjudicator.active_num+1

	for adjudicator in tournament["adjudicator_list"]:
		if (adjudicator not in next_active_adjudicators) and ((max_active_num - adjudicator.active_num) > 0) and not(adjudicator.absent):
				large_warnings.append("warning : an adjudicator does nothing :{0:20s}, {1}".format(adjudicator.name, adjudicator.active_num))

	if round_num > 0:
		for adjudicator in tournament["adjudicator_list"]:
			if adjudicator.active_num_as_chair == 0:
				large_warnings.append("warning : a judge hasn't experienced a chair yet :"+str(adjudicator.name))
	return large_warnings

def lattice_list_checks(lattice_list, constants_of_adj, round_num):
	for lattice in lattice_list:
		lattice.warnings = []
		lattice.large_warnings = []
	lattice_check_conflict(lattice_list)
	lattice_check_bubble_round(lattice_list, constants_of_adj, round_num)
	lattice_check_same_round(lattice_list)

def lattice_check_conflict(lattice_list):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)

			if list(conflicting_insti1 | conflicting_insti2):
				lattice.warnings.append(InstitutionConflict(lattice.chair, lattice.grid.teams))
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams:
				lattice.warnings.append(PersonalConflict(lattice.chair, lattice.grid.teams))

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[1], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
	else:
		for i, lattice in enumerate(lattice_list):
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
			conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.chair.institutions)
			conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.chair.institutions)

			if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
				lattice.warnings.append(InstitutionConflict(lattice.chair, lattice.grid.teams))
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams or lattice.grid.teams[2].name in lattice.chair.conflict_teams or lattice.grid.teams[3].name in lattice.chair.conflict_teams:
				lattice.warnings.append(PersonalConflict(lattice.chair, lattice.grid.teams))

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[1], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams or lattice.grid.teams[2].name in lattice.panel[1].conflict_teams or lattice.grid.teams[3].name in lattice.panel[1].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.warnings.append(InstitutionConflict(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					lattice.warnings.append(PersonalConflict(lattice.panel[0], lattice.grid.teams))

def lattice_check_bubble_round(lattice_list, constants_of_adj, round_num):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.warnings.append(BubbleRound(lattice.grid.teams))
		
	else:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.warnings.append(BubbleRound(lattice.grid.teams))
		
def lattice_check_same_round(lattice_list):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams:
				lattice.warnings.append(WatchingAgain(lattice.chair, lattice.grid.teams))
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
	else:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams or lattice.grid.teams[2] in lattice.chair.watched_teams or lattice.grid.teams[3] in lattice.chair.watched_teams:
				lattice.warnings.append(WatchingAgain(lattice.chair, lattice.grid.teams))
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams or lattice.grid.teams[2] in lattice.panel[1].watched_teams or lattice.grid.teams[3] in lattice.panel[1].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[1], lattice.grid.teams))
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					lattice.warnings.append(WatchingAgain(lattice.panel[0], lattice.grid.teams))

pass