# -*- coding: utf-8 -*-
import sys
import copy
from property_modules import *
from bit_modules import *
import time
import random
try:
	import readline
except:
	pass
	
def show_matchups_by_grid(grid_list_with_info_origin, round_num):
	if len(grid_list_with_info_origin[0][0].teams) == 2:
		grid_list_with_info = [copy.copy(grid_list_with_info_origin[0]), grid_list_with_info_origin[1]]
		grid_list_with_info[0].sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking)
		b_codes = ['93', '92', '96', '94', '97', '93', '92', '96', '94', '97', '93', '92', '96', '94', '97']
		print "---------------------------------matchups No." +str(grid_list_with_info[1].matchups_no)+ "-------------------------------------"
		#print "matchups for round:", round_num
		if round_num > 1: print "power pairing indicator: %.2f(the smaller, the better; min = 1)" % (grid_list_with_info[1].power_pairing_indicator)
		print "adopt indicator: %.2f (sd: %.2f, ot: %.2f) (the larger, the better; min = 0)" % (grid_list_with_info[1].adopt_indicator, grid_list_with_info[1].adopt_indicator_sd, grid_list_with_info[1].adopt_indicator2)
		#print "same institution indicator: %.2f(the smaller, the better; min = 0)" % (grid_list_with_info[1].same_institution_indicator)
		print "scattered institutions indicator: %.2f(the larger, the better; min = 1)" % (grid_list_with_info[1].scatter_indicator)
		print "number of warnings: %4d" % grid_list_with_info[1].num_of_warnings
		print "------------------------------------warnings----------------------------------------"
		for large_warning in grid_list_with_info[1].large_warnings:
			print large_warning
		print "------------------------------------matchups----------------------------------------"
		print "\033[33m             Gov     :     Opp     \033[0m"
		for grid in grid_list_with_info[0]:
			if is_one_sided(grid.teams[0], "gov", True) != 0:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';41m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+'m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
			if is_one_sided(grid.teams[1], "opp", True) != 0:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';41m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+'m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[1].institutions):
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[1].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'

			print text_1+" : "+text_2+" |",
			for warning in grid.warnings:
				warning += ","
				print '\033[31m'+warning+'\033[0m',
			print
	else:
		grid_list_with_info = [copy.copy(grid_list_with_info_origin[0]), grid_list_with_info_origin[1]]
		grid_list_with_info[0].sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking+grid.teams[2].ranking+grid.teams[3].ranking)
		b_codes = ['93', '92', '96', '94', '97', '93', '92', '96', '94', '97', '93', '92', '96', '94', '97']
		print "---------------------------------matchups No." +str(grid_list_with_info[1].matchups_no)+ "-------------------------------------"
		#print "matchups for round:", round_num
		if round_num > 1: print "power pairing indicator: %.2f(the smaller, the better; min = 1)" % (grid_list_with_info[1].power_pairing_indicator)
		print "adopt indicator: %.2f (sd: %.2f, ot: %.2f) (the larger, the better; min = 0)" % (grid_list_with_info[1].adopt_indicator, grid_list_with_info[1].adopt_indicator_sd, grid_list_with_info[1].adopt_indicator2)
		print "same institution indicator: %.2f(the smaller, the better; min = 0)" % (grid_list_with_info[1].same_institution_indicator)
		print "number of warnings: %4d" % grid_list_with_info[1].num_of_warnings
		print "------------------------------------warnings----------------------------------------"
		for large_warning in grid_list_with_info[1].large_warnings:
			print large_warning
		print "------------------------------------matchups----------------------------------------"
		print "\033[33m             Gov     :     Opp     \033[0m"
		print "---------------------------------------------"
		for grid in grid_list_with_info[0]:#0123: 0123, 456: 0123, 456, 789 #012,3: 012,345,6 /3+1
			wins = [sum(team.wins) for team in grid.teams]
			diff_wins = list(set(wins))
			division_num = min(5, len(wins))

			if is_one_sided(grid.teams[0], "og", False) != 0:
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';41m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+'m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
			if is_one_sided(grid.teams[1], "oo", False) != 0:
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';41m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+'m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			if is_one_sided(grid.teams[2], "cg", False) != 0:
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';41m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			else:
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+'m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			if is_one_sided(grid.teams[3], "co", False) != 0:
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';41m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			else:
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+'m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[1].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[2].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[3].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			if set(grid.teams[1].institutions) & set(grid.teams[2].institutions):
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			if set(grid.teams[1].institutions) & set(grid.teams[3].institutions):
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			if set(grid.teams[2].institutions) & set(grid.teams[3].institutions):
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			"""
			if grid.teams[0].name in grid.teams[1].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[2].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[3].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20s}".format(grid.teams[0].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			if grid.teams[1].name in grid.teams[2].past_opponents:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
			if grid.teams[1].name in grid.teams[3].past_opponents:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20s}".format(grid.teams[1].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			if grid.teams[2].name in grid.teams[3].past_opponents:
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20s}".format(grid.teams[2].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20s}".format(grid.teams[3].name)+'\033[0m'
			"""

			print text_1+" : "+text_2+" |"
			print text_3+" : "+text_4+" |",
			for warning in grid.warnings:
				warning += ","
				print "\033[31m"+warning+"\033[0m",
			print
			print "---------------------------------------------"

