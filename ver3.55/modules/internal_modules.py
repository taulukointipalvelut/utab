# -*- coding: utf-8 -*-
import random
import time
import itertools
import collections
import re
try:
	import readline
except:
	pass
import math
from bit_modules import *
from commandline_modules import *
from classes import *
from property_modules import *
from filter_modules import *
from select_modules import *

def addpriority(grid_list):
	all_len = len(grid_list)
	for p, grid in enumerate(grid_list):

		for k, bit in enumerate(eachbit(grid.adoptbits)):
			if bit == 0:
				grid.adoptness1 = k
				break

		count = 0
		for k, bit in enumerate(eachbit(grid.adoptbits)):
			if bit == 1:
				count += 1
		grid.adoptness2 = count

		for k, bit in enumerate(eachbit(grid.adoptbitslong)):
			if bit == 0:
				grid.adoptness1long = k
				break

		count = 0
		for k, bit in enumerate(eachbit(grid.adoptbitslong)):
			if bit == 1:
				count += 1
		grid.adoptness2long = count


		for k, bit in enumerate(eachbit(grid.adoptbits_strict)):
			if bit == 0:
				grid.adoptness_strict1 = k
				break

		count = 0
		for k, bit in enumerate(eachbit(grid.adoptbits_strict)):
			if bit == 1:
				count += 1
		grid.adoptness_strict2 = count




		progress_bar2(p+1, all_len)
	print

def check_adjudicator_list(adjudicator_list):
	adjudicators_names = [adjudicator.name for adjudicator in adjudicator_list]
	for adjudicator_name in adjudicators_names:
		if adjudicators_names.count(adjudicator_name) > 1:
			print "error : same adjudicator appears :", adjudicator_name
			time.sleep(5)

def check_team_list(team_list):
	team_names = [team.name for team in team_list]
	for team_name in team_names:
		if team_names.count(team_name) > 1:
			print "error : same team appears :", team_name
			time.sleep(5)

	for team in team_list:
		if not(team.institution_scale == "c" or team.institution_scale == "a" or team.institution_scale == "b"):
			print "error : team scale broken", team_name
			time.sleep(5)

def initial_check(team_list, venue_list, adjudicator_list, filter_lists, filter_of_adj_lists, constants, constants_of_adj, teamnum2):
	if len(constants) != len(constants_of_adj):
		print "error : settings of adjudicators and tournament don't match"
		time.sleep(1)
	if teamnum2:
		if len(venue_list) < len(team_list)/2.0:
			print "error : few rooms"
			time.sleep(1)
		if len(team_list)/2.0 > len(adjudicator_list):
			print "error : few adjudicators"
			time.sleep(1)
	else:
		if len(venue_list) < len(team_list)/4.0:
			print "error : few rooms"
			time.sleep(1)
		if len(team_list)/4.0 > len(adjudicator_list):
			print "error : few adjudicators"
			time.sleep(1)

def sort_adjudicator_list_by_score(adjudicator_list):
	adjudicator_list.sort(key=lambda adjudicator: adjudicator.evaluation, reverse=True)
	for rank, adjudicator in enumerate(adjudicator_list):
		adjudicator.ranking = rank+1

def create_lattice_list(matchups, adjudicator_list):
	if len(matchups[0].teams) == 2:
		lattice_list = []
		for grid in matchups:
			for chair in adjudicator_list:
				lattice_list.append(Lattice(grid, chair))

		for lattice in lattice_list:
			if not(lattice.grid.teams[0].available) or not(lattice.grid.teams[1].available) or lattice.chair.absent:
				lattice.available = False
		return lattice_list
	else:
		lattice_list = []
		for grid in matchups:
			for chair in adjudicator_list:
				lattice_list.append(Lattice(grid, chair))

		for lattice in lattice_list:
			if not(lattice.grid.teams[0].available) or not(lattice.grid.teams[1].available) or not(lattice.grid.teams[2].available) or not(lattice.grid.teams[3].available) or lattice.chair.absent:
				lattice.available = False
		return lattice_list

def return_lattice_list_info(selected_lattice_list, adjudicator_list, constants_of_adj, round_num):
	selected_lattice_list_with_info = Lattice_list_info()
	lattice_list_checks(selected_lattice_list, constants_of_adj, round_num)
	errors = lattice_list_errors(selected_lattice_list, adjudicator_list, round_num)
	selected_lattice_list_with_info.large_warnings.extend(errors)
	for lattice in selected_lattice_list:
		selected_lattice_list_with_info.large_warnings.extend(lattice.large_warnings)
	selected_lattice_list_with_info.large_warnings = [large_warning for large_warning in selected_lattice_list_with_info.large_warnings if large_warning != '']
	selected_lattice_list_with_info.strong_strong_indicator = calc_str_str_indicator(selected_lattice_list)
	selected_lattice_list_with_info.num_of_warnings = calc_num_of_warnings(selected_lattice_list)

	return selected_lattice_list_with_info

