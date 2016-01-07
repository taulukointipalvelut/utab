# -*- coding: utf-8 -*-
from .bit_modules import *
from .property_modules import *
import copy
import math
import random
import itertools

def power_pairing(grid_list, round_num, team_list, shift):
	if len(grid_list[0].teams) == 2:
		for grid in grid_list:
			grid.power_pairing = abs(grid.teams[0].ranking - grid.teams[1].ranking)

		all_len = len(grid_list)
		all_len_teams = len(team_list)*2
		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid: grid.power_pairing)
		for k, grid in enumerate(grid_list_cp):
			if k < int(0.60*all_len+3):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
			if k < int(0.20*all_len+4):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)

			if grid.power_pairing < 0.5*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)

			if grid.power_pairing < 0.25*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)

			if grid.power_pairing < 0.1*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
	else:
		
		for grid in grid_list:
			grid.power_pairing = 0
			grid_average = sum([team.ranking for team in grid.teams])/4
			for team in grid.teams:
				grid.power_pairing = (team.ranking - grid_average)**2
			grid.power_pairing = math.sqrt(grid.power_pairing/4)

		all_len = len(grid_list)
		all_len_teams = len(team_list)/4.0
		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid: grid.power_pairing)
		team_list_cp = copy.copy(team_list)
		team_list_cp.sort(key=lambda team: (sum(team.wins), sum(team.scores), (team.margin)), reverse=True)
		best_teams_tuple_list = list(zip(*[iter(team_list_cp)]*4))
		best_teams_set_list = [set(tp) for tp in best_teams_tuple_list]
		for k, grid in enumerate(grid_list_cp):
			if k < int(0.60*all_len+3):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
			if k < int(0.20*all_len+4):
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
			else:
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)

			if set(grid.teams) in best_teams_set_list:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)


			"""
			if grid.power_pairing < 0.5*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)

			if grid.power_pairing < 0.25*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)

			if grid.power_pairing < 0.1*all_len_teams:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			"""
		
		"""
		continuous_grid_list = []
		team_list_cp = copy.copy(team_list)
		#team_list_cp.sort(key=lambda team: team)
		#sort_team_list_by_score(team_list_cp)
		for i in range(len(team_list_cp)-3):
			continuous_grid_teams_list.append([team_list_cp[i], team_list_cp[i+1], team_list_cp[i+2], team_list_cp[i+3]])
		best_grid_teams_list = zip(*[iter(team_list_cp)]*4)
		print best_grid_teams_list
		for grid in grid_list:
			if set(grid.teams) in set(best_grid_teams_list):
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			elif set(grid.teams) in set(continuous_grid_teams_list):
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
		"""

def random_pairing(grid_list, round_num, team_list, shift):
	if len(grid_list[0].teams) == 2:
		team_code_list1 = [i for i in range(len(team_list))]
		team_code_list2 = [i for i in range(len(team_list))]
		team_codes = []
		for i in range(4):
			random.shuffle(team_code_list1)
			random.shuffle(team_code_list2)
			for team_code1, team_code2 in zip(team_code_list1, team_code_list2):
				if team_code1 != team_code2:
					team_codes.append([team_code1, team_code2])

		for grid in grid_list:
			if [grid.teams[0].code, grid.teams[1].code] in team_codes:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
	else:
		team_code_list1 = [i for i in range(len(team_list))]
		team_code_list2 = [i for i in range(len(team_list))]
		team_code_list3 = [i for i in range(len(team_list))]
		team_code_list4 = [i for i in range(len(team_list))]
		team_codes = []
		for i in range(4):
			random.shuffle(team_code_list1)
			random.shuffle(team_code_list2)
			random.shuffle(team_code_list3)
			random.shuffle(team_code_list4)
			for team_code1, team_code2, team_code3, team_code4 in zip(team_code_list1, team_code_list2, team_code_list3, team_code_list4):
				if len(set([team_code1, team_code2, team_code3, team_code4])) != len([team_code1, team_code2, team_code3, team_code4]):
					team_codes.append([team_code1, team_code2, team_code3, team_code4])

		for grid in grid_list:
			if [team.code for team in grid.teams] in team_codes:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)

