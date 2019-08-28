from Model import Move
from PyQt5 import QtCore


class Board():
    def __init__(self):
        # Spielbrett mit 24 Positionen, -1 heißt Position leer,
        self.nodes = tuple([-1 for i in range(24)])
        # Wie ist weiß codiert
        self.white = 0

        # Phases setzen 0, ziehen 1 und springen 2, self.phases[self.white] = white_phase!!!!
        self.phases = [0, 0]

        # Relevant für die Remis
        self.last_muehle_counter = 0
        # In node_states sollen alle erreichten Brettstellungen gespeichert werden.
        # Nach einer Mühle können alle vorherigen Stellungen nicht mehr erreicht werden, oder? TODO
        self.node_states = [].append(self.nodes)

    # Wieviele Steine einer Farbe gibt es?
    def get_num_pieces(self, color):
        return self.nodes.count(color)

    def update_phases(self):
        white_phase = 0
        black_phase = 0
        if len(self.node_states) >= 18:
            white_phase += 1
            if self.get_num_pieces(self.white) == 3:
                white_phase += 1
        if len((self.node_states)) >= 19:
            black_phase += 1
            if self.get_num_pieces((self.white + 1) % 2) == 3:
                black_phase += 1
        self.phases[self.white] = white_phase
        self.phases[(self.white + 1) % 2] = black_phase

    def is_move_legal(self, move):
        if self.nodes[move.to_pos] != -1:
            # Nicht auf besetzes Feld setzen
            return False
        if self.phases[move.color] == 0 and move.from_pos != -1:
            # Man darf gesetzte Steine nicht in der Setzen Phase bewegen
            return False
        if self.phases[move.color] == 1 and not self.are_positions_adjacent(move.from_pos, move.to_pos):
            # In der Ziehen Phase darf man nicht springen
            return False
        if move.remove_pos != -1:
            if not self.is_position_in_muehle_of_color(move.to_pos, move.color):
                # Man darf nur Steine entfernen, wenn man eine Muehle gemacht hat
                return False
            if move.color == self.nodes[
                move.remove_pos]:  # TODO spieler muss ja stein entfernen, wie könnte man das erzwingen?
                # Man darf nicht eigene Steine entfernen
                return False
            if self.is_position_in_muehle_of_color(move.remove_pos, (move.color + 1) % 2):
                if self.are_pieces_free((move.color + 1) % 2):
                    # Man muss Pieces entfernen, die nicht in einer Muehle sind
                    return False
        return True

    # Prüft, ob eine gegebene Farbe color an einer gegebenen Position pos in einer Mühle ist
    def is_position_in_muehle_of_color(self, pos, color):
        MUEHLEN_hor = [{i, i + 1, i + 2} for i in range(0, 22, 3)]
        MUEHLEN_ver = [{0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17}, {5, 13, 20},
                       {2, 14, 23}]
        muehle_hor, muehle_ver = set([]), set([])
        for muehle in MUEHLEN_hor:
            if pos in muehle:
                muehle_hor = muehle
        for muehle in MUEHLEN_ver:
            if pos in muehle:
                muehle_ver = muehle
        muehle_ver.discard(pos)
        muehle_hor.discard(pos)
        is_muehle_hor, is_muehle_ver = True, True
        for i in muehle_hor:
            if i != color:
                is_muehle_hor = False
        for i in muehle_ver:
            if i != color:
                is_muehle_ver = False
        return is_muehle_hor or is_muehle_ver

    # Prüft, ob Pieces nicht in Muehle sind
    def are_pieces_free(self, color):
        positions = [pos for pos in range(24) if self.nodes[pos] == color]
        for pos in positions:
            if not self.is_position_in_muehle_of_color(pos, color):
                return True
        return False

    # Prüft, ob Positionen benachbart sind
    def are_positions_adjacent(self, pos1, pos2):
        ADJ_hor = [{i, i + 1} for i in range(0, 22, 3)] + [{i + 1, i + 2} for i in range(0, 22, 3)]
        ADJ_ver = [{0, 9}, {9, 21}, {3, 10}, {10, 18}, {6, 11}, {11, 15}, {1, 4}, {4, 7}] + \
                  [{16, 19}, {19, 22}, {8, 12}, {12, 17}, {5, 13}, {13, 20}, {2, 14}, {14, 28}]
        return {pos1, pos2} in ADJ_hor + ADJ_ver

    # Gibt Menge der zu pos benachbarten Knoten aus
    def get_adjacent_positions(self, pos):
        adj_positions = set([])
        for i in range(24):
            if self.are_positions_adjacent(pos, i):
                adj_positions.add(i)
        return adj_positions

    def make_move(self, move):
        # wurde schon geprüft, ob der Move legal ist?
        new_nodes = [self.nodes[i] for i in range(24)]
        if move.from_pos != -1:
            new_nodes[move.from_pos] = -1
        new_nodes[move.to_pos] = move.color
        if move.remove_pos != -1:
            new_nodes[move.remove_pos] = -1
            self.last_muehle_counter = 0
        else:
            self.last_muehle_counter += 1
        self.nodes = tuple(new_nodes)
        self.node_states.append(self.nodes)
        self.update_phases()

    # Nur relevant fuer die Ziehen Phase und auch so geschrieben!
    def phase_one_get_legal_moves(self, color):
        positions = [pos for pos in range(24) if self.nodes[pos] == color]
        legal_moves = set([])
        for position in positions:
            adj_positions = self.get_adjacent_positions(position)
            for adj_position in adj_positions:
                if self.nodes[adj_position] == -1:
                    move = Move.Move(color, position, adj_position)
                    legal_moves.add(move)
        return legal_moves

    #soll bestimmen, ob ein spieler gewonnen hat
    def check_win(self):    
        # Spieler kann sich nicht mehr bewegen 
        if len(self.phase_two_get_legal_moves(0)) == 0 or len(self.phase_two_get_legal_moves(1)) == 0:
            return True
        # mindestens ein Spieler muss in der letzten Phase sein
        if not self.phases[0] == 2 or self.phases[1] == 2
            return False
        # Weniger als 3 Steine
        if self.get_num_pieces(0) < 3:
            return True
        if self.get_num_pieces(1) < 3:
            return True
            
        

    #Soll bestimmen, ob ein Remis vorliegt
    def check_remis(self):
        # 50 Züge ohne Mühle
        if self.last_muehle_counter == 50:
            return True
        # 3 mal die gleiche Stellung
        if node_states.count(self.nodes) == 3:
            return True

    #Soll die obrigen beiden Funktionen zusammenfassen und eine einheitliche schnittstelle bieten
    # return "w" falls weiß gewinnt, return "l" falls schwarz gewinnt, return "r" falls remis, return "" sonst
    def check_game_end(self):
        if self.check_remis == True:
            return "r"
        if self.check_win == True:
        # welcher Spieler hat gewonnen?
            if self.get_num_pieces(0) < 3:
                return "l"
            if self.get_num_pieces(1) < 3:
                return "w"
            if len(self.phase_two_get_legal_moves(0)) == 0:
                return "l"
            if len(self.phase_two_get_legal_moves(1)) == 0:
                return "w"
        else:
            return ""

    # Interface Methode zum Handling von Click Events aus dem Spielplan
    def receive_position(self, pos):
        None

    # Mache letzten Zug rückgängig
    def undo(self, steps=1):
        None

    # Mache Spiel rückgängig
    def reset(self):
        self.nodes = tuple([-1 for i in range(24)])
        self.phases = [0, 0]

        self.last_muehle_counter = 0
        self.node_states = []
