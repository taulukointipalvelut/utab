# -*- coding: utf-8 -*-
import math

class Team:
	def __init__(self, code, name, debater_names, institution_scale, institutions):
		self.code = code
		self.name = name
		self.institutions = [institution for institution in institutions if institution != '']
		self.institution_scale = institution_scale
		self.debaters = [Debater(debater_name) for debater_name in debater_names]
		self.past_opponents = []
		self.past_sides = []
		self.past_sides_sub = []
		self.wins = []
		self.wins_sub = []
		self.scores = []
		self.scores_sub = []
		self.score = 0
		self.margin = 0
		#self.bubble = 0
		self.ranking = 0
		#self.unfairity = 0
		self.available = True
		#self.side_priority = None

	def average(self):
		if len(self.scores) == 0:
			return 0
		else:
			return sum(self.scores)/len(self.scores)

	def sum_scores(self):
		return sum(self.scores)

	def sum_wins(self):
		return sum(self.wins)

	def sd(self):
		if len(self.scores) == 0:
			return 0
		else:
			avrg = self.average()
			return math.sqrt(sum([(score - avrg)**2 for score in self.scores])/len(self.scores))

	def __eq__(self, other):
		return self.code == other

	def __ne__(self, other):
		return self.code != other

	def __hash__(self):
		hash_value = self.code + (self.ranking<<10) + (len(self.institutions)<<20)
		for k, debater in enumerate(self.debaters):
			hash_value += len(debater.name)<<(20+k*10)
		return hash_value

	def finishing_process(self, opponent, score, side, win, margin):
		self.past_opponents.extend(opponent)
		self.past_sides.append(side)
		self.past_sides_sub.append(side)
		self.scores.append(score)
		self.score = score
		self.wins.append(win)
		self.scores_sub.append(score)
		self.wins_sub.append(win)
		self.margin += margin

	def dummy_finishing_process(self):
		self.scores_sub.append('n/a')
		self.wins_sub.append('n/a')
		self.past_sides_sub.append('n/a')

class Debater:
	def __init__(self, name):
		self.name = name
		self.score_lists = []
		self.scores = []
		self.score_lists_sub = []
		self.scores_sub = []
		self.rankings = []
		self.rankings_sub = []

	def average(self, style_cfg):
		score_weight = style_cfg["score_weight"]
		average_list = []
		for i in range(len(self.score_lists)):
			avrg_in_r = self.average_in_round(i+1, style_cfg)
			if avrg_in_r != 'n/a':
				average_list.append(avrg_in_r)

		if len(average_list) == 0:
			return 0
		else:
			return sum(average_list)/len(average_list)

	def average_in_round(self, round_num, style_cfg):
		score_weight = style_cfg["score_weight"]
		average_list = []
		weight = 0
		avrg = 0
		if 'n/a' in self.score_lists[round_num-1]:
			return 'n/a'
		else:
			for score, w in zip(self.score_lists[round_num-1], score_weight):
				if score != 0:
					avrg += score
					weight += w
			if weight != 0:
				return avrg/weight
			else:
				return 0

	def sum_scores(self, style_cfg):
		s = 0
		for i in range(len(self.score_lists)):
			avrg_in_r = self.average_in_round(i+1, style_cfg)
			s += avrg_in_r
		return s

	def sd(self, style_cfg):
		avrg = self.average(style_cfg)
		sd = 0
		n = 0
		for i in range(len(self.score_lists)):
			avrg_in_r = self.average_in_round(i, style_cfg)
			if avrg_in_r != 'n/a':
				sd += (avrg_in_r-avrg)**2
				n += 1
		if n == 0:
			return 0
		else:
			return math.sqrt(sd/n)

	def finishing_process(self, score_list, score):
		self.score_lists.append(score_list)
		self.score_lists_sub.append(score_list)
		self.scores.append(score)
		self.scores_sub.append(score)

	def __eq__(self, other):
		return self.name == other

	def __ne__(self, other):
		return self.name != other

class Venue:
	def __init__(self, name, priority):
		self.name = name
		self.available = True
		self.priority = priority

class Lattice:
	def __init__(self, grid, chair):
		self.grid = grid
		self.chair = chair
		self.panel = []
		self.adoptbits = 0
		self.adoptbitslong = 0
		self.adoptbits_strict = 0
		self.adoptness1 = 0
		self.adoptness2 = 0
		self.adoptness1long = 0
		self.adoptness2long = 0
		self.adoptness_strict1 = 0
		self.adoptness_strict2 = 0
		self.adoptness_weight1 = 0
		self.adoptness_weight2 = 0
		self.comparison1 = 0
		self.comparison2 = 0
		self.available = True
		self.warnings = []
		self.large_warnings = []
		self.venue = None
		#self.avoid_by_conflict = False
		#self.adj_unfair = False
		#self.strength_coordinating = 0
		#self.uncoordinateness = 0
		#self.conflict = False
		#self.personal_conflict = False

	def __eq__(self, other):
		if self.grid.teams == other.grid.teams and self.chair == other.chair:
			return True
		else:
			return False

	def __ne__(self, other):
		if self.grid.teams != other.grid.teams or self.chair != other.chair:
			return True
		else:
			return False

	def __hash__(self):
		hash_value = ord(self.chair.name[0])
		for k, team in enumerate(self.grid.teams):
			hash_value += team.code<<10*k
		return hash_value

	def grid_type(self):
		return self.__class__.__name__

