import sys
from tree_struct import Leaf, Node, Tree
from utils import occurences, build_initial_seq
from display_tree import plot_tree


def leafs_between(i, j, nodes):
    for node in nodes[i+1:j]:
        if isinstance(node, Leaf):
            return True
    return False


def select_args_nodes_to_merge(nodes):
    combined_min = (sys.maxsize, None, None)
    for i in range(len(nodes)):
        q_i : Node = nodes[i]
        for j in range(i+1, len(nodes)):
            q_j : Node = nodes[j]
            if leafs_between(i, j, nodes):
                break
            combined_weight = q_i.weight + q_j.weight
            if (combined_weight < combined_min[0]):
                combined_min = (combined_weight, i, j)
    return combined_min[1], combined_min[2]


# Phase One
def combination(initial_seq, debug=False):
    nodes = initial_seq.copy()
    k = 0
    while len(nodes) > 1:
        i, j = select_args_nodes_to_merge(nodes)
        q_i, q_j = nodes[i], nodes[j]
        new_node = Node(q_i.weight+q_j.weight, q_i, q_j)
        nodes[i] = new_node
        nodes.pop(j)
        if debug:
            plot_tree(Tree(nodes[i]), outputname=f"wip_phase_1_tree_{k}")
            k += 1
    return Tree(nodes[0])

def level_assignment_aux(node, index_map, leaf_levels, level=0):
    if isinstance(node, Leaf):
        i = index_map[node]
        leaf_levels[i] = (node, level)
    else:
        level_assignment_aux(node.child_left, index_map, leaf_levels, level=level+1)
        level_assignment_aux(node.child_right, index_map, leaf_levels, level=level+1)

# Phase Two
def level_assignment(tree, initial_seq):
    index_map = {node: i for i, node in enumerate(initial_seq)}
    leaf_levels = [(node, None) for node in initial_seq]
    level_assignment_aux(tree.root, index_map, leaf_levels)
    return leaf_levels

def select_args_nodes_to_merge_levels(levels):
    _, max_level = max(levels, key=lambda node_level: node_level[1])
    for i in range((len(levels)-1)):
        j = i+1
        _, l_i = levels[i]
        _, l_j = levels[j]
        if l_i == max_level and l_i == l_j:
            return i, j
    assert(False)

# Phase Three
def recombination(leaf_levels, debug=False):
    levels = leaf_levels.copy()
    k = 0
    while len(levels) > 1:
        i, j = select_args_nodes_to_merge_levels(levels)
        assert(i+1==j)
        q_i, l_i = levels[i]
        q_j, l_j = levels[j]
        assert(l_i==l_j)
        new_node = Node(q_i.weight+q_j.weight, q_i, q_j)
        levels[i] = (new_node, l_i - 1)
        levels.pop(j)
        if debug:
            plot_tree(Tree(new_node), outputname=f"wip_phase_3_tree_{k}")
            k += 1
    assert(levels[0][1]==0)
    return Tree(levels[0][0])

def main(debug):
    #phrase = "aaaaaaaaaazzeertyyyyuuuuuuuuuuuuuuuiiiiiiiiiiiiiiiiiooooooooooooooooooooooooo"
    phrase = "aaaaazzeeeeeeerrtyuiiooooppppp" # Même configuration que dans l'exemple de la thèse (5272111245)
    occs = occurences(phrase)
    initial_seq = build_initial_seq(occs)
    # Fin du Set-up

    # Phase 1
    comb_tree = combination(initial_seq, debug=debug)
    if debug:
        plot_tree(comb_tree, outputname="phase_1_tree")

    # Phase 2
    leaf_levels = level_assignment(comb_tree, initial_seq)
    if debug:
        for leaf, level in leaf_levels:
            print(leaf.__repr__(0), "niveau", level, "\n")

    # Phase 3
    hu_tucker_tree = recombination(leaf_levels, debug=debug)
    plot_tree(hu_tucker_tree, label_edges=True, outputname="hu_tucker_tree_naive")

if __name__== '__main__':
    main(debug=False)

