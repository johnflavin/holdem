from pokerhandtype import *
from cards import Card

class PokerHand:
	'''Poker Hand
		A virtual class, meant to be derived into a child class that knows the rules of some poker game. See find_best_hand.

		Hands can be compared using comparison operators <, <=, >, >=, ==, and !=. These operators will compare the PokerHandTypes stored in best_hand.
		
		hand.cards 
			Holds a sorted list of Cards
		hand.best_hand 
			A PokerHandType child class which is the best hand given the cards and the rules of the game

		hand.string()
			Returns a string formatted as "card.string(), card.string(), ..." for all the cards in hand.cards
		
		hand.best_string()
			Returns the string stored in whichever PokerHandType is stored in best_hand. Formatted something like "Pair of {}s" or "{} High", etc.

		hand.find_best_hand() 
			In each child class, write this method to look at self.cards and find the best PokerHandType those cards support.
			This is based on the rules of the game you are playing.
		'''
	def __init__(self,cards):
		self.cards = list(cards)
		self.cards.sort()
		self.best_hand = self.find_best_hand()

	def __lt__(self, other):
		return self.best_hand < other.best_hand

	def __le__(self, other):
		return self.best_hand <= other.best_hand

	def __eq__(self, other):
		return self.best_hand == other.best_hand

	def __ne__(self, other):
		return self.best_hand != other.best_hand

	def __gt__(self, other):
		return self.best_hand > other.best_hand

	def __ge__(self, other):
		return self.best_hand >= other.best_hand

	def card_string(self):
		return Card.list_string( self.cards )

	def best_string(self):
		return self.best_hand.string, Card.list_string( self.best_hand.cards )

	def find_best_hand(self):
		pass

