import random, sys

class Card:
	# A simple class representing a card
	value, suite = 0, 0
	def __init__(self, v, s):
		self.value = v
		self.suite = s
	def __repr__(self):
		return str(self.value) + " of " + self.suite
	def __str__(self):
		return str(self.value) + " of " + self.suite

class Deck:
	# A simple class representing a deck of cards
	values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
	suites = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
	cards = []
	# init function. Create the deck
	def __init__(self):
		for value in self.values:
			for suite in self.suites:
				self.cards.append(Card(value, suite))
	# Shuffle the cards
	def shuffle(self):
		print "The dealer shuffles the deck\n"
		random.shuffle(self.cards)
	def draw(self, num):
		ret = []
		for card in self.cards[:num]:
			ret.append(card)
			self.cards.remove(card)
		return ret

class Person:
	hand = []
	def receiveCards(self, cards):
		for card in cards:
			self.hand.append(card)
	def hit(self, card):
		print "\nHit me!"
		self.hand.append(card)
		print "\nDealt:"
		print card
		print "\nYour hand:"
		print self
		if self.total() > 21:
			print "BUSTED"
		elif self.total() == 21:
			print "21!"
		else:
			print "Total: %d" % self.total()
	def total(self):
		total = 0
		for card in self.hand:
			if(card.value in ('Jack', 'Queen', 'King')):
				total += 10
			elif card.value == 'Ace':
				if(total + 11 > 21):
					total = total + 1
				else: 
					total = total + 11
			else: 
				total += card.value
		return total
	def __repr__(self):
		return self.hand
	def __str__(self):
		return '%s' % ', '.join(map(str, self.hand))

class Dealer(Person):
	hand = []
	deck = []
	# init function. Get a deck
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
	def deal(self, players):
		for _ in range(2):
			for person in players:
				person.receiveCards(self.deck.draw(1))
	def hit(self, card):
		print "\nThe dealer takes a card"
		self.hand.append(card)
		print "\nDealt:"
		print card
		print "\nThe dealer's hand:"
		print '%s' % ', '.join(map(str, self.hand))
		if self.total() > 21:
			print "\nOh no! BUSTED"
		elif self.total() == 21:
			print "\nYES! 21!"
		else:
			print "Total: %d" % self.total()
	def hitPlayer(self, person):
		person.hit(self.deck.draw(1)[0])
	def revealSecond(self):
		return self.hand[1]
	def revealAll(self):
		return '%s' % ', '.join(map(str, self.hand))
	def __repr__(self):
		return self.hand
	def __str__(self):
		return str(self.hand[0])

class Game:
	dealer, player = 0, 0
	players = []
	def __init__(self):
		print "===================================="
		print "        WELCOME TO BLACKJACK        "
		print "===================================="
		print "\n\nThe dealer beckons you over. \"Come play a game!\"\n"
	def playGame(self):
		self.dealer = Dealer()
		self.players.append(self.dealer)
		self.player = Person()
		self.players.append(self.player)
		self.deal()
	def deal(self):
		print "The dealer deals the deck\n"
		self.dealer.deal(self.players)
		self.showCards()
	def showCards(self):
		print "You were dealt:"
		print self.player
		print "\nThe dealer shows:"
		print self.dealer
		self.playerMoves()
	def playerMoves(self):
		move = ""
		while self.player.total() < 21 and move not in ("No", "no"):
			move = raw_input("\nWould you like to hit? Yes or No: ")
			if move in ("Yes", "yes"):
				self.dealer.hitPlayer(self.player)
		if self.player.total() == 21:
			print "21! Hell yeah!"
		elif self.player.total() > 21:
			print "\nBUSTED! You lost"
			sys.exit()
		else:
			print "\nYour total is %d - let's see what the dealer has!" % self.player.total()
		self.dealerMoves()
	def dealerMoves(self):
		print "\nThe dealer reveals his next card:"
		print self.dealer.revealSecond()
		print "\nHis hand is:"
		print self.dealer.revealAll()
		if self.dealer.total() == 21:
			print "\nBLACKJACK!\n"
			if self.player.total() == 21:
				print "It's a tie!"
				sys.exit()
			else:
				print "Dealer wins, try again"
				sys.exit()	
		elif self.dealer.total() < 17:
			while self.dealer.total() <= 17:
				self.dealer.hitPlayer(self.dealer)
		self.results()
	def results(self):
		if self.dealer.total() == 21:
			if self.player.total() == 21:
				print "\nIt's a tie!"
			else:
				print "\nDealer wins with 21, try again"
		elif self.dealer.total() > 21 and self.player.total() <= 21:
			print "\nDealer BUSTED! You win!"
		elif self.dealer.total() < 21 and self.dealer.total() < self.player.total():
			print "\nYou were closer to 21! You win!"
		sys.exit()


game = Game()
game.playGame()
