import time
import sys
import numpy as np
import hu_tucker as ht
import huffman as hm
import os
import matplotlib.pyplot as plt

path = os.getcwd()
files_100 = [f for f in os.listdir(path + "/corpus_tests/100_char")]
files_500 = [f for f in os.listdir(path + "/corpus_tests/500_char")]
files_1000 = [f for f in os.listdir(path + "/corpus_tests/1000_char")]

def bench_hu_tucker(save=True):
    print("Hu-Tucker benchmark start")
    times_100 = np.zeros(len(files_100))
    times_500 = np.zeros(len(files_500))
    times_1000 = np.zeros(len(files_1000))
    if save:
        output = open(path + "/output/result_hu_tucker_benchmark.csv", 'w')

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
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_100[i] = t_end - t_start
    print(str(len(files_100)) + " 100 characters files processed in " + str(np.sum(times_100)) + "s")
    if save:
        output.write('\n')

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
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_500[i] = t_end - t_start
    print(str(len(files_500)) + " 500 characters files processed in " + str(np.sum(times_500)) + "s")
    if save:
        output.write('\n')

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
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_1000[i] = t_end - t_start
    print(str(len(files_1000)) + " 1000 characters files processed in " + str(np.sum(times_1000)) + "s")
    if save:
        output.write('\n')
        output.close()

    times = [times_100, times_500, times_1000]
    means = [np.mean(t) for t in times]
    labels = ['100 char', '500 char', '1000 char']
    fig, axes = plt.subplots(1 + len(times), 1, figsize=(8, 12))
    axes[0].bar(labels, means, color=['blue', 'red', 'green'])
    axes[0].set_xlabel('nombre de caractères différents')
    axes[0].set_ylabel('Temps moyen')
    axes[0].set_title('Temps moyen par nombre de caractères différents')

    for i, tableau in enumerate(times):
        axes[i + 1].plot(tableau, marker='o', linestyle='', color='black')
        axes[i + 1].set_title(labels[i])
        axes[i + 1].set_ylabel('Temps')
        axes[i + 1].set_xlabel('Fichier')
        axes[i + 1].set_ylim(bottom=0)
    plt.tight_layout()
    plt.show()




def bench_huffman(save=True):
    print("Huffman benchmark start")
    times_100 = np.zeros(len(files_100))
    times_500 = np.zeros(len(files_500))
    times_1000 = np.zeros(len(files_1000))
    if save:
        output = open(path + "/output/result_huffman_benchmark.csv", 'w')

    print("Processing 100 characters files...")
    for i, f in enumerate(files_100):
        file = open("corpus_tests/100_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        t_start = time.time()
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_100[i] = t_end - t_start
    print(str(len(files_100)) + " 100 characters files processed in " + str(np.sum(times_100)) + "s")
    if save:
        output.write('\n')

    print("Processing 500 characters files...")
    for i, f in enumerate(files_500):
        file = open("corpus_tests/500_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        t_start = time.time()
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_500[i] = t_end - t_start
    print(str(len(files_500)) + " 500 characters files processed in " + str(np.sum(times_500)) + "s")
    if save:
        output.write('\n')

    print("Processing 1000 characters files...")
    for i, f in enumerate(files_1000):
        file = open("corpus_tests/1000_char/" + f, mode='r', encoding="utf-8")
        text = file.read()
        occs_phrase = hm.occurences(text)
        leafs = hm.build_initial_seq(occs_phrase)
        t_start = time.time()
        tree = hm.build_huffman_tree(leafs)
        huff_code = hm.huffman_code(tree)
        t_end = time.time()
        file.close()
        if save:
            output.write(str(t_end - t_start) + ';')
        times_1000[i] = t_end - t_start
    print(str(len(files_1000)) + " 1000 characters files processed in " + str(np.sum(times_1000)) + "s")
    if save:
        output.write('\n')
        output.close()

    times = [times_100, times_500, times_1000]
    means = [np.mean(t) for t in times]
    labels = ['100 char', '500 char', '1000 char']
    fig, axes = plt.subplots(1 + len(times), 1, figsize=(8, 12))
    axes[0].bar(labels, means, color=['blue', 'red', 'green'])
    axes[0].set_xlabel('nombre de caractères différents')
    axes[0].set_ylabel('Temps moyen')
    axes[0].set_title('Temps moyen par nombre de caractères différents')

    for i, tableau in enumerate(times):
        axes[i + 1].plot(tableau, marker='o', linestyle='', color='black')
        axes[i + 1].set_title(labels[i])
        axes[i + 1].set_ylabel('Temps')
        axes[i + 1].set_xlabel('Fichier')
        axes[i + 1].set_ylim(bottom=0)
    plt.tight_layout()
    plt.show()
    

def main():
    options = sys.argv[1:]
    right_option = False
    if "-nosave" in options:
        save = False
    else:
        save = True

    if "-a" in options or len(options) == 0 or (not save and len(options) == 1):
        right_option = True
        bench_huffman(save)
        bench_hu_tucker(save)
    elif "-hf" in options:
        right_option = True
        bench_huffman(save)
    elif "-ht" in options:
        right_option = True
        bench_hu_tucker(save)
    if "-h" in options or not right_option:
        print("Here is the list of the different options that you can use for this benchmark :")
        print("No option or -a : execute every test function of the benchmark")
        print("-hf : execute the bench_huffman function")
        print("-ht : execute the bench_hu_tucker function")
        print("-nosave : disable the save of the results in a csv file")
        print("-h : get the list of the available options")
        print("For instance, the line 'python3 benchmark.py -ht -ds' execute the bench_hu_tucker function but don't save the results in a csv file.")

if __name__ == '__main__':
  main()
# bench_hu_tucker()
# bench_huffman()