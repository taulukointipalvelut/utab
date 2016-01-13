# -*- coding: utf-8 -*-
import math
import itertools

def perm(n, r):
	return math.factorial(n)/math.factorial(n-r)

def calc_scatter_indicator(grid_list):
	institutions = []
	for grid in grid_list:
		for team in grid.teams:
			institutions += team.institutions
	institutions = list(set(institutions))
	institutions_by_institutions = []
	for institution in institutions:
		institutions_by_institution = []
		for grid in grid_list:
			for team in grid.teams:
				if institution in team.institutions:#if the team insti == insti
					for team2 in grid.teams:
						if team2 != team:
							institutions_by_institution.extend(team2.institutions)

		institutions_by_institutions.append(list(set(institutions_by_institution)))

	institutions_by_institutions = [flatten for inner in institutions_by_institutions for flatten in inner]
	return len(institutions_by_institutions)/float(len(institutions))

def calc_power_pairing_indicator(grid_list, teamnum):
	"""
	if False:#len(grid_list[0].teams) == 2:
		power_pairing_indicator = 0
		for grid in grid_list:
			power_pairing_indicator += (grid.teams[0].ranking - grid.teams[1].ranking)**2
		power_pairing_indicator /= float(len(grid_list))
		power_pairing_indicator = math.sqrt(power_pairing_indicator)
		return power_pairing_indicator
	else:
	"""
	power_pairing_indicator = 0
	for grid in grid_list:
		grid_average = sum([team.ranking for team in grid.teams])/float(len(grid.teams))
		for team in grid.teams:
			power_pairing_indicator += (team.ranking - grid_average)**2
	power_pairing_indicator /= float(len(grid_list)*teamnum)
	power_pairing_indicator = math.sqrt(power_pairing_indicator)
	return power_pairing_indicator

def calc_same_institution_indicator(grid_list):
	insti_indi = 0
	for grid in grid_list:
		institutions = []
		for team_pair in itertools.combinations(grid.teams, 2):
			institutions.extend(list(set(team_pair[0].institutions) & set(team_pair[1].institutions)))
		if len(institutions) != 0:
			insti_indi += len(institutions)
	return float(insti_indi)/len(grid_list)*100

def calc_adopt_indicator(grid_list):
	adopt_sum = 0
	for grid in grid_list:
		adopt_sum += grid.adoptness1
	mean = adopt_sum/float(len(grid_list))

	S = 0
	for grid in grid_list:
		S += (grid.adoptness1-mean)**2
	sd = S/float(len(grid_list))

	adopt_sum2 = 0

	for grid in grid_list:
		adopt_sum2 += grid.adoptness2

	return adopt_sum, sd, adopt_sum2

def calc_adoptlong_indicator(grid_list):
	adopt_sum = 0
	for grid in grid_list:
		adopt_sum += grid.adoptness1long
	mean = adopt_sum/float(len(grid_list))

	S = 0
	for grid in grid_list:
		S += (grid.adoptness1long-mean)**2
	sd = S/float(len(grid_list))

	adopt_sum2 = 0

	for grid in grid_list:
		adopt_sum2 += grid.adoptness2long

	return adopt_sum, sd, adopt_sum2

def calc_num_of_warnings(grid_list):
	num_of_warnings = 0
	for grid in grid_list:
		num_of_warnings += len(grid.warnings)
	return num_of_warnings


def is_one_halfed(team, position):#0->fair, 1->many govs, -1->many opps, 2->many openings, -2->many closings
	side = 0
	half = 0

	gov_num = 0
	opp_num = 0
	if position == "og" or position == "cg":
		gov_num = team.past_sides.count("og")+team.past_sides.count("cg")+1
		opp_num = team.past_sides.count("oo")+team.past_sides.count("co")
	else:
		gov_num = team.past_sides.count("og")+team.past_sides.count("cg")
		opp_num = team.past_sides.count("oo")+team.past_sides.count("co")+1
	if abs(gov_num - opp_num) <= 1:
		side = 0
	elif gov_num - opp_num > 1:
		side = 1
	else:
		side = -1

	opening_num = 0
	closing_num = 0
	if position == "og" or position == "oo":
		opening_num = team.past_sides.count("og")+team.past_sides.count("oo")+1
		closing_num = team.past_sides.count("cg")+team.past_sides.count("co")
	else:
		opening_num = team.past_sides.count("og")+team.past_sides.count("oo")
		closing_num = team.past_sides.count("cg")+team.past_sides.count("co")+1

	if abs(opening_num - closing_num) <= 1:
		half = 0
	elif opening_num - closing_num > 1:
		half = 2
	else:
		half = -2

	if half == 0:
		return side
	else:
		return half