def prevent_same_opponent(grid_list, round_num, team_list, shift):
	if len(grid_list[0].teams) == 2:
		for grid in grid_list:
			grid.past_match = grid.teams[1].past_opponents.count(grid.teams[0].name)
		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid: grid.past_match, reverse = True)

		all_len = len(grid_list)
		for k, grid in enumerate(grid_list_cp):
			if grid.past_match == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				continue
			else:
				if k < int(0.20*all_len+4):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				if k < int(0.40*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				if k < int(0.60*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				if grid.past_match == 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif grid.past_match > 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)


		#grid_check_past_opponent(grid_list, team_list, round_num)
	else:
		for grid in grid_list:
			grid.past_match = 0
			pair_list = list(itertools.combinations(grid.teams, 2))
			for pair in pair_list:
				grid.past_match += pair[0].past_opponents.count(pair[1].name)

		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid: grid.past_match, reverse = True)

		all_len = len(grid_list)
		for k, grid in enumerate(grid_list_cp):
			if grid.past_match == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				continue
			else:
				if k < int(0.20*all_len+4):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				if k < int(0.40*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				if k < int(0.60*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				if grid.past_match == 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif grid.past_match > 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)

def prevent_same_institution_a(grid_list, round_num, team_list, shift):
	for grid in grid_list:#mark true on grids which should be avoided by institution affirmative action
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = (set(pair[0].institutions) & set(pair[1].institutions))
			if list(conflicting_insti) != [] and pair[0].institution_scale == "a":
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				break
		else:
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)

def prevent_same_institution_b(grid_list, round_num, team_list, shift):
	for grid in grid_list:#mark true on grids which should be avoided by institution affirmative action
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = (set(pair[0].institutions) & set(pair[1].institutions))
			if list(conflicting_insti) != [] and pair[0].institution_scale == "b":
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				break
		else:
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)

def prevent_same_institution_c(grid_list, round_num, team_list, shift):
	for grid in grid_list:#mark true on grids which should be avoided by institution affirmative action
		pair_list = list(itertools.combinations(grid.teams, 2))
		for pair in pair_list:
			conflicting_insti = (set(pair[0].institutions) & set(pair[1].institutions))
			if list(conflicting_insti) != [] and pair[0].institution_scale == "c":
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				break
		else:
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
			grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)

