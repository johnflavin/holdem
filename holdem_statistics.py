import holdem
import argparse
import sys
import csv
from itertools import starmap

# parser = OptionParser()
# parser.add_option("-i",type="int",dest="iter")
# parser.add_option("-p",type="int",dest="players")
# parser.add_option("-e",type="int",dest="exp")
# (options, args) = parser.parse_args()


# num_players = options.players
# if options.iter != None:
#     iterations = options.iter
# elif options.exp != None:
#     iterations = 10**options.exp
# else:
#     print '''Specify a number of iterations with '-i' or '-e'. '''
#     iterations = 0

parser = argparse.ArgumentParser(description="Runs a bunch of Texas Hold'Em hands and keeps statistics.")

parser.add_argument('n', type=int, help='Number of players')
parser.add_argument('exp', type=int, help='Order of magnitude of runs. Will run 10^exp hands.')
parser.add_argument('--name', type=str, default='players.csv',\
					help='Write results to the specified file. If no filename is specified, writes to "nplayers.csv".')
# parser.add_argument('--log', action='store_true', default=False, \
# 					help='Write every hand to log file if set.')

args = parser.parse_args(sys.argv[1:])

num_players = args.n
runs = 10**args.exp
total_runs = runs
if args.name == 'players.csv':
	filename = str(num_players)+args.name
# log = args.log



##########
# Dicts with useful info
suit_strings = {0:'clubs', 1:'diamonds', 2:'hearts', 3:'spades'}
value_strings = {0:'2',1:'3',2:'4',3:'5',4:'6',5:'7',6:'8',7:'9',8:'10',9:'J',10:'Q',11:'K',12:'A'}
hand_strings = { 0:'High Card', 1:'Pair', 2:'Two Pair', 3:'Trips', 4:'Straight', \
			5:'Flush', 6:'Full House', 7:'Quads', 8:'Straight Flush' }

##########
# Initialize arrays to hold hole-card stats
# These are 13x13x2 arrays, with two 13x13 matrices for the hole card values
# that are suited or not
num_wins = [ [ [0 for i in range(13)] for j in range(13)] for k in range(2)]
num_losses = [ [ [0 for i in range(13)] for j in range(13)] for k in range(2)]
num_splits = [ [ [0 for i in range(13)] for j in range(13)] for k in range(2)]
win_percent = [ [ [0 for i in range(13)] for j in range(13)] for k in range(2)]

##########
# Initialize array to count card frequencies 
seen_card = [0]*52

##########
# Initialize array to count hand frequencies (with an extra spot for a running total)
seen_hand = [0]*10
seen_hand_win = [0]*10

##########
# Before we run any games, we see if games have been run before. If so, we read in that data. No use letting our old data go to waste.
try:
	print('Reading old data')
	f = open(filename,'r')
except:
	print('Tried reading old data but it failed')
else:
		reader = csv.reader(f)
		line_list = list(reader)
		##########
		# First Row: Get runs and num_players
		row = line_list[0]
		runs_old = int(row[0])
		num_players_old = int(row[2])

		##########
		# We only want the old data if the number of players is the same now as then
		if num_players_old != num_players:
			raise Exception
		total_runs += runs_old

		##########
		# Second line is blank, third line is titles. Skip to fourth line.
		next_index = 3
		row = line_list[next_index]

		##########
		# Cards Seen
		# This row has one blank space then all the 'seen_card' data.
		for i in range(52):
			seen_card[i] += int(row[i+1])

		##########
		# Hands Seen / Hands Seen Win
		# We move the index to the line with the 'seen_hands' data, and we read it into the proper list along with 'seen_hands_win'.
		# Each data row is formatted with a blank space, then 9 data spaces
		# We keep a running total in the 10th matrix entry
		next_index += 4
		index = [next_index,next_index+4]
		li = [seen_hand,seen_hand_win]
		for i in 0,1:
			row = line_list[ index[i] ]
			for j in range(9):
				li[i][j] += int(row[j+1])
				li[i][-1] += int(row[j+1])

		##########
		# Reading old win/loss/split data
		next_index += 8
		index = [next_index,next_index+30]
		matrix = [num_wins,num_losses,num_splits]
		for suited in 0,1:
			for index1 in range(13):
				row = line_list[index[1-suited]+index1]
				for offset in range(3):
					for index2 in range(index1+1):
						matrix[offset][suited][index1][index2] += int( row[1+index2+15*offset] )
		
		f.close()
		


