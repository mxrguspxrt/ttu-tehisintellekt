

table1 = """
1 1 0
? 1 ?
1 1 0
"""

table2 = """
0 0 0 .
1 2 1 1
. . ? .
"""

table3 = """
? . . . 0
. 4 2 1 .
. 2 0 0 .
"""

def main():
  print_info(table=table1)
  print_info(table=table2)
  print_info(table=table3)

def print_info(table=None):
  kb = KnowledgeBase(table=table)
  kb.print_resolution()


class KnowledgeBase:

  def __init__(self, table=None):
    stripped_table = table.strip()
    rows = stripped_table.split("\n")
    self.rows = map(lambda row: row.split(" "), rows)

  def print_resolution(self):
    print("lol")

main()