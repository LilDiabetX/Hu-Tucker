from tree_struct import Leaf

def occurences(phrase):
    occs = {}
    for c in phrase:
        if c not in occs.keys():
            occs[c] = 1
        else:
            occs[c] += 1
    return occs

def build_initial_seq(occs):
    leafs = []
    for c in occs.keys():
        leafs.append(Leaf(c, occs[c]))
    return leafs