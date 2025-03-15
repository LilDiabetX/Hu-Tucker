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

def build_tree(leafs):
    nodes = leafs.copy()
    k = 0
    while len(nodes) > 1:
        i, j = select_args_nodes_to_merge(nodes)
        q_i, q_j = nodes[i], nodes[j]
        new_node = Node(q_i.weight+q_j.weight, q_i, q_j)
        nodes[i] = new_node
        nodes.pop(j)
        plot_tree(Tree(nodes[i]), outputname="wip_tree_"+str(k))
        k += 1
    return Tree(nodes[0])

# Phase One
def combination(phrase):
    occs = occurences(phrase)
    initial_seq = build_initial_seq(occs)
    return build_tree(initial_seq)

def level_assignment_aux(node, leaf_levels, level=0):
    if isinstance(node, Leaf):
        leaf_levels.append((node, level))
    else:
        level_assignment_aux(node.child_left, leaf_levels, level=level+1)
        level_assignment_aux(node.child_right, leaf_levels, level=level+1)

# Phase Two
def level_assignment(tree):
    leaf_levels = []
    level_assignment_aux(tree.root, leaf_levels)
    return leaf_levels

# Phase Three
def recombination():
    pass


#phrase = "je mange des saucisses seches venant d'estonie"
phrase = "aaaaazzeeeeeeerrtyuiiooooppppp" # Même configuration que dans l'exemple de la thèse (5272111245)
comb_tree = combination(phrase)
plot_tree(comb_tree)
leaf_levels = level_assignment(comb_tree)
for leaf, level in leaf_levels:
    print(leaf.__repr__(0), "niveau", level, "\n")

