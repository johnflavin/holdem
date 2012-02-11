from random import shuffle

class Card:
	def __init__(self,integer):
		self.rank = integer
		self.value = integer%13
		self.suit = (integer - self.value)/13

	def __lt__(self, other):
		if self.value == other.value:
			return self.suit < other.suit
		return self.value < other.value

	def __le__(self, other):
		if self.value == other.value:
			return self.suit <= other.suit
		return self.value <= other.value

	def __eq__(self, other):
		return self.rank == other.rank

	def __ne__(self, other):
		return self.rank != other.rank

	def __gt__(self, other):
		if self.value == other.value:
			return self.suit > other.suit
		return self.value > other.value

	def __ge__(self, other):
		if self.value == other.value:
			return self.suit >= other.suit
		return self.value >= other.value

class Hand:
	def __init__(self,two_cards,five_cards):
		self.hole_cards = list(two_cards)
		self.community_cards = list(five_cards)

	def unique_values(self,cards):
		'''Unique Values
			Given a list of cards, returns a subset with unique values.
			I.e. if cards has two 10s, then unique_values returns a list with one 10.'''
		unique_vals = []
		for card in cards:
			if all( [card.value!=other_card.value for other_card in cards if card!=other_card] ):
				unique_vals.append( card )

		return unique_vals

	def straight_test(self,unique_vals):
		'''Straight Test
			Takes a list of cards with unique values and tests them for a straight.
			Returns a -2 if no straight is found. If a straight is found,
			returns its index (this includes -1 for a low-Ace straight'''
		index = self.straight_test_once(unique_vals)

		# If we have already found a straight, then we won't find a higher-valued
		# one by checking for a low-Ace straight. If we have not, we should check.
		if index == -2 and unique_vals[-1].value == 12:

			# We create a temporary deck of new cards with values one above the old (mod 52).
			# This makes every Ace a 2, every 2 a 3, and so on.
			shifted_cards = [Card((card.rank + 1)%52) for card in unique_vals]
			shifted_cards.sort()					# CHECK IF THIS WORKS
			index = self.straight_test_once( shifted_cards )

			# If there was a low-Ace straight, the function would have returned a 0.
			# We want to indicate this case by returning a -1, however.
			if index==0: index=-1
			
		return index

	def straight_test_once(self,unique_vals):								# STRAIGHT TEST. CHECK 
		#Test every five-card window to see if they are in numerical order.
		index = -2
		for i in range(len(unique_vals) - 4):
			if all( [unique_vals[i+j].value+1 == unique_vals[i+j+1].value for j in range(4)] ):
				index = i
		return index

	def best_hand(self):
		seven_cards = self.hole_cards + self.community_cards 				# LIST CONCAT? CHECK 
		seven_cards.sort()													# LIST SORT? CHECK 

		# A list of cards with no repeat values. This is useful when testing for straights.
		unique_vals = self.unique_values(seven_cards)

		# We keep the best hand in two variables: hand_rank and best_cards
		# best_cards stores the five cards that make the best hand.
		# hand_rank holds an integer, corresponding to a poker hand.
		# Order ranking of hands:
		# 0 = high card, 1 = pair, 2 = 2 pair, 3 = trips, 4 = straight,
		# 5 = flush, 6 = full house, 7 = quads, 8 = straight flush
		# They are initialized to hand_rank = 0, best_cards=[five highest-valued cards]
		hand_rank = 0
		best_cards = seven_cards[-5:]

		# Test for flush and str flush
		for suit in range(4):
			# For each suit, find all the cards of that suit.
			# If there are five or more, then we have a flush and we store that in 'best'
			suited_cards = [card for card in cards if card.suit==suit]
			if len(suited_cards) >= 5:
				hand_rank = 5
				best_cards = suited_cards[-5:]

				#Test for straight flush
				straight_index = straight_test(suited_cards)
				if straight_index != -2:
						
					hand_rank = 8

					if straight_index == -1:
						best_cards = [flushvalues[i-1] for i in range(5)]
					else:
						best_cards = flushvalues[straight_index:5+straight_index]
				break

		# Test for straight
		# Conditions: Only run test if...
		# 1. we haven't found a flush or straight flush (i.e. hand_rank < 5)
		# 2. There are at least five unique values in our hand of seven
		# 	(i.e. len(unique_vals)>=5)
		if len(unique_vals) >= 5 and hand_rank < 5:
			# Find out if there is a straight, and if so, where.
			straight_index = straight_test(unique_vals)
			if straight_index != -2:
				hand_rank = 4
				
				if straight_index == -1:
					best_cards = [unique_vals[i-1] for i in range(5)]
				else:
					best_cards = unique_vals[straight_index:5+straight_index]

		# Test for pair, 2pair, trips, full house, and quads
		# We do this successively. We first see if we have two cards
		# that are the same (pair), then see if we have three cards the same
		# (trips), etc.
		for card in unique_vals:
			# Find all the cards in the seven-card hand with the same value as
			# the current card in the uniques-only hand
			same_value = [other_card for other_card in seven_cards \
						if (other_card != card and other_card.value == card.value)]
			if len(same_value) >= 2:

				# We know the card we are testing now is in at least a pair.
				# If it is in only a pair (len(same_value) == 2), we check some other
				# conditions and assign the hand. If it is greater than a pair, we check
				# for trips, full house, or quads.
				if len(same_value) == 2:
					# We know the card we are testing now is in only a pair.
					# We first test for other hands. If we find none, 
					# then we set 'pair' as the best hand.

					# If we have previously found one pair ( hand_rank == 1 )
					# then we know we now have 2 pair.
					if hand_rank == 1:
						# We make a list holding the current pair and the old pair.
						two_pairs = same_value+best_cards[-2:]						# LIST CONCAT? CHECK !
						two_pairs.sort()											# LIST SORT? CHECK 
						# We find all the cards not part of the pairs
						# (We want the highest, which will be at the end of the already-sorted list)
						other_cards = [other_card for other_card in seven_cards \
										if other_card not in two_pairs]

						hand_rank = 2
						best_cards = other_cards[-1:]+two_pairs
						continue
					# If we have previously found two pairs (hand_rank == 2)
					# then we have three pairs and we pick the best two
					elif hand_rank == 2:
						high_pair_old = best_cards[-2:]
						low_pair_old = best_cards[1:2]
						other_cards = [other_card for other_card in seven_cards if \
										other_card not in high_pair_old and \
										other_card not in low_pair_old and \
										other_card not in same_value]
						# We first have to figure out which pairs are the highest two.
						# Once we know that, we need to know which of the remaining cards is highest.
						# 1. If the current pair is smaller than both old pairs, then the best hand has not changed. Do nothing.
						# 2. Otherwise, see if the current pair is less than or greater than the highest pair.
						if card < low_pair_old[0]:
							pass
						else:
							other_cards = other_cards+low_pair_old
							other_cards.sort()										# LIST SORT? CHECK 
							highest_other = other_cards[-1:]

							if high_pair_old[0] < card:
								high_pair_new = same_value
								low_pair_new = high_pair_old
							else:
								high_pair_new = high_pair_old
								low_pair_new = same_value

							best_cards = highest_other+low_pair_new+high_pair_new	# LIST CONCAT? CHECK 
						continue
					# If we have previously found trips ( hand_rank == 3 )
					# then we have a full house
					elif hank_rank == 3:
						hand_rank = 6
						trips_old = best_cards[-3:]
						best_cards = same_value+trips_old							# LIST CONCAT
						continue
					# If...
					# 1. we have previously found a full house (hand_rank==6)
					# 2. the pair we have now is better than the previous pair
					# ...then update the pair
					elif hand_rank == 6 and best_cards[0] < card:
						trips_old = best_cards[-3:]
						best_cards = same_value+trips_old							# LIST CONCAT
						continue
					# If we have not already had a straight or above (hand_rank < 4)
					# then the pair is the best thing we have seen so far
					elif hand_rank < 4:
						other_cards = [other_card for other_card in seven_cards \
										if other_card not in same_value]

						hand_rank = 1
						best_cards = other_cards[-3:]+same_value					# LIST CONCAT
						continue
				# The card we are testing has more than a pair.
				# Does it have trips? (len(same_value) == 3)
				elif len(same_value) == 3:
					# If we have previously seen a pair OR 2 pair,
					# then we have a full house.
					# We keep the highest pair and append the trips.
					if hand_rank == 1 or hand_rank == 2:
						high_pair_old = best_cards[-2:]

						hand_rank = 6
						best_cards = high_pair_old+same_value						# LIST CONCAT
						continue
					# If we have previously seen trips,
					# then we have a full house.
					# We keep all three of the higher set but only two of the lower.
					if hand_rank == 3:
						set_old = best_cards[-3:]
						if set_old[0] < card:
							low_set = set_old
							high_set = same_value
						else:
							low_set = same_value
							high_set = set_old

						hand_rank = 6
						best_cards = low_set[-2:]+high_set							# LIST CONCAT
						continue
					# If we have not already had a straight or above (hand_rank < 4)
					# then the trips is the best thing we have seen so far
					elif hand_rank < 4:
						other_cards = [other_card for other_card in seven_cards \
										if other_card not in same_value]

						hand_rank = 3
						best_cards = other_cards[-2:]+same_value					# LIST CONCAT
						continue
				# If the card has more than trips, it has quads.
				# We can't have quads along with a straight flush (the only higher-ranked hand)
				# So if we see it now, we know we can set it as best hand.
				else:
					other_cards = [other_card for other_card in seven_cards \
										if other_card not in same_value]
					hand_rank = 7
					best_cards = other_cards[-1:]+same_value

		return hand_rank,best_cards