def show_matchups_by_lattice(selected_lattice_list_with_info_origin, round_num, constants_of_adj):
	if len(selected_lattice_list_with_info_origin[0][0].grid.teams) == 2:
		selected_lattice_list_with_info = [copy.copy(selected_lattice_list_with_info_origin[0]), selected_lattice_list_with_info_origin[1]]
		selected_lattice_list_with_info[0].sort(key=lambda lattice: (lattice.grid.teams[0].ranking+lattice.grid.teams[1].ranking)/2.0+lattice.chair.ranking)
		b_codes = ['94', '96', '92', '93']
		print "---------------------------------allocation No." +str(selected_lattice_list_with_info[1].allocation_no)+ "------------------------------------"
		#print "matchups for round:", round_num
		if round_num > 1: print "power allocation indicator: %.2f(the smaller, the better; min = 0)" % (selected_lattice_list_with_info[1].strong_strong_indicator)
		print "------------------------------------warnings----------------------------------------"
		for large_warning in selected_lattice_list_with_info[1].large_warnings:
			print large_warning
		print "------------------------------------matchups----------------------------------------"
		print "\033[33m             Gov     :     Opp     \033[0m"

		chair_list = [lattice.chair for lattice in selected_lattice_list_with_info[0]]
		grid_list = [lattice.grid for lattice in selected_lattice_list_with_info[0]]
		chair_list.sort(key=lambda chair: chair.ranking)
		grid_list.sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking)

		for lattice in selected_lattice_list_with_info[0]:
			if (lattice.grid.bubble < 5) and constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				text_1 = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+';45m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+'m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'

			if set(lattice.chair.institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[1].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name])&set(lattice.chair.conflict_teams):
				text_2 = '\033['+b_codes[int(4*chair_list.index(lattice.chair)/float(len(chair_list)))]+';41m'+"chair : {0:20s}".format(lattice.chair.name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[int(4*chair_list.index(lattice.chair)/float(len(chair_list)))]+'m'+"chair : {0:20s}".format(lattice.chair.name)+'\033[0m'

			if len(lattice.panel) == 2:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%(lattice.panel[0].name, lattice.panel[1].name),
			elif len(lattice.panel) == 1:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%(lattice.panel[0].name, ""),
			else:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%("", ""),
			for warning in lattice.warnings:
				warning += ","
				print "\033[31m"+warning+"\033[0m",
			print
		print
	else:
		selected_lattice_list_with_info = [copy.copy(selected_lattice_list_with_info_origin[0]), selected_lattice_list_with_info_origin[1]]
		selected_lattice_list_with_info[0].sort(key=lambda lattice: (lattice.grid.teams[0].ranking+lattice.grid.teams[1].ranking)/2.0+lattice.chair.ranking)
		b_codes = ['94', '96', '92', '93']
		print "---------------------------------allocation No." +str(selected_lattice_list_with_info[1].allocation_no)+ "------------------------------------"
		#print "matchups for round:", round_num
		if round_num > 1: print "power allocation indicator: %.2f(the smaller, the better; min = 0)" % (selected_lattice_list_with_info[1].strong_strong_indicator)
		print "------------------------------------warnings----------------------------------------"
		for large_warning in selected_lattice_list_with_info[1].large_warnings:
			print large_warning
		print "------------------------------------matchups----------------------------------------"
		print "\033[33m             Gov     :     Opp     \033[0m"
		print "--------------------------------------------"

		chair_list = [lattice.chair for lattice in selected_lattice_list_with_info[0]]
		grid_list = [lattice.grid for lattice in selected_lattice_list_with_info[0]]
		chair_list.sort(key=lambda chair: chair.ranking)
		grid_list.sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking+grid.teams[2].ranking+grid.teams[3].ranking)

		for lattice in selected_lattice_list_with_info[0]:
			if (lattice.grid.bubble < 5) and constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				text_1 = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+';45m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
				text_1d = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+';45m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[2].name, lattice.grid.teams[3].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+'m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
				text_1d = '\033['+b_codes[int(4*grid_list.index(lattice.grid)/float(len(grid_list)))]+'m'+"{0:20s} : {1:20s}".format(lattice.grid.teams[2].name, lattice.grid.teams[3].name)+'\033[0m'

			if set(lattice.chair.institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[1].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[2].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[3].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])&set(lattice.chair.conflict_teams):
				text_2 = '\033['+b_codes[int(4*chair_list.index(lattice.chair)/float(len(chair_list)))]+';41m'+"chair : {0:20s}".format(lattice.chair.name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[int(4*chair_list.index(lattice.chair)/float(len(chair_list)))]+'m'+"chair : {0:20s}".format(lattice.chair.name)+'\033[0m'

			if len(lattice.panel) == 2:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%(lattice.panel[0].name, lattice.panel[1].name)
				print text_1d+"|",
			elif len(lattice.panel) == 1:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%(lattice.panel[0].name, "")
				print text_1d+"|",
			else:
				print text_1+"|"+text_2+"(panel : %-20s, %-20s)"%("", "")
				print text_1d+"|",
			for warning in lattice.warnings:
				warning += ","
				print "\033[31m"+warning+"\033[0m",
			print
			print "--------------------------------------------"
		print

def check_matchups_only_for_venues(lattice_list, venue_list):
	large_warnings = []
	multi3 = {lattice.venue:0 for lattice in lattice_list}
	for lattice in lattice_list:
		multi3[lattice.venue] += 1
	for k, v in multi3.items():
		if v > 1:
			large_warnings.append(("error : a room appears more than two times :"+str(k)+": "+str(v)))

	vacant_venues = [venue for venue in venue_list if venue not in multi3.keys() and venue.available]

	if vacant_venues:
		str_vacant_venues = "vacant rooms are : "
		for vacant_venue in vacant_venues:
			str_vacant_venues+=str(vacant_venue.name)+str(" ")
		large_warnings.append(str_vacant_venues)

	return large_warnings

def show_matchups_by_venue(allocations, venue_list, round_num):
	if len(allocations[0].grid.teams) == 2:	
		print "\033[1;35m"+"------------------------------------ venue -----------------------------------------"+"\033[0m"	
		print "------------------------------------warnings----------------------------------------"
		large_warnings = check_matchups_only_for_venues(allocations, venue_list)
		for large_warning in large_warnings:
			print large_warning
		print "------------------------------matchups with venue-----------------------------------"
		print "matchups with venues for round:", round_num
		print "\033[33m             Gov     :     Opp     \033[0m"
		for lattice in allocations:
			if len(lattice.panel) == 2:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name),
			elif len(lattice.panel) == 1:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name),
			else:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name),
			print
		print
	else:
		print "\033[1;35m"+"------------------------------------ venue -----------------------------------------"+"\033[0m"		
		print "------------------------------------warnings----------------------------------------"
		large_warnings = check_matchups_only_for_venues(allocations, venue_list)
		for large_warning in large_warnings:
			print large_warning
		print "------------------------------matchups with venue-----------------------------------"
		print "matchups with venues for round:", round_num
		print "\033[33m             Gov     :     Opp     \033[0m"
		print "---------------------------------------------"
		for lattice in allocations:
			if len(lattice.panel) == 2:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name)
				print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
				print "---------------------------------------------"
			elif len(lattice.panel) == 1:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name)
				print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
				print "---------------------------------------------"
			else:
				print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name)
				print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
				print "---------------------------------------------"
			print
		print

