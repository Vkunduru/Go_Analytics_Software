# import Stone
import globals

class Player(object):

    def __init__(self, Color):
        self.strings = [[]]     #[string, string, string, ..etc] all strings for this Player object
        self.color = Color
        self.prisoners = 0
        self.territories = 0
        self.lastmove = None

    # Returns the GB position of the move made or global.PASS
    def make_move(self):

        ko = 0
        ret_val = -1
        while(ret_val == -1):
            move = raw_input("What move should be made: ( 'pass' 'stone' ): ")

            if(move == 'pass'):
                return globals.PASS
                break

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

        liberties = self.get_liberties(pos)

        captured = 0
        for lib in liberties:
            if lib == None or globals.GB[lib] == None: continue
            if globals.GB[lib] != pc: captured = self.capture(lib)

        self.printGB()
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
    #        0 if string cannot be captured
    #TODO: make sure prisoner count is being updated correctly
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

        return captured

    # return a list of the liberties
    def get_liberties(self, pos):

        lib  = [None, None, None, None]

        left   = pos - 1;
        right  = pos + 1;
        top    = pos - 19;
        bottom = pos + 19;

        if (pos % 19 != 0):  lib[0] = left;
        if (pos % 19 != 18): lib[1] = right;
        if (pos > 18):       lib[2] = top;
        if (pos < 342):      lib[3] = bottom;

        return lib

    #TODO: finish function calculate_Territories to determine winnings of a game GO
    def calculate_territories(self):
        return None

    #creates a text file displaying the gameboard
    def printGB(self):

        txt = open("GB.txt", 'w')
        txt.write("GAMEBOARD \n")
        txt.write("  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 \n")

        str = ''

        for x in range(globals.BOARD_SIDE):
            if x < 10: x_str = "%r  " % x
            else: x_str = "%r " % x

            for y in range(globals.BOARD_SIDE):
                str = str + { None : '.  ', 1 : '1  ', 0 : '0  '}[ globals.GB[x * globals.BOARD_SIDE + y] ]
            txt.write(x_str + str + '\n')
            str = ''

        txt.close()