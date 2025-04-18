import sys
import heapq
from tree_struct import Leaf, Node, Tree, Node_opt, Leaf_opt
from utils import occurences, build_initial_seq, build_initial_seq_inter
from display_tree import plot_tree
from collections import deque


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
            plot_tree(Tree(nodes[i]), outputname="wip_phase_1_tree_{k}")
            k += 1
    return Tree(nodes[0])

def combination_inter(initial_seq, debug=False) -> Tree:
    N = len(initial_seq)
    T = list(initial_seq)
    """
    A = initial_seq.copy()
    MPQ = deque()
    HPQs = []

    for i in range (N - 1):
        hpq = deque()
        hpq.append(A[i])
        hpq.append(A[i+1])
        HPQs.append(hpq)

        
        MPQ.append(hpq)

    for _ in range(N):
        n1, n2 = extract_min(MPQ)
        for hpq in n1.queue_participation:
            hpq.remove(n1)
        for hpq in n2.queue_participation:
            hpq.remove(n2)
    """
    A = list(T)

    HPQs = []  # Liste des HPQs (chacune = [deque, heap])
    MPQ = []   # Heap contenant (somme des 2 plus petits poids, HPQ index)

    # Initialisation
    for i in range(N - 1):
        sequence = deque([T[i], T[i+1]])
        hpq_heap = [(T[i].weight, T[i]), (T[i+1].weight, T[i+1])]
        heapq.heapify(hpq_heap)
        HPQs.append((sequence, hpq_heap))

        T[i].add_participation(i)
        T[i+1].add_participation(i)

        total = T[i].weight + T[i+1].weight
        heapq.heappush(MPQ, (total, i))

    while len(A) > 1:
        while True:
            if not MPQ:
                return Tree(A[0])
            total, hpq_id = heapq.heappop(MPQ)
            seq, hpq = HPQs[hpq_id]
            if len(hpq) >= 2:
                break

        # On prend les deux plus petits éléments
        (w1, n1), (w2, n2) = heapq.nsmallest(2, hpq)
        print("FUSION DE :", n1.character, "et", n2.character)
        print("Poids :", n1.weight, "+", n2.weight, "=", n1.weight + n2.weight)


        # Supprimer n1 et n2 de toutes les HPQs où ils sont
        affected_hpq_ids = set(n1.queue_participation + n2.queue_participation)
        for hid in affected_hpq_ids:
            s, h = HPQs[hid]
            h[:] = [(w, n) for (w, n) in h if n != n1 and n != n2]
            try: s.remove(n1)
            except: pass
            try: s.remove(n2)
            except: pass
            heapq.heapify(h)

        # Fusionner toutes les HPQs concernées (on les merge en une seule nouvelle)
        merged_seq = deque()
        merged_heap = []
        for hid in sorted(affected_hpq_ids):
            s, h = HPQs[hid]
            merged_seq.extend(s)
            merged_heap.extend(h)
            HPQs[hid] = (deque(), [])  # on vide l’ancienne HPQ

        heapq.heapify(merged_heap)

        # Créer un nouveau noeud combiné
        new_node = Node_opt(w=n1.weight + n2.weight, left=n1, right=n2)
        if(debug):
            plot_tree(Tree(new_node))

        # Mise à jour de A
        A = [n for n in A if n != n1 and n != n2]
        A.append(new_node)

        # Ajouter le nouveau noeud à la séquence et au heap
        merged_seq.append(new_node)
        heapq.heappush(merged_heap, (new_node.weight, new_node))

        # Créer une nouvelle HPQ
        new_hpq_id = len(HPQs)
        HPQs.append((merged_seq, merged_heap))
        new_node.queue_participation = [new_hpq_id]

        # Ajouter à MPQ
        if len(merged_heap) >= 2:
            w1, _ = heapq.nsmallest(1, merged_heap)[0]
            w2, _ = heapq.nsmallest(2, merged_heap)[1]
            heapq.heappush(MPQ, (w1 + w2, new_hpq_id))
    print(type(A[0]))
    print(type(Tree(A[0])))
    return Tree(A[0])
        

#def combination_fast(initial_seq, debug=False):
#    T = initial_seq.copy()
#    A = initial_seq.copy()
#    MPQ = deque() # FIFO - use popleft()

def level_assignment_aux(node, initial_seq, leaf_levels, level=0):
    if isinstance(node, Leaf) or isinstance(node, Leaf_opt):
        i = initial_seq.index(node)
        leaf_levels[i] = (node, level)
    else:
        level_assignment_aux(node.child_left, initial_seq, leaf_levels, level=level+1)
        level_assignment_aux(node.child_right, initial_seq, leaf_levels, level=level+1)

# Phase Two
def level_assignment(tree, initial_seq):
    leaf_levels = [(node, None) for node in initial_seq]
    level_assignment_aux(tree.root, initial_seq, leaf_levels)

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
            plot_tree(Tree(new_node), outputname="wip_phase_3_tree_{k}")
            k += 1
    assert(levels[0][1]==0)
    return Tree(levels[0][0])

def recombination_stack(leaf_levels, debug=False):
    stack = deque() # LIFO - use pop()
    queue = deque() # FIFO - use popleft()
    for leaf in leaf_levels:
        queue.appendleft(leaf)
    
    k = 0
    while queue or len(stack)!=1:
        if debug:
            print(f"Queue Content : {[l for _, l in queue]}")
            print(f"Stack Content : {[l for _, l in stack]}")
        if len(stack) < 2 or stack[-1][1] != stack[-2][1]:
            elt = queue.popleft()
            stack.append(elt)
        else:
            q_1, l_1 = stack.pop()
            q_2, _ = stack.pop()
            new_elt = Node(q_1.weight+q_2.weight, q_1, q_2)
            stack.append((new_elt, l_1-1))
            if debug:
                plot_tree(Tree(new_elt), outputname=f"wip_phase_3_opt_tree_{k}")
                k += 1
    assert(len(stack) == 1)
    assert(stack[0][1] == 0)
    return Tree(stack[0][0])



def main(debug):
    #phrase = "je mange des saucisses seches venant d'estonie"
    phrase = "aaaaazzeeeeeeerrtyuiiooooppppp" # Même configuration que dans l'exemple de la thèse (5272111245)
    occs = occurences(phrase)
    #initial_seq = build_initial_seq(occs)
    initial_seq = build_initial_seq_inter(occs)
    # Fin du Set-up

    # Phase 1
    #comb_tree = combination(initial_seq, debug=debug)
    comb_tree = combination_inter(initial_seq, debug=debug)
    if debug:
        plot_tree(comb_tree, outputname="phase_1_tree")

    # Phase 2
    leaf_levels = level_assignment(comb_tree, initial_seq)
    if debug:
        for leaf, level in leaf_levels:
            print(leaf.__repr__(0), "niveau", level, "\n")

    # Phase 3
    # Here, set if you want to use the optimal version of phase 3 or not by uncommenting the right lines
    #hu_tucker_tree = recombination(leaf_levels, debug=debug)
    hu_tucker_tree = recombination_stack(leaf_levels, debug=debug)
    #plot_tree(hu_tucker_tree, label_edges=True, outputname="hu_tucker_tree")
    plot_tree(hu_tucker_tree, label_edges=True, outputname="hu_tucker_tree_opt")

if __name__== '__main__':
    main(debug=True)

