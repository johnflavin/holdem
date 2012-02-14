class PokerHandType:
	rank = -1

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.name = 'Hand Type'

	def __lt__(self, other):
		if self.rank == other.rank:
			pass
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			pass
		return self.rank < other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			pass

	def __ne__(self, other):
		if self.rank == other.rank:
			pass
		return self.rank != other.rank

	def __gt__(self, other):
		if self.rank == other.rank:
			pass
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			pass
		return self.rank > other.rank

class HighCard(PokerHandType):
	rank = 0

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.string = '{} High'.format(self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			return self.hand < other.hand
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			return self.hand <= other.hand
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			return self.hand == other.hand

	def __ne__(self, other):
		if self.rank == other.rank:
			return self.hand != other.hand
		return self.rank != other.rank

	def __gt__(self, other):
		if self.rank == other.rank:
			return self.hand > other.hand
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			return self.hand >= other.hand
		return self.rank >= other.rank

	def high_card(self):
		return self.hand[-1]

class Pair(PokerHandType):
	rank = 1

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.pair = self.hand[-1].value
		self.string = 'Pair of {}s'.format(self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand < other.hand
			return self.pair < other.pair
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand <= other.hand
			return self.pair < other.pair
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand == other.hand
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand != other.hand
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand > other.hand
			return self.pair > other.pair
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			if self.pair == other.pair:
				return self.hand >= other.hand
			return self.pair > other.pair
		return self.rank >= other.rank

class TwoPair(PokerHandType):
	rank = 2

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.high = self.hand[-1].value
		self.low = self.hand[-3].value
		self.string = 'Two Pair: {}s and {}s'.format(self.hand[-1].name,self.hand[-3].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value < other.hand[0].value
				return self.low < other.low
			return self.high < other.high
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value <= other.hand[0].value
				return self.low < other.low
			return self.high < other.high
		return self.rank < other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value == other.hand[0].value
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value != other.hand[0].value
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value > other.hand[0].value
				return self.low > other.low
			return self.high > other.high
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				if self.low == other.low:
					return self.hand[0].value >= other.hand[0].value
				return self.low > other.low
			return self.high > other.high
		return self.rank > other.rank

class Trips(PokerHandType):
	rank = 3

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.trips = self.hand[-1].value
		self.string = 'Set of {}s'.format(self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand < other.hand
			return self.trips < other.trips
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand <= other.hand
			return self.trips < other.trips
		return self.rank < other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand == other.hand
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand != other.hand
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand > other.hand
			return self.trips > other.trips
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			if self.trips == other.trips:
				return self.hand >= other.hand
			return self.trips > other.trips
		return self.rank > other.rank

class Straight(PokerHandType):
	rank = 4

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.to_the = self.hand[-1].value
		self.string = 'Straight to the {}'.format(self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			return self.to_the < other.to_the
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			return self.to_the <= other.to_the
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			return self.to_the == other.to_the
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			return self.to_the != other.to_the
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			return self.to_the > other.to_the
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			return self.to_the >= other.to_the
		return self.rank >= other.rank

class Flush(PokerHandType):
	rank = 5

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.to_the = self.hand[-1].value
		self.string = 'Flush in {} to the {}'.format(self.hand[-1].suitname,self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			return self.hand < other.hand
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			return self.hand <= other.hand
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			return self.hand == other.hand
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			return self.hand != other.hand
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			return self.hand > other.hand
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			return self.hand >= other.hand
		return self.rank >= other.rank

class FullHouse(PokerHandType):
	rank = 6

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.high = self.hand[-1].value
		self.low = self.hand[0].value
		self.string = 'Full House, {}s full of {}s'.format(self.hand[-1].name,self.hand[0].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low < other.low
			return self.high < other.high
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low <= other.low
			return self.high < other.high
		return self.rank < other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low == other.low
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low != other.low
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low > other.low
			return self.high > other.high
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			if self.high == other.high:
				return self.low >= other.low
			return self.high > other.high
		return self.rank > other.rank

class Quads(PokerHandType):
	rank = 7

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.quads = self.hand[-1].value
		self.string = 'Four {}s'.format(self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value < other.hand[0].value
			return self.quads < other.quads
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value <= other.hand[0].value
			return self.quads < other.quads
		return self.rank < other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value == other.hand[0].value
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value != other.hand[0].value
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value > other.hand[0].value
			return self.quads > other.quads
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			if self.quads == other.quads:
				return self.hand[0].value >= other.hand[0].value
			return self.quads > other.quads
		return self.rank > other.rank

class StraightFlush(PokerHandType):
	rank = 8

	def __init__(self,poker_hand):
		self.hand = poker_hand
		self.to_the = self.hand[-1].value
		if self.to_the < 12:
			self.string = 'Straight {} flush to the {}'.format(self.hand[-1].suitname,self.hand[-1].name)
		else:
			self.string = 'Royal flush in {}'.format(self.hand[-1].suitname,self.hand[-1].name)

	def __lt__(self, other):
		if self.rank == other.rank:
			return self.to_the < other.to_the
		return self.rank < other.rank

	def __le__(self, other):
		if self.rank == other.rank:
			return self.to_the <= other.to_the
		return self.rank <= other.rank

	def __eq__(self, other):
		if self.rank == other.rank:
			return self.to_the == other.to_the
		return False

	def __ne__(self, other):
		if self.rank == other.rank:
			return self.to_the != other.to_the
		return True

	def __gt__(self, other):
		if self.rank == other.rank:
			return self.to_the > other.to_the
		return self.rank > other.rank

	def __ge__(self, other):
		if self.rank == other.rank:
			return self.to_the >= other.to_the
		return self.rank >= other.rank