from tree_struct import Node, Leaf, Tree
from display_tree import plot_tree
from utils import occurences, build_initial_seq

def build_huffman_tree(leafs):
    nodes = leafs.copy()
    while len(nodes) > 1:
        min_1 = min(nodes, key=lambda n: n.weight)
        nodes.remove(min_1)
        min_2 = min(nodes, key=lambda n: n.weight)
        nodes.remove(min_2)
        
        new_node = Node(min_1.weight+min_2.weight, min_1, min_2)
        nodes.append(new_node)

    return Tree(nodes[0])

def huffman_code_rec(node, codes, code):
    if isinstance(node, Leaf):
        codes[node.character] = code
    else:
        if node.child_left:
            huffman_code_rec(node.child_left, codes, code+"0")
        if node.child_right:
            huffman_code_rec(node.child_right, codes, code+"1")

def huffman_code(tree):
    codes = {}
    code = ""
    huffman_code_rec(tree.root, codes, code)
    return codes
