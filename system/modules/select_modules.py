# -*- coding: utf-8 -*-
from .property_modules import *
from .quick_modules import *
from . import interaction_modules
import copy
import random

def disavail_grids(grid_list, grid1, pid):
	"""
	for grid2 in grid_list:
		if grid1.related(grid2):
			grid2.set_not_available(pid)
	"""
	if grid1.grid_type() == "Grid":
		teams_names = [team.name for team in grid1.teams]
		for grid2 in grid_list:
			for team2 in grid2.teams:
				if team2.name in teams_names:
					grid2.set_not_available(pid)
					break

		"""
		if len(grid_list[0].teams) == 2:
			for grid2 in grid_list:
				if grid2.teams[0] == grid1.teams[0]:
					grid2.available = False
				elif grid2.teams[1] == grid1.teams[0]:
					grid2.available = False
				elif grid2.teams[0] == grid1.teams[1]:
					grid2.available = False
				elif grid2.teams[1] == grid1.teams[1]:
					grid2.available = False
		else:
			teams_names = [team.name for team in grid1.teams]
			for grid2 in grid_list:
				if grid2.teams[0].name in teams_names:
					grid2.available = False
				elif grid2.teams[1].name in teams_names:
					grid2.available = False
				elif grid2.teams[2].name in teams_names:
					grid2.available = False
				elif grid2.teams[3].name in teams_names:
					grid2.available = False
		"""
		"""
		for grid2 in grid_list:
			if grid2.teams[0] in grid1.teams:
				grid2.available = False
			elif grid2.teams[1] in grid1.teams:
				grid2.available = False
			elif grid2.teams[2] in grid1.teams:
				grid2.available = False
			elif grid2.teams[3] in grid1.teams:
				grid2.available = False
		"""

				#if set(grid2.teams) & set(grid1.teams):
				#	grid2.available = False

	elif grid1.grid_type() == "Lattice":
		#c = 0
		for grid2 in grid_list:
			if grid2.chair == grid1.chair:
				#c += 1
				grid2.set_not_available(pid)
			elif grid2.grid == grid1.grid:
				grid2.set_not_available(pid)
		#		c += 1
		#interaction_modules.warn(str(c))
		#gridss = [grid.grid for grid in grid_list]
		#print [[grid.teams[0].name, grid.teams[1].name] for grid in gridss]
		#show_lattice_list(grid_list)

def select_lattice2(lattice_list, cp_pair, pid):
	#interaction_modules.warn("called"+str(pid))
	lattice = find_min_grid(lattice_list, cp_pair, pid)
	lattice_list_adjs = [lattice2 for lattice2 in lattice_list if lattice2.grid == lattice.grid]
	lattice_list_grids = [lattice1 for lattice1 in lattice_list if lattice1.chair == lattice.chair]
	max_in_row, grid_row = find_max_grid(lattice_list_adjs, cp_pair, pid)
	max_in_column, grid_column = find_max_grid(lattice_list_grids, cp_pair, pid)

	if max_in_column > max_in_row:
		return grid_column
	else:
		return grid_row

def select_grid2(grid_list, team_list, cp_pair, pid):#####????work well????
	grid = find_min_grid(grid_list, cp_pair, pid)
	grid_list_teams_list = []
	for k, team in enumerate(grid.teams):
		grid_list_teams = []
		for grid2 in grid_list:
			if grid2.teams[k] == team:
				grid_list_teams.append(grid2)
		grid_list_teams_list.append(grid_list_teams)

	max_in_xs_list = []
	grid_xs_list = []
	for grid_list_teams in grid_list_teams_list:
		max_in_xs, grid_xs = find_max_grid(grid_list_teams, cp_pair, pid)
		max_in_xs_list.append(max_in_xs)
		grid_xs_list.append(grid_xs)

	teams_dict = {str(i)+"s": max_in_xs for i, max_in_xs in enumerate(max_in_xs_list)}
	grid_dict = {str(i)+"s": grid_xs for i, grid_xs in enumerate(grid_xs_list)}
	teams_dict_sorted = sorted(list(teams_dict.items()), key=lambda x:x[1], reverse=True)

	return grid_dict[teams_dict_sorted[0][0]]