def prevent_unfair_side(grid_list, round_num, team_list, shift):
	if len(grid_list[0].teams) == 2:
		grid_list_cp = copy.copy(grid_list)
		for grid in grid_list_cp:
			one_sided_value = abs(is_one_sided(grid.teams[0], "gov", 2))+abs(is_one_sided(grid.teams[1], "opp", 2))
			if one_sided_value == 2:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			elif one_sided_value == 1:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
		"""
		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid: abs(is_one_sided(grid.teams[0], "gov", True))+abs(is_one_sided(grid.teams[1], "opp", True)), reverse=True)
		all_len = len(grid_list)
		for k, grid in enumerate(grid_list_cp):
			one_sided_value = abs(is_one_sided(grid.teams[0], "gov", True))+abs(is_one_sided(grid.teams[1], "opp", True))
			if one_sided_value == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				if k < int(0.20*all_len+4):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				if k < int(0.40*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				if k < int(0.60*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)

				if one_sided_value == 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif one_sided_value > 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
		"""

		"""
		for grid in grid_list:
			if grid.teams[0].past_sides.count(True)-grid.teams[1].past_sides.count(True) > 1 or grid.teams[0].past_sides.count(False)-grid.teams[1].past_sides.count(False) < -1:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			elif grid.teams[0].past_sides.count(True)-grid.teams[1].past_sides.count(True) > 0 or grid.teams[0].past_sides.count(False)-grid.teams[1].past_sides.count(False) < 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
		"""
		"""
		grid_list_cp = copy.copy(grid_list)
		all_len = len(grid_list)
		grid_list_cp.sort(key=lambda grid: grid_unfairness(grid), reverse=True)#3, 2,1, 1,0,0,0,0,0
		#print [abs(team_gov_percentage(grid.teams[0])-0.5)+abs(team_gov_percentage(grid.teams[1])-0.5) for grid in grid_list_cp]
		for k, grid in enumerate(grid_list_cp):
			if grid_unfairness(grid) == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:	
				if k < int(0.2*all_len+4):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				if k < int(0.4*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				if k < int(0.6*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)


		"""

		"""
		for team in team_list:
			team.unfairity = team.past_sides.count(True) - team.past_sides.count(False)
		unfairity_count_dict = {team.unfairity:[] for team in team_list}
		for team in team_list:
			unfairity_count_dict[team.unfairity].append(team)
		unfairities = unfairity_count_dict.keys()
		unfairities.sort(key=abs, reverse=True)

		max_in_unfairities = max(unfairities, key=abs)
		c = 0#prior teams whose next side should be opp/gov
		d = 0
		if not max_in_unfairities == 0:
			for unfairity in unfairities:
				for team in unfairity_count_dict[unfairity]:
					if team.available:
						if unfairity == abs(max_in_unfairities):
							if c >= len_available(team_list)/2:
								break
							else:
								team.side_priority = True
								c += 1
						elif unfairity == -abs(max_in_unfairities):
							if d >= len_available(team_list)/2:
								break
							else:
								team.side_priority = True
								d += 1

		for grid in grid_list:
			if grid.teams[0].side_priority and grid.teams[1].side_priority:
				grid.pair_grid.adoptbits = bitshiftadd(grid.pair_grid.adoptbits, 1, shift)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3+1)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3+2)
			elif grid.teams[0].side_priority:
				grid.pair_grid.adoptbits = bitshiftadd(grid.pair_grid.adoptbits, 1, shift)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3+1)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 0, shift*3+2)
			elif grid.teams[1].side_priority:
				grid.pair_grid.adoptbits = bitshiftadd(grid.pair_grid.adoptbits, 1, shift)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 1, shift*3+1)
				grid.pair_grid.adoptbitslong = bitshiftadd(grid.pair_grid.adoptbitslong, 0, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
		"""
		#grid_check_one_sided(grid_list, team_list, round_num)
		#show_adoptbits(grid_list, shift)
	else:
		grid_list_cp = copy.copy(grid_list)
		for grid in grid_list_cp:
			one_sided_value = abs(is_one_halfed(grid.teams[0], "og"))+abs(is_one_halfed(grid.teams[1], "oo"))+abs(is_one_halfed(grid.teams[2], "cg"))+abs(is_one_halfed(grid.teams[3], "co"))
			if int(one_sided_value/2) >= 3:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			elif int(one_sided_value/2) == 2:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			elif int(one_sided_value/2) == 1:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			elif int(one_sided_value/2) == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
			else:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
		"""
		grid_list_cp = copy.copy(grid_list)
		grid_list_cp.sort(key=lambda grid:abs(is_one_sided(grid.teams[0], "og", False))+abs(is_one_sided(grid.teams[1], "oo", False))+abs(is_one_sided(grid.teams[2], "cg", False))+abs(is_one_sided(grid.teams[3], "co", False)), reverse=True)
		for k,grid in enumerate(grid_list_cp):
			one_sided_value = abs(is_one_sided(grid.teams[0], "og", False))+abs(is_one_sided(grid.teams[1], "oo", False))+abs(is_one_sided(grid.teams[2], "cg", False))+abs(is_one_sided(grid.teams[3], "co", False))
			if one_sided_value == 0:
				grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
				grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)
			else:
				if k < int(0.20*all_len+4):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3)
				if k < int(0.40*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 0, shift)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits = bitshiftadd(grid.adoptbits, 1, shift)
				if k < int(0.60*all_len+3):
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				else:
					grid.adoptbitslong = bitshiftadd(grid.adoptbitslong, 1, shift*3+2)

				if one_sided_value == 4:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif one_sided_value == 3:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif one_sided_value == 2:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
				elif one_sided_value == 1:
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 1, shift*3+1)
					grid.adoptbits_strict = bitshiftadd(grid.adoptbitslong, 0, shift*3+2)
		"""

