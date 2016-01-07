# -*- coding: utf-8 -*-
#
# チームの得点は真の点数から正規分布で分布していると仮定
# 4Round試行回数100回
# 強いチームと対戦するとき点数が伸びると仮定(1)
# 点数が変わらないと仮定(2)
# チーム数100
# チームのスコアは正規分布と仮定
import random
import math
import numpy as np
from . import modules.plot_modules as plt2

class Ele:
	def __init__(self, real_score):
		self.real_ranking = 0
		self.ranking = 0
		self.real_score = real_score
		self.scores = []
		self.win = 0
		self.margin = 0

def random_pairing(elements):
	random.shuffle(elements)
	pairs = []
	for j in range(len(elements)/2):
		pairs.append([elements[2*j], elements[2*j+1]])
	return pairs

def power_pairing(elements):
	pairs = []
	sort_elements(elements)
	for j in range(len(elements)/2):
		pairs.append([elements[2*j], elements[2*j+1]])
	return pairs

def str_wek_pairing(elements):
	pairs = []
	for j in range(len(elements)/2):
		pairs.append([elements[j], elements[-j-1]])
	return pairs

def str_wek_pairing2(elements):
	pairs = []
	for j in range(len(elements)/2):
		pairs.append([elements[j], elements[len(elements)/2+j]])
	return pairs

def str_wek_pairing3(elements):
	pairs = []
	for j in range(len(elements)/4):
		pairs.append([elements[j], elements[len(elements)/4+j]])
		pairs.append([elements[len(elements)/2+j], elements[len(elements)*3/4+j]])
	return pairs

def str_wek_pairing_n(elements, n):
	pairs = []
	for j in range(len(elements)/n):
		for i in range(n/2):
			pairs.append([elements[len(elements)*i/n+j], elements[len(elements)*(i+1)/n+j]])
	return pairs

def fight(elements, pairs, ratio_diff_on_score, sd_of_score):#ratio.. => the ratio how the difference of strength of each pair affects the scorings
	for pair in pairs:
		pair0_score = pair[0].real_score - ratio_diff_on_score*(pair[0].real_score-pair[1].real_score) + random.normalvariate(0, sd_of_score)
		pair1_score = pair[1].real_score + ratio_diff_on_score*(pair[0].real_score-pair[1].real_score) + random.normalvariate(0, sd_of_score)
		if pair0_score > pair1_score:
			pair[0].win += 1
			pair[0].margin += pair0_score - pair1_score
			pair[1].margin += pair1_score - pair0_score
		else:
			pair[1].win += 1
			pair[0].margin += pair0_score - pair1_score
			pair[1].margin += pair1_score - pair0_score
		pair[0].scores.append(pair0_score)
		pair[1].scores.append(pair1_score)
	elements.sort(key=lambda ele: sum(ele.scores), reverse=True)
	for r, ele in enumerate(elements):
		ele.ranking = r +1

def str_str_indicator(elements):
	indicator = 0
	for ele in elements:
		indicator += (ele.ranking - ele.real_ranking)**2
		#print indicator
		#print "f"
	indicator /= round(float(len(elements)), 2)
	indicator = math.sqrt(indicator)
	return indicator

def sort_elements(elements):
	elements.sort(key=lambda ele:(ele.win, sum(ele.scores), ele.margin), reverse=True)
	for r, ele in enumerate(elements):
		ele.ranking = r+1

def initialize(average, sd, num_teams):
	elements = [Ele(random.normalvariate(average, sd)) for i in range(num_teams)]
	elements.sort(key=lambda ele: ele.real_score, reverse=True)
	for r, ele in enumerate(elements):
		ele.real_ranking = r + 1
		ele.ranking = 0
	#print [[ele.margin, ele.real_score, ele.ranking, ele.real_ranking, ele.win] for ele in elements]
	random.shuffle(elements)###initialize	

	return elements

def show_rankings(elements):
	for ele in elements:
		print(str(ele.ranking) + ", ", end=' ')
	print()
	for ele in elements:
		print(str(ele.real_ranking) + ", ", end=' ')
	print()

