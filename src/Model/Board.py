from Model import Move


class Board:
    def __init__(self):
        # Spielbrett mit 24 Positionen, -1 heißt Position leer,
        self.nodes = tuple([-1 for i in range(24)])
        # Wie ist weiß codiert
        self.white = 0

        self.game_ended = False

        # Phases setzen 0, ziehen 1 und springen 2, self.phases[self.white] = white_phase!!!!
        self.phases = [0, 0]

        # Relevant für die Remis
        self.last_muehle_counter = 0
        # In node_states sollen alle erreichten Brettstellungen gespeichert werden.
        # Nach einer Mühle können alle vorherigen Stellungen nicht mehr erreicht werden.
        self.node_states = [self.nodes]
        self.game_end_info = ""
        self.next_move = Move.Move(0)

    # Wieviele Steine einer Farbe gibt es?
    def get_num_of_pieces_on_board(self, color):
        return self.nodes.count(color)

    def update_phases(self):
        white_phase = 0
        black_phase = 0
        if len(self.node_states) >= 18:
            white_phase += 1
            if self.get_num_of_pieces_on_board(self.white) == 3:
                white_phase += 1
        if len((self.node_states)) >= 19:
            black_phase += 1
            if self.get_num_of_pieces_on_board((self.white + 1) % 2) == 3:
                black_phase += 1
        self.phases[self.white] = white_phase
        self.phases[(self.white + 1) % 2] = black_phase

    def get_num_of_pieces_left_to_place(self, color):
        a, b = divmod(len(self.node_states), 2)
        num_white, num_black = 9 - a, 9 - a
        if b == 0: num_black += 1
        if num_white < 0: num_white = 0
        if num_black < 0: num_black = 0
        if color == 0:
            return num_white
        if color == 1:
            return num_black

    def is_move_legal(self, move):
        if move.to_pos != -1 and self.nodes[move.to_pos] != -1:
            # Nicht auf besetzes Feld setzen
            return False
        if self.phases[move.color] == 0 and move.from_pos != -1:
            # Man darf gesetzte Steine nicht in der Setzen Phase bewegen
            return False
        if self.phases[move.color] != 0 and self.nodes[move.from_pos] != move.color:
            #Man muss eigenen Steine ziehen oder springen lassen
            return False
        if self.phases[move.color] == 1 and not self.are_positions_adjacent(move.from_pos, move.to_pos) and move.to_pos != -1:
            # In der Ziehen Phase darf man nicht springen
            return False
        if self.phases[move.color] == 1 and not self.is_piece_free_to_move(self.next_move.from_pos):
            # In Ziehen Phase darf kein Stein ausgewählt werden, der nicht ziehen kann
            return False
        if move.remove_pos != -1:
            if not self.is_position_in_muehle_of_color(move.to_pos, move.color):
                # Man darf nur Steine entfernen, wenn man eine Muehle gemacht hat
                return False
            if (move.color+1)%2 != self.nodes[move.remove_pos] or move.to_pos == move.remove_pos:
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
            if self.nodes[i] != color:
                is_muehle_hor = False
        for i in muehle_ver:
            if self.nodes[i] != color:
                is_muehle_ver = False
        return is_muehle_hor or is_muehle_ver

    def is_move_outside_of_muehle(self, move):
        MUEHLEN_hor = [{i, i + 1, i + 2} for i in range(0, 22, 3)]
        MUEHLEN_ver = [{0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17}, {5, 13, 20},
                       {2, 14, 23}]
        muehle_hor, muehle_ver = set([]), set([])
        for muehle in MUEHLEN_hor:
            if move.to_pos in muehle:
                muehle_hor = muehle
        for muehle in MUEHLEN_ver:
            if move.to_pos in muehle:
                muehle_ver = muehle
        muehle_ver.discard(move.to_pos)
        muehle_hor.discard(move.to_pos)
        is_muehle_hor, is_muehle_ver = True, True
        for i in muehle_hor:
            if self.nodes[i] != move.color or i == move.from_pos:
                is_muehle_hor = False
        for i in muehle_ver:
            if self.nodes[i] != move.color or i == move.from_pos:
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
        if pos1 == pos2:
            return False
        ADJ_hor = [{i, i + 1} for i in range(0, 22, 3)] + [{i + 1, i + 2} for i in range(0, 22, 3)]
        ADJ_ver = [{0, 9}, {9, 21}, {3, 10}, {10, 18}, {6, 11}, {11, 15}, {1, 4}, {4, 7}] + \
                  [{16, 19}, {19, 22}, {8, 12}, {12, 17}, {5, 13}, {13, 20}, {2, 14}, {14, 23}]
        return {pos1, pos2} in ADJ_hor + ADJ_ver

    def yield_move_to_muehle(self, move):
        MUEHLEN_hor = [{i, i + 1, i + 2} for i in range(0, 22, 3)]
        MUEHLEN_ver = [{0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17}, {5, 13, 20},
                       {2, 14, 23}]
        for muehle in MUEHLEN_ver:
            if move.from_pos in muehle:
                MUEHLEN_ver.remove(muehle)
        for muehle in MUEHLEN_hor:
            if move.from_pos in muehle:
                MUEHLEN_hor.remove(muehle)
        muehle_hor, muehle_ver = set([]), set([])
        for muehle in MUEHLEN_hor:
            if move.to_pos in muehle:
                muehle_hor = muehle
        for muehle in MUEHLEN_ver:
            if move.to_pos in muehle:
                muehle_ver = muehle
        muehle_ver.discard(move.to_pos)
        muehle_hor.discard(move.to_pos)
        is_muehle_hor, is_muehle_ver = True, True
        for i in muehle_hor:
            if self.nodes[i] != move.color:
                is_muehle_hor = False
        for i in muehle_ver:
            if self.nodes[i] != move.color:
                is_muehle_ver = False
        return (is_muehle_hor and len(muehle_hor) > 0) or (is_muehle_ver and len(muehle_ver)>0)


    # Gibt Menge der zu pos benachbarten Knoten aus
    def get_adjacent_positions(self, pos):
        adj_positions = set([])
        for i in range(24):
            if self.are_positions_adjacent(pos, i):
                adj_positions.add(i)
        return adj_positions

    def is_piece_free_to_move(self, pos):
        adj_positions = self.get_adjacent_positions(pos)
        for adj_position in adj_positions:
            if self.nodes[adj_position] == -1:
                return True
        return False

    def receive_pos(self, pos):
        if self.game_ended:
            return
        changed = -1  # this variable shows which attribute of self.next_move is changed,
        # -1 means nothing, 0 means from_pos, 1 means to_pos, 2 means remove_pos
        if self.phases[self.next_move.color] == 0:
            if self.next_move.to_pos == -1:
                self.next_move.to_pos = pos
                changed = 1
            elif self.next_move.remove_pos == -1:
                self.next_move.remove_pos = pos
                changed = 2
        else:
            if self.next_move.from_pos == -1 :
                self.next_move.from_pos = pos
                changed = 0
            elif self.next_move.to_pos == -1:
                self.next_move.to_pos = pos
                changed = 1
            elif self.next_move.remove_pos == -1:
                self.next_move.remove_pos = pos
                changed = 2
        print(str(self.next_move))
        if self.is_move_legal(self.next_move):
            if self.next_move.to_pos != -1 and \
                    (not self.yield_move_to_muehle(self.next_move) or
                     self.next_move.remove_pos != -1):
                self.make_move(self.next_move)
                self.next_move = Move.Move(self.next_move.color + 1)
        else:
            if changed == 0:
                self.next_move.from_pos = -1
            if changed == 1:
                self.next_move.to_pos = -1
            if changed == 2:
                self.next_move.remove_pos = -1
            if changed == -1:
                raise RuntimeError("Der Move war schon fertig gebaut: " + str(self.next_move))

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
        self.update_game_end()

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


    # soll bestimmen, ob ein spieler gewonnen hat
    def check_win(self):
        # Spieler kann sich nicht mehr bewegen 
        if len(self.phase_one_get_legal_moves(0)) == 0 or len(self.phase_one_get_legal_moves(1)) == 0:
            return True
        # mindestens ein Spieler muss in der letzten Phase sein
        if not self.phases[0] == 2 or self.phases[1] == 2:
            return False
        # Weniger als 3 Steine
        if self.get_num_of_pieces_on_board(0) < 3:
            return True
        if self.get_num_of_pieces_on_board(1) < 3:
            return True

    # Soll bestimmen, ob ein Remis vorliegt
    def check_remis(self):
        # 50 Züge ohne Mühle
        if self.last_muehle_counter == 50:
            return True
        # 3 mal die gleiche Stellung
        if self.node_states.count(self.nodes) == 3:
            return True
        return False

    # Soll die obrigen beiden Funktionen zusammenfassen und eine einheitliche schnittstelle bieten
    # return "w" falls weiß gewinnt, return "l" falls schwarz gewinnt, return "r" falls remis, return "" sonst
    def update_game_end(self):
        if self.check_remis == True:
            self.game_ended = True
            self.game_end_info = "Remi" # TODO expliziter angeben, wieso Remi besteht
        if self.check_win == True:
            self.game_ended = True
            # welcher Spieler hat gewonnen?
            if self.get_num_of_pieces_on_board(0) < 3:
                self.game_end_info = "Schwarz gewinnt - Weiß hat nur noch zwei Steine übrig"
            if self.get_num_of_pieces_on_board(1) < 3:
                self.game_end_info = "Weis gewinnt - Schwarz hat nur noch zwei Steine übrig"
            if len(self.phase_one_get_legal_moves(0)) == 0:
                self.game_end_info = "Schwarz gewinnt - Weiß kann nicht mehr ziehen"
            if len(self.phase_one_get_legal_moves(1)) == 0:
                self.game_end_info = "Weiß gewinnt - Schwarz kann nicht mehr ziehen"
        else:
            return ""

    # Mache letzten Zug rückgängig
    def undo(self, steps=1):
        pass

    # Mache Spiel rückgängig
    def reset(self):
        self.nodes = tuple([-1 for i in range(24)])
        self.phases = [0, 0]
        self.next_move = Move.Move(0)
        self.game_ended = False
        self.last_muehle_counter = 0
        self.node_states = [self.nodes]