class HoldEmGame:
	def __init__(self, num_players):
		#Iniitalize deck
		integer_deck = list(range(52))
		shuffle(integer_deck)
		deck = [Card(integer) for integer in integer_deck]

		#Deal the hole cards, make the hands
		first_card = deck[:num_players]
		second_card = deck[num_players:2*num_players]
		self.hands = [Hand(hole_cards) for hole_cards in zip(first_card,second_card)]

		#Deal the community cards
		#	Burn one, turn 3, burn one, turn one, burn one, turn one
		self.community_cards = [deck[2*num_players + offset] for offset in [1,2,3,5,7]]

		self.best_hands = [player.best_hand(self.community_cards) for player in self.players]
#############################

# def play(num_players):

# 	holdcards, community = deal(num_players)

# 	best=[]
# 	[best.append( besthand(hands,community) ) for hands in holdcards]

# 	return community,holdcards,best

# def sort(values,suits):
# 	valsource,valsink = list(values),[]
# 	suitsource,suitsink = list(suits),[]

# 	while len(valsource) > 0:
# 		loc = valsource.index( min(valsource) )

# 		valsink.append( valsource.pop(loc) )
# 		suitsink.append( suitsource.pop(loc) )

# 	return valsink, suitsink

def cull(hands,holds,metric_list,good_value):
	temphands,tempholds = [],[]
	for index in range(len(hands)):
		if metric_list[index] == good_value:
			temphands.append( hands[index] )
			tempholds.append( holds[index] )

	return temphands,tempholds