def prevent_str_wek_round(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	true_grids_list1 = []
	true_grids_list2 = []
	true_grids_list3 = []
	lattice_list_cp = copy.copy(lattice_list)
	lattice_list_cp.sort(key=lambda lattice: abs(return_lattice_average_ranking(lattice)-lattice.chair.ranking))

	all_len = len(lattice_list)
	for k, lattice in enumerate(lattice_list_cp):
		if k < int(0.60*all_len+3):
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
		else:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
		if k < int(0.40*all_len+3):
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
		else:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
		if k < int(0.20*all_len+4):
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
		else:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)

def prevent_conflicts(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	if len(lattice_list[0].grid.teams) == 2:
		for lattice in lattice_list:
			if lattice.grid.teams[0].name in lattice.chair.conflict_teams or lattice.grid.teams[1].name in lattice.chair.conflict_teams:#personal conflict
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
			else:#not personal conflict
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
				if list(conflicting_insti1 | conflicting_insti2):#conflict
					if list(conflicting_insti1 & conflicting_insti2):
						lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
						lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					else:
						lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
						lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
				else:#no conflict
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
		"""
		for lattice in lattice_list:
			conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
			conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
			if list(conflicting_insti1 | conflicting_insti2):
				lattice.conflict = True
			if lattice.grid.teams[0].team_name in lattice.chair.conflict_teams or lattice.grid.teams[1].team_name in lattice.chair.conflict_teams:
				lattice.personal_conflict = True

		grids_of_adj_and_grid_without_personal_conflict_list = [lattice for lattice in lattice_list if not(lattice.personal_conflict)]
		grids_of_adj_and_grid_without_personal_and_institution_conflict_list = [lattice for lattice in lattice_list if not(lattice.personal_conflict) and not(lattice.conflict)]
		grids_of_adj_and_grid_without_personal_and_with_same_institution_list = [lattice for lattice in lattice_list if (not(lattice.personal_conflict) and lattice.conflict and list(conflicting_insti1&conflicting_insti2))]

		for lattice in lattice_list:
			if lattice in grids_of_adj_and_grid_without_personal_conflict_list:
				lattice.adopt.append(True)
			else:
				lattice.adopt.append(False)
		
		#show_recent_adopt(grids_of_adj_and_grid)
		
		grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list = grids_of_adj_and_grid_without_personal_and_with_same_institution_list+grids_of_adj_and_grid_without_personal_and_institution_conflict_list
		grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new = []
		for lattice in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list:
			if lattice not in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new:
				grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new.append(lattice)

		for lattice in lattice_list:
			if lattice in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new:
				lattice.adopt.append(True)
			else:
				lattice.adopt.append(False)
		
		#show_recent_adopt(grids_of_adj_and_grid)
		
		for lattice in lattice_list:
			if lattice in grids_of_adj_and_grid_without_personal_and_institution_conflict_list:
				lattice.adopt.append(True)
			else:
				lattice.adopt.append(False)
		else:
			for lattice in lattice_list:
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
				if list(conflicting_insti1 | conflicting_insti2):
					lattice.conflict = True
				if lattice.grid.teams[0].team_name in lattice.chair.conflict_teams or lattice.grid.teams[1].team_name in lattice.chair.conflict_teams:
					lattice.personal_conflict = True

			grids_of_adj_and_grid_without_personal_conflict_list = [lattice for lattice in lattice_list if not(lattice.personal_conflict)]
			grids_of_adj_and_grid_without_personal_and_institution_conflict_list = [lattice for lattice in lattice_list if not(lattice.personal_conflict) and not(lattice.conflict)]
			grids_of_adj_and_grid_without_personal_and_with_same_institution_list = [lattice for lattice in lattice_list if (not(lattice.personal_conflict) and lattice.conflict and list(conflicting_insti1&conflicting_insti2))]

			for lattice in lattice_list:
				if lattice in grids_of_adj_and_grid_without_personal_conflict_list:
					lattice.adopt.append(True)
				else:
					lattice.adopt.append(False)
			
			#show_recent_adopt(grids_of_adj_and_grid)
			
			grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list = grids_of_adj_and_grid_without_personal_and_with_same_institution_list+grids_of_adj_and_grid_without_personal_and_institution_conflict_list
			grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new = []
			for lattice in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list:
				if lattice not in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new:
					grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new.append(lattice)

			for lattice in lattice_list:
				if lattice in grids_of_adj_and_grid_without_personal_and_with_same_institution_and_without_conflict_list_new:
					lattice.adopt.append(True)
				else:
					lattice.adopt.append(False)
			
			#show_recent_adopt(grids_of_adj_and_grid)
			
			for lattice in lattice_list:
				if lattice in grids_of_adj_and_grid_without_personal_and_institution_conflict_list:
					lattice.adopt.append(True)
				else:
					lattice.adopt.append(False)
			
			#show_recent_adopt(grids_of_adj_and_grid)
			
		"""
		#lattice_check_conflict(lattice_list)
	else:
		for lattice in lattice_list:
			team_names = [team.name for team in lattice.grid.teams]
			if list(set(team_names) & set(lattice.chair.conflict_teams)):#personal conflict
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
			else:#not personal conflict
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				conflicting_insti1 = set(lattice.grid.teams[0].institutions) & set(lattice.chair.institutions)
				conflicting_insti2 = set(lattice.grid.teams[1].institutions) & set(lattice.chair.institutions)
				conflicting_insti3 = set(lattice.grid.teams[2].institutions) & set(lattice.chair.institutions)
				conflicting_insti4 = set(lattice.grid.teams[3].institutions) & set(lattice.chair.institutions)
				if list(conflicting_insti1 | conflicting_insti2 | conflicting_insti3 | conflicting_insti4):#conflict
					if list(conflicting_insti1 & conflicting_insti2 & conflicting_insti3 & conflicting_insti4):
						lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
						lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					else:
						lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
						lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
				else:#no conflict
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)

