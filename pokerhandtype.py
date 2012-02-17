class PokerHandType:
	hand_type_strings = { 0:'High Card', 1:'Pair', 2:'Two Pair', 3:'Trips', 4:'Straight', \
			5:'Flush', 6:'Full House', 7:'Quads', 8:'Straight Flush' }

	rank = -1

	def __init__(self,card_list):
		self.cards = card_list

	def __lt__(self, other):
		if self.rank == other.rank:
			return self.cards < other.cards
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			return self.cards <= other.cards
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			return self.cards == other.cards

	def __ne__(self, other):
		if self.rank == other.rank:
			return self.cards != other.cards
		return self.rank != other.rank

	def __gt__(self, other):
		if self.rank == other.rank:
			return self.cards > other.cards
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			return self.cards >= other.cards
		return self.rank >= other.rank

	def string(self):
		return self.hand_type_strings[self.rank]

class HighCard(PokerHandType):
	
	rank = 0

class Pair(PokerHandType):
	
	rank = 1

class TwoPair(PokerHandType):
	
	rank = 2

class Trips(PokerHandType):
	
	rank = 3

class Straight(PokerHandType):
	
	rank = 4

class Flush(PokerHandType):
	
	rank = 5

class FullHouse(PokerHandType):
	
	rank = 6

class Quads(PokerHandType):

	rank = 7

class StraightFlush(PokerHandType):

	rank = 8
