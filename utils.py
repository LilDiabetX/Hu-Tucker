from tree_struct import Leaf, Leaf_opt

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
        leafs.append(Leaf(occs[c], c))
    return leafs

def build_initial_seq_inter(occs):
    leafs = []
    for c in occs.keys():
        leafs.append(Leaf_opt(occs[c], c))
    return leafs