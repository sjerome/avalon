from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect

import smtplib
import random
import uuid

PLAYERS = ['prankcalls11@gmail.com', 'prankcalls11@gmail.com', 'prankcalls11@gmail.com','prankcalls11@gmail.com','prankcalls11@gmail.com','prankcalls11@gmail.com']
CARDS = ['MARLIN', 'PERISCOPE', 'GOOD', 'GOOD', 'BAD', 'BAD']
PASSWORDS = [str(uuid.uuid4()) for i in xrange(len(PLAYERS))]
PERSON = 0
CURRENT_ROUND = 0
ROUND = {0:2, 1:3, 2:4, 3:3, 4:3}
VOTES = {}
MISSION_VOTES = {}
CHOSEN_PLAYERS = []
DEALT = []

ROUNDS = {}

# Create your views here.
@csrf_protect
def index(request):
	global ROUNDS
	context = {'whos_up': whos_up(), 'chosen_players' : chosen(), 'votes': votes(), 'rounds' : ROUNDS.items()}
	return render(request, "index.html", context);

def whos_up():
	global PERSON, PLAYERS
	return PLAYERS[PERSON]

def chosen():
	global CHOSEN_PLAYERS
	return CHOSEN_PLAYERS

def votes():
	global VOTES, PLAYERS
	return VOTES if len(VOTES.keys()) == len(PLAYERS) else VOTES.keys()

def mission_votes():
	global MISSION_VOTES, CHOSEN_PLAYERS
	if len(MISSION_VOTES.keys()) == len(CHOSEN_PLAYERS):
		values = MISSION_VOTES.values()
		random.shuffle(values)
		return values
	else:
		return MISSION_VOTES.keys()

@csrf_protect
def new_game(request):
	if request.GET['password'] != 'hi':
		return HttpResponse('<html> No. Sorry. </html>')

	global PLAYERS, CARDS, PASSWORDS, DEALT

	PLAYERS = [request.GET['player%s'%i] for i in xrange(1,7)]
	PASSWORDS = ['' for i in xrange(len(PLAYERS))]

	random.shuffle(CARDS)
	DEALT = zip(PLAYERS, CARDS, PASSWORDS)
	bad = filter(lambda x : x[1] == 'BAD', DEALT)
	marlin = filter(lambda x : x[1] == 'MARLIN', DEALT)
	periscope = filter(lambda x : x[1] == 'PERISCOPE', DEALT)
	print DEALT

	for player, card, password in DEALT:
		fromaddr = 'avalon.messenger@gmail.com'
		toaddrs = player
		msg = 'You are %s.\nYour password is %s.'%(card, password)
		if card == 'BAD' or card == 'MARLIN':
			msg = msg + '\n' + 'Bad players: %s, %s'%(bad[0][0], bad[1][0])
		if card == 'PERISCOPE':
			msg = msg + '\n' + 'Marlin: %s'%marlin[0][0]

		username = 'avalon.messenger@gmail.com'
		password = 'avalonmessenger'

		# server = smtplib.SMTP('smtp.gmail.com:587')
		# server.starttls()
		# server.login(username,password)
		# server.sendmail(fromaddr, toaddrs, msg)
		# server.quit()

	return HttpResponse('<html>' + str(PLAYERS) +'</html>')

def is_authenticated(request):
	global DEALT
	hand = filter(lambda x : x[0] == request.GET['player'], DEALT)
	person, password = hand[0][0], hand[0][2]
	return request.GET['password'] == password and request.GET['player'] == person

def choose_players(request):
	global PERSON, PLAYERS, CHOSEN_PLAYERS, ROUND

	if not is_authenticated(request) or PLAYERS[PERSON] != request.GET['player']:
		return HttpResponse('<html> Stop going for someone else. </html>')

	chosen_players = request.GET['players'].split(',')

	if len(chosen_players) != ROUND[CURRENT_ROUND]:
		return HttpResponse('<html> Wrong number of players. </html>')
	for play in chosen_players:
		if len(filter(lambda x : x == play, PLAYERS)) != 1:
			return HttpResponse('<html> Bad Players </html>')

	CHOSEN_PLAYERS = chosen_players
	return HttpResponse('<html> You chose %s. </html>'%str(CHOSEN_PLAYERS))

def vote(request):
	global VOTES
	if not is_authenticated(request):
		return HttpResponse('<html> Stop going for someone else. </html>')
	if request.GET['vote'] != 'A' and request.GET['vote'] != 'R':
		return HttpResponse('<html> Bad Vote </html>')

	VOTES[request.GET['player']] = request.GET['vote']
	
	return HttpResponse('<html> Voted. </html>')

def refresh(request):
	global VOTES, PLAYERS
	if len(VOTES.keys()) != 6 or len(filter(lambda x : x == 'R', VOTES.values())) <= 2: 
		return HttpResponse('Fucking Liar')
	else:
		VOTES = {}
	PERSON = (PERSON + 1) % len(PLAYERS)

	return HttpResponse('K.')

def mission(request):
	global CHOSEN_PLAYERS, MISSION_VOTES

	if not is_authenticated(request) or request.GET['player'] not in CHOSEN_PLAYERS:
		return HttpResponse('<html> Stop going for someone else. </html>')

	if request.GET['vote'] != 'S' and request.GET['vote'] != 'F':
		return HttpResponse('<html> Bad Vote [S|F] </html>')
	
	MISSION_VOTES[request.GET['player']] = request.GET['vote']
	if (len(MISSION_VOTES.keys()) == len(CHOSEN_PLAYERS)):
		refresh_after_mission()

	return HttpResponse('<html> Voted. </html>')

def refresh_after_mission():
	global ROUNDS, CURRENT_ROUND, MISSION_VOTES, CHOSEN_PLAYERS, VOTES, PERSON
	ROUNDS[CURRENT_ROUND] = MISSION_VOTES.values()
	CURRENT_ROUND += 1
	PERSON += 1
	CHOSEN_PLAYERS = []
	VOTES = {}