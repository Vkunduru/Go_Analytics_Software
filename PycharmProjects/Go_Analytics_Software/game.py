import sys
import globals
from Player import Player

def play_GO():
    p1 = Player(globals.BLACK)
    p2 = Player(globals.WHITE)

    cur_player = p1
    passes = 0
    turns_taken = 0

    while (passes != 2):

        if(cur_player.get_color() == globals.BLACK):
            passes = 0
            turns_taken += 1

        if(cur_player.make_move() == globals.PASS): # make_move()
            passes += 1

        print cur_player.get_color()
        if(cur_player.get_color() == globals.BLACK): cur_player = p2
        else: cur_player = p1

    print "BLACK: %r. White: %r." % ( p1.calculate_territories(), p2.calculate_territories() )
    print "Game has ended. %r turns have been taken" % (turns_taken)


#this is where the program should be run from
play_GO()
