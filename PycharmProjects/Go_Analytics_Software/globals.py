#define all constants and globals needed for this game script
import array

BOARD_SIDE = 9
GAME_SIZE = BOARD_SIDE * BOARD_SIDE
PASS = GAME_SIZE + 1

BLACK = 1
WHITE = 0

#global gameboard array to contain the stone color in the respective location
GB = [None] * GAME_SIZE
TER = [None] * GAME_SIZE

WTER = 0
BTER = 1
WALL = 2
NEUT = 3