def prevent_unfair_adjudicators(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	lattice_list_cp = copy.copy(lattice_list)
	lattice_list_cp.sort(key=lambda lattice: lattice.chair.active_num)
	
	max_active_num = 0
	for adjudicator in adjudicator_list:
		if adjudicator.active_num > max_active_num:
			max_active_num = adjudicator.active_num
	
	unfair_lattice_num = 0
	for lattice in lattice_list:
		if lattice.chair.active_num < max_active_num:
			unfair_lattice_num+=1 

	#lattice_list_cp2 = [lattice for lattice in lattice_list_cp if lattice.chair.active_num < max_active_num]

	#print [lattice.chair.active_num for lattice in lattice_list]
	
	#all_len = len(lattice_list)

	for i, lattice in enumerate(lattice_list_cp):
		if i < unfair_lattice_num:
			if i < int(unfair_lattice_num/2):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
		else:
			break

	relatively_fair_lattice_list = lattice_list_cp[unfair_lattice_num:]
	relatively_fair_lattice_list.sort(key=lambda lattice: lattice.chair.evaluation)
	for j, lattice in enumerate(relatively_fair_lattice_list):
		if j < unfair_lattice_num:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
		else:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)

		"""


		for k, lattice in enumerate(lattice_list_cp):
			if k < int(0.60*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
			if k < int(0.20*all_len+4):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
		
		"""
		"""

		for k, lattice in enumerate(lattice_list_cp):
			if lattice.chair.active_num < max_active_num:
				if k < int(0.60*all_len+3):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
			if lattice.chair.active_num < max_active_num-1:
				if k < int(0.60*all_len+3):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			if lattice.chair.active_num < max_active_num-2:
				if k < int(0.60*all_len+3):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
		"""

