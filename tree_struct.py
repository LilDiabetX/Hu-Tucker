import itertools

class Node:

    id_iter = itertools.count()

    def __init__(self, w, left, right):
        self.id = next(Node.id_iter) # Pour l'affichage de l'arbre
        self.weight = w
        self.child_left = left
        self.child_right = right

    def __repr__(self, depth=0):
        ret = "\t"*depth+repr(self.weight)+"\n"
        if self.child_left:
            ret += self.child_left.__repr__(depth+1)
        if self.child_right:
            ret += self.child_right.__repr__(depth+1)
        return ret
    
    def __le__(self, other):
        return (isinstance(other, Leaf) or isinstance(other, Node)) and self.weight <= other.weight
    
    def __lt__(self, other):
        return (isinstance(other, Leaf) or isinstance(other, Node)) and self.weight < other.weight

class Leaf(Node):

    def __init__(self, w, c):
        Node.__init__(self, w, None, None)
        self.character = c

    def __repr__(self, depth):
        return "\t"*depth+repr(self.weight)+" : "+repr(self.character)+"\n"
    
    def __eq__(self, other):
        return isinstance(other, Leaf) and self.character == other.character

    def __hash__(self):
        return hash(self.character)
    
    def __le__(self, other):
        return (isinstance(other, Leaf) or isinstance(other, Node)) and self.weight <= other.weight
    
    def __lt__(self, other):
        return (isinstance(other, Leaf) or isinstance(other, Node)) and self.weight < other.weight

class Tree:

    def __init__(self, root):
        self.root = root

    def __repr__(self):
        return self.root.__repr__(0)
    

class Node_opt(Node):

    def __init__(self, w, left, right):
        super().__init__(w, left, right)
        self.queue_participation = []

    def add_participation(self, queue):
        self.queue_participation.append(queue)

    def __lt__(self, other):
        return self.weight < other.weight


class Leaf_opt(Node_opt):

    def __init__(self, w, c):
        super().__init__(w, None, None)
        self.character = c

    def __repr__(self, depth=0):
        return "\t"*depth+repr(self.weight)+" : "+repr(self.character)+"\n"