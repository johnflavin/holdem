from random import choice

'''class cards.Card(int integer)
	Impliments a playing card.
	It is constructed with an integer in the range [0,51], which is then stored
	as a value, suit pair as divmod(integer,13).

	self.suit
		An integer in the range 0--3 inclusive representing the suit of a card, ordered clubs, diamonds, hearts, spades.

	self.value
		An integer in the range 0--12 inclusive representing the value of a card (Aces high).

	self.integer_val
		An integer in the range 0--51 inclusive representing the unique value of a card. 
		self.suit, self.value = divmod( self.integer_val, 13 )

	self.name
		A string of the value of the card. For example, if self.value is 0, self.name is '2'.

	self.suitname
		A string of the suit of the card. For example, if self.suit is 0, self.suitname is 'clubs'.
	
	Cards can be compared with <,>,<=,>=,==, and !=. These comparisons are ONLY with regard to the cards' values.
	For instance, the ace of spades and the ace of clubs are "equal" according to ==. 
	The 10 of clubs is "greater than" the 9 of spades according to >, even though the 9 of spades has a higher integer_val than the 10 of clubs.
	If you want to compare the integer_vals, use card1.ltstrict(card2), card1.lestrict(card2), etc.

	card.string(self) returns a string formatted as "'value' of 'suit'".

	The Card class stores two constant dictionaries, Card.suits and Card.values, that
	convert the numerical suits and values to strings. For instance,
	Card.suits[0] = 'clubs'.

	The Card class has a constant method,
	Card.list_string(card_list)
		Returns a string 'value0 of suit0, value1 of suit1, ...' for all the cards in card_list.

class cards.Deck 
	Impliments a deck of playing cards using the Card class.
	When initialized (no arguments), creates a "deck" of 52 integers. When these integers are dealt (with random.choice(deck)) they are returned
	as Card objects.

	self.deck 	
		A list of 52 Cards. Stored in numerical order (unshuffled).

	self.deal_one()
		Randomly deals out a single Card, selected using random.choice(), and removes it from the deck.

	self.deal([num_players=1,[num_cards_per_player=1]])
		With no arguments (or both arguments = 1), returns a single card.
		If one argument is = 1 and the other > 1, returns a list of cards.
		If both arguments are > 1, returns a length-num_players list of length-num_cards_per_player lists of Cards.
	'''

class Card:

	suits = {0:'clubs', 1:'diamonds', 2:'hearts', 3:'spades'}
	values = {0:'2',1:'3',2:'4',3:'5',4:'6',5:'7',6:'8',7:'9',8:'10',9:'J',10:'Q',11:'K',12:'A'}

	def __init__(self,integer):
		self.integer_val = integer
		self.suit, self.value = divmod(integer,13)
		self.name = self.values[self.value]
		self.suitname = self.suits[self.suit]

	def __lt__(self, other):
		return self.value < other.value

	def __le__(self, other):
		return self.value <= other.value

	def __eq__(self, other):
		return self.value == other.value

	def __ne__(self, other):
		return self.value != other.value

	def __gt__(self, other):
		return self.value > other.value

	def __ge__(self, other):
		return self.value >= other.value

	def ltstrict(self, other):
		if self.value == other.value:
			return self.suit < other.suit
		return self.value < other.value

	def lestrict(self, other):
		if self.value == other.value:
			return self.suit <= other.suit
		return self.value <= other.value

	def eqstrict(self, other):
		return self.integer_val == other.integer_val

	def nestrict(self, other):
		return self.integer_val != other.integer_val

	def gtstrict(self, other):
		if self.value == other.value:
			return self.suit > other.suit
		return self.value > other.value

	def gestrict(self, other):
		if self.value == other.value:
			return self.suit >= other.suit
		return self.value >= other.value

	def string(self):
		return '{} of {}'.format(self.name,self.suitname)

	def list_string(card_list):
		return ', '.join( [card.string() for card in card_list] )

class Deck:
	def __init__(self):
		self.deck = list(range(52))

	def deal(self,num_players=1,num_cards_per_player=1):
		if num_players > 1 and num_cards_per_player > 1:
			dealt_cards = []
			for i in range(num_players):
				player_cards = []

				for j in range(num_cards_per_player):
					player_cards.append( self.deal_one() )

				dealt_cards.append(player_cards)
		elif num_players > 1 or num_cards_per_player > 1:
			dealt_cards = []*(num_players*num_cards_per_player)

			for j in range(num_cards_per_player):
				dealt_cards.append( self.deal_one() )
		else:
			dealt_cards = self.deal_one()

		return dealt_cards
	
	def deal_one(self):
		integer = choice(self.deck)

		self.deck.remove(integer)

		return Card(integer)