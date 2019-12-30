import random


def main():
    queens4 = Queens(queens_count=4)
    # queens4 = Queens(queens_count=10)
    # queens100 = Queens(queens_count=100)

    queens4.print_best_local_optimum()
    print(queens4.queens_map)
    # queens4.print_best_local_optimum()
    # queens100.print_best_local_optimum()


class Queens:

    def __init__(self, queens_count=None):
        self.queens_map = [None]*queens_count
        for i in range(0, queens_count):
          self.queens_map[i] = [None]*queens_count
        self.queens_count = queens_count
        self.assign_random_queens(queens_count=queens_count)

        #self.queens_map = [[None, '♕', None, None], [None, None, '♕', None], [None, None, None, '♕'], [None, None, '♕', None]]
        print("Initialized a map:", self.get_queens_map_as_string())

    def assign_random_queens(self, queens_count=None):
        for new_queen_row in range(0, queens_count):
            used_columns = self.get_used_columns()
            available_positions = list(set(range(0, queens_count)) - set(used_columns))
            new_queen_column = random.choice(available_positions)
            print("New queen pos: ", [new_queen_row, new_queen_column])
            self.queens_map[new_queen_row][new_queen_column] = "♕"

    def get_used_columns(self):
      used_columns = []
      for row in range(0, self.queens_count):
        for column in range(0, self.queens_count):
          if self.queens_map[row][column] == "♕":
            used_columns.append(column)
      return used_columns

    def get_queens_map_as_string(self):
        string_map = ""
        for i in range(0, len(self.queens_map)):
            string_map += "\n"
            for j in range(0, len(self.queens_map)):
                string_map += self.queens_map[i][j] or "□"
        return string_map

    def print_best_local_optimum(self):
        print(self.get_queens_map_as_string(), self.get_conflicts_count())

    def get_conflicts_count(self):
        queens_count = self.queens_count
        queens_map = self.queens_map
        conflict_count = 0
        # iterate over map
        for a_row in range(0, queens_count):
            for a_column in range(0, queens_count):
                if queens_map[a_row][a_column] == "♕":
                    # iterate over map that is only below the current row (no double counting)
                    for b_row in range(a_row+1, queens_count):
                        for b_column in range(0, queens_count):
                            if queens_map[b_row][b_column] == "♕":
                                # check if they conflict
                                has_conflict = get_has_conflict(
                                    [a_row, a_column], [b_row, b_column])
                                if has_conflict:
                                    conflict_count += 1
        return conflict_count


def get_has_conflict(a, b):
    has_conflict = abs(b[0]-a[0]) == abs(b[1]-a[1])
    if has_conflict:
        print("Has conflict", a, b)
    return has_conflict


main()