def show_matchups(allocations, round_num):
	if len(allocations[0][0].grid.teams) == 2:	
		print "\033[1;35m"+"------------------------------- matchups for round"+str(round_num)+" ------------------------------------"+"\033[0m"	
		print "\033[33m             Gov     :     Opp     \033[0m"
		for lattice in allocations[0]:
			if lattice.venue:
				if len(lattice.panel) == 2:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name),
				elif len(lattice.panel) == 1:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name),
				else:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name),
				print
			else:
				if len(lattice.panel) == 2:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""),
				elif len(lattice.panel) == 1:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""),
				else:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""),
				print

		print
	else:
		print "\033[1;35m"+"------------------------------- matchups for round"+str(round_num)+" ------------------------------------"+"\033[0m"	
		print "\033[33m             Gov     :     Opp     \033[0m"
		print "---------------------------------------------"
		for lattice in allocations[0]:
			if lattice.venue:
				if len(lattice.panel) == 2:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name)
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"
				elif len(lattice.panel) == 1:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name)
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"
				else:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name)
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"
			else:
				if len(lattice.panel) == 2:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, "")
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"
				elif len(lattice.panel) == 1:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", "")
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"
				else:
					print "%20s : %-20s |chair : %-20s(panel : %-20s, %-20s)|venue : %-10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", "")
					print "%20s : %-20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name)
					print "---------------------------------------------"

		print

