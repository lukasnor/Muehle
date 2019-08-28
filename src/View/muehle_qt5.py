import sys, Model.Board
from PyQt5 import QtCore, QtWidgets, uic


Ui_MainWindow, WindowBaseClass = uic.loadUiType("Muehle.ui")

class MyDialog(WindowBaseClass, Ui_MainWindow):
    def __init__(self, parent=None):
        WindowBaseClass.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.board = Model.Board.Board()

        self.widget_board.position_pressed.connect(self.receive_pos)
        self.resetButton.clicked.connect(self.reset_button_clicked)

        self.update_gui()

    def receive_pos(self, pos):
        self.board.receive_pos(pos)
        self.update_gui()

    def update_gui(self):
        self.widget_board.set_nodes(self.board.nodes)
        self.widget_board.set_marked_node(self.board.next_move.from_pos)
        self.players_turn.setPlainText(self.get_players_turn_string())
        self.set_black.setText(self.get_num_pieces_string(1))
        self.set_white.setText(self.get_num_pieces_string(0))
        self.phase_black.setPlainText(self.get_phase_string(1))
        self.phase_white.setPlainText(self.get_phase_string(0))
        #self.spielausgang TODO

    def reset_button_clicked(self):
        self.board.reset()
        self.update_gui()

    def get_players_turn_string(self):
        color = self.board.next_move.color
        if color == 0:
            return "Weiß"
        if color == 1:
            return "Schwarz"
        return "Fehler"

    def get_num_pieces_string(self, color):
        return str(self.board.get_num_of_pieces_left_to_place(color))

    def get_phase_string(self,color):
        return str(self.board.phases[color])

if __name__ == "__main__":
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
    