line_out = '{},Hands,{},Players\n'.format(total_runs,args.n)
print('Starting games...')
every_ten = 10
for this_game in range(runs):
	if (this_game+1) % every_ten == 0:
		print('Played {} games'.format(this_game+1))
		if every_ten < runs/10:
			every_ten *= 10
			
	##########
	# Play the game
	game = holdem.HoldEm(num_players)
	community = game.community_cards
	all_hole_cards = game.all_hole_cards
	hands = game.hands
	winners = game.winners
	losers = game.losers

	##########
	# Find the hole cards that created the winning hand(s). All the rest are losers
	winning_hole_cards = [all_hole_cards[i] for i in range(num_players) if hands[i] in winners]
	losing_hole_cards = [hole_cards for hole_cards in all_hole_cards if hole_cards not in winning_hole_cards]

	##########
	# Mark community cards 'seen'
	for card in community:
		seen_card[card.integer_val] += 1

	##########
	# Mark hole cards 'seen' 
	for hole in all_hole_cards:
		for card in hole:
			seen_card[card.integer_val] += 1


	##########
	# Mark Winning and Losing hand types 'seen'
	for hand in winners:
		seen_hand[ hand.best_hand.rank ] += 1
		seen_hand[-1] += 1
		seen_hand_win[-1] += 1

		seen_hand_win[ hand.best_hand.rank ] += 1
		
	for hand in losers:
		seen_hand[ hand.best_hand.rank ] += 1
		seen_hand[-1] += 1
		seen_hand_win[-1] += 1

	##########
	# Record Losses for losing hole card pairs
	for hole_cards in losing_hole_cards:
		suited = hole_cards[0].suit == hole_cards[1].suit
		index = [card.value for card in hole_cards]
		index.sort()
		num_losses[suited][index[1]][index[0]] += 1
	##########
	# If more than one hand won, then they actually split, and we record that
	if len(winning_hole_cards) > 1:
		for hole_cards in winning_hole_cards:
			suited = hole_cards[0].suit == hole_cards[1].suit
			index = [card.value for card in hole_cards]
			index.sort()
			num_splits[suited][index[1]][index[0]] += 1
	##########
	# Otherwise, we record the win
	else:
		hole_cards = winning_hole_cards[0]
		suited = hole_cards[0].suit == hole_cards[1].suit
		index = [card.value for card in hole_cards]
		index.sort()
		num_wins[suited][index[1]][index[0]] += 1

print('Organizing results')
#########
# Write cards /hands seen out to filename
for matrix in (seen_card,seen_hand,seen_hand_win):
	if matrix == seen_card:
		title_list = starmap( lambda div,rem:'{} of {}'.format(value_strings[rem],suit_strings[div]) , [divmod(integer,13) for integer in range(52)])
		matrix_name = 'Cards Seen,'
		avg_list = [float(elem)/float(total_runs*(2*num_players+5)) for elem in matrix]
		data_matrix = matrix
		avg_string = str( 1/52 )+','
	else:
		title_list = [hand_strings[integer] for integer in range(9)]
		avg_string = ','
		data_matrix = matrix[:-1]
		if matrix == seen_hand:
			matrix_name = 'Hands Seen,'
			avg_list = [float(matrix[i])/float(matrix[-1]) for i in range(len(matrix)-1)]
		else:
			matrix_name = 'Hands Seen Win,'
			avg_list = []
			for i in range(len(matrix)-1):
				if seen_hand[i] == 0:
					avg_list.append( float('NaN') )
				else:
					avg_list.append(float(matrix[i])/float(seen_hand[i]))
		
	title_line = '\n'+matrix_name+','.join( title_list )+'\n'
	line_out += title_line

	seen_data_line = ','+','.join( list(map(str,data_matrix)) )+'\n'
	line_out += seen_data_line

	seen_pct_line = avg_string+','.join( list(map(str,avg_list)) )+'\n'
	line_out += seen_pct_line


#########
# write wins/losses out to filename
for suited in 1,0:
	if suited:
		suited_string = 'Suited '
	else:
		suited_string = 'Unsuited '
	
	##########
	# Make and write title line
	title_line = '\n'
	for title_string in ['Wins,','Losses,','Splits,']:
		title_line += suited_string+title_string+','.join( [value_strings[key] for key in range(13)] )+',,'
	title_line += '\n'
	line_out += title_line

	##########
	# Make and write lines with the data from each matrix and blank spaces for alignment
	for index1 in range(13):
		line = ''
		for matrix in [num_wins,num_losses,num_splits]:
			data_string = ','.join( [str(matrix[suited][index1][index2]) for index2 in range(index1+1)] )
			blank_string = ','.join( ['' for index in range(15-index1)] )
			line += value_strings[index1]+','+data_string+blank_string
		line += '\n'
		line_out += line

	##########
	# Make and write title line for win percent matrix
	title_line = '\n'+suited_string+'Win %,'+','.join( [value_strings[key] for key in range(13)] )+'\n'
	line_out += title_line

	##########
	# Calculate win percent matrix, and write each line
	for index1 in range(13):
		for index2 in range(index1+1):
			if num_wins[suited][index1][index2] == 0 and num_losses[suited][index1][index2] == 0 and num_splits[suited][index1][index2] == 0:
				win_percent[suited][index1][index2] = float('NaN')
			else:
				denom = num_wins[suited][index1][index2]+num_losses[suited][index1][index2]+num_splits[suited][index1][index2]
				win_percent[suited][index1][index2] = float(num_wins[suited][index1][index2])/float(denom)
		
		line = ''	
		data_string = ','.join( [str(win_percent[suited][index1][index2]) for index2 in range(index1+1)] )
		line += value_strings[index1]+','+data_string+'\n'
		line_out += line
		
print('Writing results to file')
with open(filename,'w') as f:
	f.write(line_out)
