# -*- coding: utf-8 -*-
#from internal_modules import *
#from io_modules_for_bp import *

def select_alg3_high(grid_list, team_list):
	selected_square_list = []

	square_lists_by_team = []

	square_list = grid_list2square_list(grid_list)
	#print square_list

	for team in team_list:
		square_lists_by_team.append([square for square in square_list if is_in_square(team.code, square)])

	#print square_lists_by_team
	square_lists_by_team.sort(key=lambda square_list: min_square_comparison1(square_list))
	for square_list_by_team in square_lists_by_team:
		square_list_by_team.sort(key=lambda square: (comparison1_from_square(square), comparison2_from_square(square)), reverse=True)
		for square in square_list_by_team:
			if square_available(square):
				selected_square_list.append(square)
				disavail_squares(square_list, square)
				break

	selected_grid_list = [square2grid(square, grid_list) for square in selected_square_list]
	"""
	for grid in selected_grid_list:
		disavail_grids(grid_list, grid)

	while len_available(grid_list):#complete selected grids list
		grid = select_grid2(grid_list)
		selected_grid_list.append(grid)
		disavail_grids(grid_list, grid)

	refresh_grids_for_adopt(grid_list)
	#print selected_grid_list
	"""

	return selected_grid_list

def is_in(name, teams):
	if name == teams[0].name:
		return True
	elif name == teams[1].name:
		return True
	elif name == teams[2].name:
		return True
	elif name == teams[3].name:
		return True
	else:
		return False

def is_in_square(code, square):
	if code == team_code_from_square(square, 0):
		return True
	elif code == team_code_from_square(square, 1):
		return True
	elif code == team_code_from_square(square, 2):
		return True
	elif code == team_code_from_square(square, 3):
		return True
	else:
		return False

def ret_grid_list_teams(grid_list, grid, num):
	return [grid2 for grid2 in grid_list if grid2.teams[num].name == grid.teams[num].name]

def grid_list2square_list(grid_list):
	#def unsigned long square[2]
	square_list = []
	for grid in grid_list:
		square = [0, 0]
		square[0] = (grid.comparison1 << 1) + (grid.comparison2 << 6) + (grid.teams[0].code << 11) + (grid.teams[1].code << 21)
		square[1] = (grid.teams[2].code) + (grid.teams[3].code << 10)
		if grid.available:
			square[0] += 1
		square_list.append(square)

	#print square_list
	return square_list

def square2grid(square, grid_list):
	team_codes = [team_code_from_square(square, 0), team_code_from_square(square, 1), team_code_from_square(square, 2), team_code_from_square(square, 3)]
	for grid in grid_list:
		if grid.teams[0].code == team_codes[0] or grid.teams[1].code == team_codes[2] or grid.teams[2].code == team_codes[2] or grid.teams[3].code == team_codes[3]:
			return grid

def team_code_from_square(square, x):
	if x == 0:
		return (square[0] >> 11)&(0b1111111111)
	elif x == 1:
		return (square[0] >> 21)&(0b1111111111)
	elif x == 2:
		return (square[1]&0b1111111111)
	elif x == 3:
		return (square[1] >> 10)&(0b1111111111)

def comparison1_from_square(square):
	return (square[0] >> (1))&(0b11111)

def comparison2_from_square(square):
	return (square[0] >> (6))&(0b11111)

def square_available(square):
	if square[0]&1 == 1:
		return True
	else:
		return False

def ret_same_team_code_square_list(square_list, code):
	return [square for square in square_list if (code == team_code_from_square(square, 0) or code == team_code_from_square(square, 1) or code == team_code_from_square(square, 2) or code == team_code_from_square(square, 2))]

def min_square_comparison1(square_list):
	min_square = min(square_list, key=lambda square: comparison1_from_square(square))
	return comparison1_from_square(min_square)

def disavail_squares(square_list, square):
	square_team0_code = team_code_from_square(square, 0)
	square_team1_code = team_code_from_square(square, 1)
	square_team2_code = team_code_from_square(square, 2)
	square_team3_code = team_code_from_square(square, 3)
	for square2 in square_list:
		if team_code_from_square(square2, 0) == square_team0_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 0) == square_team1_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 0) == square_team2_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 0) == square_team3_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 1) == square_team0_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 1) == square_team1_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 1) == square_team2_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 1) == square_team3_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 2) == square_team0_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 2) == square_team1_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 2) == square_team2_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 2) == square_team3_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 3) == square_team0_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 3) == square_team1_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 3) == square_team2_code:
			square2[0] = (square2[0] >> 1)<<1
		elif team_code_from_square(square2, 3) == square_team3_code:
			square2[0] = (square2[0] >> 1)<<1

"""
def same(a, b):
	if (a^b) == 0:
		return True
	else:
		return False
"""
"""
print same(0b1111, 0b1111)
"""
"""
team_list = read_teams('../dat/teams.csv')
grid_list = create_grid_list(team_list, False)

square_list = grid_list2square_list(grid_list)
print

print [team.code for team in grid_list[2].teams]
print square_list[2]
print team_code_from_square(square_list[2], 0)
print team_code_from_square(square_list[2], 1)
print team_code_from_square(square_list[2], 2)
print team_code_from_square(square_list[2], 3)
#print same(team_code_from_square(square_list[2], 0), team_code_from_square(square_list[3], 0))
#print same(team_code_from_square(square_list[2], 0), team_code_from_square(square_list[2], 1))
print "a"
for team in team_list:
	same_team_code_square_list = ret_same_team_code_square_list(square_list, team.code)
print "b"

selected_square_list = []
for square in square_list:
	if square_available(square):
		selected_square_list.append(square)
		disavail_squares(square_list, square)
	if len(selected_square_list) == len(team_list)/4:
		break
print "c"
print selected_square_list

print comparison1_from_square(square_list[0])
print comparison2_from_square(square_list[0])
"""
