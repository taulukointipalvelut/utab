# -*- coding: utf-8 -*-

class Team:
	def __init__(self, code, name, debater_names, institution_scale, institutions):
		self.code = code
		self.name = name
		self.institutions = [institution for institution in institutions if institution != '']
		self.institution_scale = institution_scale
		self.debaters = [Debater(debater_name) for debater_name in debater_names]
		self.past_opponents = []
		self.past_sides = []
		self.wins = []
		self.scores = []
		self.score = 0
		self.margin = 0
		#self.bubble = 0
		self.ranking = 0
		#self.unfairity = 0
		self.available = True
		#self.side_priority = None

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
		self.scores.append(score)
		self.score = score
		self.wins.append(win)
		self.margin += margin

class Debater:
	def __init__(self, name):
		self.name = name
		self.score_lists = []
		self.scores = []
	"""

	def finishing_process(self, opponent, team_score, side, win, margin):
		self.past_opponents.append(opponent)
		self.past_sides.append(side)
		self.team_scores.append(team_score)
		self.team_score = team_score
		self.wins.append(win)
		self.margin += margin
	"""

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
		if set(self.grid.teams) == set(other.grid.teams) and self.chair == other.chair:
			return True
		else:
			return False

	def __ne__(self, other):
		if set(self.grid.teams) != set(other.grid.teams) or self.chair != other.chair:
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
	def __init__(self, name, reputation, judge_test, institutions, conflict_teams):
		self.name = name
		self.reputation = reputation
		self.judge_test = judge_test
		self.institutions = [institution for institution in institutions if institution != '']
		self.absent = False#absent?
		self.score = 0
		self.scores = []
		self.watched_debate_score = 0
		self.watched_debate_scores = []
		self.watched_debate_ranks = []
		self.watched_teams = []
		self.active_num = 0
		self.active_num_as_chair = 0
		self.ranking = 0
		self.active = False
		self.evaluation = 0
		self.conflict_teams = [conflict_team for conflict_team in conflict_teams if conflict_team != '']

	def finishing_process(self, score, teams, watched_debate_score, chair):
		self.score = score
		self.scores.append(score)
		self.active_num += 1
		self.active = False
		if chair:
			self.active_num_as_chair += 1
		self.watched_teams.extend(teams)
		self.watched_debate_score = watched_debate_score
		self.watched_debate_scores.append(watched_debate_score)

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
		self.comparison1 = 0
		self.comparison2 = 0
		self.warnings = []
		self.large_warnings = []
		self.past_match = 0
		self.power_pairing = None
		self.pair_grid = None
		self.bubble_ranking = 0
		self.bubble = 10

	def __eq__(self, other):
		if set(self.teams) == set(other.teams):
			return True
		else:
			return False

	def __ne__(self, other):
		if set(self.teams) != set(other.teams):
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
		self.matchups_no = None
		self.large_warnings = []

class Lattice_list_info:
	def __init__(self):
		self.strong_strong_indicator = None
		self.num_of_warnings = None
		self.large_warnings = []
		self.allocation_no = None