import View,Model
from PyQt5 import QtCore, QtWidgets, uic

# "main_window.ui" muss zu der .ui-Datei in der View führen
Ui_MainWindow, WindowBaseClass = uic.loadUiType("main_window.ui")

class Controller(WindowBaseClass, Ui_MainWindow):
    def __init__(self, parent=None):
        WindowBaseClass.__init(self,parent)
        Ui_MainWindow.__init(self)
        self.setupUi(self)
        self.resize(1100,800)
        self.board = Model.Board.Board()

    # Slots for GUI

    def receive_clicked_position(self, position): # from Boardwidget
        pass

    def reset_board(self):  # from Infopanel
        pass

    # Slots for Model

    def receive_move_info(self, info): # from Board.is_move_legal()
        pass

    def receive_game_info(self, info): # from Board.check_game_end
        pass

    def receive_phase_info(self, phases): # from Board.update_phases()
        pass

    def receive_turn_info(self, player_number): # from Board.make_move()
        pass

    def receive_unset_pieces_number(self, lst): # from Board.make_move()
        pass

    def change_nodes(self, nodes): # from Board.make_move()
        pass

    # Signals for GUI

    received_move_info = QtCore.pyqtSignal(str)

    received_game_info = QtCore.pyqtSignal(str)

    received_phase_info = QtCore.pyqtSignal(list)

    received_turn_info = QtCore.pyqtSignal(int)

    received_unset_pieces_number = QtCore.pyqtSignal(list)

    received_changed_nodes = QtCore.pyqtSignal(tuple)