def test(elements, pairing, rounds, ratio_diff_on_score, sd_of_score):
	for i in range(rounds):
		pairs = pairing(elements)
		fight(elements, pairs, ratio_diff_on_score, sd_of_score)
	sort_elements(elements)
	return elements

def get_str_str_indicators(num_simulation, average, sd_of_population, num_teams, rounds, ratio_diff_on_score, sd_of_scores, pairing):
	str_str_indicators = []
	for i in range(num_simulation):
		elements = initialize(average, sd_of_population, num_teams)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, pairing, rounds, ratio_diff_on_score, sd_of_scores)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators.append(str_str_indi/str_str_indi_0*100)
	#print str_str_indicators_random
	#plt2.bar_1d(str_str_indicators_random)
	return str_str_indicators

if __name__ == "__main__":
	NUM_SIMULATION = 1000
	AVERAGE = 75
	SD_OF_POPULATION = 5
	NUM_TEAMS = 128 # recommended: x % 2**n  == 0
	ROUNDS = 4
	RATIO_DIFF_ON_SCORE = 0.2
	SD_OF_SCORES = 1

	data_list = []

	for i in range(5):
		n = 2**(i+1)
		print("str wek pairing")
		str_wek_pairing_n_wrapped = lambda elements: str_wek_pairing_n(elements, n)
		str_str_indicators_str_wek = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, str_wek_pairing_n_wrapped)
		data_list.append(str_str_indicators_str_wek)
	plt2.hist(data_list)

	"""
	for i in range(30):
		RATIO_DIFF_ON_SCORE = i*0.05
		print "random pairing"
		str_str_indicators_random = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, random_pairing)
		data_list.append(str_str_indicators_random)
	plt2.hist(data_list)
	"""
	"""
	for i in range(20):
		SD_OF_POPULATION = i*0.5
		print "random pairing"
		str_str_indicators_random = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, random_pairing)
		data_list.append(str_str_indicators_random)
	plt2.hist(data_list)
	"""
	"""
	for i in range(5):
		SD_OF_SCORES = i*0.5
		print "random pairing"
		str_str_indicators_random = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, random_pairing)
		data_list.append(str_str_indicators_random)
	plt2.hist(data_list)
	"""
	"""
	for i in range(30):
		RATIO_DIFF_ON_SCORE = i*0.05
		print "power pairing"
		str_str_indicators_power = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, power_pairing)
		data_list.append(str_str_indicators_power)
	plt2.hist(data_list)
	"""
	"""
	for i in range(20):
		SD_OF_POPULATION = i*0.5
		print "power pairing"
		str_str_indicators_power = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, power_pairing)
		data_list.append(str_str_indicators_power)
	plt2.hist(data_list)
	"""
	"""
	for i in range(5):
		SD_OF_SCORES = i*0.5
		print "power pairing"
		str_str_indicators_power = get_str_str_indicators(100, AVERAGE, SD_OF_POPULATION, NUM_TEAMS, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES, power_pairing)
		data_list.append(str_str_indicators_power)
	plt2.hist(data_list)
	"""
	"""
	print "random pairing"
	str_str_indicators_random = []
	for i in range(NUM_SIMULATION):
		elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, random_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators_random.append(str_str_indi/str_str_indi_0*100)
	print str_str_indicators_random
	plt2.bar_1d(str_str_indicators_random)

	print "power pairing"
	str_str_indicators_power = []
	for i in range(NUM_SIMULATION):
		elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, power_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators_power.append(str_str_indi/str_str_indi_0*100)
	print str_str_indicators_power
	plt2.bar_1d(str_str_indicators_power)

	print "str vs str pairing"
	str_str_indicators_str_wek = []
	for i in range(NUM_SIMULATION):
		elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, str_wek_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators_str_wek.append(str_str_indi/str_str_indi_0*100)
	print str_str_indicators_str_wek
	plt2.bar_1d(str_str_indicators_str_wek)

	print "[1] vs [1/2*all_len+1]"
	str_str_indicators_str_wek2 = []
	for i in range(NUM_SIMULATION):
		elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, str_wek_pairing2, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators_str_wek2.append(str_str_indi/str_str_indi_0*100)
	print str_str_indicators_str_wek2
	plt2.bar_1d(str_str_indicators_str_wek2)

	print "[1] vs [1/4*all_len+1]..."
	str_str_indicators_str_wek3 = []
	for i in range(NUM_SIMULATION):
		elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
		str_str_indi_0 = str_str_indicator(elements)
		elements = test(elements, str_wek_pairing3, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
		#show_rankings(elements)
		str_str_indi = str_str_indicator(elements)
		#print str_str_indi
		str_str_indicators_str_wek3.append(str_str_indi/str_str_indi_0*100)
	print str_str_indicators_str_wek3
	plt2.bar_1d(str_str_indicators_str_wek3)
	plt2.hist([str_str_indicators_random, str_str_indicators_power, str_str_indicators_str_wek, str_str_indicators_str_wek2, str_str_indicators_str_wek3])
	"""
	"""
	for i in range(5):
		RATIO_DIFF_ON_SCORE = i*0.1
		print "random pairing"
		str_str_indicators_random = []
		for i in range(NUM_SIMULATION):
			elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
			str_str_indi_0 = str_str_indicator(elements)
			elements = test(elements, random_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
			#show_rankings(elements)
			str_str_indi = str_str_indicator(elements)
			#print str_str_indi
			str_str_indicators_random.append(str_str_indi/str_str_indi_0*100)
		print str_str_indicators_random
		#plt2.bar_1d(str_str_indicators_random)

		print "power pairing"
		str_str_indicators_power = []
		for i in range(NUM_SIMULATION):
			elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
			str_str_indi_0 = str_str_indicator(elements)
			elements = test(elements, power_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
			#show_rankings(elements)
			str_str_indi = str_str_indicator(elements)
			#print str_str_indi
			str_str_indicators_power.append(str_str_indi/str_str_indi_0*100)
		print str_str_indicators_power
		#plt2.bar_1d(str_str_indicators_power)

		print "str vs str pairing"
		str_str_indicators_str_wek = []
		for i in range(NUM_SIMULATION):
			elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
			str_str_indi_0 = str_str_indicator(elements)
			elements = test(elements, str_wek_pairing, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
			#show_rankings(elements)
			str_str_indi = str_str_indicator(elements)
			#print str_str_indi
			str_str_indicators_str_wek.append(str_str_indi/str_str_indi_0*100)
		print str_str_indicators_str_wek
		#plt2.bar_1d(str_str_indicators_str_wek)

		print "[1] vs [1/2*all_len+1]"
		str_str_indicators_str_wek2 = []
		for i in range(NUM_SIMULATION):
			elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
			str_str_indi_0 = str_str_indicator(elements)
			elements = test(elements, str_wek_pairing2, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
			#show_rankings(elements)
			str_str_indi = str_str_indicator(elements)
			#print str_str_indi
			str_str_indicators_str_wek2.append(str_str_indi/str_str_indi_0*100)
		print str_str_indicators_str_wek2
		#plt2.bar_1d(str_str_indicators_str_wek2)

		print "[1] vs [1/4*all_len+1]..."
		str_str_indicators_str_wek3 = []
		for i in range(NUM_SIMULATION):
			elements = initialize(AVERAGE, SD_OF_POPULATION, NUM_TEAMS)
			str_str_indi_0 = str_str_indicator(elements)
			elements = test(elements, str_wek_pairing3, ROUNDS, RATIO_DIFF_ON_SCORE, SD_OF_SCORES)
			#show_rankings(elements)
			str_str_indi = str_str_indicator(elements)
			#print str_str_indi
			str_str_indicators_str_wek3.append(str_str_indi/str_str_indi_0*100)
		print str_str_indicators_str_wek3
		#plt2.bar_1d(str_str_indicators_str_wek3)
		plt2.hist([str_str_indicators_random, str_str_indicators_power, str_str_indicators_str_wek, str_str_indicators_str_wek2, str_str_indicators_str_wek3])	
	"""
	