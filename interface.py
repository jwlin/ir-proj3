#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module docstring
"""

import json
from searcher import Searcher
from ndcg import Ndcg


class Interface:
    def __init__(self):
        self.searcher_body = Searcher(
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2\\index',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
            'body', 'lsi')
        self.searcher_title = Searcher(
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2\\index',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
            'title', 'tfidf')
        self.searcher_anchor = Searcher(
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2\\index',
            'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
            'anchor', 'tfidf')


    def query(self, query_str):
        dkey_to_score = {}
        body_list = self.searcher_body.query(query_str)
        self.accumulate(body_list, dkey_to_score)
        title_list = self.searcher_title.query(query_str)
        self.accumulate(title_list, dkey_to_score)
        anchor_list = self.searcher_anchor.query(query_str)
        self.accumulate(anchor_list, dkey_to_score)
        # add pagerank score
        self.page_rank(dkey_to_score)
        # todo: if same score, move shorter url forward
        scores = [v for k, v in dkey_to_score.items()]
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)
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

    def page_rank(self, score_map, weight=1.0):
        # add weight of page rank
        with open('PageRank.json', 'r') as f:
            pgrk = json.load(f)
        # first pass, get max pgrk value
        max_pg = 0
        for dkey in score_map.keys():
            if dkey in pgrk.keys() and pgrk[dkey] > max_pg:
                max_pg = pgrk[dkey]
        # second pass, add weighted page rank to the urls
        for k, v in score_map.items():
            if k in pgrk.keys():
                v['score'] += weight * (pgrk[k]/max_pg)


if __name__ == '__main__':
    interface = Interface()
    terms = ['mondego', 'machine learning', 'software engineering', 'security', 'student affairs',
             'graduate courses', 'Crista Lopes', 'REST', 'computer games', 'information retrieval']

    accu_ndcg = 0
    ndcg = Ndcg()
    for term in terms:
        print(term)
        results = interface.query(term)
        links = list()
        for r in results:
            #print(r['score'], r['link'])
            print(r['link'])
            links.append(r['link'])
        perf = ndcg.get_ndcg(term, links)
        accu_ndcg += perf
        #print('---')
        #input()
    print('Avg NDCG@5:', accu_ndcg/10)