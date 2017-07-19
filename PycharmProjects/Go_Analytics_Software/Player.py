# import Stone
import globals

class Player(object):

    def __init__(self, Color):
        self.strings = [[]]     #[string, string, string, ..etc] all strings for this Player object
        self.color = Color
        self.prisoners = 0
        self.territories = 0
        self.lastmove = None


    # ***** GAMEPLAY *****

    # Returns the GB position of the move made or global.PASS
    def make_move(self):

        ko = 0
        ret_val = -1
        while(ret_val == -1):
            move = raw_input("What move should be made: ( 'pass' 'stone' 'exit' ): ")

            if(move == 'pass'):
                return globals.PASS
                break

            if(move == 'exit'): return -1

            if(move == 'stone'):
                x , y = map(int, raw_input("X and Y coordinates: ").split())
                pos = x * globals.BOARD_SIDE + y

                #ko rule check
                if(pos != self.lastmove):
                    ko = 0
                else: ko = 1

                if(pos < globals.GAME_SIZE and not(ko)):
                    self.lastmove = pos
                    ret_val = self.place_stone(pos)  # place_stone(pos)

            if(ret_val == -1 or ko == 1): print("Invalid Move. Still your turn.")

        return ret_val

    # Return -1 if stone cannot be placed
    #        pos if stone can be placed
    def place_stone(self, pos):

        if( not(self.is_legal(pos)) ): return -1

        pc = self.get_color()

        globals.GB[pos] = pc
        globals.TER[pos] = globals.WALL

        liberties = self.get_liberties(pos)

        captured = 0
        for lib in liberties:
            if lib == None or globals.GB[lib] == None: continue
            if globals.GB[lib] != pc: captured = self.capture(lib)

        self.printGB()
        self.printTERBOARD()

        return pos
    # Return 0 if pos on GB is occupied or stone placement is self capture
    #        1 if not ^
    def is_legal(self, pos):

        if pos < globals.GAME_SIZE:
            if globals.GB[pos] == None:
                return not(self.self_capture(pos))
        else: return 0

    # Return: 1 if pos is self capture
    #         0 if pos is not self capture
    def self_capture(self, pos):

        self_capture = 1
        liberties = self.get_liberties(pos)
        pc = self.get_color()

        for lib in liberties:
            if lib == None : continue
            if globals.GB[lib] == pc or globals.GB[lib] == None :
                self_capture = 0
                break

        if(self_capture):
            for lib in liberties:
                globals.GB[pos] = pc
                if( not(self.capture(lib)) ): globals.GB[pos] = None
                else:
                    self.add_to_strings(pos)
                    self_capture = 0

        return self_capture

    # Return color of player
    def get_color(self):
        return self.color

    # Returns 1 if capture successful (stones removed/ prisoners updated)
    #         0 if string not captured (stones not removed/ prisoners not updated)
    def capture(self, pos):

        return self.captureHelper(pos, None)

    # Return 1 if string can be captured
    def captureHelper(self, pos, prevpos):

        pos_c = globals.GB[pos]
        captured = 1

        liberties = self.get_liberties(pos)

        #base case
        for lib in liberties:
            if lib != None and globals.GB[lib] == None:
                captured = 0

        # recursion
        for lib in liberties:
            if lib == None: continue
            if globals.GB[lib] == pos_c and lib != prevpos:
                captured = captured and self.captureHelper(lib, pos)

        #backtrace
        if (captured):
            self.prisoners += 1
            globals.GB[pos] = None
            globals.TER[pos] = None

        return captured

    # return a list of the liberties
    def get_liberties(self, pos):

        lib  = [None, None, None, None]

        left   = pos - 1;
        right  = pos + 1;
        top    = pos - globals.BOARD_SIDE;
        bottom = pos + globals.BOARD_SIDE;

        if pos % globals.BOARD_SIDE != 0:                       lib[0] = left
        if pos % globals.BOARD_SIDE != (globals.BOARD_SIDE -1): lib[1] = right
        if pos > (globals.BOARD_SIDE -1):                       lib[2] = top
        if pos < ( (globals.BOARD_SIDE - 1) * globals.BOARD_SIDE):  lib[3] = bottom

        return lib



    # ***** SCORING *****

    def calculate_score(self):

        stones = self.stones_on_board()
        self.total_territories()
        self.printTERBOARD()

        if(self.lastmove == None): return 0 # if no moves have been made on board, Score is 0
        else: return stones + self.territories

    # Return the number of stones player has on board
    def stones_on_board(self):

        pc = self.get_color()
        stones = 0

        for i in range(globals.BOARD_SIDE):
            for j in range(globals.BOARD_SIDE):
                if globals.GB[i*globals.BOARD_SIDE + j] == pc: stones += 1

        return stones

    # void fn: increments self.territories according to number of territories player has on board
    def total_territories(self):

        pc = self.get_color()

        for i in range(globals.GAME_SIZE):
            if globals.TER[i] == None:
                self.ttHelper(i) # return value not required

        self.fix_neutral_ters()

        for i in range(globals.GAME_SIZE):
            if globals.TER[i] == globals.NEUT:   globals.TER[i] = None
            if globals.TER[i] == pc:  self.territories += 1

        return

    #Returns 1 if territory can count towards final score
    #        0 if territory is neutral
    def ttHelper(self, pos):

        pc = self.get_color()
        all_pc = 1
        liberties = self.get_liberties(pos)

        globals.TER[pos] = pc

        for lib in liberties:
            if lib == None: continue
            if globals.TER[lib] == None:
                all_pc = all_pc and self.ttHelper(lib)
            else:
                if globals.TER[lib] == globals.WALL and globals.GB[lib] != pc : all_pc = 0

        if(not all_pc): globals.TER[pos] = globals.NEUT
        return all_pc

    # void fn: fixes neutral territories to be all neutral
    def fix_neutral_ters(self):

        for i in range(globals.GAME_SIZE):
            liberties = self.get_liberties(i)
            for lib in liberties:
                if lib == None: continue
                if globals.TER[i] != globals.WALL:
                    if(globals.TER[lib] == globals.NEUT):
                        globals.TER[i] = globals.NEUT
                        break
            continue



    # ***** PRINTING BOARDS *****

    #creates a text file displaying the gameboard
    def printGB(self):

        txt = open("GB.txt" , 'w')
        txt.write("BOARD \n" )
        txt.write("  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 \n")

        str = ''

        for x in range(globals.BOARD_SIDE):
            if x < 10: x_str = "%r  " % x
            else:      x_str = "%r " % x

            for y in range(globals.BOARD_SIDE):
                str = str + { None : '.  ', 1 : '1  ', 0 : '0  '}[ globals.GB[x * globals.BOARD_SIDE + y] ]
            txt.write(x_str + str + '\n')
            str = ''

        txt.close()

    #creates a text file displaying territory board
    def printTERBOARD(self):

        txt = open("TERBOARD.txt" , 'w')
        txt.write("BOARD \n" )
        txt.write("  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 \n")

        str = ''

        for x in range(globals.BOARD_SIDE):
            if x < 10: x_str = "%r  " % x
            else:      x_str = "%r " % x

            for y in range(globals.BOARD_SIDE):
                str = str + { None : '.  ', 0 : '0  ', 1 : '1  ', 2 : '2  ', 3 : '3  '}[ globals.TER[x * globals.BOARD_SIDE + y] ]
            txt.write(x_str + str + '\n')
            str = ''

        txt.close()