def rotation_allocation(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	lattice_list_cp = copy.copy(lattice_list)
	lattice_list_cp.sort(key=lambda lattice: lattice.chair.active_num_as_chair)

	all_active_num_as_chair_list = [lattice.chair.active_num_as_chair for lattice in lattice_list]
	all_active_num_as_chair_list.sort()
	max_active_num_as_chair = all_active_num_as_chair_list[-1]
	min_active_num_as_chair = all_active_num_as_chair_list[0]

	if max_active_num_as_chair == min_active_num_as_chair:
		for lattice in lattice_list_cp:
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
	else:
		all_len = len(lattice_list)
		for k, lattice in enumerate(lattice_list_cp):
			if lattice.chair.active_num_as_chair == max_active_num_as_chair:
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			else:
				if k < int(0.60*all_len+3):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				if k < int(0.40*all_len+3):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
					lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
				if k < int(0.20*all_len+4):
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				else:
					lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)

	if max_active_num_as_chair == min_active_num_as_chair:
		for lattice in lattice_list_cp:
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
	elif max_active_num_as_chair == min_active_num_as_chair + 1:
		for lattice in lattice_list_cp:
			if lattice.chair.active_num == max_active_num_as_chair:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			else:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
	else:
		for lattice in lattice_list_cp:
			if lattice.chair.active_num == max_active_num_as_chair:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			elif lattice.chair.active_num == max_active_num_as_chair - 1:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			elif lattice.chair.active_num < max_active_num_as_chair - 1:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)

