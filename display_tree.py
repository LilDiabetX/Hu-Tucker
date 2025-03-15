from graphviz import Digraph
from tree_struct import Node, Leaf

def create_graph(dot, node, label_edges=False, root=False):
    if root:
        dot.node(str(node.id), "w: "+str(node.weight))
    if isinstance(node, Leaf):
        label = f"w: \\'{node.weight}\\'\\nc: \'{node.character}\'"
        dot.node(str(node.id), label)
    else:
        if node.child_left:
            dot.node(str(node.child_left.id), f"w: {node.child_left.weight}")
            dot.edge(str(node.id), str(node.child_left.id), "0" if label_edges else "")
            create_graph(dot, node.child_left, label_edges=label_edges)
        if node.child_right:
            dot.node(str(node.child_right.id), f"w: {node.child_right.weight}")
            dot.edge(str(node.id), str(node.child_right.id), "1" if label_edges else "")
            create_graph(dot, node.child_right, label_edges=label_edges)

def plot_tree(tree, label_edges=False, outputname="tree"):
    dot = Digraph(format="png")
    create_graph(dot, tree.root, label_edges=label_edges, root=True)
    dot.attr(rankdir="TB")

    output_path = "output/"+outputname
    dot.render(output_path, view=True)
