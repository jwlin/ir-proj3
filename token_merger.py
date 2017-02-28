#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
merge the same tokens from two files
"""


from collections import defaultdict


if __name__ == '__main__':
    fpaths = ['tokens1.txt', 'tokens2.txt']
    tokens = defaultdict(int)
    with open(fpaths[0], 'r') as f:
        for line in f:
            word, count = line.strip().split(',')
            tokens[word] += int(count)
    with open(fpaths[1], 'r') as f:
        for line in f:
            word, count = line.strip().split(',')
            tokens[word] += int(count)

    token_list = sorted([word for word, _ in tokens.items()])
    for word in token_list:
        print('%s, %d' % (word, tokens[word]))
