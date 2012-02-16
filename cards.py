from random import choice

class Card:
	'''Card impliments a playing card.
		It is constructed with an integer in the range [0,51], which is then stored
		as a value, suit pair as divmod(integer,13).
		
		Cards can be compared with <,>,<=,>=,==, and !=. These comparisons are ONLY with regard to the cards' values.
		For instance, the ace of spades and the ace of clubs are "equal" according to ==. 
		The 10 of clubs is "greater than" the 9 of spades according to >.
		If you want value and suit rankings, use card1.ltstrict(card2), card1.lestrict(card2), etc.

		card.string(self) returns a string "'value' of 'suit'".

		Card has two constant dictionaries, Card.suits and Card.values, that
		convert the numerical suits and values to strings. For instance,
		Card.suits[0] = 'clubs'.

		Card.list_string(card_list)
			Returns a string '"value0" of "suit0", "value1" of "suit1", ...' for all the cards in card_list.
		'''
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
	'''Deck impliments a deck of playing cards using the Card class.

		Three members:

		Deck.deck 	
			A list of 52 Cards. Stored in numerical order (unshuffled).

		Deck.deal_one()
			Randomly deals out a single Card, selected using random.choice(), and removes it from the deck.

		Deck.deal([num_players=1,[num_cards_per_player=1]])
			With no arguments (or both arguments = 1), returns a single card.
			If one argument is = 1 and the other > 1, returns a list of cards.
			If both arguments are > 1, returns a length-num_players list of length-num_cards_per_player lists of Cards.
		'''
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