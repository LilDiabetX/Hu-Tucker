from tree_struct import Node, Leaf, Tree
from display_tree import plot_tree

def occurences(seq):
    occs = {}
    for c in seq:
        if c not in occs.keys():
            occs[c] = 1
        else:
            occs[c] += 1
    return occs

def build_leafs(occs):
    leafs = []
    for c in occs.keys():
        leafs.append(Leaf(c, occs[c]))
    return leafs

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


phrase = "je mange des saucisses seches venant d'estonie"
occs_phrase = occurences(phrase)
leafs = build_leafs(occs_phrase)
tree = build_huffman_tree(leafs)
print(tree)
plot_tree(tree)
huff_code = huffman_code(tree)
print(huff_code)
