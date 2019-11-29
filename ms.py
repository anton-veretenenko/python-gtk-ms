import minefield

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MinesWindow(Gtk.Window):

    GAME_ROWS = 9
    GAME_COLS = 9
    GAME_MINES = 30

    __grid = None
    __mf = None

    def __init__(self):
        Gtk.Window.__init__(self, title="Mines")

        grid = Gtk.Grid(row_spacing = 3, column_spacing = 3, margin = 10)
        self.add(grid)
        self.__grid = grid
        self.__drawField();
    
    def __drawField(self):
        self.__mf = minefield.Minefield(self.GAME_COLS, self.GAME_ROWS, self.GAME_MINES)
        print(self.__mf)
        b1 = Gtk.Button(label='b1', width_request = 40 , height_request = 40)
        #Gtk.Widget.set_size_request(b1, 12, 32)
        b2 = Gtk.Button(label='b2', width_request = 40 , height_request = 40)

        self.__grid.attach(b1, 0, 0, 1, 1)
        self.__grid.attach(b2, 1, 0, 1, 1)

window = MinesWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()