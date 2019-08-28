#Ein Move soll einen, evtl. noch unvollständigen Zug, modellieren. Hat ein Spieler in der Ziehen-Phase einen Stein
#ausgewaehlt (from_pos) und das Ziel angegeben (to_pos) soll, der Zug schon gespeichert sein, obwohl u.U. noch ein zu
#entfernender Stein ausgewählt werden muss.

class Move:
    #Werte von -1 bis 23 sind Positionen auf dem Brett, wobei, -1 ein Platzhalterwert sein soll
    #Z.B. wenn ein Move nicht zu einer Muehle geführt hat, soll remove = -1 sein
    def __init__(self, color, from_pos = -1, to_pos = -1, remove_pos = -1):
        self.color = color % 2
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.remove_pos = remove_pos

    #Wenn klar ist, wohin Stein platziert wird, wird diese Methode aufgerufen.
    def set_to(self, to_pos):
        self.to_pos = to_pos

    #Wenn klar ist, das eine Mühle verursacht wurde und welcher Stein entfernt werden soll, wird diese Methode aufgerufen
    def set_remove(self, remove_pos):
        self.remove_pos = remove_pos


