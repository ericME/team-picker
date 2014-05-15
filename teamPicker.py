import random
import math

sr = random.SystemRandom()
random.randrange = sr.randrange
random.randint = sr.randint

class Team:
	def __init__(self, name, rank):
		self.name = name
		self.rank = rank
		self.games_won = 0

	def won_a_game(self):
		self.games_won += 1

	def reset_games(self):
		self.games_won = 0

class Round:
	def __init__(self, number, division):
		self.number = number
		self.division = division
		self.nextround = []
		self.currentround = []

	def play_round(self):
		print "*** playing round ", self.number, " ***"
		for i, team in enumerate(self.division):
			self.currentround.append(team)
			if i % 2 == 1:
				self.nextround.append(play_series(self.currentround))
				self.currentround = []

def play_rounds(division, max_rounds = 3):
	rnd = Round(1, division)
	rnd.play_round()
	for i in xrange(2,max_rounds + 1):
		rnd = Round(i, rnd.nextround)
		rnd.play_round()
	return rnd.nextround[0]

def play_series(teams, max_games = 7):
	series_clinched = max_games/2 + 1
	for team in teams:
		team.reset_games()
	for game in xrange(1, max_games + 1):
		play_game(teams)
		for team in teams:
			if team.games_won == series_clinched:
				print team.name, "wins in: ", game
				return team

		
def play_game(teams, lo_range = 1, hi_range = 101):
	#choose a winner at random, with a slight preference for the higher ranked team
	winner = random.randrange(lo_range, hi_range)
	a, b = 0, 1
	if teams[b].rank > teams[a].rank:
		a, b = 1, 0
	rank_delta = abs(teams[a].rank - teams[b].rank)
	#print winner, hi_range, lo_range, rank_delta, teams[a].name, teams[a].rank, teams[b].name, teams[b].rank #debug
	if winner <= (hi_range - lo_range)/2 + rank_delta:
		teams[a].won_a_game()
	else:
		teams[b].won_a_game()

#western conf teams
COL = Team('COL', 1)
MIN = Team('MIN', 4)
STL = Team('STL', 2)
CHI = Team('CHI', 3)
ANA = Team('ANA', 1)
DAL = Team('DAL', 4)
SJS = Team('SJS', 2)
LAK = Team('LAK', 3)

#eastern conf teams
BOS = Team('BOS', 1)
DET = Team('DET', 4)
TBL = Team('TBL', 2)
MTL = Team('MTL', 3)
PIT = Team('PIT', 1)
CBJ = Team('CBJ', 4)
NYR = Team('NYR', 2)
PHI = Team('PHI', 3)

#set up the conferences, in playoff order
west = [COL, MIN,\
		STL, CHI,\
		ANA, DAL,\
		SJS, LAK]

east = [BOS, DET,\
		TBL, MTL,\
		PIT, CBJ,\
		NYR, PHI]

#determine conference champs
western_champs = play_rounds(west)
eastern_champs = play_rounds(east)

print "### and now ", western_champs.name, " will play ", eastern_champs.name, "for the stanley cup ###"

#play for the cup
lord_stanley_goes_to = play_series([western_champs, eastern_champs])

print "!!! the cup goes to:", lord_stanley_goes_to.name, " !!!"