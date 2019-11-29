import minefield

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MinesWindow(Gtk.Window):

    GAME_ROWS = 9
    GAME_COLS = 9
    GAME_MINES = 30
    GAME_STATUS_OK = 1
    GAME_STATUS_ENDED = 2

    __grid = None
    __mf = None
    __status = GAME_STATUS_OK
    __btns = None
    __open_cells = 0

    def __init__(self):
        Gtk.Window.__init__(self, title="Mines")

        grid = Gtk.Grid(row_spacing = 3, column_spacing = 3, margin = 10)
        self.add(grid)
        self.__grid = grid
        self.__drawField();
    
    def __drawField(self):
        self.__mf = minefield.Minefield(self.GAME_COLS, self.GAME_ROWS, self.GAME_MINES)
        #print(self.__mf)
        field = self.__mf.field
        self.__open_cells = self.GAME_COLS * self.GAME_ROWS

        # init buttons array
        self.__btns = [0] * self.GAME_ROWS
        for h in range(self.GAME_ROWS):
            self.__btns[h] = [0] * self.GAME_COLS

        # generate buttons
        for h in range(self.GAME_ROWS):
            for w in range(self.GAME_COLS):
                btn = Gtk.Button(label='   ', width_request = 40, height_request = 40)
                btn.connect('clicked', self.on_cell_click, h*self.GAME_COLS + w)
                self.__grid.attach(btn, w, h, 1, 1)
                self.__btns[h][w] = btn;
    
    def on_cell_click(self, button, id):
        if self.__status == self.GAME_STATUS_OK and button.is_sensitive():
            # process clicks
            pos_h = int (id / self.GAME_COLS)
            pos_w = id % self.GAME_COLS
            field = self.__mf.field
            cell = field[pos_h][pos_w]

            if cell == minefield.Minefield.CELL_MINE:
                # we've got mine
                self.__status = self.GAME_STATUS_ENDED
                self.__grid.set_sensitive(False)
                button.set_label(' X ')
                self.__showEndGame(False)

            elif cell == minefield.Minefield.CELL_EMPTY:
                # check each near cell and if that one clear, click it
                button.set_sensitive(False)
                self.openCleanArea(id)

            else:
                # else show counter
                button.set_label(' {} '.format(cell[1]))

            button.set_sensitive(False)
            self.__open_cells -= 1
            if self.__open_cells == self.__mf.mines:
                # WON
                self.__status = self.GAME_STATUS_ENDED
                self.__grid.set_sensitive(False)
                self.__showEndGame(True)

        else:
            # do not process clicks when game ended
            pass
    
    def openCleanArea(self, pos: int):
        pos_h = int (pos / self.GAME_COLS)
        pos_w = pos % self.GAME_COLS
        field = self.__mf.field
        
        if field[pos_h][pos_w] == minefield.Minefield.CELL_EMPTY:
            #left
            if pos_w > 0 and field[pos_h][pos_w-1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h][pos_w-1], pos_h * self.GAME_COLS + pos_w-1)
            #right
            if pos_w < self.GAME_COLS-1 and field[pos_h][pos_w+1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h][pos_w+1], pos_h * self.GAME_COLS + pos_w+1)
            #top
            if pos_h > 0 and field[pos_h-1][pos_w] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h-1][pos_w], (pos_h-1) * self.GAME_COLS + pos_w)
            #top left
            if pos_h > 0 and pos_w > 0 and field[pos_h-1][pos_w-1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h-1][pos_w-1], (pos_h-1) * self.GAME_COLS + pos_w-1)
            #top right
            if pos_h > 0 and pos_w < self.GAME_COLS-1 and field[pos_h-1][pos_w+1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h-1][pos_w+1], (pos_h-1) * self.GAME_COLS + pos_w+1)
            #bottom
            if pos_h < self.GAME_ROWS-1 and field[pos_h+1][pos_w] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h+1][pos_w], (pos_h+1) * self.GAME_COLS + pos_w)
            #bottom left
            if pos_h < self.GAME_ROWS-1 and pos_w > 0 and field[pos_h+1][pos_w-1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h+1][pos_w-1], (pos_h+1) * self.GAME_COLS + pos_w-1)
            #bottom rigt
            if pos_h < self.GAME_ROWS-1 and pos_w < self.GAME_COLS-1 and field[pos_h+1][pos_w+1] != minefield.Minefield.CELL_MINE:
                self.on_cell_click(self.__btns[pos_h+1][pos_w+1], (pos_h+1) * self.GAME_COLS + pos_w+1)

    
    def __showEndGame(self, won):
        if won == True:
            # show winning message
            dialog = Gtk.MessageDialog(parent=self, message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK, text='Congratulations! You have WON!')
        else:
            # show fail message
            dialog = Gtk.MessageDialog(parent=self, message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK, text='B00M')
        dialog.format_secondary_text('Restart me to play again')
        dialog.run()
        dialog.destroy()

window = MinesWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()