def return_selected_lattice_lists(lattice_list, round_num, team_list, adjudicator_list, constants_of_adj):
	selected_lattice_lists_with_info = []
	alg_list = [select_alg_adj2, select_alg_adj11, select_alg_adj13, select_alg_adj14]
	selected_lattice_lists = []

	entire_length = len(alg_list) * 6
	c = 1
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness1
		lattice.comparison2 = lattice.adoptness2
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness1long
		lattice.comparison2 = lattice.adoptness2long
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness2
		lattice.comparison2 = lattice.adoptness1
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness2long
		lattice.comparison2 = lattice.adoptness1long
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness_strict1
		lattice.comparison2 = lattice.adoptness_strict2
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	for lattice in lattice_list:
		lattice.comparison1 = lattice.adoptness_strict2
		lattice.comparison2 = lattice.adoptness_strict1
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_lattice_lists.append(alg(lattice_list, round_num, team_list))
	print

	selected_lattice_lists2 = []
	for selected_lattice_list in selected_lattice_lists:
		if selected_lattice_list not in selected_lattice_lists2:
			selected_lattice_lists2.append(selected_lattice_list)

	for selected_lattice_list in selected_lattice_lists2:
		selected_lattice_list_with_info = return_lattice_list_info(selected_lattice_list, adjudicator_list, constants_of_adj, round_num)
		selected_lattice_lists_with_info.append([selected_lattice_list, selected_lattice_list_with_info])

	selected_lattice_lists_with_info.sort(key=lambda selected_lattice_list: selected_lattice_list[1].strong_strong_indicator, reverse=True)
			
	return selected_lattice_lists_with_info

def lattice_filtration(adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, round_num, filter_lists):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [random_allocation, prevent_str_wek_round, prevent_unfair_adjudicators, prevent_conflicts, avoid_watched_teams, prioritize_bubble_round]
	function_list = filter_lists[round_num-1]
	#random.shuffle(function_list)
	for k, function in enumerate(function_list):
		progress_bar2(k+1, len(function_list))
		function(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, k)
		#show_adoptbits_lattice(adjudicator_list, lattice_list, k)
		#print
		#show_adoptbitslong_lattice(adjudicator_list, lattice_list, k)
	print

def create_grid_list(team_list, teamnum2):
	if teamnum2:
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
			progress_bar2(j+1, len_bundle)
			grid_list.append(Grid(list(bundle)))
		print

		for grid in grid_list:
			if not(grid.teams[0].available) or not(grid.teams[1].available) or not(grid.teams[2].available) or not(grid.teams[3].available):
				grid.available = False

		return grid_list

def filtration(grid_list, round_num, team_list, filter_lists):#max_filters = 20
	#for i in range(9):
	#	filter1(grid_list, i)
	#function_list = [power_pairing, prevent_same_institution_small, prevent_same_opponent, prevent_same_institution_middle, prevent_unfair_side, prevent_same_institution_large, random_pairing]
	function_list = filter_lists[round_num-1]
	#random.shuffle(function_list)
	for k, function in enumerate(function_list):
		progress_bar2(k+1, len(function_list))
		function(grid_list, round_num, team_list, k)
		#print str(function)#passpass
		#show_adoptbits(team_list, grid_list, k)
		#print
		#show_adoptbitslong(team_list, grid_list, k)
	print

def find_grid_from_grid_list(grid_list, teams):
	for grid in grid_list:
		if grid.teams == teams:
			return grid