def find_min_grid(grid_list, cp_pair, pid):
	#return min(grid_list, key=lambda grid: (grid.comparison1, grid.comparison2))
	
	grid_list = copy.copy(grid_list)
	grid_list.sort(key=lambda grid: ((cp_pair[0](grid), cp_pair[1](grid))))
	for grid in grid_list:
		if grid.get_available(pid):
			return grid

def find_max_grid(grid_list_teamxs, cp_pair, pid):
	#print(cp_pair)
	#print()
	#print(len(grid_list_teamxs))
	#print()
	grid_list = copy.copy(grid_list_teamxs)
	grid_list.sort(key=lambda grid: ((cp_pair[0](grid), cp_pair[1](grid))), reverse=True)
	for grid in grid_list:
		if grid.get_available(pid):
			return grid.comparison1, grid

def refresh_grids_for_adopt(grid_list, *args):
	if grid_list:
		if grid_list[0].grid_type() == "Grid":
			for grid in grid_list:
				if True in [not(team.available) for team in grid.teams]:
					grid.set_not_available(*args)
				#elif len(list(set(grid.teams))) != len(grid.teams):
				#	grid.available = True
				else:
					grid.set_available(*args)

		elif grid_list[0].grid_type() == "Lattice":
			#interaction_modules.warn(str(len([grid for grid in grid_list if grid.get_available(*args)])))
			for grid in grid_list:
				if True in ([not(team.available) for team in grid.grid.teams]+[grid.chair.absent]):
					grid.set_not_available(*args)
				#elif len(list(set(grid.teams))) != len(grid.teams):
				#	grid.available = True
				else:
					grid.set_available(*args)
			#interaction_modules.warn(str(len([grid for grid in grid_list if grid.get_available(*args)])))

def select_alg2(pid, grid_list, round_num, team_list, cp_pair):#!!#picking up from the highly desired
	selected_grid_list = []
	available_team_num = 0
	for team in team_list:
		if team.available: available_team_num+=1
	expected_grid_num = int(available_team_num/len(grid_list[0].teams))

	grid_list.sort(key=lambda grid: cp_pair[0](grid), reverse=True)
	for grid in grid_list:
		if grid.get_available(pid):
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)
		if len(selected_grid_list) == expected_grid_num:
			break

	while len_available(grid_list, pid):#complete selected grids list""
		grid = select_grid2(grid_list, team_list, cp_pair, pid)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid, pid)

	refresh_grids_for_adopt(grid_list, pid)
	
	#print selected_grid_list
	return selected_grid_list

def select_alg3(pid, grid_list, round_num, team_list, cp_pair):#picking up by disavailing the worse ones(by team)
	selected_grid_list = []

	##############bottle neck
	grid_lists_by_team = []
	for team in team_list:
		grid_list_by_team = [grid for grid in grid_list if team in grid.teams]
		grid_list_by_team = list(set(grid_list_by_team))
		grid_lists_by_team.append(grid_list_by_team)

	grid_lists_by_team.sort(key=lambda grid_list: min_grid_comparison1(grid_list))
	for grid_list_by_team in grid_lists_by_team:
		grid_list_by_team.sort(key=lambda grid: (cp_pair[0](grid), cp_pair[1](grid)), reverse=True)
		for grid in grid_list_by_team:
			if grid.get_available(pid):
				selected_grid_list.append(grid)
				disavail_grids(grid_list, grid, pid)
				break

	while len_available(grid_list, pid):#complete selected grids list
		grid = select_grid2(grid_list, team_list, cp_pair, pid)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid, pid)

	refresh_grids_for_adopt(grid_list, pid)
	#print selected_grid_list
	return selected_grid_list