def avoid_watched_teams(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	lattice_list_cp = copy.copy(lattice_list)
	lattice_list_cp.sort(key=lambda lattice: seen_num(lattice), reverse = True)
	all_len = len(lattice_list)
	for k, lattice in enumerate(lattice_list_cp):
		if seen_num(lattice) == 0:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
		else:
			if k < int(0.2*all_len+4):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			if k < int(0.4*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			if k < int(0.6*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)

			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)

		#lattice_check_same_round(lattice_list)

def add_bubble(selected_grid_list, may_be_breaking_wins):	
	if len(selected_grid_list[0].teams) == 2:
		for grid in selected_grid_list:
			team1_win = sum(grid.teams[0].wins)
			team2_win = sum(grid.teams[1].wins)
			wins = set([team1_win, team2_win])
			if wins == set([may_be_breaking_wins-1, may_be_breaking_wins-1]):
				grid.bubble = 1
			elif wins == set([may_be_breaking_wins, may_be_breaking_wins-1]):
				grid.bubble = 2
			elif wins == set([may_be_breaking_wins, may_be_breaking_wins]):
				grid.bubble = 3
			elif wins == set([may_be_breaking_wins-2, may_be_breaking_wins-1]):
				grid.bubble = 4
			elif wins == set([may_be_breaking_wins-2, may_be_breaking_wins]):
				grid.bubble = 5
			elif wins == set([may_be_breaking_wins-2, may_be_breaking_wins-2]):
				grid.bubble = 6
			else:
				grid.bubble = 7
	else:
		for grid in selected_grid_list:
			team1_win = sum(grid.teams[0].wins)
			team2_win = sum(grid.teams[1].wins)
			team3_win = sum(grid.teams[2].wins)
			team4_win = sum(grid.teams[3].wins)
			wins = set([team1_win, team2_win, team3_win, team4_win])
			if may_be_breaking_wins-1 in wins:
				grid.bubble = 1
			elif may_be_breaking_wins-2 in wins:
				grid.bubble = 2
			elif may_be_breaking_wins-3 in wins:
				grid.bubble = 3
			elif may_be_breaking_wins in wins:
				grid.bubble = 4
			else:
				grid.bubble = 5

def prioritize_bubble_round(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	if len(lattice_list[0].grid.teams) == 2:
		available_team_num = 0
		for team in team_list:
			if team.available:
				available_team_num += 1
		wins_distribution = [sum(team.wins) for team in team_list if team.available]

		expected_wins_distribution = next_wins_distribution(wins_distribution, 2)

		may_be_breaking_wins = expected_wins_distribution[break_team_num-1]

		add_bubble(selected_grid_list, may_be_breaking_wins)

		selected_grid_list_cp = copy.copy(selected_grid_list)
		selected_grid_list_cp.sort(key=lambda grid: grid.bubble)
		for k, grid in enumerate(selected_grid_list_cp):
			grid.bubble_ranking += k+1

		lattice_list_cp = copy.copy(lattice_list)
		lattice_list_cp.sort(key=lambda lattice: abs(lattice.chair.ranking-lattice.grid.bubble_ranking))

		all_len = len(lattice_list_cp)

		for k, lattice in enumerate(lattice_list_cp):
			if k < int(0.60*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			if k < int(0.20*all_len+4):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)

			if lattice.grid.bubble < 4:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			elif lattice.grid.bubble < 7:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			else:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
		"""
		may_be_breaking_wins = 0
		team_list_cp = copy.copy(team_list)
		team_list_cp.sort(key=lambda team: team.ranking)
		may_be_breaking_wins = team_list_cp[break_team_num-1].wins.count(True)
		for team in team_list:
			if team.wins.count(True) == may_be_breaking_wins:
				team.bubble = 1
			elif team.wins.count(True) == may_be_breaking_wins - 1 or team.wins.count(True) == may_be_breaking_wins + 1:
				team.bubble = 2
			else:
				team.bubble = 4
		
		selected_grid_list_cp = copy.copy(selected_grid_list)
		selected_grid_list_cp.sort(key=lambda grid: (grid.teams[0].bubble + grid.teams[1].bubble, grid.teams[0].ranking+grid.teams[1].ranking))
		for k, grid in enumerate(selected_grid_list_cp):
			grid.bubble_ranking = k

		lattice_list_cp = copy.copy(lattice_list)
		lattice_list_cp.sort(key=lambda lattice: abs(lattice.chair.ranking - lattice.grid.bubble_ranking))

		all_len = len(lattice_list)
		for k, lattice in enumerate(lattice_list_cp):
			if k < int(0.60*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			if k < int(0.20*all_len+4):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)

		#lattice_check_bubble_round(lattice_list)
		"""
	else:
		available_team_num = 0
		for team in team_list:
			if team.available:
				available_team_num += 1
		wins_distribution = [sum(team.wins) for team in team_list if team.available]

		expected_wins_distribution = next_wins_distribution(wins_distribution, 4)

		may_be_breaking_wins = expected_wins_distribution[break_team_num-1]

		add_bubble(selected_grid_list, may_be_breaking_wins)

		selected_grid_list_cp = copy.copy(selected_grid_list)
		selected_grid_list_cp.sort(key=lambda grid: grid.bubble)
		for k, grid in enumerate(selected_grid_list_cp):
			grid.bubble_ranking += k+1

		lattice_list_cp = copy.copy(lattice_list)
		lattice_list_cp.sort(key=lambda lattice: abs(lattice.chair.ranking-lattice.grid.bubble_ranking))

		all_len = len(lattice_list_cp)

		for k, lattice in enumerate(lattice_list_cp):
			if k < int(0.60*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			if k < int(0.40*all_len+3):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			if k < int(0.20*all_len+4):
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
			else:
				lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
				lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)

			if lattice.grid.bubble < 4:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			elif lattice.grid.bubble == 4:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			else:
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
				lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)

def random_allocation(round_num, adjudicator_list, selected_grid_list, team_list, lattice_list, break_team_num, shift):
	lattice_list_cp = copy.copy(lattice_list)
	random.shuffle(lattice_list_cp)

	for k, lattice in enumerate(lattice_list_cp):
		if k < int(len(lattice_list_cp)*0.3):
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 1, shift*3+2)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 1, shift)
		else:
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbitslong = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+1)
			lattice.adoptbits_strict = bitshiftadd(lattice.adoptbitslong, 0, shift*3+2)
			lattice.adoptbits = bitshiftadd(lattice.adoptbits, 0, shift)



pass