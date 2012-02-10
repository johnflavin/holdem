from shuffle import shuffle

def play(num_players):

    holdcards, community = deal(num_players)

    best=[]
    [best.append( besthand(hands,community) ) for hands in holdcards]

    return community,holdcards,best

def deal(num_players):
    deck = shuffle()

    holds = [ [format(deck[i*num_players + j]) for i in 0,1] \
                 for j in range(num_players) ]

    #Burn, turn 3, burn, turn, burn, turn
    community = [format(deck[num_players*2 + i]) for i in 1,2,3,5,7]

    return holds, community

def format(card):
    value = card%13
    suit = (card-value)/13

    return [value,suit]

def sort(values,suits):
    valsource,valsink = list(values),[]
    suitsource,suitsink = list(suits),[]

    while len(valsource) > 0:
        loc = valsource.index( min(valsource) )

        valsink.append( valsource.pop(loc) )
        suitsink.append( suitsource.pop(loc) )

    return valsink, suitsink

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

def besthand(hold, community):
    temphand = list(hold)
    temphand.extend(community)

    #Temphand is a list of cards, which are formatted
    #as '[value,suit]'. If we use zip we can separate the values
    #and suits out, but zip outputs tuples so we must list them
    #NOTE: I wrote a 'sort' method that sorts values and puts the
    #associated suits in the same order
    valsandsuits = zip(*temphand)
    values,suits = sort( list(valsandsuits[0]),list(valsandsuits[1]) )
    del temphand
    del valsandsuits

    #'Singles' stores the same stuff as 'values' with no duplicates
    singles = list( set(values) )

    #'best' is formatted as [hand rank,[best five]]
    #ranking of hands:
    #0 = high card, 1 = pair, 2 = 2 pair, 3 = trips, 4 = straight,
    #5 = flush, 6 = full house, 7 = quads, 8 = straight flush
    #It is initialized to [0,[five highest cards]]

    best = [0,values[-5:]]

    #Test for flush and str flush
    for suit in 0,1,2,3:
        if suits.count( suit ) >= 5:
            flushvalues = [values[i] for i in range(len(values)) \
                               if suits[i] == suit]
            best = [5, flushvalues[-5:] ]

            #Test for straight flush
            loc = straightIndex(flushvalues)
            if loc != -2:
                if loc == -1:
                    best = [8, [flushvalues[i-1] for i in range(5)] ]
                else:
                    best = [8, flushvalues[loc:5+loc] ]
            break

    #Test for straight
    #Only run if we haven't found a flush or str flush
    if len(singles) >= 5 and best[0] < 5:
        loc = straightIndex(singles)
        if loc != -2:
            if loc == -1:
                best = [4, [singles[i-1] for i in range(5)] ]
            else:
                best = [4, singles[loc:5+loc] ]

    #Test for pair, 2pair, trips, fhouse, quads
    for card in singles:
        if values.count( card ) >= 2:

            #We know we have a pair now. If we've already
            #had one pair then now we have 2 pair.
            if best[0] == 1 and values.count( card ) == 2:
                temp = list(values) 
                oldpair = best[1][4]
                [temp.remove(oldpair) for i in 0,1]
                [temp.remove(card) for i in 0,1]
                low = min(oldpair,card)
                high = max(oldpair,card)
                best = [2, [temp[-1],low,low,high,high] ]
                continue
            #If we've already had 2 pair, and now we have 
            #a 3rd pair, then we pick the best two
            elif best[0] == 2 and values.count( card ) == 2:
                hand = list(values)
                oldpairbig = best[1][4]
                oldpairsmall = best[1][2]
                for i in 0,1:
                    hand.remove(oldpairbig)
                    hand.remove(oldpairsmall)
                    hand.remove(card)
                if oldpairbig < card:
                    best = [2, [max(hand[0],oldpairsmall),\
                                    oldpairbig,oldpairbig,\
                                    card,card] ]
                elif oldpairsmall < card:
                    best = [2, [max(hand[0],oldpairsmall),\
                                    card,card,\
                                    oldpairbig,oldpairbig] ]
                continue
            #If we've already had trips and now we have a
            #pair, then we have a full house
            elif best[0] == 3 and values.count( card ) == 2:
                best[0] = 6
                best[1][0:2] = card,card
                continue
            #If we've already had a full house and the
            #pair we have now is better than the pair
            #we had before, update the pair
            elif best[0] == 6 and best[1][0] < card:
                best[1][0:2] = card,card
                continue
            #Anything else str or above takes priority, so don't set
            #pair as 'best' if best[0] >= 4
            elif best[0] < 4 and values.count( card ) == 2:
                temp = list(values)
                [temp.remove(card) for i in 0,1]
                best = [1,[temp[-3],temp[-2],temp[-1],card,card] ]
                continue

            #Now test for trips or above
            if values.count( card ) >= 3:

                #If we've already had a pair or 2 pair and now we have
                #trips of a diff. card, then we have a full house
                if (best[0] == 1 or best[0] == 2) and \
                        (best[1][4] != card or best[1][2] != card) and \
                        values.count( card ) == 3:
                    pair = best[1][4]
                    best = [6,[pair,pair,card,card,card]]
                    continue
                #If we've already had str or above, that wins, so don't
                #set trips as 'best' if best[0] >= 4
                elif best[0] < 4 and values.count( card ) == 3:
                    temp = list(values)
                    [temp.remove(card) for i in 0,1,2]
                    best = [3, [temp[-2],temp[-1],card,card,card] ]
                    continue

                #Test for quads
                if values.count( card ) == 4:
                    temp = list(values)
                    [temp.remove(card) for i in 0,1,2,3]
                    best = [7, [temp[-1],card,card,card,card] ]

    return best


