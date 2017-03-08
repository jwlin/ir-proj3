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
        did_to_score = {}
        body_list = self.searcher_body.query(query_str)
        #print(len(body_list), body_list)
        self.accumulate(body_list, did_to_score, self.searcher_body.index_to_key)
        title_list = self.searcher_title.query(query_str)
        #print(len(title_list), title_list)
        self.accumulate(title_list, did_to_score, self.searcher_title.index_to_key)
        scores = [(e[0], e[1]) for e in did_to_score.items()]
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        #print(len(scores), scores)
        return [self.searcher_body.book_data[key] for key, _ in scores[:5]]

    def accumulate(self, rank_list, score_map, did_to_dkey, weight=1.0):
        for did, sim in rank_list:
            dkey = did_to_dkey[str(did)]
            if dkey in score_map.keys():
                score_map[dkey] += weight * sim
            else:
                score_map[dkey] = weight * sim


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