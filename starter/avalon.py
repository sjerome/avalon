import smtplib
import random
import uuid

PLAYERS = ['prankcalls11@gmail.com', 'prankcalls11@gmail.com', 'prankcalls11@gmail.com','prankcalls11@gmail.com','prankcalls11@gmail.com','prankcalls11@gmail.com']
CARDS = ['MARLIN', 'PERISCOPE', 'GOOD', 'GOOD', 'BAD', 'BAD']
PASSWORDS = [str(uuid.uuid4())[:8] for i in xrange(len(PLAYERS))]

if __name__ == '__main__':
	random.shuffle(CARDS)
	dealt = zip(PLAYERS, CARDS, PASSWORDS)
	bad = filter(lambda x : x[1] == 'BAD', dealt)
	marlin = filter(lambda x : x[1] == 'MARLIN', dealt)
	periscope = filter(lambda x : x[1] == 'PERISCOPE', dealt)

	for player, card, password in dealt:
		fromaddr = 'avalon.messenger@gmail.com'
		toaddrs = player
		msg = 'You are %s.\nYour password is %s.'%(card, password)
		if card == 'BAD' or card == 'MARLIN':
			msg = msg + '\n' + 'Bad players: %s, %s'%(bad[0][0], bad[1][0])
		if card == 'PERISCOPE':
			msg = msg + '\n' + 'Marlin: %s'%marlin[0][0]

		username = 'avalon.messenger@gmail.com'
		password = ''

		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()