def return_selected_grid_lists(grid_list, round_num, team_list):
	selected_grid_lists_with_info = []
	alg_list = [select_alg2, select_alg3, select_alg4, select_alg11, select_alg13, select_alg14]

	selected_grid_lists = []

	entire_length = len(alg_list) * 6
	c = 1
	for grid in grid_list:
		grid.comparison1 = grid.adoptness1
		grid.comparison2 = grid.adoptness2
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	for grid in grid_list:
		grid.comparison1 = grid.adoptness1long
		grid.comparison2 = grid.adoptness2long
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	for grid in grid_list:
		grid.comparison1 = grid.adoptness2
		grid.comparison2 = grid.adoptness1
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	for grid in grid_list:
		grid.comparison1 = grid.adoptness2long
		grid.comparison2 = grid.adoptness1long
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	for grid in grid_list:
		grid.comparison1 = grid.adoptness_strict1
		grid.comparison2 = grid.adoptness_strict2
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	for grid in grid_list:
		grid.comparison1 = grid.adoptness_strict2
		grid.comparison2 = grid.adoptness_strict1
	for alg in alg_list:
		progress_bar2(c, entire_length)
		c+=1
		selected_grid_lists.append(alg(grid_list, round_num, team_list))
	print
	selected_grid_lists2 = []
	for selected_grid_list in selected_grid_lists:
		if (selected_grid_list not in selected_grid_lists2) and (selected_grid_list != None):
			selected_grid_lists2.append(selected_grid_list)

	selected_grid_lists3 = []
	#print [[[t.name for t in g.teams] for g in gl] for gl in selected_grid_lists2]
	if len(grid_list[0].teams) == 2:
		for selected_grid_list in selected_grid_lists2:
			new_selected_grid_list = []
			for grid in selected_grid_list:
				if ((grid.teams[0].past_sides.count("gov")-grid.teams[0].past_sides.count("opp")+1) > 0) and ((grid.teams[1].past_sides.count("gov")-grid.teams[1].past_sides.count("opp")-1) < 0):
					new_selected_grid_list.append(grid.pair_grid)
				else:
					new_selected_grid_list.append(grid)
			selected_grid_lists3.append(new_selected_grid_list)
	else:
		for selected_grid_list in selected_grid_lists2:###passpasspasspass
			new_selected_grid_list = []
			for grid in selected_grid_list:
				new_grid = grid
				#print [t.name for t in grid.teams]
				#while changable:
				if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("oo")+1) > 0) and ((new_grid.teams[1].past_sides.count("og")-new_grid.teams[1].past_sides.count("oo")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
				if ((new_grid.teams[2].past_sides.count("cg")-new_grid.teams[2].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("cg")-new_grid.teams[3].past_sides.count("co")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
				if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("og")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[1], new_grid.teams[0], new_grid.teams[2], new_grid.teams[3]])
				if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("oo")-new_grid.teams[3].past_sides.count("co")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[1], new_grid.teams[3], new_grid.teams[2]])
				if ((new_grid.teams[0].past_sides.count("og")-new_grid.teams[0].past_sides.count("co")+1) > 0) and ((new_grid.teams[3].past_sides.count("og")-new_grid.teams[3].past_sides.count("co")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[3], new_grid.teams[1], new_grid.teams[2], new_grid.teams[0]])
				if ((new_grid.teams[1].past_sides.count("oo")-new_grid.teams[1].past_sides.count("cg")+1) > 0) and ((new_grid.teams[2].past_sides.count("oo")-new_grid.teams[2].past_sides.count("cg")-1) < 0):
					new_grid = find_grid_from_grid_list(grid_list, [new_grid.teams[0], new_grid.teams[2], new_grid.teams[1], new_grid.teams[3]])

				new_selected_grid_list.append(new_grid)
			selected_grid_lists3.append(new_selected_grid_list)

	if len(grid_list[0].teams) == 2:
		selected_grid_lists4 = copy.copy(selected_grid_lists3)
		for selected_grid_list in selected_grid_lists3:
			selected_grid_lists4.append(revise_selected_grid_list(selected_grid_list, grid_list))
	else:
		selected_grid_lists4 = copy.copy(selected_grid_lists3)


	for selected_grid_list in selected_grid_lists4:
		selected_grid_list_info = return_grid_list_info(selected_grid_list, team_list, round_num)
		selected_grid_lists_with_info.append([selected_grid_list, selected_grid_list_info])
		##################################################################################################

	selected_grid_lists_with_info.sort(key=lambda selected_grid_list: (selected_grid_list[1].power_pairing_indicator, -selected_grid_list[1].adopt_indicator, selected_grid_list[1].same_institution_indicator), reverse=True)

	return selected_grid_lists_with_info

def revise_selected_grid_list(selected_grid_list, grid_list):
	selected_grid_list2 = []
	many_gov_teams = []
	many_opp_teams = []
	for grid in selected_grid_list:
		if is_one_sided(grid.teams[0], "gov", True) > 0: many_gov_teams.append(grid.teams[0])
		if is_one_sided(grid.teams[1], "opp", True) < 0: many_opp_teams.append(grid.teams[1])

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

