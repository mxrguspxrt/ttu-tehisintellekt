import random
import time


def main():
    queens4 = Queens(queens_count=4)
    queens4.print_best_local_optimum()

    queens20 = Queens(queens_count=20)
    queens20.print_best_local_optimum()

    queens30 = Queens(queens_count=30)
    queens30.print_best_local_optimum()

    queens50 = Queens(queens_count=50)
    queens50.print_best_local_optimum()



class Queens:

    def __init__(self, queens_count=None, queens_map=None):
        # queens map has columns = [row_index, row_index, row_index, row_index] structure

        self.queens_count = queens_count

        if queens_map == None:
            self.queens_map = [None]*queens_count
            self.assign_random_queens()
            print("Initialized a map:", self.get_queens_map_as_string(), self.get_conflicts_count())

        if queens_map != None:
            self.queens_map = queens_map


    def assign_random_queens(self):
        queens_count = self.queens_count

        for new_queen_column in range(0, queens_count):
            self.queens_map[new_queen_column] = random.choice(
                list(range(0, queens_count)))

    def get_queens_map_as_string(self):
        string_map = ""
        for row_index in range(0, self.queens_count):
            string_map += "\n"
            string_map += self.get_row_as_string(row_index)
        return string_map

    def get_row_as_string(self, row_index):
        parts = ["▢"]*self.queens_count

        for column_index in range(0, self.queens_count):
            if self.queens_map[column_index] == row_index:
                parts[column_index] = "▇"

        return " ".join(parts)

    def print_best_local_optimum(self):
        print("Original map:", self.get_queens_map_as_string(),
              " has conflicts ", self.get_conflicts_count())
        start = time.time()
        fixed_map = self.get_fixed_map()
        print("Fixed map:", fixed_map.get_queens_map_as_string(),
              " has conflicts ", fixed_map.get_conflicts_count())
        end = time.time()
        print("Took time", end - start)

    def get_fixed_map(self):
        previous_best_move = self.get_best_move() 

        no_improvement_for_iterations_count = 0

        while True:
            if previous_best_move.conflicts_count == 0:
                return previous_best_move.queens

            next_best_move = previous_best_move.queens.get_best_move()

            if next_best_move.conflicts_count >= previous_best_move.conflicts_count:
               no_improvement_for_iterations_count = no_improvement_for_iterations_count + 1 
               print("No improvement for iteration: ", no_improvement_for_iterations_count) 
            if no_improvement_for_iterations_count > self.queens_count:
                next_best_move = previous_best_move.queens.get_random_suffle_to_break_out_of_local_optimum()
                previous_best_move = next_best_move
                no_improvement_for_iterations_count = 0

            if next_best_move.conflicts_count <= previous_best_move.conflicts_count:
                print("\n", next_best_move.queens.get_queens_map_as_string(), "\nConflicts: ", next_best_move.queens.get_conflicts_count())
                previous_best_move = next_best_move

    def get_random_suffle_to_break_out_of_local_optimum(self):
        new_map = self.queens_map.copy()
        for column_index in range(0, self.queens_count):
            new_map[column_index] = random.choice(list(range(0, self.queens_count)))

        queens = Queens(queens_count=self.queens_count, queens_map=new_map)
        return AfterMove(queens=queens, conflicts_count=queens.get_conflicts_count())                

    def get_best_move(self):
        after_best_move = AfterMove(queens=self, conflicts_count=self.get_conflicts_count())

        column_indexes = list(range(0, self.queens_count))
        random.shuffle(column_indexes)

        for column_index in column_indexes:
            current_value = self.queens_map[column_index]
            
            row_indexes = list(set(range(0, self.queens_count)) - set([current_value]))
            random.shuffle(row_indexes)

            for new_row_index in row_indexes:
                after_next_move = self.get_after_move(Move(column_index=column_index, new_row_index=new_row_index))
                if after_next_move.conflicts_count <= after_best_move.conflicts_count:
                    after_best_move = after_next_move

        return after_best_move

    def get_after_move(self, move = None):
        new_map = self.queens_map.copy()
        new_map[move.column_index] = move.new_row_index
        
        queens = Queens(queens_count=self.queens_count, queens_map=new_map)

        return AfterMove(move=move, queens=queens, conflicts_count=queens.get_conflicts_count())

    def get_conflicts_count(self):
        queens_count = self.queens_count
        queens_map = self.queens_map
        conflict_count = 0
        # iterate over map
        a_column_indexes = list(range(0, queens_count))
        random.shuffle(a_column_indexes)
        for a_column_index in a_column_indexes:
            # iterate over map that is only below the current row (no double counting)
            b_column_indexes = list(range(0, queens_count))
            random.shuffle(b_column_indexes)
            for b_column_index in b_column_indexes:
                # check if they conflict
                if a_column_index != b_column_index:
                    has_conflict = get_has_conflict(
                        [a_column_index, queens_map[a_column_index]], [b_column_index, queens_map[b_column_index]])
                    if has_conflict:
                        conflict_count += 1
        return conflict_count


class AfterMove: 

    def __init__(self, move=None, conflicts_count=None, queens=None):
        self.move = move
        self.conflicts_count = conflicts_count
        self.queens = queens

class Move:

    def __init__(self, column_index = None, new_row_index = None):
        self.column_index = column_index
        self.new_row_index = new_row_index

def get_has_conflict(a, b):
    diagonal_conflict = abs(b[0]-a[0]) == abs(b[1]-a[1])
    x_or_y_conflict = a[0] == b[0] or a[1] == b[1]
    has_conflict = diagonal_conflict or x_or_y_conflict
    # if has_conflict:
    #     print("Has conflict", a, b)
    return has_conflict


main()
