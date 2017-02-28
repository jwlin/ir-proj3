#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tokenize a web page
"""

import re
from collections import Counter, defaultdict
from util import merge_href


class Tokenizer:
    @classmethod
    def tokenize(cls, text):
        # todo: add LINQUISTIC MODELS
        t_list = re.split('[^a-zA-Z0-9]', text.strip().lower())
        t_list = [t for t in t_list if len(t) > 0]
        return t_list

    @classmethod
    def tokenize_link(cls, orig_url, soup_a_links):
        data = {}
        for a in soup_a_links:
            print(a)
            t_list = cls.tokenize(a.text)
            print(t_list)
            point_to = ''
            if 'href' in a.attrs.keys():
                point_to = merge_href(orig_url, a['href'])
                print('point to:', point_to)
            if t_list and point_to:
                data[point_to] = ' '.join(t_list)
            #input()
        return data

    '''
    def word_freq(self):
        tokens = list()
        for word, _ in sorted(self.__tokens.items(), key=lambda k: k[1], reverse=True):
            tokens.append((word, self.__tokens[word]))
        return tokens

    def tokens(self):
        tokens_list = [word for word, _ in self.__tokens.items()]
        return sorted(tokens_list)
    '''

if __name__ == '__main__':
    pass
    '''
    fpath = 'D:\PartA\A10'
    tokenizer = Tokenizer(fpath)
    print(tokenizer.tokens())
    print(tokenizer.word_freq())
    '''