def straightIndex(values):
	#Method returns a -2 if no straight is found. Any other value
	#is the index of the lowest card in the straight (with a -1 returned
	#if the hand has a low-Ace straight, since Aces are stored high)
	straight_index = -2

	#We test every five-card window to see if they are in numerical order.
	#This will catch everything except the low-Ace case.
	for i in range(len(values) - 4):
		if all( [values[i+j]+1 == values[i+j+1] for j in range(4)] ):
			straight_index = i

	#If we have already found a straight, then we won't find a higher
	#valued one by moving the Ace down. If we have not, we should check.
	if straight_index == -2 and values[-1] == 12:

		#We move the Ace to the bottom of the list and everything else up one,
		#then we promote all the values up one mod 13 (thus the Ace which
		#was 12 goes to 0, the two was 0 goes to 1, etc.) and test again

		tempvalues = [ (values[i-1]+1)%13 for i in range(len(values)) ]
		for i in range(len(tempvalues) - 4):
			if all( [tempvalues[i+j]+1 == tempvalues[i+j+1] for j in range(4)] ):
				straight_index = -1

	return straight_index

# def besthand(hold, community):
# 	temphand = list(hold)
# 	temphand.extend(community)

# 	#Temphand is a list of cards, which are formatted
# 	#as '[value,suit]'. If we use zip we can separate the values
# 	#and suits out, but zip outputs tuples so we must list them
# 	#NOTE: I wrote a 'sort' method that sorts values and puts the
# 	#associated suits in the same order
# 	valsandsuits = zip(*temphand)
# 	values,suits = sort( list(valsandsuits[0]),list(valsandsuits[1]) )
# 	del temphand
# 	del valsandsuits

# 	#'Singles' stores the same stuff as 'values' with no duplicates
# 	singles = list( set(values) )

# 	#'best' is formatted as [hand rank,[best five]]
# 	#ranking of hands:
# 	#0 = high card, 1 = pair, 2 = 2 pair, 3 = trips, 4 = straight,
# 	#5 = flush, 6 = full house, 7 = quads, 8 = straight flush
# 	#It is initialized to [0,[five highest cards]]