def return_grid_list_info(selected_grid_list, team_list, round_num):
	selected_grid_list_info = Grid_list_info()
	grid_list_checks(selected_grid_list, team_list, round_num)
	errors = grid_list_errors(selected_grid_list, team_list, round_num)
	selected_grid_list_info.large_warnings.extend(errors)
	for grid in selected_grid_list:
		selected_grid_list_info.large_warnings.extend(grid.large_warnings)
	selected_grid_list_info.large_warnings = [large_warning for large_warning in selected_grid_list_info.large_warnings if large_warning != '']
	selected_grid_list_info.power_pairing_indicator = calc_power_pairing_indicator(selected_grid_list)
	selected_grid_list_info.same_institution_indicator = calc_same_institution_indicator(selected_grid_list)
	selected_grid_list_info.adopt_indicator, selected_grid_list_info.adopt_indicator_sd, selected_grid_list_info.adopt_indicator2 = calc_adopt_indicator(selected_grid_list)
	selected_grid_list_info.num_of_warnings = calc_num_of_warnings(selected_grid_list)

	return selected_grid_list_info

def set_venue(allocations, venue_list):
	available_venue_list = [venue for venue in venue_list if venue.available]
	random.shuffle(available_venue_list)
	available_venue_list.sort(key=lambda venue:venue.priority)
	for lattice, venue in zip(allocations, available_venue_list):
		lattice.venue = venue
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

def exchange_teams(matchups, team_a, team_b):
	if len(matchups[0].teams) == 2:
		for grid in matchups:
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				grid.teams[0], grid.teams[1] = team_b, team_a
				break
			elif grid.teams[1] == team_a and grid.teams[0] == team_b:
				grid.teams[0], grid.teams[1] = team_a, team_b
				break
			else:
				if grid.teams[0] == team_a:
					grid.teams[0] = team_b
				elif grid.teams[1] == team_b:
					grid.teams[1] = team_a
				elif grid.teams[1] == team_a:
					grid.teams[1] = team_b
				elif grid.teams[0] == team_b:
					grid.teams[0] = team_a
	else:
		for grid in matchups:
			if grid.teams[0] == team_a and grid.teams[1] == team_b:
				grid.teams[0], grid.teams[1] = team_b, team_a
				break
			elif grid.teams[0] == team_a and grid.teams[2] == team_b:
				grid.teams[0], grid.teams[2] = team_b, team_a
				break
			elif grid.teams[0] == team_a and grid.teams[3] == team_b:
				grid.teams[0], grid.teams[3] = team_b, team_a
				break
			elif grid.teams[1] == team_a and grid.teams[2] == team_b:
				grid.teams[1], grid.teams[2] = team_b, team_a
				break
			elif grid.teams[1] == team_a and grid.teams[3] == team_b:
				grid.teams[1], grid.teams[3] = team_b, team_a
				break
			elif grid.teams[2] == team_a and grid.teams[3] == team_b:
				grid.teams[2], grid.teams[3] = team_b, team_a
				break
			elif grid.teams[0] == team_a and grid.teams[1] == team_b:
				grid.teams[0], grid.teams[1] = team_a, team_b
				break
			elif grid.teams[0] == team_a and grid.teams[2] == team_b:
				grid.teams[0], grid.teams[2] = team_a, team_b
				break
			elif grid.teams[0] == team_a and grid.teams[3] == team_b:
				grid.teams[0], grid.teams[3] = team_a, team_b
				break
			elif grid.teams[1] == team_a and grid.teams[2] == team_b:
				grid.teams[1], grid.teams[2] = team_a, team_b
				break
			elif grid.teams[1] == team_a and grid.teams[3] == team_b:
				grid.teams[1], grid.teams[3] = team_a, team_b
				break
			elif grid.teams[2] == team_a and grid.teams[3] == team_b:
				grid.teams[2], grid.teams[3] = team_a, team_b
				break
			else:
				if grid.teams[0] == team_a:
					grid.teams[0] = team_b
				elif grid.teams[1] == team_a:
					grid.teams[1] = team_b
				elif grid.teams[2] == team_a:
					grid.teams[2] = team_b
				elif grid.teams[3] == team_a:
					grid.teams[3] = team_b
				elif grid.teams[0] == team_b:
					grid.teams[0] = team_a
				elif grid.teams[1] == team_b:
					grid.teams[1] = team_a
				elif grid.teams[2] == team_b:
					grid.teams[2] = team_a
				elif grid.teams[3] == team_b:
					grid.teams[3] = team_a

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
		print "please write a valid chair name"

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

