#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Perform query
"""

import os
import json
from gensim import corpora, models, similarities
from tokenizer import Tokenizer


class Searcher:
    def __init__(self, doc_dir, output_dir, book_file, index_type='title', model_type='tfidf'):
        self.doc_dir = doc_dir
        self.output_dir = output_dir
        self.book_file = book_file
        self.index_type = index_type  # body/title
        self.model_type = model_type  # tfidf/lsi
        self.book_data = {}
        self.index_to_key = {}
        self.dict = None
        self.id2token = {}
        self.model = None
        self.corpus = None
        self.sim_index = None

        self.load_all_data()

    def load_all_data(self):
        # book_data
        self.book_data = self.load_json(self.book_file)
        # index_to_key
        self.index_to_key = self.load_json(os.path.join(self.output_dir, self.index_type + '_index_to_key.json'))
        # dict
        self.dict = corpora.Dictionary.load(os.path.join(self.output_dir, self.index_type + '.dict'))
        self.id2token = self.load_json(self.index_type + '.dict.json')
        # model

        if self.model_type == 'tfidf':
            self.model = models.TfidfModel.load(os.path.join(self.output_dir, self.index_type + '.corpus.tfidf.model'))
            corpus_name = self.index_type + '.corpus.tfidf'
        elif self.model_type == 'lsi':
            self.model = models.LsiModel.load(os.path.join(self.output_dir, self.index_type + '.corpus.lsi.model'))
            #print(len(self.model.print_topics()))
            corpus_name = self.index_type + '.corpus.lsi'
        # corpus
        self.corpus = corpora.MmCorpus(os.path.join(self.output_dir, corpus_name))
        #print('sim index..')
        # sim_index
        if os.path.exists(os.path.join(self.output_dir, self.index_type + '.sim_index')):
            self.sim_index = similarities.MatrixSimilarity.load(os.path.join(self.output_dir, self.index_type + '.sim_index'))
        else:
            self.sim_index = similarities.MatrixSimilarity(self.corpus)
            self.sim_index.save(os.path.join(self.output_dir, self.index_type + '.sim_index'))

    def query(self, query_str):
        t_list = Tokenizer.tokenize(query_str)
        #print('t_list:', t_list)
        vec_bow = self.dict.doc2bow(t_list)
        vec_transformed = self.model[vec_bow]
        #print(vec_transformed)
        sims = self.sim_index[vec_transformed]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        top20 = [e for e in sims[:20] if e[1] > 0.5]
        #for did, sim in results:
        #    dkey = self.index_to_key[str(did)]
        #    with open(os.path.join(self.doc_dir, dkey.split('/')[0], dkey.split('/')[1] + '.' + self.index_type), 'r') as f:
        #        print(did, dkey, f.readlines(), sim)
        # retrieve info
        results = []
        for did, sim in top20:
            dkey = self.index_to_key[str(did)]
            url = self.book_data[dkey]
            title = ''
            if os.path.exists(os.path.join(self.doc_dir, dkey.split('/')[0], dkey.split('/')[1] + '.title')):
                with open(os.path.join(self.doc_dir, dkey.split('/')[0], dkey.split('/')[1] + '.title'), 'r') as f:
                    title = f.read().replace('\n', '')
            content = self.retrieve_text(dkey, t_list)
            results.append((dkey, sim, url, title, content))
        return results

    def load_json(self, fname):
        with open(os.path.join(self.output_dir, fname), 'r') as f:
            return json.load(f)

    def retrieve_text(self, dkey, t_list):
        if os.path.exists(os.path.join(self.doc_dir, dkey.split('/')[0], dkey.split('/')[1] + '.body')):
            with open(os.path.join(self.doc_dir, dkey.split('/')[0], dkey.split('/')[1] + '.body'), 'r') as f:
                text = f.read().replace('\n', ' ').split()
            for token in t_list:
                if token in text:
                    i = text.index(token)
                    i_start = i-20 if i-20 > -1 else 0
                    i_end = i+20 if i+20 < len(text) else len(text)-1
                    return ' '.join(text[i_start:i_end])
        return ''

if __name__ == '__main__':
    searcher_body = Searcher(
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed',
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed\\index',
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
        'body', 'lsi')
    searcher_body.query('Crista Lopes')
    searcher_title = Searcher(
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed',
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed\\index',
        'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
        'title', 'lsi')
    searcher_title.query('Crista Lopes')