# 	best = [0,values[-5:]]

# 	#Test for flush and str flush
# 	for suit in 0,1,2,3:
# 		if suits.count( suit ) >= 5:
# 			flushvalues = [values[i] for i in range(len(values)) \
# 							   if suits[i] == suit]
# 			best = [5, flushvalues[-5:] ]

# 			#Test for straight flush
# 			loc = straightIndex(flushvalues)
# 			if loc != -2:
# 				if loc == -1:
# 					best = [8, [flushvalues[i-1] for i in range(5)] ]
# 				else:
# 					best = [8, flushvalues[loc:5+loc] ]
# 			break

# 	#Test for straight
# 	#Only run if we haven't found a flush or str flush
# 	if len(singles) >= 5 and best[0] < 5:
# 		loc = straightIndex(singles)
# 		if loc != -2:
# 			if loc == -1:
# 				best = [4, [singles[i-1] for i in range(5)] ]
# 			else:
# 				best = [4, singles[loc:5+loc] ]

# 	#Test for pair, 2pair, trips, fhouse, quads
# 	for card in singles:
# 		if values.count( card ) >= 2:

# 			#We know we have a pair now. If we've already
# 			#had one pair then now we have 2 pair.
# 			if best[0] == 1 and values.count( card ) == 2:
# 				temp = list(values) 
# 				oldpair = best[1][4]
# 				[temp.remove(oldpair) for i in 0,1]
# 				[temp.remove(card) for i in 0,1]
# 				low = min(oldpair,card)
# 				high = max(oldpair,card)
# 				best = [2, [temp[-1],low,low,high,high] ]
# 				continue
# 			#If we've already had 2 pair, and now we have 
# 			#a 3rd pair, then we pick the best two
# 			elif best[0] == 2 and values.count( card ) == 2:
# 				hand = list(values)
# 				oldpairbig = best[1][4]
# 				oldpairsmall = best[1][2]
# 				for i in 0,1:
# 					hand.remove(oldpairbig)
# 					hand.remove(oldpairsmall)
# 					hand.remove(card)
# 				if oldpairbig < card:
# 					best = [2, [max(hand[0],oldpairsmall),\
# 									oldpairbig,oldpairbig,\
# 									card,card] ]
# 				elif oldpairsmall < card:
# 					best = [2, [max(hand[0],oldpairsmall),\
# 									card,card,\
# 									oldpairbig,oldpairbig] ]
# 				continue
# 			#If we've already had trips and now we have a
# 			#pair, then we have a full house
# 			elif best[0] == 3 and values.count( card ) == 2:
# 				best[0] = 6
# 				best[1][0:2] = card,card
# 				continue
# 			#If we've already had a full house and the
# 			#pair we have now is better than the pair
# 			#we had before, update the pair
# 			elif best[0] == 6 and best[1][0] < card:
# 				best[1][0:2] = card,card
# 				continue
# 			#Anything else str or above takes priority, so don't set
# 			#pair as 'best' if best[0] >= 4
# 			elif best[0] < 4 and values.count( card ) == 2:
# 				temp = list(values)
# 				[temp.remove(card) for i in 0,1]
# 				best = [1,[temp[-3],temp[-2],temp[-1],card,card] ]
# 				continue

# 			#Now test for trips or above
# 			if values.count( card ) >= 3:

# 				#If we've already had a pair or 2 pair and now we have
# 				#trips of a diff. card, then we have a full house
# 				if (best[0] == 1 or best[0] == 2) and \
# 						(best[1][4] != card or best[1][2] != card) and \
# 						values.count( card ) == 3:
# 					pair = best[1][4]
# 					best = [6,[pair,pair,card,card,card]]
# 					continue
# 				#If we've already had str or above, that wins, so don't
# 				#set trips as 'best' if best[0] >= 4
# 				elif best[0] < 4 and values.count( card ) == 3:
# 					temp = list(values)
# 					[temp.remove(card) for i in 0,1,2]
# 					best = [3, [temp[-2],temp[-1],card,card,card] ]
# 					continue

# 				#Test for quads
# 				if values.count( card ) == 4:
# 					temp = list(values)
# 					[temp.remove(card) for i in 0,1,2,3]
# 					best = [7, [temp[-1],card,card,card,card] ]

# 	return best


