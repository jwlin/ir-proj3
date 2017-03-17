#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tokenize a web page
"""

import re
from util import merge_href


class Tokenizer:
    @classmethod
    def tokenize(cls, text):
        # todo: add LINQUISTIC MODELS
        # todo: stemming
        stopwords_set = cls.get_stopwords()
        synonyms_list = cls.get_synonyms()
        t_list = re.split('[^a-zA-Z0-9]', text.strip().lower())
        # remove stopwords
        t_list = [t for t in t_list if len(t) > 0 and t not in stopwords_set]
        # add synonyms
        # [(['crista'], ['cristina']), (['cs'], ['computer', 'science']), ...]
        for list1, list2 in synonyms_list:
            if cls.contain(t_list, list1):
                t_list += list2
                continue
            if cls.contain(t_list, list2):
                t_list += list1
                continue
        return t_list

    @classmethod
    def tokenize_link(cls, orig_url, soup_a_links):
        data = {}
        for a in soup_a_links:
            #print(a)
            t_list = cls.tokenize(a.text)
            #print(t_list)
            point_to = ''
            if 'href' in a.attrs.keys():
                point_to = merge_href(orig_url, a['href'])
                #print('point to:', point_to)
            if t_list and point_to:
                data[point_to] = ' '.join(t_list)
            #input()
        return data

    @classmethod
    def get_stopwords(cls):
        stopwords = list()
        with open('stopwords.txt', 'r') as f:
            words = f.readlines()
            for w in words:
                stopwords += re.split('[^a-zA-Z0-9]', w.strip().lower())
        return set(stopwords)

    @classmethod
    def get_synonyms(cls):
        synos = list()
        with open('synonyms.txt', 'r') as f:
            for line in f:
                line = line.strip().lower()
                synos.append((line.split(',')[0].split(), line.split(',')[1].split()))
        return synos

    @classmethod
    def contain(cls, t_list, token_list):
        if len(token_list) == 1:
            return token_list[0] in t_list
        else:
            if token_list[0] in t_list:
                index = t_list.index(token_list[0])
                for i in range(1, len(token_list)):
                    if (index+i) > (len(t_list)-1):
                        return False
                    if t_list[index+i] != token_list[i]:
                        return False
                return True
        return False
