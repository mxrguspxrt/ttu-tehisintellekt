# k6ikide numbriga ruutude peal kutsun välja cnf_sweeper()
# enne peab olema teada kinniste naabrite list

def cnf_sweeper(m, neighbors):
    """CNF komponent ühe ruudu kohta
    parameetrid: m - miinide arv
                neighbors - naabrite list"""
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
        if ones != m:
            cnf.append(tuple(clause))
            #print(binform, ones, clause)
    return cnf

test = cnf_sweeper(1, [4, 5, 6, 7])
print(test)