def show_grid_list(grid_list):
	rows = []
	teamspast = []
	for grid1 in grid_list:
		if grid1.teams[0] in teamspast:
			continue
		else:
			teamspast.append(grid1.teams[0])
		row = ""
		for grid2 in grid_list:
			if grid1.teams[0] == grid2.teams[1]:
				row += str(xbit(grid2.adoptbits, 0))## shita x keta
		rows.append(row)
	show_rows(rows)

def show_lattice_list(lattice_list):
	rows = []
	gridpast = None
	for lattice1 in lattice_list:
		if gridpast == lattice1.grid:
			continue
		else:
			gridpast = lattice1.grid
		row = ""
		for lattice2 in lattice_list:
			if lattice1.grid == lattice2.grid:
				n = "1" if lattice2.available else "0"
				row += n## shita x keta
		rows.append(row)
	show_rows(rows)
	
def show_adoptness1(grid_list, team_list):
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(grid.adoptness1)
		rows.append(row)
	show_rows(rows)

def show_adoptness2(grid_list, team_list):
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(grid.adoptness2)
		rows.append(row)
	show_rows(rows)

def show_adoptbits(team_list, grid_list, level):
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(xbit(grid.adoptbits, level))## shita x keta
		rows.append(row)
	show_rows(rows)

