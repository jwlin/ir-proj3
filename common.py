#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Find tokens in common
"""

from tokenizer import Tokenizer


if __name__ == '__main__':
    fpaths = ['''C:\enwiki-20170120-pages-articles26.xml-4000000''',
              '''D:\enwiki-20170120-pages-articles26.xml-300000''']
    tokenizer1 = Tokenizer(fpaths[0])
    tokenizer2 = Tokenizer(fpaths[1])

    tokens1 = tokenizer1.tokens()
    tokens2 = tokenizer2.tokens()
    tokens2 = set(tokens2)

    common_tokens = []
    for token in tokens1:
        if token in tokens2:
            common_tokens.append(token)
    print(len(common_tokens))
    print(sorted(common_tokens))
