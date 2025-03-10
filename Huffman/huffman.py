class Node:

    def __init__(self, w, left, right):
        self.weight = w
        self.child_left = left
        self.child_right = right

    def __repr__(self, depth):
        ret = "\t"*depth+repr(self.weight)+"\n"
        if self.child_left:
            ret += self.child_left.__repr__(depth+1)
        if self.child_right:
            ret += self.child_right.__repr__(depth+1)
        return ret
    
    def huffman_code(self, codes, code):
        if isinstance(self, Leaf):
            codes[self.character] = code
        else:
            if self.child_left:
                self.child_left.huffman_code(codes, code+"0")
            if self.child_right:
                self.child_right.huffman_code(codes, code+"1")

class Leaf(Node):

    def __init__(self, c, w):
        Node.__init__(self, w, None, None)
        self.character = c

    def __repr__(self, depth):
        return "\t"*depth+repr(self.weight)+" : "+repr(self.character)+"\n"


class huffman_tree:

    def __init__(self, root):
        self.root = root


    def __repr__(self):
        return self.root.__repr__(0)


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

def build_tree(leafs):
    nodes = leafs.copy()
    while len(nodes) > 1:
        min_1 = min(nodes, key=lambda n: n.weight)
        nodes.remove(min_1)
        min_2 = min(nodes, key=lambda n: n.weight)
        nodes.remove(min_2)
        
        new_node = Node(min_1.weight+min_2.weight, min_1, min_2)
        nodes.append(new_node)

    return huffman_tree(nodes[0])

def huffman_code(tree):
    codes = {}
    code = ""
    tree.root.huffman_code(codes, code)
    return codes



phrase = "je mange des saucisses seches venant d'estonie"
occs_phrase = occurences(phrase)
leafs = build_leafs(occs_phrase)
tree = build_tree(leafs)
print(tree)
huff_code = huffman_code(tree)
print(huff_code)