def show_adoptbitslong(team_list, grid_list, level):
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(xbit(grid.adoptbitslong, 3*level))## shita x keta
		rows.append(row)
	show_rows(rows)
	print
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(xbit(grid.adoptbitslong, 3*level+1))## shita x keta
		rows.append(row)
	show_rows(rows)
	print
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(xbit(grid.adoptbitslong, 3*level+2))## shita x keta
		rows.append(row)
	show_rows(rows)

def show_adoptbits_lattice(adjudicator_list, lattice_list, level):
	rows = []
	"""
	print [team.name for team in team_list]
	print [lattice.grid.teams[0].name for lattice in lattice_list]
	for team in team_list:
		if team.name not in [lattice.grid.teams[0].name for lattice in lattice_list]:
			print "invalid", team.name
	"""
	for adjudicator in adjudicator_list:
		row = ""
		for lattice in lattice_list:
			if lattice.chair == adjudicator:
				row += str(xbit(lattice.adoptbits, level))## shita x keta
				#if xbit(lattice.adoptbits, level) == 1: print adjudicator.name, lattice.grid.teams[0].name, lattice.grid.teams[1].name
		if row != "": rows.append(row)
	show_rows(rows)

def show_adoptbitslong_lattice(adjudicator_list, lattice_list, level):
	rows = []
	for adjudicator in adjudicator_list:
		row = ""
		for lattice in lattice_list:
			if lattice.chair == adjudicator:
				row += str(xbit(lattice.adoptbitslong, 3*level))## shita x keta
		if row != "": rows.append(row)
	show_rows(rows)
	print
	rows = []
	for adjudicator in adjudicator_list:
		row = ""
		for lattice in lattice_list:
			if lattice.chair == adjudicator:
				row += str(xbit(lattice.adoptbitslong, 3*level+1))## shita x keta
		if row != "": rows.append(row)
	show_rows(rows)
	print
	rows = []
	for adjudicator in adjudicator_list:
		row = ""
		for lattice in lattice_list:
			if lattice.chair == adjudicator:
				row += str(xbit(lattice.adoptbitslong, 3*level+2))## shita x keta
		if row != "": rows.append(row)
	show_rows(rows)

def show_rows(rows):
	for row in rows:
		print row

def progress(sentence):

	print sentence + "..."

def show_teams_scores(team_list, teamnum2):
	if teamnum2:
		for team in team_list:
			text = "%20s: %2d wins, %.2f points, %2d Govs, %+3d margin, wins(1:win, 0:lose):[ " % (team.name, sum(team.wins), sum(team.scores), team.past_sides.count("gov"), team.margin)
			for win in team.wins:
				if win == 1:
					text += "1 "
				else:
					text += "0 "
			text += "]"
			print text
	else:
		for team in team_list:
			text = "%20s: %2d win-points, %.2f points, position(og, oo, cg, co):[ %1d %1d %1d %1d ], win-points:[ " % (team.name, sum(team.wins), sum(team.scores), team.past_sides.count("og"), team.past_sides.count("oo"), team.past_sides.count("cg"), team.past_sides.count("co"))
			for win in team.wins:
				text += "{0:1d} ".format(win)
			text += "]"
			print text

def show_debater_scores(team_list):
	for team in team_list:
		for debater in team.debaters:
			print "%20s (%20s): " % (debater.name, team.name),
			for i, score_list in enumerate(debater.score_lists):
				print "[R %2d]"%(i+1),
				for score in score_list:
					print "%02.2f" % score,
			print

def show_evaluation(adjudicator_list):
	print "----------------------------------evaluation----------------------------------------"
	for adjudicator in adjudicator_list:
		print "%20s: evaluation: %2.2f"%(adjudicator.name, adjudicator.evaluation)
	print

