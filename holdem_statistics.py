import holdem
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i",type="int",dest="iter")
parser.add_option("-p",type="int",dest="players")
parser.add_option("-e",type="int",dest="exp")
(options, args) = parser.parse_args()


num_players = options.players
if options.iter != None:
    iterations = options.iter
elif options.exp != None:
    iterations = 10**options.exp
else:
    print '''Specify a number of iterations with '-i' or '-e'. '''
    iterations = 0

num_wins = [ [ [0 for value in range(13)] for value2 in range(13) ] \
                 for suited in 0,1 ]
num_losses = [ [ [0 for value in range(13)] for value2 in range(13) ] \
                   for suited in 0,1 ]
num_splits = [[[0 for v in range(13)] for v2 in range(13)] for s in 0,1]
w_perc = [[[0 for v in range(13)] for v2 in range(13)] for s in 0,1]

for k in range(iterations):
    community,holds,best = holdem.play(num_players)
    temp = zip(*best)
    ranks,bestfive = list(temp[0]),list(temp[1])
    del temp

    split = False

    #One or more ranks will be the highest
    winning_rank = max(ranks)

    #Is there a clear winner?
    if ranks.count( winning_rank ) == 1:
        winner = holds[ ranks.index(winning_rank) ]
    #If there is no clear winner (i.e. >1 hands have the same 'rank')
    #We must dig deeper and compare the cards on a case-by-case basis
    else:
        #First we cut out those hands that are not winning
        winning_hands,winning_holds = \
            holdem.cull( bestfive,holds,ranks,winning_rank )

        #Make an easy comparison list and find the top pertinent
        #card among the possible winners
        card_by_card = list( zip(*winning_hands) )
        top_card = max( card_by_card[4] )
        top_index = card_by_card[4].index( top_card )

        #If only one person has the top card, there is
        #a clear winner
        if card_by_card[4].count( top_card ) == 1:
            winner = winning_holds[top_index]
        #If not, we further cull the list to only those hands
        #that all have the same highest pertinent card
        else:
            #Again, cull the hands that will not win
            winning_hands,winning_holds = \
                holdem.cull(winning_hands,winning_holds,\
                                card_by_card[4],top_card)

            #How we proceed from here differs depening on the hands
            if winning_rank == 8 or winning_rank == 4:

                #If >1 person has a str or str flush
                #to the same card, they split
                split = True
                winner = winning_holds
            elif winning_rank == 7 or winning_rank == 6:

                #For quads/full house we have to look 
                #at the kicker/pair
                card_by_card = list(zip(*winning_hands))
                top_kicker = max(card_by_card[0])

                #If only one person has top kicker, they win
                if card_by_card[0].count(top_kicker) == 1:
                    loc = card_by_card[0].index(top_kicker)
                    winner = winning_holds[loc]
                else:
                    split = True
                    winner = [winning_holds[i] for i in \
                                  range(len(winning_holds)) \
                                  if card_by_card[0][i] == top_kicker]
            elif winning_rank == 5 or winning_rank == 0:

                #For flush or high card, we must go down the line 
                #and look at each successive card. This would be 
                #easy if we knew how many players we were comparing, 
                #but we don't. At this point, we've already culled
                #all our lists to only those hands that have the
                #winning rank and the same top card, so we start with
                #the next card down.

                for i in range(4):
                    card_by_card = list(zip(*winning_hands))
                    top = max( card_by_card[3-i] )
                    if card_by_card[3-i].count( top ) == 1:
                        loc = card_by_card[3-i].index( top )
                        winner = winning_holds[loc]
                        break
                    else:
                        winning_hands,winning_holds = \
                            holdem.cull(winning_hands,winning_holds,\
                                            card_by_card[3-i],top)
                        if i == 3:
                            split = True
                            winner = winning_holds
            elif winning_rank == 3 or winning_rank == 2:
                #We know the trips/top pair are/is the same. 
                #Now we check the kickers/bottom pair and kicker
                for i in 0,1:
                    card_by_card = list(zip(*winning_hands))
                    kick = max( card_by_card[1-i] )
                    if card_by_card[1-i].count( kick ) == 1:
                        loc = card_by_card[1-i].index( kick )
                        winner = winning_holds[loc]
                        break
                    else:
                        winning_hands,winning_holds = \
                            holdem.cull(winning_hands,winning_holds,\
                                            card_by_card[1-i],kick)
                        if i == 1:
                            split = True
                            winner = winning_holds
            elif winning_rank == 1:
                #We know the pair is the same. Check the kickers.
                for i in 0,1,2:
                    card_by_card = list(zip(*winning_hands))
                    kick = max( card_by_card[2-i] )
                    if card_by_card[2-i].count( kick ) == 1:
                        loc = card_by_card[2-i].index( kick )
                        winner = winning_holds[loc]
                        break
                    else:
                        winning_hands,winning_holds = \
                            holdem.cull(winning_hands,winning_holds,\
                                            card_by_card[2-i],kick)
                        if i == 2:
                            split = True
                            winner = winning_holds
    if not split:
        suited = winner[0][1]==winner[1][1]
        num_wins[suited][winner[0][0]][winner[1][0]] += 1

        holds.remove(winner)
    else:
        for splits in winner:
            suited = splits[0][1]==splits[1][1]
            num_splits[suited][splits[0][0]][splits[1][0]] += 1

            holds.remove( splits )

    for losers in holds:
        suited = losers[0][1]==losers[1][1]
        num_losses[suited][losers[0][0]][losers[1][0]] += 1

print ''
print "Players =",num_players,"| Runs =",iterations

def f(i):
    if i<=8:
        return str(i+2)
    elif i==9:
        return "J"
    elif i==10:
        return "Q"
    elif i==11:
        return "K"
    else:
        return "A"

sep = ' '
suited = ['Unsuited','Suited']
titles = ['Wins','Losses','Splits']

for s in 0,1:
    print suited[s]

    display = [['' for i in range(13)] for d in 0,1,2]

    for i in range(13):
        for j in range(i+1):
            if i != j:
                num_wins[s][i][j] += num_wins[s][j][i]

                num_losses[s][i][j] += num_losses[s][j][i]

                num_splits[s][i][j] += num_splits[s][j][i]

            if display[0][i] == '':
                display[0][i] = str( num_wins[s][i][j] )
            else:
                display[0][i] = sep.join( [display[0][i], str(num_wins[s][i][j])] )
            if display[1][i] == '':
                display[1][i] = str( num_losses[s][i][j] )
            else:
                display[1][i] = sep.join( [display[1][i], str(num_losses[s][i][j])] )
            if display[2][i] == '':
                display[2][i] = str( num_splits[s][i][j] )
            else:
                display[2][i] = sep.join( [display[2][i], str(num_splits[s][i][j])] )

    for d in 0,1,2:
        print titles[d]
        for i in range(13):
            print display[d][i]
        print ''