def select_alg4(pid, grid_list, round_num, team_list, cp_pair):#picking up by disavailing the worse ones(by row/column)
	if len(grid_list[0].teams) == 2:
		selected_grid_list = []

		while len_available(grid_list, pid) > 0:
			grid = find_min_grid(grid_list, cp_pair, pid)

			if grid is None:
				break
			grid = find_min_grid(grid_list, cp_pair, pid)
			grid_list_team2s = [grid1 for grid1 in grid_list if grid1.teams[0].name == grid.teams[0].name]
			grid_list_team1s = [grid1 for grid1 in grid_list if grid1.teams[1].name == grid.teams[1].name]
			max_in_row, grid_row = find_max_grid(grid_list_team2s, cp_pair, pid)
			max_in_column, grid_column = find_max_grid(grid_list_team1s, cp_pair, pid)

			if grid_row is None: break
			if grid_column is None: break
			if max_in_column > max_in_row:
				selected_grid_list.append(grid_column)
				disavail_grids(grid_list, grid_column, pid)
			else:
				selected_grid_list.append(grid_row)
				disavail_grids(grid_list, grid_row, pid)

		while len_available(grid_list, pid):#complete selected grids list
			grid = select_grid2(grid_list, team_list, cp_pair, pid)
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)

		refresh_grids_for_adopt(grid_list, pid)
		#print selected_grid_list
		return selected_grid_list

	else:
		selected_grid_list = []

		while len_available(grid_list, pid) > 0:
			grid = find_min_grid(grid_list, cp_pair, pid)

			if grid is None:
				break
			#############bottleneck
			grid = find_min_grid(grid_list, cp_pair, pid)
			grid_list_team0s = ret_grid_list_teams(grid_list, grid, 0)
			grid_list_team1s = ret_grid_list_teams(grid_list, grid, 1)
			grid_list_team2s = ret_grid_list_teams(grid_list, grid, 2)
			grid_list_team3s = ret_grid_list_teams(grid_list, grid, 3)

			max_in_0s, grid_0s = find_max_grid(grid_list_team2s, cp_pair, pid)
			max_in_1s, grid_1s = find_max_grid(grid_list_team1s, cp_pair, pid)
			max_in_2s, grid_2s = find_max_grid(grid_list_team2s, cp_pair, pid)
			max_in_3s, grid_3s = find_max_grid(grid_list_team1s, cp_pair, pid)
			if grid_0s is None: break
			if grid_1s is None: break
			if grid_2s is None: break
			if grid_3s is None: break

			teams_dict = {"0s": max_in_0s, "1s": max_in_1s, "2s": max_in_2s, "3s": max_in_3s}
			teams_dict_sorted = sorted(list(teams_dict.items()), key=lambda x:x[1], reverse=True)

			if teams_dict_sorted[0][0] == "0s":
				selected_grid_list.append(grid_0s)
				disavail_grids(grid_list, grid_0s, pid)
			elif teams_dict_sorted[0][0] == "1s":
				selected_grid_list.append(grid_1s)
				disavail_grids(grid_list, grid_1s, pid)
			elif teams_dict_sorted[0][0] == "2s":
				selected_grid_list.append(grid_2s)
				disavail_grids(grid_list, grid_2s, pid)
			elif teams_dict_sorted[0][0] == "3s":
				selected_grid_list.append(grid_3s)
				disavail_grids(grid_list, grid_3s, pid)

		while len_available(grid_list, pid):#complete selected grids list
			grid = select_grid2(grid_list, team_list, cp_pair, pid)
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)

		refresh_grids_for_adopt(grid_list, pid)
		#print selected_grid_list
		return selected_grid_list
	

def select_alg11(pid, grid_list, round_num, team_list, cp_pair):#!!#picking up from the highly desired(2 criteria)
	selected_grid_list = []
	available_team_num = 0
	for team in team_list:
		if team.available: available_team_num+=1
	expected_grid_num = int(available_team_num/len(grid_list[0].teams))

	grid_list.sort(key=lambda grid: (cp_pair[0](grid), cp_pair[1](grid)), reverse=True)
	#print [grid.comparison2 for grid in grid_list]
	for grid in grid_list:
		if grid.get_available(pid):
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)
		if len(selected_grid_list) == expected_grid_num:
			break

	while len_available(grid_list, pid):#complete selected grids list
		grid = select_grid2(grid_list, team_list, cp_pair, pid)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid, pid)

	refresh_grids_for_adopt(grid_list, pid)
	#print selected_grid_list
	return selected_grid_list

def select_alg13(pid, grid_list, round_num, team_list, cp_pair):#!!#picking up harmless ones
	selected_grid_list = []
	available_team_num = 0
	for team in team_list:
		if team.available: available_team_num+=1
	expected_grid_num = int(available_team_num/len(grid_list[0].teams))

	grid_list.sort(key=lambda grid: (cp_pair[0](grid), -calc_deleting_effect(grid_list, grid, pid)), reverse=True)
	for grid in grid_list:
		if grid.get_available(pid):
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)
		if len(selected_grid_list) == expected_grid_num:
			break	

	while len_available(grid_list, pid):#complete selected grids list
		grid = select_grid2(grid_list, team_list, cp_pair, pid)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid, pid)

	refresh_grids_for_adopt(grid_list, pid)
	#print selected_grid_list
	return selected_grid_list

