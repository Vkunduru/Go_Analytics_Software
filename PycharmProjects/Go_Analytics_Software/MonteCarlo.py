import globals
import random

root_node = MonteCarloNode()  # node pointer to base of tree
root_node.node_level = 0

# **** Main 4 Steps in Monte Carlo Tree Search *****

    # start from root R and select successive child nodes down to a leaf node L
    def selection():

        #start from root node R
        L_node = root_node

        # select successive child nodes down to a leaf node L
        while len(L_node.next_moves) != 0:
            L_node = exploit_explore(L_node.next_moves)

        return L_node

    # Exploitation + Exploration formula applied on the list of next_moves
    def exploit_explore(moves_list):
         return None # formula application goes here

    # unless L ends the game with a W/L for either player,
    # create one or more child nodes and choose node C from one of them
    def expansion(L_node):

        # unless L ends the game with a W/L for either player
        if(L_node.who_wins != None): return 1 # note to backpropagate if 1 is returned from expansion

        # TODO: note to keep a tally of number of moves available on the board after L_node's move is made somewhere to know how many
        # TODO: child nodes can still be added to L_node's next_move list

        # TODO: have used the number 5 for now

        # create one or more child nodes
        children_created = L_node.create_children( random.randrange(5) )

        # choose and return node C
        return children_created[random.randrange(5)]


    # play a random playout from a node C
    def simulation(self):
         pass # this function is taken care of by the script1.sh file as of now

    # use the result of the playout to update information in the nodes on the path form C to R
    def backpropagation(self, cur_node, winner):

        while (cur_node != None):
            cur_node.update_ratio(winner)

            # update next_best_move
            cur_node_p = cur_node.parent
            if cur_node_p != None and cur_node_p.next_best_move.get_ratio() < cur_node.get_ratio(): cur_node_p.next_best_move = cur_node

            cur_node = cur_node_p

    # # RAPID ACTION VALUE ESTIMATION  - use to reduce the exploratory phase significantly
    # def RAVE(self):
    #     pass

    #checks if is next best move in its parent node, if so updates returns 1
    # otherwise returns 0

#TODO: need a pointer to whole tree to stay stagnant across multiple iterations of the program
#TODO: might make tree creation a separate program to run concurrently with GO program iterations

class MonteCarloNode:

    # TODO: are the variables initialized in __init__ the right variables needed (?) are any more variables applicable (?)
    def __init__(self):
        node_level = None
        move = None

        won_games = 0
        played_games = 0

        parent = None    # pointer
        next_moves = []  # list of next move nodes within tree from current move ( pointers to other nodes)

        next_best_move = None # holds pointer to next move node that has highest w/p ratio

        who_wins = None  # this var is to denote the winner at a given leaf node


    # returns the w/p ratio of the current node
    def get_ratio(self):
        return self.won_games / self.played_games

    # returns current node move
    def get_move(self):
        return self.move

    # updates win/played ratio of each node on backtrace
    def update_ratio(self, winner):
        if self.get_player_color() == winner: self.won_games = self.won_games + 1
        self.played_games = self.played_games + 1

    # determine player_color depending on level of tree (Black plays first, B-0, W-1, B-2, W-3 ,etc.)
    def get_player_color(self):
        if self.node_level % 2 == 0: return globals.BLACK
        else: return globals.WHITE


    # returns next_move node if node exists, adds move to next_move list otherwise
    def get_next_move(self, my_move):

        for nm in self.next_moves:
            if nm.get_move == my_move: return nm

        return self.add_next_move(my_move)

    # returns next_move node after move has been added
    def add_next_move(self, p_move):

        #create next_move node
        node = MonteCarloNode()
        node.node_level = self.node_level + 1
        node.move = p_move
        node.parent = self

        i = 0
        for nm in self.next_moves:
            if nm.get_move() > p_move:
                self.next_moves.insert(i, node)
                return node
            i = i + 1

        #if p_move > moves in next_moves then append node to end of list
        self.next_moves.append(node)
        return node

    # fn needed for MC tree search algorithm
    def create_children(self, num_child):
        moves_added = []
        for j in range(num_child):
            for i in range(globals.GAME_SIZE):
                if is_legal(
                        i):  # TODO: is_legal() is a fn from the player class and can be applied here. HOW TO DO THAT CORRECTLY?
                    moves_added.append(self.get_next_move(i))

        return moves_added
