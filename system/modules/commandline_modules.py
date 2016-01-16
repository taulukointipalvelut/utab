# -*- coding: utf-8 -*-
import sys
import copy
from .property_modules import *
from .bit_modules import *
from . import interaction_modules
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
		interaction_modules.commandline("---------------------------------matchups No." +str(grid_list_with_info[1].matchups_no)+ "-------------------------------------")
		#print "matchups for round:", round_num
		if grid_list_with_info[1].comment != "" : interaction_modules.commandline("Note: "+str(grid_list_with_info[1].comment))
		if round_num > 1: interaction_modules.commandline("power pairing indicator: %.2f(the smaller, the better; min = 1)" % (grid_list_with_info[1].power_pairing_indicator))
		interaction_modules.commandline("adopt indicator: %.2f (sd: %.2f, ot: %.2f) (the larger, the better; min = 0)" % (grid_list_with_info[1].adopt_indicator, grid_list_with_info[1].adopt_indicator_sd, grid_list_with_info[1].adopt_indicator2))
		#print "same institution indicator: %.2f(the smaller, the better; min = 0)" % (grid_list_with_info[1].same_institution_indicator)
		interaction_modules.commandline("scattered institutions indicator: %.2f(the larger, the better; min = 1)" % (grid_list_with_info[1].scatter_indicator))
		interaction_modules.commandline("number of warnings: %4d" % grid_list_with_info[1].num_of_warnings)
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		for large_warning in grid_list_with_info[1].large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------------matchups----------------------------------------")
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		for grid in grid_list_with_info[0]:
			if is_one_sided(grid.teams[0], "gov", 2) != 0:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';41m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+'m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
			if is_one_sided(grid.teams[1], "opp", 2) != 0:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';41m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+'m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[1].institutions):
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[1].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'

			line = text_1+" : "+text_2+" |"
			for warning in grid.warnings:
				line = line + ' \033[31m'+str(warning)+'\033[0m'
			interaction_modules.commandline(line)
	else:
		grid_list_with_info = [copy.copy(grid_list_with_info_origin[0]), grid_list_with_info_origin[1]]
		grid_list_with_info[0].sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking+grid.teams[2].ranking+grid.teams[3].ranking)
		b_codes = ['93', '92', '96', '94', '97', '93', '92', '96', '94', '97', '93', '92', '96', '94', '97']
		interaction_modules.commandline("---------------------------------matchups No." +str(grid_list_with_info[1].matchups_no)+ "-------------------------------------")
		#print "matchups for round:", round_num
		if grid_list_with_info[1].comment != "" : interaction_modules.commandline("Note: "+str(grid_list_with_info[1].comment))
		if round_num > 1: interaction_modules.commandline("power pairing indicator: %.2f(the smaller, the better; min = 1)" % (grid_list_with_info[1].power_pairing_indicator))
		interaction_modules.commandline("adopt indicator: %.2f (sd: %.2f, ot: %.2f) (the larger, the better; min = 0)" % (grid_list_with_info[1].adopt_indicator, grid_list_with_info[1].adopt_indicator_sd, grid_list_with_info[1].adopt_indicator2))
		interaction_modules.commandline("same institution indicator: %.2f(the smaller, the better; min = 0)" % (grid_list_with_info[1].same_institution_indicator))
		interaction_modules.commandline("number of warnings: %4d" % grid_list_with_info[1].num_of_warnings)
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		for large_warning in grid_list_with_info[1].large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------------matchups----------------------------------------")
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		interaction_modules.commandline("---------------------------------------------")
		wins = [sum(team.wins) for grid in grid_list_with_info[0] for team in grid.teams]
		wins.sort()#reverse=True
		for grid in grid_list_with_info[0]:#0123: 0123, 456: 0123, 456, 789 #012,3: 012,345,6 /3+1
			diff_wins = list(set(wins))
			division_num = min(5, len(list(set(wins))))

			text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+'m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
			text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+'m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+'m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+'m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			
			if set(grid.teams[0].institutions) & set(grid.teams[1].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[2].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			if set(grid.teams[0].institutions) & set(grid.teams[3].institutions):
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			if set(grid.teams[1].institutions) & set(grid.teams[2].institutions):
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			if set(grid.teams[1].institutions) & set(grid.teams[3].institutions):
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			if set(grid.teams[2].institutions) & set(grid.teams[3].institutions):
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'

			if is_one_halfed(grid.teams[0], "og") != 0:
				text_1 = '\033['+b_codes[ret_wei(sum(grid.teams[0].wins), wins, division_num)]+';41m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
			if is_one_halfed(grid.teams[1], "oo") != 0:
				text_2 = '\033['+b_codes[ret_wei(sum(grid.teams[1].wins), wins, division_num)]+';41m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			if is_one_halfed(grid.teams[2], "cg") != 0:
				text_3 = '\033['+b_codes[ret_wei(sum(grid.teams[2].wins), wins, division_num)]+';41m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			if is_one_halfed(grid.teams[3], "co") != 0:
				text_4 = '\033['+b_codes[ret_wei(sum(grid.teams[3].wins), wins, division_num)]+';41m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			"""
			if grid.teams[0].name in grid.teams[1].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[2].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			if grid.teams[0].name in grid.teams[3].past_opponents:
				text_1 = '\033['+b_codes[sum(grid.teams[0].wins)]+';45m'+"{0:20.20s}".format(grid.teams[0].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			if grid.teams[1].name in grid.teams[2].past_opponents:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
			if grid.teams[1].name in grid.teams[3].past_opponents:
				text_2 = '\033['+b_codes[sum(grid.teams[1].wins)]+';45m'+"{0:20.20s}".format(grid.teams[1].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			if grid.teams[2].name in grid.teams[3].past_opponents:
				text_3 = '\033['+b_codes[sum(grid.teams[2].wins)]+';45m'+"{0:20.20s}".format(grid.teams[2].name)+'\033[0m'
				text_4 = '\033['+b_codes[sum(grid.teams[3].wins)]+';45m'+"{0:20.20s}".format(grid.teams[3].name)+'\033[0m'
			"""
			line1 = text_1+" : "+text_2+" |"
			line2 = text_3+" : "+text_4+" |"
			for warning in grid.warnings:
				line2 += " \033[31m"+str(warnin)+"\033[0m"
			interaction_modules.commandline(line1)
			interaction_modules.commandline(line2)
			interaction_modules.commandline("---------------------------------------------")

def show_matchups_by_lattice(selected_lattice_list_with_info_origin, round_num, constants_of_adj):
	if len(selected_lattice_list_with_info_origin[0][0].grid.teams) == 2:
		selected_lattice_list_with_info = [copy.copy(selected_lattice_list_with_info_origin[0]), selected_lattice_list_with_info_origin[1]]
		selected_lattice_list_with_info[0].sort(key=lambda lattice: (lattice.grid.teams[0].ranking+lattice.grid.teams[1].ranking)/2.0+lattice.chair.ranking)
		b_codes = ['94', '96', '92', '93']
		interaction_modules.commandline("---------------------------------allocation No." +str(selected_lattice_list_with_info[1].allocation_no)+ "------------------------------------")
		#print "matchups for round:", round_num
		if selected_lattice_list_with_info[1].comment != "" : interaction_modules.commandline("Note: "+str(selected_lattice_list_with_info[1].comment))
		if round_num > 1: interaction_modules.commandline("power allocation indicator: %.2f(the smaller, the better; min = 0)" % (selected_lattice_list_with_info[1].strong_strong_indicator))
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		for large_warning in selected_lattice_list_with_info[1].large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------------matchups----------------------------------------")
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")

		chair_list = [lattice.chair for lattice in selected_lattice_list_with_info[0]]
		grid_list = [lattice.grid for lattice in selected_lattice_list_with_info[0]]
		chair_list.sort(key=lambda chair: chair.ranking)
		grid_list.sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking)

		for lattice in selected_lattice_list_with_info[0]:
			chair_color_index = int(4*chair_list.index(lattice.chair)/float(len(chair_list))) if round_num != 1 else 3
			grid_color_index = int(4*grid_list.index(lattice.grid)/float(len(grid_list))) if round_num != 1 else 3
			if (lattice.grid.bubble < 5) and constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				text_1 = '\033['+b_codes[grid_color_index]+';45m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[grid_color_index]+'m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'

			if set(lattice.chair.institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[1].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name])&set(lattice.chair.conflict_teams):
				text_2 = '\033['+b_codes[chair_color_index]+';41m'+"chair : {0:20.20s}".format(lattice.chair.name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[chair_color_index]+'m'+"chair : {0:20.20s}".format(lattice.chair.name)+'\033[0m'

			if len(lattice.panel) == 2:
				line = text_1+"|"+text_2+"(panel:"
				panel1_text = lattice.panel[0].name
				panel2_text = lattice.panel[1].name
				if set(lattice.panel[0].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[1].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name])&set(lattice.panel[0].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel1_text)+'\033[0m' + ","
				else:
					line = line + "%-20.20s"%panel1_text + ","
				if set(lattice.panel[1].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[1].institutions) & set(lattice.grid.teams[1].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name])&set(lattice.panel[1].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel2_text)+'\033[0m' + ")"
				else:
					line = line + "%-20.20s)"%panel2_text

			elif len(lattice.panel) == 1:
				line = text_1+"|"+text_2+"(panel:"
				panel1_text = lattice.panel[0].name
				if set(lattice.panel[0].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[1].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name])&set(lattice.panel[0].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel1_text)+'\033[0m' + ","
				else:
					line = line + "%-20.20s)"%""

			else:
				line = text_1+"|"+text_2+"(panel: %-20.20s, %-20.20s)"%("", "")

			for warning in lattice.warnings:
				line = line + " \033[31m"+str(warning)+"\033[0m"
			interaction_modules.commandline(line)
		interaction_modules.commandline("")
	else:
		selected_lattice_list_with_info = [copy.copy(selected_lattice_list_with_info_origin[0]), selected_lattice_list_with_info_origin[1]]
		selected_lattice_list_with_info[0].sort(key=lambda lattice: (lattice.grid.teams[0].ranking+lattice.grid.teams[1].ranking)/2.0+lattice.chair.ranking)
		b_codes = ['94', '96', '92', '93']
		interaction_modules.commandline("---------------------------------allocation No." +str(selected_lattice_list_with_info[1].allocation_no)+ "------------------------------------")
		#print "matchups for round:", round_num
		if selected_lattice_list_with_info[1].comment != "" : interaction_modules.commandline("Note: "+str(selected_lattice_list_with_info[1].comment))
		if round_num > 1: interaction_modules.commandline("power allocation indicator: %.2f(the smaller, the better; min = 0)" % (selected_lattice_list_with_info[1].strong_strong_indicator))
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		for large_warning in selected_lattice_list_with_info[1].large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------------matchups----------------------------------------")
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		interaction_modules.commandline("--------------------------------------------")

		chair_list = [lattice.chair for lattice in selected_lattice_list_with_info[0]]
		grid_list = [lattice.grid for lattice in selected_lattice_list_with_info[0]]
		chair_list.sort(key=lambda chair: chair.ranking)
		grid_list.sort(key=lambda grid: grid.teams[0].ranking+grid.teams[1].ranking+grid.teams[2].ranking+grid.teams[3].ranking)

		for lattice in selected_lattice_list_with_info[0]:
			chair_color_index = int(4*chair_list.index(lattice.chair)/float(len(chair_list))) if round_num != 1 else 3
			grid_color_index = int(4*grid_list.index(lattice.grid)/float(len(grid_list))) if round_num != 1 else 3
			if (lattice.grid.bubble < 5) and constants_of_adj[round_num-1]["des_priori_bubble"] != 0:
				text_1 = '\033['+b_codes[grid_color_index]+';45m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
				text_1d = '\033['+b_codes[grid_color_index]+';45m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[2].name, lattice.grid.teams[3].name)+'\033[0m'
			else:
				text_1 = '\033['+b_codes[grid_color_index]+'m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[0].name, lattice.grid.teams[1].name)+'\033[0m'
				text_1d = '\033['+b_codes[grid_color_index]+'m'+"{0:20.20s} : {1:20.20s}".format(lattice.grid.teams[2].name, lattice.grid.teams[3].name)+'\033[0m'

			if set(lattice.chair.institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[1].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[2].institutions) or set(lattice.chair.institutions) & set(lattice.grid.teams[3].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])&set(lattice.chair.conflict_teams):
				text_2 = '\033['+b_codes[chair_color_index]+';41m'+"chair : {0:20.20s}".format(lattice.chair.name)+'\033[0m'
			else:
				text_2 = '\033['+b_codes[chair_color_index]+'m'+"chair : {0:20.20s}".format(lattice.chair.name)+'\033[0m'

			if len(lattice.panel) == 2:
				line = text_1+"|"+text_2+"(panel:"
				panel1_text = lattice.panel[0].name
				panel2_text = lattice.panel[1].name
				if set(lattice.panel[0].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[1].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[2].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[3].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])&set(lattice.panel[0].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel1_text)+'\033[0m' + ","
				else:
					line = line + "%-20.20s"%panel1_text + ","

				if set(lattice.panel[1].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[1].institutions) & set(lattice.grid.teams[1].institutions) or set(lattice.panel[1].institutions) & set(lattice.grid.teams[2].institutions) or set(lattice.panel[1].institutions) & set(lattice.grid.teams[3].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])&set(lattice.panel[1].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel2_text)+'\033[0m' + ")"
				else:
					line = line + "%-20.20s)"%panel2_text
				line2 = text_1d+"|"
			elif len(lattice.panel) == 1:
				line = text_1+"|"+text_2+"(panel:"
				panel1_text = lattice.panel[0].name
				if set(lattice.panel[0].institutions) & set(lattice.grid.teams[0].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[1].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[2].institutions) or set(lattice.panel[0].institutions) & set(lattice.grid.teams[3].institutions) or set([lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.grid.teams[2].name, lattice.grid.teams[3].name])&set(lattice.panel[0].conflict_teams):
					line = line + '\033[;41m'+"%-20.20s"%(panel1_text)+'\033[0m' + ","
				else:
					line = line + "%-20.20s"%panel1_text + ","
				line = line + "%-20.20s)"%""
				line2 = text_1d+"|"
			else:
				line = text_1+"|"+text_2+"(panel: %-20.20s, %-20.20s)"%("", "")
				line2 = text_1d+"|"
			for warning in lattice.warnings:
				line2 = line2 + " \033[31m"+str(warning)+"\033[0m"
			interaction_modules.commandline(line1)
			interaction_modules.commandline(line2)
			interaction_modules.commandline("--------------------------------------------")
		interaction_modules.commandline("")

def check_matchups_only_for_venues(lattice_list, venue_list):
	large_warnings = []
	multi3 = {lattice.venue:0 for lattice in lattice_list}
	for lattice in lattice_list:
		multi3[lattice.venue] += 1
	for k, v in list(multi3.items()):
		if v > 1:
			large_warnings.append(("error : a room appears more than two times :"+str(k)+": "+str(v)))

	vacant_venues = [venue for venue in venue_list if venue not in list(multi3.keys()) and venue.available]

	if vacant_venues:
		str_vacant_venues = "vacant rooms are : "
		for vacant_venue in vacant_venues:
			str_vacant_venues+=str(vacant_venue.name)+str(" ")
		large_warnings.append(str_vacant_venues)

	return large_warnings

def show_matchups_by_venue(allocations, venue_list, round_num):
	if len(allocations[0].grid.teams) == 2:	
		interaction_modules.commandline("\033[1;35m"+"------------------------------------ venue -----------------------------------------"+"\033[0m")	
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		large_warnings = check_matchups_only_for_venues(allocations, venue_list)
		for large_warning in large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------matchups with venue-----------------------------------")
		interaction_modules.commandline("matchups with venues for round:", round_num)
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		for lattice in allocations:
			if len(lattice.panel) == 2:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name))
			elif len(lattice.panel) == 1:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name))
			else:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name))
		interaction_modules.commandline("")
	else:
		interaction_modules.commandline("\033[1;35m"+"------------------------------------ venue -----------------------------------------"+"\033[0m")		
		interaction_modules.commandline("------------------------------------warnings----------------------------------------")
		large_warnings = check_matchups_only_for_venues(allocations, venue_list)
		for large_warning in large_warnings:
			interaction_modules.commandline(large_warning)
		interaction_modules.commandline("------------------------------matchups with venue-----------------------------------")
		interaction_modules.commandline("matchups with venues for round:", round_num)
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		interaction_modules.commandline("---------------------------------------------")
		for lattice in allocations:
			if len(lattice.panel) == 2:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name))
				interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
				interaction_modules.commandline("---------------------------------------------")
			elif len(lattice.panel) == 1:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name))
				interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
				interaction_modules.commandline("---------------------------------------------")
			else:
				interaction_modules.commandline("%20.20s : %-20.20s |chair : %-20.20s(panel : %-20.20s, %-20.20s)|venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name))
				interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
				interaction_modules.commandline("---------------------------------------------")
		interaction_modules.commandline("")

def show_matchups(allocations, round_num):
	if len(allocations[0][0].grid.teams) == 2:	
		interaction_modules.commandline("\033[1;35m"+"------------------------------- matchups for round"+str(round_num)+" ------------------------------------"+"\033[0m")	
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		for lattice in allocations[0]:
			if lattice.venue:
				if len(lattice.panel) == 2:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name))
				elif len(lattice.panel) == 1:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name))
				else:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name))
			else:
				if len(lattice.panel) == 2:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""))
				elif len(lattice.panel) == 1:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""))
				else:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""))

		interaction_modules.commandline("")
	else:
		interaction_modules.commandline("\033[1;35m"+"------------------------------- matchups for round"+str(round_num)+" ------------------------------------"+"\033[0m")	
		interaction_modules.commandline("\033[33m             Gov     :     Opp     \033[0m")
		interaction_modules.commandline("---------------------------------------------")
		for lattice in allocations[0]:
			if lattice.venue:
				if len(lattice.panel) == 2:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, lattice.venue.name))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")
				elif len(lattice.panel) == 1:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", lattice.venue.name))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")
				else:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", lattice.venue.name))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")
			else:
				if len(lattice.panel) == 2:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, lattice.panel[1].name, ""))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")
				elif len(lattice.panel) == 1:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, lattice.panel[0].name, "", ""))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")
				else:
					interaction_modules.commandline("%20.20s : %-20.20s | chair : %-20.20s(panel : %-20.20s, %-20.20s)| venue : %-10.10s" % (lattice.grid.teams[0].name, lattice.grid.teams[1].name, lattice.chair.name, "", "", ""))
					interaction_modules.commandline("%20.20s : %-20.20s |" % (lattice.grid.teams[2].name, lattice.grid.teams[3].name))
					interaction_modules.commandline("---------------------------------------------")

		interaction_modules.commandline("")

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
	interaction_modules.progress("")
	rows = []
	for team in team_list:
		row = ""
		for grid in grid_list:
			if grid.teams[0] == team:
				row += str(xbit(grid.adoptbitslong, 3*level+1))## shita x keta
		rows.append(row)
	show_rows(rows)
	interaction_modules.progress("")
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
	interaction_modules.progress("")
	rows = []
	for adjudicator in adjudicator_list:
		row = ""
		for lattice in lattice_list:
			if lattice.chair == adjudicator:
				row += str(xbit(lattice.adoptbitslong, 3*level+1))## shita x keta
		if row != "": rows.append(row)
	show_rows(rows)
	interaction_modules.progress("")
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
		interaction_modules.progress(row)

def show_teams_scores(team_list, teamnum):
	team_list_cp = copy.copy(team_list)
	team_list_cp.sort(key=lambda team: (-sum(team.wins), -sum(team.scores)))
	if teamnum == 2:
		for team in team_list_cp:
			text = "%20.20s: %2d wins, % 3.2f points, %2d Govs, %+3d margin, wins(1:win, 0:lose):[ " % (team.name, sum(team.wins), sum(team.scores), team.past_sides.count("gov"), team.margin)
			for win in team.wins_sub:
				if win == 'n/a':
					text += "n "
				else:
					text += "{0:1d} ".format(win)
			text += "]"
			interaction_modules.commandline(text)
	else:
		for team in team_list_cp:
			text = "%20.20s: %2d win-points, %-3.2f points, position(og, oo, cg, co):[ %1d %1d %1d %1d ], win-points(R1, R2, ...):[ " % (team.name, sum(team.wins), sum(team.scores), team.past_sides.count("og"), team.past_sides.count("oo"), team.past_sides.count("cg"), team.past_sides.count("co"))
			for win in team.wins_sub:
				if win == 'n/a':
					text += "n "
				else:
					text += "{0:1d} ".format(win)
			text += "]"
			interaction_modules.commandline(text)

def show_debater_scores(team_list):
	"""
	for team in team_list:
		for debater in team.debaters:
			line = "%20.20s (%20.20s): " % (debater.name, team.name)
			for i, score_list in enumerate(debater.score_lists):
				line = line + "[R %2d]"%(i+1)
				for score in score_list:
					line = line + "%02.2f " % score
			interaction_modules.commandline(line)
	"""
	debater_list = [debater for team in team_list for debater in team.debaters]
	debater_list.sort(key=lambda debater: sum(debater.scores), reverse=True)
	for debater in debater_list:
		line = "%20.20s: " % (debater.name)
		for i, score_list in enumerate(debater.score_lists):
			line = line + "[R %2d]"%(i+1)
			for score in score_list:
				line = line + "%02.2f " % score
		interaction_modules.commandline(line)

def show_evaluation(adjudicator_list):
	interaction_modules.commandline("----------------------------------evaluation----------------------------------------")
	for adjudicator in adjudicator_list:
		interaction_modules.commandline("%20.20s: evaluation: %2.2f"%(adjudicator.name, adjudicator.evaluation))
	interaction_modules.commandline("")

def show_adjudicator_score(adjudicator_list):
	adjudicator_list_cp = copy.copy(adjudicator_list)
	def ret_avr(adjudicator):
		avr = float(sum(adjudicator.scores))/len(adjudicator.scores) if len(adjudicator.scores) != 0 else 0
		return avr
	adjudicator_list_cp.sort(key=lambda adjudicator: ret_avr(adjudicator), reverse=True)

	for adjudicator in adjudicator_list_cp:
		line = "%20.20s | average: % 2.2f, (previous) evaluation: % 2.2f, active: %1d (chair: %1d, panel: %1d), score (rank of debate): " % (adjudicator.name, ret_avr(adjudicator), adjudicator.evaluation, adjudicator.active_num, adjudicator.active_num_as_chair, adjudicator.active_num-adjudicator.active_num_as_chair)
		for rank, score in zip(adjudicator.watched_debate_ranks_sub, adjudicator.scores_sub):
			if score == 'n/a':
				line = line + " n/a (n/a)"
			else:
				line = line + "%2.2f (%3d)" % (score, rank)
		interaction_modules.commandline(line)

def show_adjudicators(adjudicator_list):
	for adjudicator in adjudicator_list:
		if adjudicator.absent:
			interaction_modules.commandline("\033[37m"+"%20.20s : %2d active, %20.20s, %20.20s(absent)\033[0m"%(adjudicator.name, adjudicator.active_num, str(adjudicator.institutions), str(adjudicator.conflict_teams)))
		else:
			interaction_modules.commandline("%20.20s : %2d active, %20.20s, %20.20s"%(adjudicator.name, adjudicator.active_num, str(adjudicator.institutions), str(adjudicator.conflict_teams)))

def show_teams(team_list):
	for team in team_list:
		institution_text = str(team.institutions)
		if not team.available:
			interaction_modules.commandline("\033[37m"+"{0:20s} : {1:20s}     (absent)\033[0m".format(team.name, institution_text))
		else:
			interaction_modules.commandline("{0:20s} : {1:20s}".format(team.name, institution_text))

def show_venues(venue_list):
	for venue in venue_list:
		if venue.available:
			interaction_modules.commandline("%5s (priority: %4s)"%(str(venue.name),str(venue.priority)))
		else:
			interaction_modules.commandline("\033[37m"+"%5s (priority: %4s) (not available)\033[0m"%(str(venue.name),str(venue.priority)))

