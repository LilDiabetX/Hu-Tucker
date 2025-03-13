from graphviz import Digraph
from tree_struct import Node, Leaf

def create_graph(dot, node, root=False):
    if root:
        dot.node(str(node.id), str(node.weight))
    if isinstance(node, Leaf):
        label = f"w: \\'{node.weight}\\'\\nc: \'{node.character}\'"
        dot.node(str(node.id), label)
    else:
        if node.child_left:
            dot.node(str(node.child_left.id), f"w: {node.child_left.weight}")
            dot.edge(str(node.id), str(node.child_left.id), "0")
            create_graph(dot, node.child_left)
        if node.child_right:
            dot.node(str(node.child_right.id), f"w: {node.child_right.weight}")
            dot.edge(str(node.id), str(node.child_right.id), "1")
            create_graph(dot, node.child_right)

def plot_tree(tree):
    dot = Digraph(format="png")
    create_graph(dot, tree.root, True)
    dot.attr(rankdir="TB")

    output_path = "output/tree"
    dot.render(output_path, view=True)
