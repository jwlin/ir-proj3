#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module docstring
"""

import json
import os
from searcher import Searcher


class Interface:
    def __init__(self):
        self.searcher_body = Searcher(
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed\\index',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
            'body', 'lsi')
        self.searcher_title = Searcher(
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed\\index',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
            'title', 'tfidf')

    def query(self, query_str):
        dkey_to_score = {}
        body_list = self.searcher_body.query(query_str)
        #print(len(body_list), body_list)
        self.accumulate(body_list, dkey_to_score)
        title_list = self.searcher_title.query(query_str)
        #print(len(title_list), title_list)
        self.accumulate(title_list, dkey_to_score)
        scores = [v for k, v in dkey_to_score.items()]
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        #print(len(scores), scores)
        return scores[:5]

    def accumulate(self, rank_list, score_map, weight=1.0):
        # each element is a tuple of (dkey, sim, url, title, content)
        for e in rank_list:
            dkey = e[0]
            sim = e[1]
            if dkey in score_map.keys():
                score_map[dkey]['score'] += weight * sim
            else:
                score_map[dkey] = {
                    'title': e[3],
                    'link': e[2],
                    'score': weight * sim,
                    'content': e[4]
                }


if __name__ == '__main__':
    interface = Interface()
    terms = ['mondego', 'machine learning', 'software engineering', 'security', 'student affairs',
             'graduate courses', 'Crista Lopes', 'REST', 'computer games', 'information retrieval']
    for term in terms:
        print(term)
        results = interface.query(term)
        for r in results:
            print(r)
        print('---')
        input()