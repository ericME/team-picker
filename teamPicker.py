import random
import math

#monkey fix the random module
sr = random.SystemRandom()
random.randrange = sr.randrange
random.randint = sr.randint

class Team:
	def __init__(self, name, rank, sapg, gapg, sfpg, gfpg):
		self.name = name
		self.rank = rank
		self.sapg = sapg #shots against /game
		self.gapg = gapg #goals against /game
		self.sfpg = sfpg #shots for /game
		self.gfpg = gfpg #goals for /game
		self.stop = gapg/sapg*100 #normalized probablity of stopping the shot
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
		#print ("*** playing round ", self.number, " ***")
		for i, team in enumerate(self.division):
			self.currentround.append(team)
			if i % 2 == 1:
				self.nextround.append(play_series(self.currentround))
				self.currentround = []

def play_rounds(division, max_rounds = 3):
	rnd = Round(1, division)
	rnd.play_round()
	for i in range(2,max_rounds + 1):
		rnd = Round(i, rnd.nextround)
		rnd.play_round()
	return rnd.nextround[0]

def play_series(teams, max_games = 7):
	series_clinched = math.floor(max_games/2 + 1)
	for team in teams:
		team.reset_games()
	for game in range(1, max_games + 1):
		play_game(teams)
		for team in teams:
			if team.games_won >= series_clinched:
				#print (team.name, "wins in: ", game)
				return team
	print ("error")
	exit(0)

		
def play_game(teams, lo_range = 1, hi_range = 101):
	goals = [0,0]
	a, b = 0, 1
	if teams[b].rank > teams[a].rank:
		a, b = 1, 0
	rank_delta = abs(teams[a].rank - teams[b].rank)
	for shots in range(int(teams[a].sfpg)):
		chance = random.randrange(lo_range, hi_range)
		if teams[b].stop > chance:
			goals[a] += 1
	for shots in range(int(teams[b].sfpg)):
		chance = random.randrange(lo_range, hi_range)
		if teams[a].stop > chance:
			goals[b] += 1
	#print (winner, hi_range, lo_range, rank_delta, teams[a].name, teams[a].rank, teams[b].name, teams[b].rank #debug)
	if goals[a] > goals[b]:
		teams[a].won_a_game()
	elif goals[b] > goals[a]:
		teams[b].won_a_game()
	else:
		winner = random.randrange(lo_range, hi_range)
		if winner < (hi_range - lo_range)/2 + rank_delta:
			teams[a].won_a_game()
		else:
			teams[b].won_a_game()
	#print (teams[a].name, goals[a], teams[b].name, goals[b]) #debug

#western conf teams
COL = Team('COL', 1, 32.7, 2.63, 29.5, 2.99)
MIN = Team('MIN', 4, 27.7, 2.41, 26.6, 2.43)
STL = Team('STL', 2, 26.4, 2.29, 35.8, 2.91)
CHI = Team('CHI', 3, 27.2, 2.59, 33.1, 3.18)
ANA = Team('ANA', 1, 28.7, 2.48, 31.3, 3.21)
DAL = Team('DAL', 4, 30.4, 2.72, 31.7, 2.82)
SJS = Team('SJS', 2, 27.8, 2.35, 34.8, 2.91)
LAK = Team('LAK', 3, 26.2, 2.05, 31.6, 2.41)

#eastern conf teams
BOS = Team('BOS', 1, 29.1, 2.09, 31.9, 3.15)
DET = Team('DET', 4, 29.3, 2.70, 30.0, 2.65)
TBL = Team('TBL', 2, 29.2, 2.55, 29.8, 2.83)
MTL = Team('MTL', 3, 31.0, 2.45, 28.4, 2.55)
PIT = Team('PIT', 1, 28.8, 2.49, 29.9, 2.95)
CBJ = Team('CBJ', 4, 30.8, 2.61, 29.6, 2.76)
NYR = Team('NYR', 2, 29.4, 2.32, 33.2, 2.61)
PHI = Team('PHI', 3, 30.6, 2.77, 30.4, 2.84)

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
# western_champs = play_rounds(west)
# eastern_champs = play_rounds(east)

# print ("### and now ", western_champs.name, " will play ", eastern_champs.name, "for the stanley cup ###")

# #play for the cup
# lord_stanley_goes_to = play_series([western_champs, eastern_champs])

# print ("!!! the cup goes to:", lord_stanley_goes_to.name, " !!!")

winners = []
m = 1000
for i in range (m):
	western_champs = play_rounds(west)
	eastern_champs = play_rounds(east)
	#play for the cup
	winners.append(play_series([western_champs, eastern_champs]).name)
print ("after", m, "iterations, the winner is:")
print (max(set(winners), key=winners.count))
for team in west:
	print (team.name, winners.count(team.name))
for team in east:
	print (team.name, winners.count(team.name))