def select_alg14(pid, grid_list, round_num, team_list, cp_pair):#!!#picking up harmless ones(one criterion)
	selected_grid_list = []
	available_team_num = 0
	for team in team_list:
		if team.available: available_team_num+=1
	expected_grid_num = int(available_team_num/len(grid_list[0].teams))

	grid_list.sort(key=lambda grid: calc_deleting_effect(grid_list, grid, pid))
	for grid in grid_list:
		if grid.get_available(pid):
			selected_grid_list.append(grid)
			disavail_grids(grid_list, grid, pid)
		if len(selected_grid_list) == expected_grid_num:
			break

	while len_available(grid_list, pid):#complete selected grids list
		grid = select_grid2(grid_list, team_list, cp_pair, pid)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid, pid)

	refresh_grids_for_adopt(grid_list, pid)
	#print selected_grid_list
	return selected_grid_list

def select_alg_adj2(pid, lattice_list, round_num, team_list, cp_pair):#picking up from the highly desired
	selected_lattice_list = []

	lattice_list.sort(key=lambda lattice: cp_pair[1](lattice), reverse=True)
	for lattice in lattice_list:
		if lattice.get_available(pid):#####################################
			selected_lattice_list.append(lattice)
			disavail_grids(lattice_list, lattice, pid)
	
	while len_available(lattice_list, pid):#complete selected lattices list
		lattice = select_lattice2(lattice_list, cp_pair, pid)
		selected_lattice_list.append(lattice)
		disavail_grids(lattice_list, lattice, pid)
	
	refresh_grids_for_adopt(lattice_list, pid)
	
	return selected_lattice_list

def select_alg_adj11(pid, lattice_list, round_num, team_list, cp_pair):#picking up from the highly desired(2 criteria)
	selected_lattice_list = []

	lattice_list.sort(key=lambda lattice: (cp_pair[0](lattice), cp_pair[1](lattice)), reverse=True)
	for lattice in lattice_list:
		if lattice.get_available(pid):
			selected_lattice_list.append(lattice)
			disavail_grids(lattice_list, lattice, pid)

	while len_available(lattice_list, pid):#complete selected lattices list
		lattice = select_lattice2(lattice_list, cp_pair, pid)
		selected_lattice_list.append(lattice)
		disavail_grids(lattice_list, lattice, pid)

	refresh_grids_for_adopt(lattice_list, pid)
	
	return selected_lattice_list

def select_alg_adj13(pid, lattice_list, round_num, team_list, cp_pair):#picking up harmless ones
	selected_lattice_list = []

	#random.shuffle(lattice_list)
	lattice_list.sort(key=lambda lattice: (cp_pair[1](lattice), -calc_deleting_effect_adj(lattice_list, lattice, pid)), reverse=True)
	for lattice in lattice_list:
		if lattice.get_available(pid):
			selected_lattice_list.append(lattice)
			disavail_grids(lattice_list, lattice, pid)

	while len_available(lattice_list, pid):#complete selected lattices list
		lattice = select_lattice2(lattice_list, cp_pair, pid)
		selected_lattice_list.append(lattice)
		disavail_grids(lattice_list, lattice, pid)

	refresh_grids_for_adopt(lattice_list, pid)
	
	return selected_lattice_list

def select_alg_adj14(pid, lattice_list, round_num, team_list, cp_pair):#picking up harmless ones(one criterion)
	selected_lattice_list = []

	lattice_list.sort(key=lambda lattice: calc_deleting_effect_adj(lattice_list, lattice, pid))
	for lattice in lattice_list:
		if lattice.get_available(pid):
			selected_lattice_list.append(lattice)
			disavail_grids(lattice_list, lattice, pid)

	while len_available(lattice_list, pid):#complete selected lattices list
		lattice = select_lattice2(lattice_list, cp_pair, pid)
		selected_lattice_list.append(lattice)
		disavail_grids(lattice_list, lattice, pid)

	refresh_grids_for_adopt(lattice_list, pid)
	
	return selected_lattice_list


pass