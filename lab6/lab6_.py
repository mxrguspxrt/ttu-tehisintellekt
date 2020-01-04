# def pure_mc(pos, N=200):
#     # kõik käigud algseisus
#     my_side = pos["to_move"]
#     initial_moves = moves(pos)
#     # loendurid iga käigu jaoks
#     win_counts = dict((move, 0) for move in initial_moves)

#     for move in initial_moves:
#         for i in range(N):
#             # mängi juhuslikult seis kuni lõpuni
#             res = simulate(pos, move, my_side)
#             if res == WIN:
#                 win_counts[move] += 1
#             elif res == DRAW:
#                 win_counts[move] += 0.5

#     # leia suurima võitude arvuga käik, tagasta

#     # ...


# def play_game(pos, player_side = "X"):
#     playing = True
#     while playing:
#         if pos["to_move"] == player_side:
#             # prindi info seisu kohta
#             dump_pos(pos)
#             movestr = input("Your move? ")
#             # tõlgi kasutaja tekst oma sisemisse käiguformaati (kui vaja)
#             move = parse_move(movestr)
#         else:
#             move = pure_mc(pos)

#         pos = make_move(pos, move)
#         # kontrolli kas mäng sai läbi
#         if is_over(pos):
#             playing = False

# play_game(starting_pos)


def main():
  game = Game()
  game.play()


class Game:

  X = "X"
  Y = "Y"

  def __init__(self):
    self.next_move = Game.X
    # columns 6, rows 7
    self.map = [None]*6
    for i in range(0, 6):
      self.map[i] = [None]*7
    print("Started game")

  def get_map_string(self):
    map_string = ""
    for i in range(0, 6):
      map_string += "|"
      for j in range(0, 7):
        val = self.map[i][j]
        map_string += val or " "
      map_string += "|\n"
    map_string += "|1234567|"
    return map_string
  
  def play(self):
    print(self.get_map_string())
    print("To move: " + self.next_move)
    move_to_column = int(input("Your move? "))
    self.map[5][move_to_column-1] = self.next_move 
    self.next_move = (self.next_move == Game.X and Game.Y) or Game.X
    print(self.get_map_string())




main()