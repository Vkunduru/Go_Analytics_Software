import sys
import globals
import os.path
import MonteCarlo
from Player import Player

class GAME(object):

    def __init__(self):
        p1 = None
        p2 = None
        GAME_TREE = MonteCarloNode()

    def play_GO(self):

        p1 = Player(globals.BLACK)
        p2 = Player(globals.WHITE)

        moveList = [] #black plays first, then white plays List containing all moves made in game
        move = None


        cur_player = p1
        passes = 0
        new_game = 1

        p1_score = 0
        p2_score = 0
        winner = None


        while (passes != 2):

            if(cur_player.get_color() == globals.BLACK): passes = 0

            print cur_player.get_color()

            move = cur_player.make_move()

            if (move == -1):           break
            if (move == globals.PASS): passes += 1

            moveList.append(move)


            if cur_player.get_color() == globals.BLACK: cur_player = p2
            else:                                       cur_player = p1

        if move != -1:
            p1_score = p1.calculate_score()
            p2_score = p2.calculate_score()

            if   p1_score > p2_score:   winner = globals.BLACK
            elif p1_score < p2_score:   winner = globals.WHITE


        self.print_moveList(winner, moveList)

        print "BLACK: %d. White: %d." % ( p1_score, p2_score )
        print "Game has ended."


    def print_moveList(self, winner, moveList):

        gp = open("MoveList.txt", 'w')

        player = None

        gp.write("%r \n" % winner)

        for move in moveList:

            if player == globals.BLACK: player = globals.WHITE
            else:                       player = globals.BLACK

            if move == globals.PASS:
                gp.write( "%d  PASS \n" % player)
            elif move > 0 and move < globals.GAME_SIZE:
                gp.write( "%d  %d %d \n" % (player, (move/globals.BOARD_SIDE), (move%globals.BOARD_SIDE) ) )

        gp.close()




#this is where the program should be run from
my_game = GAME()
my_game.play_GO()