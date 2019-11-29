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

    def __init__(self):
        Gtk.Window.__init__(self, title="Mines")

        grid = Gtk.Grid(row_spacing = 3, column_spacing = 3, margin = 10)
        self.add(grid)
        self.__grid = grid
        self.__drawField();
    
    def __drawField(self):
        self.__mf = minefield.Minefield(self.GAME_COLS, self.GAME_ROWS, self.GAME_MINES)
        print(self.__mf)
        field = self.__mf.field

        # generate buttons
        for h in range(self.GAME_ROWS):
            for w in range(self.GAME_COLS):
                btn = Gtk.Button(label='   ', width_request = 40, height_request = 40)
                btn.connect('clicked', self.on_cell_click, h*self.GAME_COLS + w)
                self.__grid.attach(btn, w, h, 1, 1)
    
    def on_cell_click(self, button, id):
        if self.__status == self.GAME_STATUS_OK:
            # process clicks
            pos_h = int (id / self.GAME_COLS)
            pos_w = id % self.GAME_COLS
            field = self.__mf.field
            if field[pos_h][pos_w] == minefield.Minefield.CELL_MINE:
                # we've got mine
                self.__status = self.GAME_STATUS_ENDED
                self.__showEndGame(False)
        else:
            # do not process clicks when game ended
            pass
    
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