#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module docstring
"""

import json
import math


class Ndcg:
    def __init__(self):
        self.answer = dict()
        with open('google-query.json', 'r') as f:
            data = json.load(f)
            for k, v in data.items():
                self.answer[k] = list()
                for url in v:
                    url = self.remove_url(url)
                    self.answer[k].append(url)

    def get_ndcg(self, query, result_list):
        ideal_relevance = [5, 4, 3, 2, 1]
        idcg = self.dcg(ideal_relevance)
        real_relevance = list()
        for url in result_list:
            relevance = 0
            url = self.remove_url(url)
            if url in self.answer[query]:
                relevance = ideal_relevance[self.answer[query].index(url)]
            real_relevance.append(relevance)
        dcg = self.dcg(real_relevance)
        return dcg/idcg

    def dcg(self, relevance):
        dcg = 0
        for i in range(1, len(relevance)+1):
            dcg += (math.pow(2, relevance[i-1]) - 1) / (math.log2(i+1))
        return dcg

    def remove_url(self, url):
        if url.endswith('/index.html'):
            url = url[:-11]
        elif url.endswith('/index.php'):
            url = url[:-10]
        elif url.endswith('/index.htm'):
            url = url[:-10]
        elif url[-1] == '/':
            url = url[:-1]
        return url
