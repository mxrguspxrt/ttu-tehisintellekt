

control_table = """
1 ? 1 .
1 1 1 0
0 0 0 0
"""

table1 = """
1 1 0
? 1 ?
1 1 0
"""

table2 = """
0 0 0 .
1 2 1 1
. ? . .
"""

table3 = """
? . . . 0
. 4 2 1 .
. 2 0 0 .
"""


def main():
    print_info(table=control_table)
    print_info(table=table1)
    print_info(table=table2)
    print_info(table=table3)


def print_info(table=None):
    kb = KnowledgeBase(table=table)
    kb.print_info()


class KnowledgeBase:

    def __init__(self, table=None):
        print("Inited table")
        print(table)
        stripped_table = table.strip()
        rows = stripped_table.split("\n")
        self.rows = list(map(lambda row: list(row.split(" ")), rows))
        self.rows_count = len(self.rows)
        self.columns_count = len(self.rows[0])
        self.elements_count = self.rows_count * self.columns_count

    def print_info(self):
        kb = self.get_kb()

        for columns in self.rows:
          print("table: ", " ".join(columns))


        print("KB: ", kb)

        for row_index in range(0, self.rows_count):
            for column_index in range(0, self.columns_count):
                if self.rows[row_index][column_index] == "?":
                    e_id = self.get_e_id(row_index, column_index)
                    print("\n\n CHECKING MINE FOR", e_id)
                    has_mine = self.get_has_mine(e_id=e_id, kb=kb)
                    print("Resolution for element", e_id, "is that:",
                          has_mine and "has a mine" or "does not have a mine")
                    print("\n\n")

        print("\n\n")

    def get_has_mine(self, e_id=None, kb=None):
        kb_without_duplicates = []
        for dnf in kb:
            sorted_dnf = list(dnf)
            sorted_dnf.sort()
            sorted_dnf = tuple(sorted_dnf)
            if sorted_dnf not in kb_without_duplicates:
                kb_without_duplicates.append(sorted_dnf)

        kb_without_duplicates.sort(key=lambda item: len(item))

        return self.pl_resolution(kb=kb_without_duplicates, alpha=e_id) 
    
    def pl_resolution(self, kb=None, alpha=None, previous_resolvents=None):
      candidates = []
      processed = []

      for cnf in kb: 
        for dnf in cnf:
          candidates.append(dnf+(-alpha,))

      print("Candidates", candidates)

      while True:
        if len(candidates) == 0:
          print("Ran out of candidates")
          return False 

        next = candidates.pop()
        if next in processed:
          print("Next already processed and skipping", next)
          continue 

        processed.append(next)

        for p in processed:
          resolvents = self.pl_resolve(next, p)
          for r in resolvents:
            print("Resolvent", r)
            if r == tuple():
              return True 
            candidates.append(r)





      # clauses = []

      # for cnf in kb:
      #   print("Conjucted:", cnf)
      #   cnf_copy = cnf.copy()
      #   cnf_copy.append(tuple((-alpha,)))
      #   clauses.append(cnf_copy)
      #   for disjuncted in cnf:
      #     print("Disjuncted: ", disjuncted)
      #   print("")
        
      # print("Clauses", clauses)

      # resolvents = []
      # for clause in clauses:
      #   pairs = self.get_pairs(clauses=clause)
      #   print("Pairs", pairs)
        
      #   for (c1, c2) in pairs:
      #     resolvent = self.pl_resolve(c1=c1, c2=c2)
      #     resolvents.append(resolvent)
        
      # print("Resolvents: ", resolvents)
      # print("")

      # if [tuple()] == resolvents:
      #   return True

      # if resolvents == previous_resolvents:
      #   return False

      # return self.pl_resolution(kb=[resolvents], alpha=alpha, previous_resolvents=resolvents)


    def get_pairs(self, clauses=None):
      clauses_count = len(clauses)
      pairs = []
      for i in range(0, clauses_count):
        for j in range(i+1, clauses_count):
          pairs.append((clauses[i], clauses[j]))
      return pairs

    def pl_resolve(self, c1=None, c2=None):
      print("pl_resolve")
      print("c1", c1)
      print("c2", c2)
      
      dnew = ()

      for d1 in c1:
        if d1 not in dnew and -d1 not in c2:
          dnew = dnew + (d1,)
      
      for d2 in c2:
        if d2 not in dnew and -d2 not in c1:
          dnew = dnew + (d2,)
      
      print("dnew", dnew)
      print("")
      return [dnew]
      




    def get_kb(self):
        kb = []
        for row_index in range(0, self.rows_count):
            for column_index in range(0, self.columns_count):
                cnf = self.get_cnf(row_index=row_index,
                                   column_index=column_index)
                if cnf:
                    kb.append(cnf)
        return kb

    def get_cnf(self, row_index=None, column_index=None):

        val = self.rows[row_index][column_index]
        if val == "?" or val == ".":
            return

        mines_around_count = int(val)

        elements = {}

        has_left = column_index > 0
        has_right = column_index + 1 < self.columns_count
        has_top = row_index > 0
        has_bottom = row_index + 1 < self.rows_count

        e_id = self.get_e_id

        if has_left:
            elements[e_id(row_index, column_index-1)
                     ] = self.rows[row_index][column_index-1]

        if has_right:
            elements[e_id(row_index, column_index+1)
                     ] = self.rows[row_index][column_index+1]

        if has_top:
            elements[e_id(row_index-1, column_index)
                     ] = self.rows[row_index-1][column_index]

        if has_bottom:
            elements[e_id(row_index+1, column_index)
                     ] = self.rows[row_index+1][column_index]

        if has_left and has_top:
            elements[e_id(row_index-1, column_index-1)
                     ] = self.rows[row_index-1][column_index-1]

        if has_left and has_bottom:
            elements[e_id(row_index+1, column_index-1)
                     ] = self.rows[row_index+1][column_index-1]

        if has_right and has_top:
            elements[e_id(row_index-1, column_index+1)
                     ] = self.rows[row_index-1][column_index+1]

        if has_right and has_bottom:
            elements[e_id(row_index+1, column_index+1)
                     ] = self.rows[row_index+1][column_index+1]

        selected_elements = []

        for e_id in elements:
            val = elements[e_id]

            if val == "?" or val == ".":
                selected_elements.append(e_id)

        return self.cnf_sweeper(mines_around_count=mines_around_count, neighbors=selected_elements)

    def cnf_sweeper(self, mines_around_count=None, neighbors=None):
        n = len(neighbors)
        cnf = []
        for i in range(2**n):
            binform = "{:0{n}b}".format(i, n=n)
            ones = 0
            clause = []
            for j in range(n):
                if binform[j] == "1":
                    ones += 1
                    clause.append(-neighbors[j])
                else:
                    clause.append(neighbors[j])
            if ones != mines_around_count:
                cnf.append(tuple(clause))
        return cnf

    def get_e_id(self, row_index, column_index):
        return (row_index * self.columns_count + column_index) + 1


def is_subset(a, b):
  print("a", a)
  print("b", b)
  includes_all = True 

  for e in tuple(a):
    if e not in tuple(b):
      includes_all = False 
  
  return includes_all

main()