class Adjudicator:
	def __init__(self, code, name, reputation, judge_test, institutions, conflict_teams):
		self.code = code
		self.name = name
		self.reputation = reputation
		self.judge_test = judge_test
		self.institutions = [institution for institution in institutions if institution != '']
		self.absent = False#absent?
		self.score = 0
		self.scores = []
		self.scores_sub = []
		self.watched_debate_score = 0
		self.watched_debate_scores = []
		self.watched_debate_scores_sub = []
		self.watched_debate_ranks = []
		self.watched_debate_ranks_sub = []
		self.watched_teams = []
		self.watched_teams_sub = []
		self.active_num = 0
		self.active_num_as_chair = 0
		self.ranking = 0
		self.active = False
		self.evaluation = 0
		self.conflict_teams = [conflict_team for conflict_team in conflict_teams if conflict_team != '']

	def __hash__(self):
		hash_value = self.code + (self.ranking<<10) + (int(self.reputation)<<13) + (int(self.judge_test)<<16)
		for k, institution in enumerate(self.institutions):
			hash_value += len(institution)<<(20+k*10)
		return hash_value

	def average(self):
		if len(self.scores) == 0:
			return 0
		else:
			return sum(self.scores)/len(self.scores)

	def sum_scores(self):
		return sum(self.scores)

	def sd(self):
		if len(self.scores) == 0:
			return 0
		else:
			avrg = self.average()
			return math.sqrt(sum([(score - avrg)**2 for score in self.scores])/len(self.scores))

	def finishing_process(self, score, teams, watched_debate_score, chair):
		self.score = score
		self.scores.append(score)
		self.scores_sub.append(score)
		self.active_num += 1
		self.active = False
		if chair:
			self.active_num_as_chair += 1
		self.watched_teams.extend(teams)
		self.watched_teams_sub.extend(teams)
		self.watched_debate_score = watched_debate_score
		self.watched_debate_scores.append(watched_debate_score)
		self.watched_debate_scores_sub.append(watched_debate_score)

	def dummy_finishing_process(self, teamnum):
		self.scores_sub.append('n/a')
		self.watched_debate_scores_sub.append('n/a')
		self.watched_teams_sub.extend(['n/a' for i in range(teamnum)])

	def __eq__(self, other):
		return self.name == other

	def __ne__(self, other):
		return self.name != other

class Grid:
	def __init__(self, teams):
		self.teams = teams
		if len(list(set(self.teams))) != len(self.teams):
			self.available = False
		else:
			self.available = True
		self.adoptbits = 0
		self.adoptbitslong = 0
		self.adoptbits_strict = 0
		self.adoptness1 = 0
		self.adoptness2 = 0
		self.adoptness1long = 0
		self.adoptness2long = 0
		self.adoptness_strict1 = 0
		self.adoptness_strict2 = 0
		self.adoptness_weight1 = 0
		self.adoptness_weight2 = 0
		self.comparison1 = 0
		self.comparison2 = 0
		self.warnings = []
		self.large_warnings = []
		self.past_match = 0
		self.power_pairing = None
		self.related_grids = []
		self.bubble_ranking = 0
		self.bubble = 10

	def __eq__(self, other):
		if self.teams == other.teams:
			return True
		else:
			return False

	def __ne__(self, other):
		if self.teams != other.teams:
			return True
		else:
			return False

	def __hash__(self):
		hash_value = 0
		for k, team in enumerate(self.teams):
			hash_value += team.code<<10*k
		return hash_value

	def grid_type(self):
		return self.__class__.__name__

class Grid_list_info:
	def __init__(self):
		self.power_pairing_indicator = None
		self.adopt_indicator = None
		self.adopt_indicator_sd = None
		self.adopt_indicator2 = None
		self.same_institution_indicator = None
		self.num_of_warnings = None
		self.scatter_indicator = None
		self.matchups_no = None
		self.large_warnings = []
		self.comment = ""

class Lattice_list_info:
	def __init__(self):
		self.strong_strong_indicator = None
		self.num_of_warnings = None
		self.large_warnings = []
		self.allocation_no = None
		self.comment = ""