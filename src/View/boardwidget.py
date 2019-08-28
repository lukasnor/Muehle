from PyQt5 import QtCore, QtGui, QtWidgets


class BoardWidget(QtWidgets.QWidget):
    position_pressed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)  # statt:
        # QtGui.QWidget.__init__(self, parent)
        # entnommen Python Buch S 856, Teil 2 malt das Bild dann

        # Spielbrett Bild
        self.board = QtGui.QImage("BildSpielfeld.jpg")
        self.quelle_board = QtCore.QRect(0, 0, self.board.width(), self.board.height())
        # Größe von QWidget holen: Get width und height
        a = 10  # Anfang Brett
        b = self.width()  # Größe Brett
        self.ziel_board = QtCore.QRect(a, a, b, b)  # wo das Bild angezeigt wird, skalierbar
        # Hilfsvariablen
        s = (b - a) * 0.095  # Größe der Grafik
        d = s / 2  # Durchmesser der Graphik
        l1 = d  # Ebenenhöhe
        l2 = b / 5
        l3 = b / 2.85
        m = b / 2  # Mitte
        self.board_position = (
            QtCore.QRect(a + l1 - d, a + l1 - d, s, s), QtCore.QRect(a + m - d, a + l1 - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + l1 - d, s, s),
            QtCore.QRect(a + l2 - d, a + l2 - d, s, s), QtCore.QRect(a + m - d, a + l2 - d, s, s),
            QtCore.QRect(a + b - l2 - d, a + l2 - d, s, s),
            QtCore.QRect(a + l3 - d, a + l3 - d, s, s), QtCore.QRect(a + m - d, a + l3 - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + l3 - d, s, s),
            QtCore.QRect(a + l1 - d, a + m - d, s, s), QtCore.QRect(a + l2 - d, a + m - d, s, s),
            QtCore.QRect(a + l3 - d, a + m - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + m - d, s, s), QtCore.QRect(a + b - l2 - d, a + m - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + m - d, s, s),
            QtCore.QRect(a + l3 - d, a + b - l3 - d, s, s), QtCore.QRect(a + m - d, a + b - l3 - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + b - l3 - d, s, s),
            QtCore.QRect(a + l2 - d, a + b - l2 - d, s, s), QtCore.QRect(a + m - d, a + b - l2 - d, s, s),
            QtCore.QRect(a + b - l2 - d, a + b - l2 - d, s, s),
            QtCore.QRect(a + l1 - d, a + b - l1 - d, s, s), QtCore.QRect(a + m - d, a + b - l1 - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + b - l1 - d, s, s)
        )  # hier sollen die Spielstein rein bzw werden die Mausklicks gelesen

        # Spielsteine Bild
        self.black = QtGui.QImage("black.png")
        self.quelle_black = QtCore.QRect(0, 0, self.black.width(), self.black.height())
        self.white = QtGui.QImage("white.png")
        self.quelle_white = QtCore.QRect(0, 0, self.white.width(), self.white.height())
        self.red = QtGui.QImage("Red-circle.svg")
        self.quelle_red = QtCore.QRect(0, 0, self.red.width(), self.red.height())

        # Kommunikation und Berechnung
        self.nodes = (-1, -1, -1, -1, -1, -1,
                      -1, -1, -1, -1, -1, -1,
                      -1, -1, -1, -1, -1, -1,
                      -1, -1, -1, -1, -1, -1)  # Zustad des Brettes
        self.marked_node = -1  # markierter Knoten falls vorhanden

        self.update()

    # event handler
    # Board, Steine und Markierung zeichnen
    def paintEvent(self, event):
        a = 10  # Anfang Brett
        b = min(self.width(), self.height()) - 10  # Größe Brett
        self.ziel_board = QtCore.QRect(a, a, b, b)  # wo das Bild angezeigt wird, skalierbar
        # Hilfsvariablen
        s = (b - a) * 0.095  # Größe der Grafik
        d = s / 2  # Durchmesser der Graphik
        l1 = d  # Ebenenhöhe
        l2 = b / 5
        l3 = b / 2.85
        m = b / 2  # Mitte
        self.board_position = (
            QtCore.QRect(a + l1 - d, a + l1 - d, s, s), QtCore.QRect(a + m - d, a + l1 - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + l1 - d, s, s),
            QtCore.QRect(a + l2 - d, a + l2 - d, s, s), QtCore.QRect(a + m - d, a + l2 - d, s, s),
            QtCore.QRect(a + b - l2 - d, a + l2 - d, s, s),
            QtCore.QRect(a + l3 - d, a + l3 - d, s, s), QtCore.QRect(a + m - d, a + l3 - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + l3 - d, s, s),
            QtCore.QRect(a + l1 - d, a + m - d, s, s), QtCore.QRect(a + l2 - d, a + m - d, s, s),
            QtCore.QRect(a + l3 - d, a + m - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + m - d, s, s), QtCore.QRect(a + b - l2 - d, a + m - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + m - d, s, s),
            QtCore.QRect(a + l3 - d, a + b - l3 - d, s, s), QtCore.QRect(a + m - d, a + b - l3 - d, s, s),
            QtCore.QRect(a + b - l3 - d, a + b - l3 - d, s, s),
            QtCore.QRect(a + l2 - d, a + b - l2 - d, s, s), QtCore.QRect(a + m - d, a + b - l2 - d, s, s),
            QtCore.QRect(a + b - l2 - d, a + b - l2 - d, s, s),
            QtCore.QRect(a + l1 - d, a + b - l1 - d, s, s), QtCore.QRect(a + m - d, a + b - l1 - d, s, s),
            QtCore.QRect(a + b - l1 - d, a + b - l1 - d, s, s)
        )  # hier sollen die Spielstein rein bzw werden die Mausklicks gelesen

        painter = QtGui.QPainter(self)
        painter.drawImage(self.ziel_board, self.board, self.quelle_board)
        for i in range(24): # TODO
            if self.nodes[i] == 0:
                painter.drawImage(self.board_position[i], self.white, self.quelle_white)
            elif self.nodes[i] == 1:
                painter.drawImage(self.board_position[i], self.black, self.quelle_black)
        if self.marked_node is not -1:
            painter.drawImage(self.board_position[self.marked_node], self.red, self.quelle_red)

    def mousePressEvent(self, event):
        for i in range(24):
            if self.board_position[i].contains(event.pos()):
                self.position_pressed.emit(i)

    def set_nodes(self,nodes):
        self.nodes = nodes
        self.update()

    def set_marked_node(self, node):
        self.marked_node = node
        self.update()

if __name__ == "__main__":
    import sys

    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    board = BoardWidget()
    board.show()
    sys.exit(app.exec_())
