Optimizations:

1. Not rechecking sentances
2. Sorting DNF of CNF and using only unique (otherwise last map resolves forover) 

```
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
```


RESULT:

```
Inited table
table:  1 ? 1 .
table:  1 1 1 0
table:  0 0 0 0
Resolution for element 2 is that: has a mine

Inited table
table:  1 1 0
table:  ? 1 ?
table:  1 1 0
Resolution for element 4 is that: has a mine
Resolution for element 6 is that: does not have a mine

Inited table
table:  0 0 0 .
table:  1 2 1 1
table:  . ? . .
Resolution for element 10 is that: has a mine

Inited table
table:  ? . . . 0
table:  . 4 2 1 .
table:  . 2 0 0 .
Resolution for element 1 is that: has a mine
```
