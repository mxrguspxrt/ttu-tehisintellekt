import random


def main():
    game = Game()
    game.play()


class Game:

    X = "X"
    Y = "Y"

    Win = "Win"
    Loss = "Loss"
    Tie = "Tie"

    def __init__(self, next_move=None, rows=None):
        self.next_move = next_move or Game.X

        if rows:
            self.rows = rows
        else:
            # columns 7, rows 6
            self.rows = [None]*6
            for row_index in range(0, 6):
                self.rows[row_index] = [None]*7
            print("Started game")

    def get_map_string(self):
        map_string = ""
        for row_index in range(0, 6):
            map_string += "|"
            for column_index in range(0, 7):
                val = self.rows[row_index][column_index]
                map_string += val or " "
            map_string += "|\n"
        map_string += "|1234567|"
        return map_string

    def play(self):
        while True:
            print(self.get_map_string())
            print("To move: " + self.next_move)
            player_moves = self.next_move == Game.X
            move_to_column_index = None

            if player_moves:
                move_to_column_index = int(input("Your move? ")) - 1
            else:
                move_to_column_index = self.get_best_move(allowed_simulations_count=200)

            self.make_move(move=move_to_column_index)

            winner = self.get_winner()
            is_over = self.get_is_over()

            if winner:
                print("Winner is: ", winner)
                print(self.get_map_string())
                return

            if is_over:
                print("Game is over with a Tie")
                print(self.get_map_string())
                return

    def get_free_line_index(self, column_index=None):
        rows_len = 6
        for row_index in range(0, rows_len):
            if self.rows[rows_len - row_index - 1][column_index] == None:
                return rows_len - row_index - 1
        raise Exception("No free lines for column")

    def get_best_move(self, allowed_simulations_count=None):
        initial_moves = self.get_available_moves()
        win_counts = dict((move, 0) for move in initial_moves)

        for move in initial_moves:
            for _ in range(0, allowed_simulations_count):
                winner = self.get_simulation_winner(move=move)
                if winner == self.next_move:
                    win_counts[move] += 1
                if winner == None:
                    win_counts[move] += 0.5

        best_move = initial_moves[0]

        for initial_move in initial_moves:
            if win_counts[initial_move] > win_counts[best_move]:
                best_move = initial_move

        return best_move

    def get_simulation_winner(self, move=None):
        simulation = Game(next_move=self.next_move, rows=list(
            map(lambda row: row.copy(), self.rows)))
        simulation.make_move(move)

        winner = simulation.get_winner()
        is_over = simulation.get_is_over()

        running = not (winner or is_over)

        while running:
            simulation.make_random_move()
            winner = simulation.get_winner()
            is_over = simulation.get_is_over()
            running = not (winner or is_over)

        return winner

    def make_move(self, move=None):
        try:
            next_free_line_index = self.get_free_line_index(
                column_index=move)
            self.rows[next_free_line_index][move] = self.next_move
            self.next_move = (self.next_move ==
                              Game.X and Game.Y) or Game.X

        except Exception as error:
            print("Had error: ", str(error))

    def make_random_move(self):
        available_moves = self.get_available_moves()
        random_move = random.choice(available_moves)

        return self.make_move(move=random_move)

    def get_winner(self):
        for row_start_index in range(0, 6):
            for column_start_index in range(0, 7):
                if self.has_4_in_row(row_start_index=row_start_index, column_start_index=column_start_index):
                    return self.rows[row_start_index][column_start_index]

    def has_4_in_row(self, row_start_index=None, column_start_index=None):
        a = row_start_index
        b = column_start_index
        r = self.rows

        if r[a][b] == None:
            return False

        left_to_right = b + \
            3 < 7 and r[a][b] == r[a][b+1] == r[a][b+2] == r[a][b+3]
        top_to_down = a + \
            3 < 6 and r[a][b] == r[a+1][b] == r[a+2][b] == r[a+3][b]
        diagonal_left_down = a - 3 > -1 and b + \
            3 < 7 and r[a][b] == r[a-1][b+1] == r[a-1][b+2] == r[a-3][b+3]
        diagonal_right_down = a + 3 < 6 and b + \
            3 < 7 and r[a][b] == r[a+1][b+1] == r[a+1][b+2] == r[a+3][b+3]

        return left_to_right or top_to_down or diagonal_left_down or diagonal_right_down

    def get_is_over(self):
        return not any(map(lambda x: x == None, self.rows[0]))

    def get_available_moves(self):
        available_moves = []
        for i in range(0, 7):
            if self.rows[0][i] == None:
                available_moves.append(i)
        return available_moves


main()
