import random

class Minefield:

    CELL_MINE = '[*]'
    CELL_EMPTY = '[ ]'
    CELL_COUNTER = '[%d]'
    
    __field = None
    __w = 0
    __h = 0
    __m = 0

    def __init__(self, width: int, height: int, mines: int):
        self.__w = width
        self.__h = height

        #init field array
        self.__field = [self.CELL_EMPTY] * self.__h
        for h in range(self.__h):
            self.__field[h] = [self.CELL_EMPTY] * self.__w
        
        self.__fillMines(mines)
        self.__fillCounters()
    
    def __fillMines(self, mines: int):
        # fill mines
        mines_max = self.__w * self.__h * 0.135
        if mines > mines_max:
            self.__m = int(mines_max)
        else:
            self.__m = mines
        for _ in range(self.__m):
            cell = self.CELL_MINE
            while cell == self.CELL_MINE:
                pos = random.randrange(self.__w * self.__h)
                pos_h = int(pos / self.__w)
                pos_w = pos % self.__w
                cell = self.__field[pos_h][pos_w]
            self.__field[pos_h][pos_w] = self.CELL_MINE
    
    def __countMinesAround(self, pos: int) -> int:
        mines = 0
        pos_h = int (pos / self.__w)
        pos_w = pos % self.__w
        
        if self.__field[pos_h][pos_w] == self.CELL_EMPTY:
            #left
            if pos_w > 0 and self.__field[pos_h][pos_w-1] == self.CELL_MINE:
                mines += 1
            #right
            if pos_w < self.__w-1 and self.__field[pos_h][pos_w+1] == self.CELL_MINE:
                mines += 1
            #top
            if pos_h > 0 and self.__field[pos_h-1][pos_w] == self.CELL_MINE:
                mines += 1
            #top left
            if pos_h > 0 and pos_w > 0 and self.__field[pos_h-1][pos_w-1] == self.CELL_MINE:
                mines += 1
            #top right
            if pos_h > 0 and pos_w < self.__w-1 and self.__field[pos_h-1][pos_w+1] == self.CELL_MINE:
                mines += 1
            #bottom
            if pos_h < self.__h-1 and self.__field[pos_h+1][pos_w] == self.CELL_MINE:
                mines += 1
            #bottom left
            if pos_h < self.__h-1 and pos_w > 0 and self.__field[pos_h+1][pos_w-1] == self.CELL_MINE:
                mines += 1
            #bottom rigt
            if pos_h < self.__h-1 and pos_w < self.__w-1 and self.__field[pos_h+1][pos_w+1] == self.CELL_MINE:
                mines += 1
            
        return mines

    def __fillCounters(self):
        for h in range(self.__h):
            for w in range(self.__w):
                mines = self.__countMinesAround(h * self.__w + w)
                if mines > 0:
                    self.__field[h][w] = '[{}]'.format(mines)
    
    @property
    def field(self):
        return self.__field

    def __str__(self):
        out = ''
        for h in range(self.__h):
            if h == 0:
                out += '  '
                for w in range(self.__w):
                    out += ' '+str(w)+' '
                    pass
                out += "\n"
            out += str(h)+' '
            for w in range(self.__w):
                out += str(self.__field[h][w])
            out += "\n"
        return out

