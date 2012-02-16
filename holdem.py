import cards
import pokerhand

class HoldEm:
	def __init__(self, num_players):
		self.num_players = num_players
		#Iniitalize deck
		deck = cards.Deck()

		#Deal the hole cards. Get a list of #players lists of 2 cards each
		self.all_hole_cards = deck.deal(num_players,2)
		#Deal the community cards. Get a list of one list of 5 cards
		self.community_cards = deck.deal(1,5)	
		# Make the hands
		self.hands = [pokerhand.HoldEmHand(hole_cards+self.community_cards) for hole_cards in self.all_hole_cards]
		
		# Rank them by the PokerHandType
		best_hands = [hand.best_hand for hand in self.hands]
		top_hand = max(best_hands)

		##########
		# Put all the hands with the top rank in one list, and the others in another
		self.winners = [ hand for hand in self.hands if hand.best_hand == top_hand ]
		self.losers = [ hand for hand in self.hands if hand not in self.winners ]

	def card_list_string(card_list):
		return cards.Card.list_string(card_list)