def is_one_sided(team, position, teamnum):#0->fair, 1->many govs, -1->many opps
	if teamnum == 4:
		sides = ["og", "oo", "cg", "co"]
	elif teamnum == 2:
		sides = ["gov", "opp"]
	position_dict = {side:team.past_sides.count(side) for side in sides}
	position_dict[position] += 1

	nums = list(position_dict.values())

	if position_dict[position]-min(nums) > 1:
		return 1
	else:
		return 0
	"""
	if teamnum == 2:
		if (1+len(team.past_sides))%2 == 0:
			gov_num = 0
			opp_num = 0
			if position == "gov":
				gov_num = team.past_sides.count("gov")+1
				opp_num = team.past_sides.count("opp")
			else:
				gov_num = team.past_sides.count("gov")
				opp_num = team.past_sides.count("opp")+1

			if gov_num - opp_num == 0:
				return 0
			elif gov_num - opp_num > 0:
				return 1
			else:
				return -1
		else:
			gov_num = 0
			opp_num = 0
			if position == "gov":
				gov_num = team.past_sides.count("gov")+1
				opp_num = team.past_sides.count("opp")
			else:
				gov_num = team.past_sides.count("gov")
				opp_num = team.past_sides.count("opp")+1
			if abs(gov_num - opp_num) <= 1:
				return 0
			elif gov_num - opp_num > 1:
				return 1
			else:
				return -1
	else:
		#if (1+len(team.past_sides))%2 == 0:
		position_dict = {}
		if position == "og":
			position_dict["og"] = team.past_sides.count("og")+1
			position_dict["oo"] = team.past_sides.count("oo")
			position_dict["cg"] = team.past_sides.count("cg")
			position_dict["co"] = team.past_sides.count("co")
		elif position == "oo":
			position_dict["og"] = team.past_sides.count("og")
			position_dict["oo"] = team.past_sides.count("oo")+1
			position_dict["cg"] = team.past_sides.count("cg")
			position_dict["co"] = team.past_sides.count("co")
		elif position == "cg":
			position_dict["og"] = team.past_sides.count("og")
			position_dict["oo"] = team.past_sides.count("oo")
			position_dict["cg"] = team.past_sides.count("cg")+1
			position_dict["co"] = team.past_sides.count("co")
		elif position == "co":
			position_dict["og"] = team.past_sides.count("og")
			position_dict["oo"] = team.past_sides.count("oo")
			position_dict["cg"] = team.past_sides.count("cg")
			position_dict["co"] = team.past_sides.count("co")+1

		nums = position_dict.values()

		if position_dict[position]-min(nums) > 1:
			return 1
		else:
			return 0
	"""

def calc_str_str_indicator(selected_lattice_list, teamnum):
	str_str_indicator = 0
	for lattice in selected_lattice_list:
		str_str_indicator += (sum([team.ranking for team in lattice.grid.teams])/float(teamnum) - lattice.chair.ranking)**2
	str_str_indicator /= float(len(selected_lattice_list))
	str_str_indicator = math.sqrt(str_str_indicator)
	return str_str_indicator

def calc_deleting_effect(grid_list, grid_deleting):
	comparison_list_by_grid = [grid.comparison1 for grid in grid_list if (list(set(grid.teams)&set(grid_deleting.teams))) != [] and grid.available]
	return sum(comparison_list_by_grid)-grid_deleting.comparison1

def calc_deleting_effect_adj(lattice_list, lattice_deleting):
	comparison_list_by_lattice = [lattice.comparison1 for lattice in lattice_list if ((lattice.grid == lattice_deleting.grid or lattice.chair == lattice_deleting.chair) and not(lattice.chair.active))]

	return sum(comparison_list_by_lattice)-lattice_deleting.comparison1

def min_grid_comparison1(grid_list):
	min_grid = min(grid_list, key=lambda grid: grid.comparison1)
	return min_grid.comparison1

def len_available(listing):
	c = 0
	for obj in listing:
		if obj.available:
			c += 1

	return c

def len_available_grids(lattice_list):
	c = 0
	for lattice in lattice_list:
		if lattice.available:
			c += 1

	return c
	
def return_lattice_average_ranking(lattice):
	rankings = [team.ranking for team in lattice.grid.teams]
	return sum(rankings)/float(len(rankings))

def seen_num(lattice):
	seen_num = 0
	for team in lattice.grid.teams:
		seen_num += lattice.chair.watched_teams.count(team)
	return seen_num

def next_wins_distribution(wins_distribution, teamnum):
	wins_distribution2 = []
	for i in range(100):
		weight_init = int(wins_distribution.count(i)/teamnum)
		weight_last = wins_distribution.count(i)-(teamnum-1)*int(wins_distribution.count(i)/teamnum)
		for j in range(teamnum-1):
			wins_distribution2 += [i+j]*weight_init
		wins_distribution2 += [i+teamnum-1]*weight_last
	#print wins_distribution2
	wins_distribution2.sort(reverse=True)
	return wins_distribution2

def ret_wei(num, nums, division_num):
	index = nums.index(num)
	all_len = len(nums)
	return int(division_num*index/all_len)



pass
