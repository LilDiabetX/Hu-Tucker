import sys
import heapq
from tree_struct import Leaf, Node, Tree, Node_opt, Leaf_opt
from utils import occurences, build_initial_seq, build_initial_seq_inter
from display_tree import plot_tree
from collections import deque

# Phase One
def combination(initial_seq, debug=False):
    N = len(initial_seq)
    T = list(initial_seq)
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
    k = 0
    for l in range(1, N):
        total, hpq_id = heapq.heappop(MPQ)
        seq, hpq = HPQs[hpq_id]
            
        # On prend les deux plus petits éléments
        (w1, n1) = hpq.pop()
        (w2, n2) = hpq.pop()
        print("FUSION DE ")
        print("Poids :", n1.weight, "+", n2.weight, "=", n1.weight + n2.weight)


        # Supprimer n1 et n2 de toutes les HPQs où ils sont
        affected_hpq_ids = set(n1.queue_participation) | set(n2.queue_participation)
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
        for hid in affected_hpq_ids:
            s, h = HPQs[hid]
            merged_seq.extend(s)
            merged_heap.extend(h)
            HPQs[hid] = (deque(), [])  # on vide l’ancienne HPQ

        heapq.heapify(merged_heap)
        MPQ = [(x, y) for (x, y) in MPQ if y not in affected_hpq_ids]
        heapq.heapify(MPQ)

        # Créer un nouveau noeud combiné
        new_node = Node_opt(w=n1.weight + n2.weight, left=n1, right=n2)
        if(debug):
            plot_tree(Tree(new_node), outputname=f"wip_phase_1_tree_{k}")
            k+=1

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
            smallest_two = heapq.nsmallest(2, merged_heap)
            if len(smallest_two) == 2:
                w1, _ = smallest_two[0]
                w2, _ = smallest_two[1]
                heapq.heappush(MPQ, (w1 + w2, new_hpq_id))

    print(type(A[0]))
    print(type(Tree(A[0])))
    return Tree(A[0])


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

def recombination(leaf_levels, debug=False):
    stack = deque() # LIFO - use pop()
    queue = deque() # FIFO - use popleft()
    for leaf in leaf_levels:
        queue.appendleft(leaf)
    
    k = 0
    while queue or len(stack)!=1:
        if debug:
            print(f"Queue Content : {[l for _, l in queue]}")
            print(f"Stack Content : {[l for _, l in stack]}")
        if len(stack) < 2:
            elt = queue.popleft()
            stack.append(elt)
        else:
            s_1 = stack.pop()
            s_2 = stack.pop()
            if s_1[1] != s_2[1]:
                elt = queue.popleft()
                stack.append(s_2)
                stack.append(s_1)
                stack.append(elt)
            else:
                stack.append(s_2)
                stack.append(s_1)
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
    phrase = "aaaaaaaaaazzeertyyyyuuuuuuuuuuuuuuuiiiiiiiiiiiiiiiiiooooooooooooooooooooooooo" # Même configuration que dans l'exemple de la thèse (1022114151725)
    occs = occurences(phrase)
    initial_seq = build_initial_seq_inter(occs)
    # Fin du Set-up

    # Phase 1
    comb_tree = combination(initial_seq, debug=debug)
    if debug:
        plot_tree(comb_tree, outputname="phase_1_tree")
"""
    # Phase 2
    leaf_levels = level_assignment(comb_tree, initial_seq)
    if debug:
        for leaf, level in leaf_levels:
            print(leaf.__repr__(), "niveau", level, "\n")

    # Phase 3
    hu_tucker_tree = recombination(leaf_levels, debug=debug)
    plot_tree(hu_tucker_tree, label_edges=True, outputname="hu_tucker_tree_inter")
"""
if __name__== '__main__':
    main(debug=True)

