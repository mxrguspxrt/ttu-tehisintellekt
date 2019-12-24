A* takes more time to process (2-3 times more), but the found path is 2-3 is better. I have +1 nodes in path, because I count the final node as part of the path.

```
$ python3 lab3_heuristic.py 
Took iterations to process: 3364
Path has steps: 987
Wrote result to file:  cave300x300-result-heuristic
Took iterations to process: 6389
Path has steps: 1936
Wrote result to file:  cave600x600-result-heuristic
Took iterations to process: 29454
Path has steps: 4348
Wrote result to file:  cave900x900-result-heuristic


$ python3 lab3_astar.py 
Took iterations to process: 7407
Path has steps: 555
Wrote result to file:  cave300x300-result-astar
Took iterations to process: 65492
Path has steps: 1262
Wrote result to file:  cave600x600-result-astar
Took iterations to process: 108869
Path has steps: 1864
Wrote result to file:  cave900x900-result-astar
```


Changing `abs(neighbor_node["column_index"]-goal["column_index"]) + abs(neighbor_node["row_index"]-goal["row_index"])` to `max(abs(neighbor_node["column_index"]-goal["column_index"]), abs(neighbor_node["row_index"]-goal["row_index"]))`

* did make heuristic search faster and with better quality (shorter path)
* did make astar search 3x slower and did not improve quality 

```
$ python3 lab3_heuristic_lisa1.py
Took iterations to process: 2505
Path has steps: 741
Wrote result to file:  cave300x300-result-heuristic-lisa1
Took iterations to process: 9576
Path has steps: 1758
Wrote result to file:  cave600x600-result-heuristic-lisa1
Took iterations to process: 11213
Path has steps: 2522
Wrote result to file:  cave900x900-result-heuristic-lisa1

$ python3 lab3_astar_lisa1.py 
Took iterations to process: 29957
Path has steps: 555
Wrote result to file:  cave300x300-result-astar-lisa1
Took iterations to process: 157588
Path has steps: 1248
Wrote result to file:  cave600x600-result-astar-lisa1
Took iterations to process: 361550
Path has steps: 1844
Wrote result to file:  cave900x900-result-astar-lisa1
```

Allowing movements in diagonals caused less iterations to process and shorter paths.

```
 python3 lab3_heuristic_lisa2.py 
Took iterations to process: 2064
Path has steps: 538
Wrote result to file:  cave300x300-result-heuristic-lisa2
Took iterations to process: 9211
Path has steps: 1249
Wrote result to file:  cave600x600-result-heuristic-lisa2
Took iterations to process: 10474
Path has steps: 1722
Wrote result to file:  cave900x900-result-heuristic-lisa2

$ python3 lab3_astar_lisa2.py 
Took iterations to process: 13680
Path has steps: 379
Wrote result to file:  cave300x300-result-astar-lisa2
Took iterations to process: 99639
Path has steps: 872
Wrote result to file:  cave600x600-result-astar-lisa2
Took iterations to process: 162543
Path has steps: 1234
Wrote result to file:  cave900x900-result-astar-lisa2
```