def check_team_list2(team_list, experienced_round_num, teamnum2):
	if teamnum2:
		c = 0
		for team in team_list:
			if team.available: c+=1
		if (c % 2) == 1:
			print "[warning]The number of teams is odd"
			time.sleep(1)
		for team in team_list:
			if len(team.past_opponents) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in past_opponents, round num != len(past_opponents)    {1}".format(team.name, team.past_opponents)
					time.sleep(0.01)
			if len(team.scores) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in scores, round num != len(scores)    {1}".format(team.name, team.scores)
					time.sleep(0.01)
			if len(team.past_sides) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in past_sides, round num != len(past_sides)    {1}".format(team.name, team.past_sides)
					time.sleep(0.01)
			if len(team.wins) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in wins, round num != len(wins)    {1}".format(team.name, team.wins)
					time.sleep(0.01)
	else:
		c = 0
		for team in team_list:
			if team.available: c+=1
		if (c % 4) == 1:
			print "[warning]The number of teams is not devided by 4"
			time.sleep(1)
		for team in team_list:
			if len(team.past_opponents) != experienced_round_num*3:
				if team.available:
					print "[warning]{0:15s} : uncertain data in past_opponents, round num != len(past_opponents)    {1}".format(team.name, team.past_opponents)
					time.sleep(0.1)
			if len(team.scores) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in scores, round num != len(scores)    {1}".format(team.name, team.scores)
					time.sleep(0.1)
			if len(team.past_sides) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in past_sides, round num != len(past_sides)    {1}".format(team.name, team.past_sides)
					time.sleep(0.1)
			if len(team.wins) != experienced_round_num:
				if team.available:
					print "[warning]{0:15s} : uncertain data in wins, round num != len(wins)    {1}".format(team.name, team.wins)

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

def grid_list_errors(grid_list, team_list, round_num):
	large_warnings = []
	multi = {team.name:0 for team in team_list}

	for grid in grid_list:
		for team in grid.teams:
			multi[team.name] += 1

	for k, v in multi.items():
		condemned_team = None
		for team in team_list:
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
			large_warnings.append("error : a team matching with the same team :"+str(grid.teams))
		for team in grid.teams:
			if not(team.available):
				large_warnings.append("error : an absent team appears :"+str(team.name))

	return large_warnings

def grid_list_checks(grid_list, team_list, round_num):
	for grid in grid_list:
		grid.warnings = []
		grid.large_warnings = []
	grid_check_one_sided(grid_list, team_list, round_num)
	grid_check_past_opponent(grid_list, team_list, round_num)
	grid_check_same_institution(grid_list, team_list, round_num)
	grid_check_power_pairing(grid_list, round_num)

def grid_check_power_pairing(grid_list, round_num):
	if len(grid_list[0].teams) == 2:
		if round_num > 1:
			for grid in grid_list:
				if abs(grid.teams[0].ranking - grid.teams[1].ranking) > int(0.3*2*len(grid_list)) or abs(sum(grid.teams[0].wins) - sum(grid.teams[1].wins)) > 1:
					difference = int(100*abs(grid.teams[0].ranking - grid.teams[1].ranking)/float(2*len(grid_list)))
					grid.warnings.append("wrn(diff {0:d}%, {1}:{2})".format(difference, sum(grid.teams[0].wins), sum(grid.teams[1].wins)))
					grid.large_warnings.append("warning : stronger vs weaker team, {0:12s}-{1:12s} ranking difference: {2:d}%, wins: {3:d}-{4:d}".format(grid.teams[0].name, grid.teams[1].name, difference, sum(grid.teams[0].wins), sum(grid.teams[1].wins)))
	else:
		if round_num > 1:
			for grid in grid_list:
				rankings = [team.ranking for team in grid.teams]
				wins = [sum(team.wins) for team in grid.teams]
				wins.sort()
				rankings.sort()
				wins_dict = {team: team.ranking for team in grid.teams}
				teams_sorted = sorted(wins_dict.items(), key=lambda x:x[1])
				len_teams = len(grid_list)*4
				if rankings[3]-rankings[0] > int(0.3*len_teams) or ret_wei(wins[3], wins, len(grid_list))-ret_wei(wins[0], wins, len(grid_list)) > 1:
					difference = int(100*abs(rankings[3]-rankings[0])/float(len_teams))
					grid.warnings.append("wrn(diff {0:d}%, {1:2d}:{2:2d})".format(difference, wins[3], wins[0]))
					grid.large_warnings.append("warning : stronger vs weaker team, {0:12s}:{1:12s}, ranking difference: {2:d}%, wins: {3:d}-{4:d}".format(teams_sorted[0][0].name, teams_sorted[3][0].name, difference, wins[3], wins[0]))

