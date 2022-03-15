#file  -- ending.py --
# -*- coding: UTF-8 -*-

import copy
import time
from itertools import combinations
from judge import isSeq1,isSeq2,isSeq3,isPlane
import random


class Solution:
    def __init__(self):
        # input
        self.playerA = []
        self.playerB = []

        # Generative Adversarial self.tree
        # [
        #   [val, [cards], [next]]
        #   ...
        # ]
        self.tree = [[0, [], []]]
        self.root = 0
        self.count = 0

    # card map
    def getVal(self, cards):
        vals = { '3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
        # print('getVal', cards)
        if not cards:
            return []
        for i, card in enumerate(cards):
            cards[i] = vals[card]
    def getCard(self, vals):
        cards = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        ans = []
        for val in vals:
            ans.append(cards[val])
        return ans

    # get sequence
    def getSeq(self, cards, length, size, num):
        ans = []
        seq = []
        if len(cards) >= length * num:
            for card in list(set(cards)):
                if ((len(seq) == 0 and card > (size - 2) and cards.count(card) >= num) or
                    (len(seq) != 0 and seq[-1] + 1 == card and cards.count(card) >= num)):
                    seq = seq + [card] * num
                else:
                    if card > (size - 2) and cards.count(card) >= num:
                        seq = [card] * num
                if len(seq) == length * num:
                    pattern = -1
                    if num == 1:
                        pattern = length + 2
                    elif num == 2:
                        pattern = length + 13
                    elif num == 3:
                        pattern = length + 26
                    ans.append({ 'c': copy.deepcopy(seq), 'p': pattern, 's': seq[0] + 2 })
                    seq = seq[num:]
                #new part

            if (num == 1) or (num == 2 and length >= 3) or (num == 3 and length >= 3):
                if cards.count(12) >= num and length <= 11 and (size == -1 or size == 0):
                    found = 1
                    space = [12]*num
                    for i in range(length-1):
                        if cards.count(i) < num:
                            found = 0
                            break
                        else:
                            space = space + [i] * num
                    if found == 1 :
                        if num == 1:
                            pattern = length + 2
                        elif num == 2:
                            pattern = length + 13
                        elif num == 3:
                            pattern = length + 26
                        ans.append({ 'c': space, 'p': pattern, 's': 1 })


                if cards.count(11) >= num and cards.count(12) >= num and size == -1 and length < 13:
                    found = 1
                    space = [11]*num + [12]*num
                    for i in range(length - 2):
                        if cards.count(i) < num:
                            found = 0
                            break
                        else:
                            space = space + [i]*num
                    if found == 1 :
                        if num == 1:
                            pattern = length + 2
                        elif num == 2:
                            pattern = length + 13
                        elif num == 3:
                            pattern = length + 26
                        ans.append({ 'c': space, 'p': pattern, 's': 0 })
            else:#对应num=2,3,length = 2的情况，此时默认AA22，AAA222为最大牌
                if (cards.count(12) >= num) and (cards.count(0) >= num) and (size == -1):
                    if num == 2:
                        ans.append({'c':[12,12,0,0],'p':15,'s':1})
                    else:
                        ans.append({'c':[12,12,12,0,0,0],'p':28,'s':1})
                    

        return ans

    # get airplane(sequence of triplets) with single cards
    def getPlane1(self, cards, length, size):
        ans = []
        if len(cards) >= (length*4):
            sets = set(cards)
            seq = self.getSeq(cards,length,size,3)
            for i in seq:
                cardAs = i['c']
                size = i['s']
                cardBs = list(sets - set(cardAs))
                if len(cardBs) >= length:
                    space1 = list(combinations(cardBs,length))
                    for js in space1:
                        space2 = cardAs + list(js)
                        ans.append({'c':space2,'p':length + 31,'s':size})

        return ans

    # get airplane(sequence of triplets) with pairs
    def getPlane2(self, cards,length,size):
        ans = []
        if len(cards) >= (length * 5): 
            sets = set(cards)
            seq = self.getSeq(cards,length,size,3)
            for i in seq:
                cardAs = i['c']
                size = i['s']
                cardBs = []
                for j in sets:
                    if (j not in cardAs) and (cards.count(j) >= 2):
                        cardBs.append(j)
                if len(cardBs) >= length:
                    space1 = list(combinations(cardBs,length))
                    for js in space1:
                        space2 = cardAs + list(js)*2
                        ans.append({'c':space2,'p':length + 36,'s':size})

        return ans



    # enumerate all the possible next steps
    def getNextMove(self, cards, pattern, size):
        moves = []
        sets = set(cards)
        # bomb
        for card in sets:
            if cards.count(card) == 4 and (pattern != 1 or (pattern == 1 and card > size)):
                moves.append({ 'c': [card] * 4, 'p': 1, 's': card })
        # sequence
        if pattern == -1:
            for length in range(5, 14):
                moves = moves + self.getSeq(cards, length, -1, 1)
        if pattern >= 7 and pattern <= 14:
            moves = moves + self.getSeq(cards, pattern - 2, size, 1)

        # sequence of pairs
        if pattern == -1:
            for length in range(2, 14):
                moves = moves + self.getSeq(cards, length, -1, 2)
        if pattern >= 15 and pattern <= 25:
            moves = moves + self.getSeq(cards, pattern - 13, size, 2)
        # sequence of triplets
        if pattern == -1:
            for length in range(2, 7):
                moves = moves + self.getSeq(cards, length, -1, 3)
        if pattern >= 28 and pattern <= 32:
            moves = moves + self.getSeq(cards, pattern - 26, size, 3)
    
        # triplet with an attached card
        if pattern == -1 or pattern == 5:
            for card in sets:
                if cards.count(card) >= 3 and card > size:
                    for cardB in sets:
                        if card != cardB:
                            moves.append({ 'c': [card] * 3 + [cardB], 'p': 5, 's': card })
        # triplet with an attached pair
        if pattern == -1 or pattern == 6:
            for card in sets:
                if cards.count(card) >= 3 and card > size:
                    for cardB in sets:
                        if card != cardB and cards.count(cardB) >= 2:
                            moves.append({ 'c': [card] * 3 + [cardB] * 2, 'p': 6, 's': card })
        # triplet
        if pattern == -1 or pattern == 4:
            for card in sets:
                if cards.count(card) >= 3 and card > size:
                    moves.append({ 'c': [card] * 3, 'p': 4, 's': card })

        # airplane with single cards
        if pattern == -1:
            for length in range(2, 7):
                moves = moves + self.getPlane1(cards, length, -1)
        if pattern >= 33 and pattern <= 37:
            moves = moves + self.getPlane1(cards, pattern - 31, size)

        # airplane with pairs
        if pattern == -1:
            for length in range(2,5):
                moves = moves + self.getPlane2(cards,length, -1)
        if pattern >= 38 and pattern <= 40:
            moves = moves + self.getPlane2(cards,pattern - 36, size)


        
    
        # pair
        if pattern == -1 or pattern == 3:
            for card in sets:
                if cards.count(card) >= 2 and card > size:
                    moves.append({ 'c': [card] * 2, 'p': 3, 's': card })
        # single card
        if pattern == -1 or pattern == 2:
            for card in sets:
                if card > size:
                    moves.append({ 'c': [card], 'p': 2, 's': card })
        # skip
        if pattern != -1:
            moves.append({ 'c': [], 'p': -1, 's': -1 })


        return moves

    def judgepands(self, alist):
        if not alist:
            return [-1,-1]
        sets = set(alist)
        if len(alist) == 0:
            return [-1,-1]
        # bomb
        elif len(alist) == 4 and len(sets) == 1:
            return [1,alist[0]]
        # single card
        elif len(alist) == 1:
            return [2,alist[0]]
        # pair
        elif len(alist) == 2 and len(sets) == 1:
            return [3,alist[0]]
        # triplet
        elif len(alist) == 3 and len(sets) == 1:
            return [4,alist[0]]
        # triplet with single card
        elif len(alist) == 4 and len(sets) == 2 and (alist.count(alist[0]) == 1 or 3):
            for i in sets:
                if alist.count(i) == 3:
                    return [5,i]
        # triplet with pair
        elif len(alist) == 5 and len(set(alist)) == 2 and (alist.count(alist[0]) == 2 or 3):
            for i in sets:
                if alist.count(i) == 3:
                    return [6,i]
        # sequence / airplane
        
        list1 = isSeq1(alist)
        if list1[0] == True:
            return [list1[1],list1[2]]
        else:
            list2 = isSeq2(alist)
            if list2[0] == True:
                return [list2[1],list2[2]]
            else:
                list3 = isSeq3(alist)
                if list3[0] == True:
                    return [list3[1],list3[2]]
                else:
                    list4 = isPlane(alist)
                    if list4[0] == True:
                        return [list4[1],list4[2]]

    # delete one list delete another list
    def removeElements(self, listA, listB):
        # print('removeElements', listA, listB)
        if not listB:
            return
        for element in listB:
            if element in listA:
                listA.remove(element)

    # Generative Adversarial self.tree
    def searchTree(self, playerA, playerB, pattern, size, level, parent, mode, target_time):
        # print('searching')
        # return 1, find an appropriate result
        # return 0, cannot find an appropriate result
        # judge if timeout
        now = time.time()
        if now < target_time:

            # print('self.playerA:', self.playerA)
            # print('self.playerB:', self.playerB)
            # get all the possible combination of player A
            moves = self.getNextMove(playerA, pattern, size)
            # print('moves:', moves)
            # recursively iterate all the possible combinations
            for i, move in enumerate(moves):
                newPlayerA = copy.deepcopy(playerA)
                # print('newPlayerA', newPlayerA)
                # delete the current combination of cards from player one
                self.removeElements(newPlayerA, move['c'])
                self.count += 1
                temp = self.count

                self.tree.append([0, move['c'], []])
                self.tree[parent][2].append(self.count)
                # if player A run out of cards, he wins
                # print('len(newPlayerA)', len(newPlayerA))
                # if len(newPlayerA) == 0:
                if len(newPlayerA) == 0 or mode == 'random':
                    self.tree[self.count][0] = 1
                    # print('searched')
                    return 1
                else:
                    flag = 1
                    moves_ = self.getNextMove(playerB, move['p'], move['s'])
                    for j, move_ in enumerate(moves_):
                        newPlayerB = copy.deepcopy(playerB)
                        self.removeElements(newPlayerB, move_['c'])
                        self.count += 1
                        self.tree.append([0, move_['c'], []])
                        self.tree[temp][2].append(self.count)
                        if len(newPlayerB) == 0 or self.searchTree(newPlayerA, newPlayerB, move_['p'], move_['s'], level + 1, self.count, mode, target_time) == 0:
                        #  if player B doesn't have card or card cannot win, then player A cannot make full combinations
                            flag = 0
                            break
                    if flag == 1:
                        self.tree[temp][0] = 1
                        # if player A can win, then return 1
                        return 1
                    elif flag == 0 and level < 3:
                        # if player A cannot win, then return 0
                        self.tree = self.tree[:temp]
                        self.count = temp - 1
                return 1
            return 0
        else:
            return 1

            
    def play(self, Icards, mode, target_time):            
        self.root, p, s = 0, -1, -1
        if Icards != []:
            Ival = Icards
            self.getVal(Ival)
            listps = self.judgepands(Ival)
            p = listps[0]
            s = listps[1]
            self.removeElements(self.playerB,Ival)
        if self.searchTree(self.playerA,self.playerB,p,s,0,self.root,mode, target_time):
            # print('====searchedinggg tree!!')
            flag = 1
            if self.playerB == [] or self.playerA == []:
                flag = 0
            # print('flage:', flag)
            if flag == 1:
                # if not self.root in self.tree:
                #     return []
                for node in self.tree[self.root][2]:
                    # print('node', self.tree[node][0])
                    if not node in self.tree:
                        random_move = self.getNextMove(self.playerA,p,s)
                        if random_move != []:
                            moveI = random_move[0]['c']
                            self.removeElements(self.playerA,moveI)
                            return self.getCard(moveI)
                    if self.tree[node][0] == 1:
                        moveI = self.tree[node][1]
                        self.removeElements(self.playerA,moveI)
                        self.tree = [[0,[],[]]]
                        self.count = 0
                        # print('=====moveI:', moveI)
                        return self.getCard(moveI)
        else:
            random_move = self.getNextMove(self.playerA,p,s)
            if random_move != []:
                moveI = random_move[0]['c']
                self.removeElements(self.playerA,moveI)
                return self.getCard(moveI)
            else:
                return []
        

    def playARound(self, playerACard, playerBCard):
        self.playerA, self.playerB = playerACard, playerBCard

        # Use number value instead of Poker value
        self.getVal(self.playerA)
        self.getVal(self.playerB)
        # print('playerA, playerB', playerA, playerB)

        cur_time = time.time()
        target_time = cur_time + 3
        switch_who_first = random.randint(0, 1)
        RI = ''.split()
        while len(self.playerA) != 0 and len(self.playerB) != 0:
            if switch_who_first:
                self.playerA, self.playerB = self.playerB, self.playerA
                AI = self.play(RI, 'dfs', target_time)
                self.playerA, self.playerB = self.playerB, self.playerA
                RI = self.play(AI, 'random', target_time)
            AI = self.play(RI, 'random', target_time)
            self.playerA, self.playerB = self.playerB, self.playerA
            RI = self.play(AI, 'dfs', target_time)
            self.playerA, self.playerB = self.playerB, self.playerA
        return 

    def drawCards(self, cardsize):
        card_type = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        card_pile = card_type * 4
        random.shuffle(card_pile)
        playerACard, playerBCard = [], []
        for card in range(cardsize):
            playerACard.append(card_pile.pop())
        for card in range(cardsize):
            playerBCard.append(card_pile.pop())
        # print('playerACard, playerBCard', playerACard, playerBCard)
        return playerACard, playerBCard

    def playMultipleTimes(self):
        time_per_cardsize = 100
        min_cardsize = 2
        max_cardsize = 6
        random_win, dfs_win = [], []
        for cardsize in range(min_cardsize, max_cardsize + 1):
            awin_cur, bwin_cur = 0, 0
            for times in range(time_per_cardsize):
                playerACard, playerBCard = self.drawCards(cardsize)
                self.playARound(playerACard, playerBCard)
                print('self.playerA, self.playerB', self.playerA, self.playerB)
                if len(self.playerA) == 0:
                    awin_cur += 1
                elif len(self.playerB) == 0:
                    bwin_cur += 1
            random_win.append(awin_cur)
            dfs_win.append(bwin_cur)
        print('random_win, dfs_win', random_win, dfs_win)
solution = Solution()
solution.playMultipleTimes()