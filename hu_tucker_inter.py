import sys
import heapq
from tree_struct import Leaf, Node, Tree, Node_opt, Leaf_opt
from utils import occurences, build_initial_seq, build_initial_seq_inter
from display_tree import plot_tree
from collections import deque

#Phase One
def combination(initial_seq, debug=False):
    T = [{'s': l.weight, 'nt' : 'E', 'c' : l.character, 'mpql': None, 'mpqr': None} for l in initial_seq]

    A = initial_seq.copy()
    # A = [o['s'] for o in T]
    # create HPQs from any existing T E = external node I = internal node
    hpqs = []
    started = False
    hpq = []
    n=0
    while True:
        value, node_type = T[n]['s'], T[n]['nt'] 
        hpq.append([value, n])
        if node_type == 'E' and started:
            hpqs.append(hpq)
            hpq = []
            started = False
            T[n]['mpql'] = n -1
            n = n-1
        elif node_type == 'E' and not started:
            started = True  
            T[n]['mpqr'] = n
        n = n + 1
        if n == len(T):
            # hpqs.append(hpq)
            break
    T[-1]['mpqr'] = None


    # create MPQ from HPQs
    mpq = []
    for n, hpq in enumerate(hpqs):
        heapq.heapify(hpq)
        # version that does not leaves HPQs in place
        # access = O(log(N))
        # w1, i= heapq.heappop()
        # w2, j= heapq.heappop()
        # version that leaves HPQs in place
        # access = O(NlogN) (sort) + O(1) 
        _hpq = sorted(hpq) # sort elems of the list to make the heap invariant
        w1, i= _hpq[0] # access smallest elem without popping element from HPQ
        w2, j= _hpq[1] # access 2nd smallest elem without popping element from HPQ

        heapq.heappush(mpq, [w1+w2, i,j, n]) # need i,j to resolve ties, which are resolved automatically by the leaftist heap


    iter = 0
    nodes = []
    while True:
        ### ======== UPDATE -- Main loop
        # --- extract_min
        new_node_weight, i,j, hpq_id = heapq.heappop(mpq)
        # _L, _R = hpqs[hpq_id][0], hpqs[hpq_id][-1] # main hpq
        if i < j:
            _L = [A[i].weight,i]
            _R = [A[j].weight, j]
        else:
            _L = [A[j].weight,j]
            _R = [A[i].weight, i]
        # remove nodes, not entire HPQ
        hpqs[hpq_id].remove(_L)# O(N)
        hpqs[hpq_id].remove(_R)# O(N)


        hpq_merge = [hpq_id]
        try:
            k = 1
            while (hpq_id -k > 0) and (hpqs[hpq_id-k] == []):
                k += 1
            hpqs[hpq_id-k].remove(_L) # O(N)
            hpq_merge.append(hpq_id-k)
        except (ValueError, IndexError): 
            pass
        try:
            k = 1
            while hpqs[hpq_id+k] == []:
                k += 1
            hpqs[hpq_id+k].remove(_R) # O(N)
            hpq_merge.append(hpq_id+k)
        except (ValueError, IndexError):
            pass

        # --- merge HPQs
        hpq_new = list(heapq.merge(*[hpqs[hpq_id] for hpq_id in hpq_merge]))
        min_hpq_id = int(1e10)
        for hpq_id in hpq_merge:
            if len(hpqs[hpq_id]) == 1:
                hpqs[hpq_id]  = []
            min_hpq_id = min(min_hpq_id, hpq_id)
        # --- clean remaining hpq:
        for hpq_id in hpq_merge:
            hpqs[hpq_id] = []
        # --- add new_hpq
        hpqs[min_hpq_id] = hpq_new

        # hpqs.append(hpq_new)
        # --- delete entries in MPQ

        mpq = [m for m in mpq if m[3] not in hpq_merge] # O(N)
        # --- new node
        new_node = [new_node_weight, min(i,j)]
        new_node_A = Node(new_node_weight, A[_L[1]], A[_R[1]])
        if debug:
            plot_tree(Tree(new_node_A), outputname=f"wip_phase_1_tree_{iter}")
            iter += 1
        nodes.append(new_node)
        # --- update A
        if i < j:
            A[i] = new_node_A
            A[j] = None
        else:
            A[j] = new_node_A
            A[i] = None

        # --- insert new node into hpq
        heapq.heappush(hpq_new, new_node)

        if len(hpq_new) == 1:
            break
        # --- insert hpq_new into mpq
        _hpq_new = sorted(hpq_new) # sort elems of the list to make the heap invariant
        
        w1, i= _hpq_new[0] # access smallest elem without popping element from HPQ
        w2, j= _hpq_new[1]

        heapq.heappush(mpq, [w1+w2, i,j, min_hpq_id])
    print(A[0])
    return Tree(A[0])

def level_assignment_aux(node, index_map, leaf_levels, level=0):
    if isinstance(node, Leaf_opt):
        i = index_map[node]
        leaf_levels[i] = (node, level)
    else:
        level_assignment_aux(node.child_left, index_map, leaf_levels, level=level+1)
        level_assignment_aux(node.child_right, index_map, leaf_levels, level=level+1)

# Phase Two
def level_assignment(tree, initial_seq):
    index_map = {leaf: i for i, leaf in enumerate(initial_seq)}
    leaf_levels = [(leaf, None) for leaf in initial_seq]
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
    phrase = "aaaaaaaaaazzeertyyyyuuuuuuuuuuuuuuuiiiiiiiiiiiiiiiiiooooooooooooooooooooooooo" # Même configuration que dans l'exemple de la thèse (10, 2, 2, 1, 1, 4, 15, 17, 25)
    occs = occurences(phrase)
    initial_seq = build_initial_seq_inter(occs)
    # Fin du Set-up

    # Phase 1
    comb_tree = combination(initial_seq, debug=debug)
    if debug:
        plot_tree(comb_tree, outputname="phase_1_tree")

    # Phase 2
    leaf_levels = level_assignment(comb_tree, initial_seq)
    if debug:
        for leaf, level in leaf_levels:
            print(leaf.__repr__(), "niveau", level, "\n")

    # Phase 3
    hu_tucker_tree = recombination(leaf_levels, debug=debug)
    plot_tree(hu_tucker_tree, label_edges=True, outputname="hu_tucker_tree_inter")

if __name__== '__main__':
    main(debug=True)