class HoldEmHand(PokerHand):
	def straight(self,unique_vals):
		straight_cards = []

		##########
		# For every 5-card window, check to see if cards are in
		# numerical order.
		if len(unique_vals) >= 5:
			straight_cards = self.straight_test_once( unique_vals )

			##########
			# If the straight is a low-ace straight, the above will not find it.
			# We check for a low-ace straight if...
			# 1. We didn't find a straight with the first check (b.c. if we did it is higher than low-ace)
			# 2. There is at least one ace in the list.
			# If these are met, we move the ace to the bottom of the list, change its
			# value from 12 to -1 (same mod 13), and check again.
			if len(straight_cards)==0 and unique_vals[-1].value==12:
				ace_integer = unique_vals[-1].integer_val
				temp_ace = Card(ace_integer)
				temp_ace.value = -1
				# ^^This card is now mal-formed. Its integer value does not match suit*13+value,
				# and it has a value not between 0 and 12. Still, it will work to test a straight,
				# and then we will throw it away.

				temp_vals = [temp_ace]+unique_vals[:-1]

				temp_straight_cards = self.straight_test_once( temp_vals )

				##########
				# If we find a straight now, we know it was because we moved the ace to the bottom
				# We create a proper card list with the ace at the bottom, and the next four cards.
				if len(temp_straight_cards)!=0:
					straight_cards = unique_vals[-1:] + unique_vals[:4]

		return straight_cards

	def straight_test_once(self,unique_vals):
		straight_cards = []

		##########
		# For every 5-card window, check to see if cards are in
		# numerical order.
		for i in range(len(unique_vals) - 4):
			if all( [unique_vals[i+j].value+1 == unique_vals[i+j+1].value for j in range(4)] ):
				straight_cards = unique_vals[i:i+5]

		return straight_cards

	def find_best_hand(self):
		##########
		# Create a list of cards with no repeat values. 
		# This is useful when testing for straights and iterating over cards.
		# I.e. if there are two 10s in the full seven card hand, 
		# then unique_values has only one 10.
		unique_vals = []
		for card in self.cards:
			if len(unique_vals) == 0 or \
				all( [ card.value != other_card.value for other_card in unique_vals] ):
				unique_vals.append( card )

		##########
		# Initialize the best hand to HighCard with the five highest cards
		best_hand = HighCard(self.cards[-5:])

		##########
		# Test for flush and str flush
		for suit in range(4):
			##########
			# For each suit, find all the cards of that suit.
			# If there are five or more, then we have a flush and we store that in 'best'
			suited_cards = [card for card in self.cards if card.suit==suit]
			if len(suited_cards) >= 5:

				##########
				# Test for straight flush
				straight_flush = self.straight(suited_cards)

				if len(straight_flush) > 0:
					best_hand = StraightFlush(straight_flush)
				else:
					best_hand = Flush(suited_cards[-5:])

				break

		##########
		# Test for straight
		# Conditions: Only run test if...
		# 1. we haven't found a flush or straight flush
		# 2. There are at least five unique values in our hand of seven
		# 	(i.e. len(unique_vals)>=5)
		if len(unique_vals) >= 5 and best_hand.rank < Flush.rank:
			##########
			# Get the straight, if there is one.
			straight_list = self.straight(unique_vals)

			if len(straight_list) > 0:
				best_hand = Straight(straight_list)

		##########
		# Test for pair, 2pair, trips, full house, and quads
		# We do this successively. We first see if we have two cards
		# that are the same (pair), then see if we have three cards the same
		# (trips), etc.
		for card in unique_vals:
			##########
			# Find all the cards in the seven-card hand with the same value as
			# the current card in the uniques-only hand
			same_value = [other_card for other_card in self.cards if other_card.value == card.value]
			if len(same_value) >= 2:
				##########
				# We know the card we are testing now is in at least a pair.
				# If it is in only a pair (len(same_value) == 2), we check some other
				# conditions and assign the hand. If it is greater than a pair, we check
				# for trips, full house, or quads.
				if len(same_value) == 2:
					##########
					# We know the card we are testing now is in only a pair.
					# We first test for other hands. If we find none, 
					# then we set 'pair' as the best hand.

					##########
					# FOUND A PAIR
					# If we have previously found one pair (and only one)
					# then we know we now have 2 pair.
					if best_hand.rank == Pair.rank:
						##########
						# We make a list holding the current pair and the old pair.
						two_pairs = same_value+best_hand.cards[-2:]	
						two_pairs.sort()
						##########
						# We find all the cards not part of the pairs
						# (We want the highest, which will be at the end of the already-sorted list)
						other_cards = [other_card for other_card in self.cards \
										if other_card not in two_pairs]

						best_hand = TwoPair(other_cards[-1:]+two_pairs)
						continue
					##########
					# FOUND A PAIR
					# If we have previously found two pairs
					# then we currently have three pairs and we pick the best two
					elif best_hand.rank == TwoPair.rank:
						high_pair_old = best_hand.cards[-2:]
						low_pair_old = best_hand.cards[1:2]
						other_cards = [other_card for other_card in self.cards if \
										other_card not in high_pair_old and \
										other_card not in low_pair_old and \
										other_card not in same_value]
						##########
						# We first have to figure out which pairs are the highest two.
						# Once we know that, we need to know which of the remaining cards is highest.
						# 1. If the current pair is smaller than both old pairs, then the best hand has not changed. Do nothing.
						# 2. Otherwise, see if the current pair is less than or greater than the highest pair.
						if card < low_pair_old[0]:
							pass
						else:
							other_cards = other_cards+low_pair_old
							other_cards.sort()
							highest_other = other_cards[-1:]

							if high_pair_old[0] < card:
								high_pair_new = same_value
								low_pair_new = high_pair_old
							else:
								high_pair_new = high_pair_old
								low_pair_new = same_value

							best_hand = TwoPair(highest_other+low_pair_new+high_pair_new)
						continue
					##########
					# FOUND A PAIR
					# If we have previously found trips 
					# then we now have a full house
					elif best_hand.rank == Trips.rank:
						trips_old = best_hand.cards[-3:]
						best_hand = FullHouse(same_value+trips_old)
						continue
					##########
					# FOUND A PAIR
					# If...
					# 1. we have previously found a full house
					# 2. the pair we have now is better than the previous pair
					# ...then update the pair
					elif best_hand.rank == FullHouse.rank and best_hand.cards[0] < card:
						trips_old = best_hand.cards[-3:]
						best_hand = FullHouse(same_value+trips_old)
						continue
					##########
					# FOUND A PAIR
					# If we have not already had a straight or above 
					# then the pair is the best thing we have seen so far
					elif best_hand.rank < Straight.rank:
						other_cards = [other_card for other_card in self.cards \
										if other_card not in same_value]

						best_hand = Pair(other_cards[-3:]+same_value)
						continue
				##########
				# The card we are testing has more than a pair.
				# Does it have trips? (len(same_value) == 3)
				elif len(same_value) == 3:
					##########
					# FOUND TRIPS
					# If we have previously seen a pair OR 2 pair,
					# then we have a full house.
					# We keep the highest pair and append the trips.
					if best_hand.rank == Pair.rank or best_hand.rank == TwoPair.rank:
						high_pair_old = best_hand.cards[-2:]

						best_hand = FullHouse(high_pair_old+same_value)
						continue
					##########
					# FOUND TRIPS
					# If we have previously seen trips,
					# then we have a full house.
					# We keep all three of the higher set but only two of the lower.
					if best_hand.rank == Trips.rank:
						set_old = best_hand.cards[-3:]
						if set_old[0] < card:
							low_set = set_old
							high_set = same_value
						else:
							low_set = same_value
							high_set = set_old

						best_hand = FullHouse(low_set[-2:]+high_set)
						continue
					##########
					# FOUND TRIPS
					# If we have not already had a straight or above
					# then the trips is the best thing we have seen so far
					elif best_hand.rank < Straight.rank:
						other_cards = [other_card for other_card in self.cards \
										if other_card not in same_value]

						best_hand = Trips(other_cards[-2:]+same_value)
						continue
				##########
				# If the card has more than trips, it has quads.
				# We can't have quads along with a straight flush (the only higher-ranked hand)
				# So if we see it now, we know we can set it as best hand.
				else:
					other_cards = [other_card for other_card in self.cards \
										if other_card not in same_value]
					best_hand = Quads(other_cards[-1:]+same_value)

		return best_hand












