#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module docstring
"""


import json
import os
import sys
from gensim import corpora, models, similarities
import util


class Indexer:
    def __init__(self, doc_dir, output_dir, book_file, index_type='title'):
        self.doc_dir = doc_dir
        self.output_dir = output_dir
        self.book_file = book_file
        self.index_type = index_type  # body/title
        self.book_data = {}
        self.docs = []
        self.index_to_key = {}
        self.dict = None
        self.id2token = {}
        self.index = {}
        
        with open(os.path.join(self.book_file), 'r', encoding='utf8') as f:
            self.book_data = json.load(f)
        if os.path.exists(os.path.join(self.output_dir, index_type + '_index_to_key.json')):
            with open(os.path.join(self.output_dir, index_type + '_index_to_key.json'), 'r', encoding='utf8') as f:
                self.index_to_key = json.load(f)
        if os.path.exists(os.path.join(self.output_dir, index_type + '.dict')):
            self.build_dict(index_type + '.dict')

    def load_doc(self):
        index = 0
        for key, url in self.book_data.items():
            print(key)
            if not util.is_valid(url):
                continue
            upper, lower = key.split('/')  # e.g. '0/1'
            if os.path.exists(os.path.join(self.doc_dir, upper, lower + '.' + self.index_type)):
                with open(os.path.join(self.doc_dir, upper, lower + '.' + self.index_type), 'r', encoding='utf8') as f:
                    self.docs.append(f.read().split())
                    self.index_to_key[str(index)] = key
                    index += 1
            #print(len(self.docs))
            #print(self.index_to_key)
            #input()
        self.save_json(self.index_to_key, self.index_type + '_index_to_key.json')
        self.build_dict(self.index_type + '.dict')

    def save_json(self, data, fname):
        with open(os.path.join(self.output_dir, fname), 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=True)

    def build_dict(self, fname):
        if os.path.exists(os.path.join(self.output_dir, self.index_type + '.dict')):
            self.dict = corpora.Dictionary.load(os.path.join(self.output_dir, self.index_type + '.dict'))
        else:
            self.dict = corpora.Dictionary(self.docs)
            self.dict.save(os.path.join(self.output_dir, fname))
        for k, v in self.dict.token2id.items():
            self.id2token[str(v)] = k
        assert len(self.id2token) == len(self.dict.token2id)

    def load_doc_with_index(self):
        keys = [self.index_to_key[str(i)] for i in range(len(self.index_to_key))]
        for key in keys:
            upper, lower = key.split('/')  # e.g. '0/1'
            with open(os.path.join(self.doc_dir, upper, lower + '.' + self.index_type), 'r', encoding='utf8') as f:
                self.docs.append(f.read().split())

    def build_tfidf(self, fname):
        if os.path.exists(os.path.join(self.output_dir, fname)):
            return corpora.MmCorpus(os.path.join(self.output_dir, fname))
        else:
            if os.path.exists(os.path.join(self.output_dir, fname.replace('tfidf', 'tfidf.model'))):
                tfidf = models.TfidfModel.load(os.path.join(self.output_dir, fname.replace('tfidf', 'tfidf.model')))
            else:
                bow_docs = []
                for doc in self.docs:
                    #print(doc)
                    #print(self.dict.doc2bow(doc))
                    bow_docs.append(self.dict.doc2bow(doc))
                #input()
                tfidf = models.TfidfModel(bow_docs)
                tfidf.save(os.path.join(self.output_dir, fname.replace('tfidf', 'tfidf.model')))
            tfidf_docs = tfidf[bow_docs]
            #for doc in tfidf_docs:
            #    print(doc)
            #input()
            corpora.MmCorpus.serialize(os.path.join(self.output_dir, fname), tfidf_docs)
            return tfidf_docs

    def build_index(self, id_from, id_to):
        print('loading doc')
        if self.index_to_key:  # corpus and dicts are built before
            self.load_doc_with_index()
        else:
            self.load_doc()
        print('building tfidf doc')
        tfidf_corpus = self.build_tfidf(self.index_type + '.corpus.tfidf')
        print('indexing')
        token2id = self.dict.token2id
        for doc_id in range(len(self.docs)):
            if doc_id < int(id_from) or doc_id > int(id_to):
                continue
            print(doc_id)
            # first pass for positions
            word_id_to_positions = {}
            for i in range(len(self.docs[doc_id])):
                token = self.docs[doc_id][i]
                word_id = str(token2id[token])
                pos = str(i)
                if word_id not in word_id_to_positions.keys():
                    word_id_to_positions[word_id] = [pos]
                else:
                    word_id_to_positions[word_id].append(pos)
            # second pass for index
            for token in self.docs[doc_id]:
                word_id = str(token2id[token])
                word_times = str(len(word_id_to_positions[word_id]))
                tfidf_score = -1
                for wid, score in tfidf_corpus[doc_id]:
                    if str(wid) == str(word_id):
                        tfidf_score = score
                        break
                assert tfidf_score > 0
                if word_id not in self.index.keys():
                    self.index[word_id] = {
                        'doc_length': 0,
                        'postings': [(
                            str(doc_id),
                            str(tfidf_score),
                            word_times,
                            word_id_to_positions[word_id]
                        )]
                    }
                else:
                    if str(self.index[word_id]['postings'][-1][0]) != str(doc_id):
                        self.index[word_id]['postings'].append((
                                str(doc_id),
                                str(tfidf_score),
                                word_times,
                                word_id_to_positions[word_id]
                        ))
        for wid in self.index.keys():
            self.index[wid]['doc_length'] = str(len(self.index[wid]['postings']))
        self.save_json(self.index, self.index_type + '.' + str(id_from) + '-' + str(id_to) + '.index.json')

    def merge_index(self, fnames):
        self.index = {}
        for fname in fnames:
            with open(os.path.join(self.output_dir, fname), 'r', encoding='utf8') as f:
                partial_index = json.load(f)
                for wid, data in partial_index.items()
                    # put wid into self.index
                    # merge doc_length and postings
        # update doc_length and sort postings in the end
            

if __name__ == '__main__':
    doc_id_from = sys.argv[1]
    doc_id_to = sys.argv[2]
    #indexer = Indexer(
    #    'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed',
    #    'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed\\index',
    #    'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw\\bookkeeping.json',
    #    'body')
    indexer = Indexer(
        '/home/junwel1/ir-proj3-data/webpages_parsed', 
        '/home/junwel1/ir-proj3-data/webpages_parsed/index', 
        '/home/junwel1/ir-proj3-data/WEBPAGES_RAW/bookkeeping.json',
        'body')
    indexer.build_index(doc_id_from, doc_id_to)