def grid_check_one_sided(grid_list, team_list, round_num):
	if len(grid_list[0].teams) == 2:
		for i, grid in enumerate(grid_list):
			if is_one_sided(grid.teams[0], "gov", True) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[0].name)+"("+str(grid.teams[0].past_sides.count("gov")+1)+":"+str(grid.teams[0].past_sides.count("opp"))+")")
				grid.warnings.append("wrn(unfair side)")
			if is_one_sided(grid.teams[1], "opp", True) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[1].name)+"("+str(grid.teams[1].past_sides.count("gov"))+":"+str(grid.teams[1].past_sides.count("opp")+1)+")")
				grid.warnings.append("wrn(unfair side)")
			if grid.teams[0].past_sides.count("gov") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all gov :"+str(grid.teams[0].name)+"("+str(len(grid.teams[0].past_sides)+1)+")")
					grid.warnings.append("wrn(one sided)")
			if grid.teams[1].past_sides.count("opp") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all opp :"+str(grid.teams[1].name)+"("+str(len(grid.teams[1].past_sides)+1)+")")
					grid.warnings.append("wrn(one sided)")
	else:
		for i, grid in enumerate(grid_list):
			if is_one_sided(grid.teams[0], "og", False) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[0].name)+"("+str(grid.teams[0].past_sides.count("og")+1)+":"+str(grid.teams[0].past_sides.count("oo"))+":"+str(grid.teams[0].past_sides.count("cg"))+":"+str(grid.teams[0].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if is_one_sided(grid.teams[1], "oo", False) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[1].name)+"("+str(grid.teams[1].past_sides.count("og"))+":"+str(grid.teams[1].past_sides.count("oo")+1)+":"+str(grid.teams[1].past_sides.count("cg"))+":"+str(grid.teams[1].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if is_one_sided(grid.teams[2], "cg", False) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[2].name)+"("+str(grid.teams[2].past_sides.count("og"))+":"+str(grid.teams[2].past_sides.count("oo"))+":"+str(grid.teams[2].past_sides.count("cg")+1)+":"+str(grid.teams[2].past_sides.count("co"))+")")
				grid.warnings.append("wrn(unfair side)")
			if is_one_sided(grid.teams[3], "co", False) != 0:
				grid.large_warnings.append("warning : a team's side unfair :"+str(grid.teams[3].name)+"("+str(grid.teams[3].past_sides.count("og"))+":"+str(grid.teams[3].past_sides.count("oo"))+":"+str(grid.teams[3].past_sides.count("cg"))+":"+str(grid.teams[3].past_sides.count("co")+1)+")")
				grid.warnings.append("wrn(unfair side)")
			if grid.teams[0].past_sides.count("og") == len(grid.teams[0].past_sides):# or grid.teams[0].past_sides.count(False) == len(grid.teams[0].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all og :"+str(grid.teams[0].name))
					grid.warnings.append("wrn(one sided)")
			if grid.teams[1].past_sides.count("oo") == len(grid.teams[1].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all oo :"+str(grid.teams[1].name))
					grid.warnings.append("wrn(one sided)")
			if grid.teams[2].past_sides.count("cg") == len(grid.teams[2].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all cg :"+str(grid.teams[2].name))
					grid.warnings.append("wrn(one sided)")
			if grid.teams[3].past_sides.count("co") == len(grid.teams[3].past_sides):# or grid.teams[1].past_sides.count(True) == len(grid.teams[1].past_sides):
				if round_num > 2:
					grid.large_warnings.append("warning : a team's side all co :"+str(grid.teams[3].name))
					grid.warnings.append("wrn(one sided)")

def grid_check_past_opponent(grid_list, team_list, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		past_num = 0
		for pair in pair_list:
			if pair[0].past_opponents.count(pair[1].name) > 0:
				grid.large_warnings.append("warning : a team matching again with past opponent :"+str(pair[0].name)+"-"+str(pair[1].name))
				past_num += 1
		if past_num == 1:
			grid.warnings.append("wrn(past opponent)".format(past_num))
		elif past_num > 1:
			grid.warnings.append("wrn(past opponent:{0})".format(past_num))

def grid_check_same_institution(grid_list, team_list, round_num):
	for i, grid in enumerate(grid_list):
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = set(pair[0].institutions) & set(pair[1].institutions)
			if conflicting_insti:
				grid.large_warnings.append("warning : a team matching with the same institution("+grid.teams[0].institution_scale+") :"+str(grid.teams[0].institutions)+"-"+str(grid.teams[1].institutions))
				if pair[0].institution_scale == "c":
					grid.warnings.append("wrn(same insti(c))")
				elif pair[0].institution_scale == "b":
					grid.warnings.append("wrn(same insti(b))")
				elif pair[0].institution_scale == "a":
					grid.warnings.append("wrn(same insti(a))")

def lattice_list_errors(selected_lattice_list, adjudicator_list, round_num):
	large_warnings = []
	multi2 = {adjudicator.name:0 for adjudicator in adjudicator_list}

	for lattice in selected_lattice_list:
		multi2[lattice.chair.name] += 1
		if len(lattice.panel) == 2:
			multi2[lattice.panel[0].name] += 1
			multi2[lattice.panel[1].name] += 1
		elif len(lattice.panel) == 1:
			multi2[lattice.panel[0].name] += 1

	for k, v in multi2.items():
		if v > 1:
			large_warnings.append("error : an adjudicator appears more than two times :"+str(k)+": "+str(v))
		elif v == 0:
			condemned_adjudicator = None
			for adjudicator in adjudicator_list:
				if adjudicator.name == k:
					condemned_adjudicator = adjudicator
					break
			if not condemned_adjudicator.absent:
				large_warnings.append("warning : an adjudicator does not exist in matchups :"+str(k))
			else:
				large_warnings.append("attention : an adjudicator is absent :"+str(k))

	max_active_num = 0
	for adjudicator in adjudicator_list:
		if adjudicator.active_num > max_active_num:
			max_active_num = adjudicator.active_num
	next_active_adjudicators = []
	for lattice in selected_lattice_list:
		next_active_adjudicators.append(lattice.chair)
		next_active_adjudicators += lattice.panel

	for adjudicator in next_active_adjudicators:
		if adjudicator.active_num > max_active_num-1:
			max_active_num = adjudicator.active_num+1

	for adjudicator in adjudicator_list:
		if (adjudicator not in next_active_adjudicators) and ((max_active_num - adjudicator.active_num) > 0) and not(adjudicator.absent):
				large_warnings.append("warning : an adjudicator does nothing :{0:20s}, {1}".format(adjudicator.name, adjudicator.active_num))

	if round_num > 0:
		for adjudicator in adjudicator_list:
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
				lattice.large_warnings.append("warning : a judge watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+": "+str(lattice.chair.institutions))
				lattice.warnings.append("wrn(insti conflict)")
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams:
				lattice.large_warnings.append("warning : a judge watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.chair.name))
				lattice.warnings.append("wrn(perso conflict)")

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.large_warnings.append("warn : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+": "+str(lattice.panel[0].institutions))
					lattice.warnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[0].name))
					warnings.append("wrn(perso conflict)")
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.large_warnings.append("warning : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+": "+str(lattice.panel[1].institutions))
					lattice.warnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams:
					lattice.large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[1].name))
					lattice.warnings.append("wrn(perso conflict)")
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.large_warnings.append("warning : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+": "+str(lattice.panel[0].institutions))
					latticewarnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams:
					lattice.large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[0].name))
					lattice.warnings.append("wrn(perso conflict)")
	else:
		for i, lattice in enumerate(lattice_list):
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
			conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.chair.institutions)
			conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.chair.institutions)

			if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
				lattice.large_warnings.append("warning : a judge watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+"-"+str(lattice.grid.teams[2].institutions)+"-"+str(lattice.grid.teams[3].institutions)+": "+str(lattice.chair.institutions))
				lattice.warnings.append("wrn(insti conflict)")
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams or lattice.grid.teams[2].name in lattice.chair.conflict_teams or lattice.grid.teams[3].name in lattice.chair.conflict_teams:
				lattice.large_warnings.append("warning : a judge watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.chair.name))
				lattice.warnings.append("wrn(perso conflict)")

			if len(lattice.panel) == 2:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.large_warnings.append("warning : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+"-"+str(lattice.grid.teams[2].institutions)+"-"+str(lattice.grid.teams[3].institutions)+": "+str(lattice.panel[0].institutions))
					lattice.warnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[0].name))
					warnings.append("wrn(perso conflict)")
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[1].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[1].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.large_warnings.append("warning : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+"-"+str(lattice.grid.teams[2].institutions)+"-"+str(lattice.grid.teams[3].institutions)+": "+str(lattice.panel[1].institutions))
					lattice.warnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[1].conflict_teams or lattice.grid.teams[1].name in lattice.panel[1].conflict_teams or lattice.grid.teams[2].name in lattice.panel[1].conflict_teams or lattice.grid.teams[3].name in lattice.panel[1].conflict_teams:
					lattice.large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[1].name))
					lattice.warnings.append("wrn(perso conflict)")
			elif len(lattice.panel) == 1:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.panel[0].institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.panel[0].institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):
					lattice.large_warnings.append("warning : a panel watching a team of his/her conflict :"+str(lattice.grid.teams[0].institutions)+"-"+str(lattice.grid.teams[1].institutions)+"-"+str(lattice.grid.teams[2].institutions)+"-"+str(lattice.grid.teams[3].institutions)+": "+str(lattice.panel[0].institutions))
					lattice.warnings.append("wrn(insti conflict)")
				if lattice.grid.teams[0].name in lattice.panel[0].conflict_teams or lattice.grid.teams[1].name in lattice.panel[0].conflict_teams or lattice.grid.teams[2].name in lattice.panel[0].conflict_teams or lattice.grid.teams[3].name in lattice.panel[0].conflict_teams:
					large_warnings.append("warning : a panel watching a team of his/her personal conflict :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[0].name))
					warnings.append("wrn(perso conflict)")

def lattice_check_bubble_round(lattice_list, constants_of_adj, round_num):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.large_warnings.append("attention : bubble round :"+lattice.grid.teams[0].name+"-"+lattice.grid.teams[1].name+": "+str(lattice.grid.teams[0].wins.count(True))+"-"+str(lattice.grid.teams[1].wins.count(True)))
					lattice.warnings.append("att(bbl {0:1d}:{1:1d})".format(lattice.grid.teams[0].wins.count(True), lattice.grid.teams[1].wins.count(True)))
		
	else:
		for i, lattice in enumerate(lattice_list):
			if constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				if lattice.grid.bubble < 5:
					lattice.large_warnings.append("attention : bubble round :"+lattice.grid.teams[0].name+"-"+lattice.grid.teams[1].name+": "+str(sum(lattice.grid.teams[0].wins))+"-"+str(sum(lattice.grid.teams[1].wins)))
					lattice.large_warnings.append("                          "+lattice.grid.teams[2].name+"-"+lattice.grid.teams[2].name+": "+str(sum(lattice.grid.teams[3].wins))+"-"+str(sum(lattice.grid.teams[3].wins)))
					lattice.warnings.append("att(bbl {0:1d}:{1:1d}{2:1d}:{3:1d})".format(sum(lattice.grid.teams[0].wins), sum(lattice.grid.teams[1].wins), sum(lattice.grid.teams[2].wins), sum(lattice.grid.teams[3].wins)))
		
def lattice_check_same_round(lattice_list):
	if len(lattice_list[0].grid.teams) == 2:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams:
				watched_teams = [team.name for team in lattice.chair.watched_teams]
				lattice.large_warnings.append("warning : a judge watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.chair.name)+": "+str(watched_teams))
				lattice.warnings.append("wrn(watching again)")
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					watched_teams = [team.name for team in lattice.panel[0].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[0].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams:
					watched_teams = [team.name for team in lattice.panel[1].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[1].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams:
					watched_teams = [team.name for team in lattice.panel[0].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+": "+str(lattice.panel[0].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")
	else:
		for i, lattice in enumerate(lattice_list):
			if lattice.grid.teams[0] in lattice.chair.watched_teams or lattice.grid.teams[1] in lattice.chair.watched_teams or lattice.grid.teams[2] in lattice.chair.watched_teams or lattice.grid.teams[3] in lattice.chair.watched_teams:
				watched_teams = [team.name for team in lattice.chair.watched_teams]
				lattice.large_warnings.append("warning : a judge watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.chair.name)+": "+str(watched_teams))
				lattice.warnings.append("wrn(watching again)")
			if len(lattice.panel) == 2:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					watched_teams = [team.name for team in lattice.panel[0].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[0].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")
				if lattice.grid.teams[0] in lattice.panel[1].watched_teams or lattice.grid.teams[1] in lattice.panel[1].watched_teams or lattice.grid.teams[2] in lattice.panel[1].watched_teams or lattice.grid.teams[3] in lattice.panel[1].watched_teams:
					watched_teams = [team.name for team in lattice.panel[1].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[1].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")
			elif len(lattice.panel) == 1:
				if lattice.grid.teams[0] in lattice.panel[0].watched_teams or lattice.grid.teams[1] in lattice.panel[0].watched_teams or lattice.grid.teams[2] in lattice.panel[0].watched_teams or lattice.grid.teams[3] in lattice.panel[0].watched_teams:
					watched_teams = [team.name for team in lattice.panel[0].watched_teams]
					lattice.large_warnings.append("warning : a panel watching a team again :"+str(lattice.grid.teams[0].name)+"-"+str(lattice.grid.teams[1].name)+"-"+str(lattice.grid.teams[2].name)+"-"+str(lattice.grid.teams[3].name)+": "+str(lattice.panel[0].name)+": "+str(watched_teams))
					lattice.warnings.append("wrn(watching again)")

pass