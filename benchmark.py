import time
import numpy as np
import hu_tucker as ht
import huffman as hm
import os
import matplotlib.pyplot as plt

path = os.getcwd()
files_100 = [f for f in os.listdir(path + "/corpus_tests/100_char")]
files_500 = [f for f in os.listdir(path + "/corpus_tests/500_char")]
files_1000 = [f for f in os.listdir(path + "/corpus_tests/1000_char")]
files_2000 = [f for f in os.listdir(path + "/corpus_tests/2000_char")]

def bench_hu_tucker():
    times_100 = np.zeros(len(files_100))
    times_500 = np.zeros(len(files_500))
    times_1000 = np.zeros(len(files_1000))
    times_2000 = np.zeros(len(files_2000))

    print("Processing 100 characters files...")
    for i, f in enumerate(files_100):
        file = open("corpus_tests/100_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs = ht.occurences(text)
        initial_seq = ht.build_initial_seq(occs)
        # Fin du Set-up
        t_start = time.time()
        # Phase 1
        comb_tree = ht.combination(initial_seq, debug=False)

        # Phase 2
        leaf_levels = ht.level_assignment(comb_tree, initial_seq)

        # Phase 3
        hu_tucker_tree = ht.recombination(leaf_levels, debug=False)
        t_end = time.time()
        times_100[i] = t_end - t_start
    print(str(len(files_100)) + " 100 characters files processed in " + str(np.sum(times_100)) + "s")

    print("Processing 500 characters files...")
    for i, f in enumerate(files_500):
        file = open("corpus_tests/500_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs = ht.occurences(text)
        initial_seq = ht.build_initial_seq(occs)
        # Fin du Set-up
        t_start = time.time()
        # Phase 1
        comb_tree = ht.combination(initial_seq, debug=False)

        # Phase 2
        leaf_levels = ht.level_assignment(comb_tree, initial_seq)

        # Phase 3
        hu_tucker_tree = ht.recombination(leaf_levels, debug=False)
        t_end = time.time()
        times_500[i] = t_end - t_start
    print(str(len(files_500)) + " 500 characters files processed in " + str(np.sum(times_500)) + "s")

    print("Processing 1000 characters files...")
    for i, f in enumerate(files_1000):
        file = open("corpus_tests/1000_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs = ht.occurences(text)
        initial_seq = ht.build_initial_seq(occs)
        # Fin du Set-up
        t_start = time.time()
        # Phase 1
        comb_tree = ht.combination(initial_seq, debug=False)

        # Phase 2
        leaf_levels = ht.level_assignment(comb_tree, initial_seq)

        # Phase 3
        hu_tucker_tree = ht.recombination(leaf_levels, debug=False)
        t_end = time.time()
        times_1000[i] = t_end - t_start
    print(str(len(files_1000)) + " 1000 characters files processed in " + str(np.sum(times_1000)) + "s")

    print("Processing 2000 characters files...")
    for i, f in enumerate(files_2000):
        file = open("corpus_tests/2000_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs = ht.occurences(text)
        initial_seq = ht.build_initial_seq(occs)
        # Fin du Set-up
        t_start = time.time()
        # Phase 1
        comb_tree = ht.combination(initial_seq, debug=False)

        # Phase 2
        leaf_levels = ht.level_assignment(comb_tree, initial_seq)

        # Phase 3
        hu_tucker_tree = ht.recombination(leaf_levels, debug=False)
        t_end = time.time()
        times_2000[i] = t_end - t_start
    print(str(len(files_2000)) + " 2000 characters files processed in " + str(np.sum(times_2000)) + "s")

    times = [times_100, times_500, times_1000, times_2000]
    means = [np.mean(t) for t in times]
    labels = ['100 char', '500 char', '1000 char', '2000 char']
    fig, axes = plt.subplots(1 + len(times), 1, figsize=(8, 12))
    axes[0].bar(labels, means, color=['blue', 'red', 'green', 'purple'])
    axes[0].set_xlabel('nombre de caractères différents')
    axes[0].set_ylabel('Temps moyen')
    axes[0].set_title('Temps moyen par nombre de caractères différents')

    for i, tableau in enumerate(times):
        axes[i + 1].plot(tableau, marker='o', linestyle='-', color='black')
        axes[i + 1].set_title(labels[i])
        axes[i + 1].set_ylabel('Temps')
        axes[i + 1].set_xlabel('Fichier')
    plt.tight_layout()
    plt.show()




def bench_huffman():
    times_100 = np.zeros(len(files_100))
    times_500 = np.zeros(len(files_500))
    times_1000 = np.zeros(len(files_1000))
    times_2000 = np.zeros(len(files_2000))

    print("Processing 100 characters files...")
    for i, f in enumerate(files_100):
        file = open("corpus_tests/100_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        t_start = time.time()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        times_100[i] = t_end - t_start
    print(str(len(files_100)) + " 100 characters files processed in " + str(np.sum(times_100)) + "s")

    print("Processing 500 characters files...")
    for i, f in enumerate(files_500):
        file = open("corpus_tests/500_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        t_start = time.time()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        times_500[i] = t_end - t_start
    print(str(len(files_500)) + " 500 characters files processed in " + str(np.sum(times_500)) + "s")

    print("Processing 1000 characters files...")
    for i, f in enumerate(files_1000):
        file = open("corpus_tests/1000_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        t_start = time.time()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        times_1000[i] = t_end - t_start
    print(str(len(files_1000)) + " 1000 characters files processed in " + str(np.sum(times_1000)) + "s")

    print("Processing 2000 characters files...")
    for i, f in enumerate(files_2000):
        file = open("corpus_tests/2000_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        t_start = time.time()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        times_2000[i] = t_end - t_start
    print(str(len(files_2000)) + " 2000 characters files processed in " + str(np.sum(times_2000)) + "s")

    times = [times_100, times_500, times_1000, times_2000]
    means = [np.mean(t) for t in times]
    labels = ['100 char', '500 char', '1000 char', '2000 char']
    fig, axes = plt.subplots(1 + len(times), 1, figsize=(8, 12))
    axes[0].bar(labels, means, color=['blue', 'red', 'green', 'purple'])
    axes[0].set_xlabel('nombre de caractères différents')
    axes[0].set_ylabel('Temps moyen')
    axes[0].set_title('Temps moyen par nombre de caractères différents')

    for i, tableau in enumerate(times):
        axes[i + 1].plot(tableau, marker='o', linestyle='-', color='black')
        axes[i + 1].set_title(labels[i])
        axes[i + 1].set_ylabel('Temps')
        axes[i + 1].set_xlabel('Fichier')
    plt.tight_layout()
    plt.show()
    
        
bench_hu_tucker()