def show_adjudicator_score(adjudicator_list):
	for adjudicator in adjudicator_list:
		print "%20s | evaluation :%.2f, active :%2d (chair :%2d, panel :%2d), rank of watched debate :" % (adjudicator.name, adjudicator.evaluation, adjudicator.active_num, adjudicator.active_num_as_chair, adjudicator.active_num-adjudicator.active_num_as_chair),
		for rank in adjudicator.watched_debate_ranks:
			print "%3d" % (rank), 
		print "score :",
		for score in adjudicator.scores:
			print "%.2f" % (score),
		print

def show_adjudicators(adjudicator_list):
	for adjudicator in adjudicator_list:
		if adjudicator.absent:
			print "\033[37m"+"%20s : %2d active, %20s, %20s(absent)\033[0m"%(adjudicator.name, adjudicator.active_num, str(adjudicator.institutions), str(adjudicator.conflict_teams))
		else:
			print "%20s : %2d active, %20s, %20s"%(adjudicator.name, adjudicator.active_num, str(adjudicator.institutions), str(adjudicator.conflict_teams))

def show_teams(team_list):
	for team in team_list:
		institution_text = str(team.institutions)
		if not team.available:
			print "\033[37m"+"{0:20s} : {1:20s}\033[0m".format(team.name, institution_text)
		else:
			print "{0:20s} : {1:20s}".format(team.name, institution_text)

def show_venues(venue_list):
	for venue in venue_list:
		if venue.available:
			print "%5s (priority: %4s)"%(str(venue.name),str(venue.priority))
		else:
			print "\033[37m"+"%5s (priority: %4s) (not available)\033[0m"%(str(venue.name),str(venue.priority))

def get_progressbar_str(progress):
	MAX_LEN = 30
	BAR_LEN = int(MAX_LEN * progress)
	return ('[' + '=' * BAR_LEN + ('>' if BAR_LEN < MAX_LEN else '') + ' ' * (MAX_LEN-BAR_LEN) + '] %.1f%%' % (progress * 100.0))

def progress_bar2(k, length):
	progress = float(k) / length
	sys.stderr.write('\r\033[K' + get_progressbar_str(progress))
	sys.stderr.flush()

def show_logo_star():
	length = 120
	sentence = "UTab for PDA ver3.1"
	base = "-"*length
	for k, char in enumerate(reversed(sentence)):
		for i in range(int(length/2)+int(len(sentence)/2)-k):
			base = base[:i+1]+"-"+base[i+2:]
			base = base[:i+2]+char+base[i+3:]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.001*(1+int((k+1)**(1/2.0))))
	time.sleep(0.7)
	for i in range(length*2):
		for j in range(i+1):
			base = base[:length-j]+" "+base[length-j:-1]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.0015/int(1+(i**1.2)*0.1))
	time.sleep(0.3)
	sys.stdout.write("\r"*length)
		
def show_logo_random_fade():
	length = 120
	sentence = "UTab for PDA ver2.5"
	base = "-"*length
	for k, char in enumerate(reversed(sentence)):
		for i in range(int(length/2)+int(len(sentence)/2)-k):
			base = base[:i+1]+"-"+base[i+2:]
			base = base[:i+2]+char+base[i+3:]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.001*(1+int((k+1)**(1/2.0))))
	time.sleep(0.7)
	numbers = [i for i in range(length)]
	random.shuffle(numbers)
	for i in range(length):
		n = numbers[i]
		base = base[:n+1]+" "+base[n+2:]
		sys.stdout.write("\r"+base)
		sys.stdout.flush()
		time.sleep(0.004)
	time.sleep(0.7)

	sys.stdout.write("\r"*length)

def progress_bar():
	END = 170
	for i in range(END+1):
		time.sleep(0.01)
		progress = 1.0 * i / END
		sys.stderr.write('\r\033[K' + get_progressbar_str(progress))
		sys.stderr.flush()
	sys.stderr.write('\n')
	sys.stderr.flush()
	time.sleep(0.7)
