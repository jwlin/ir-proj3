#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module docstring
"""

import os
import json
import util
import sys
from bs4 import BeautifulSoup
from tokenizer import Tokenizer


class Parser:
    def __init__(self, base_dir, output_dir, book_file):
        self.base_dir = base_dir
        self.output_dir = output_dir
        self.book_file = book_file

    def preprocess(self, key_from, key_to):
        '''
        Generate sanitized text files for each document. Ignore invalid files.
        For each document, the text files for Title, Anchor and Body are generated
        '''
        with open(os.path.join(self.base_dir, self.book_file), 'r', encoding='utf8') as f:
            book_data = json.load(f)
        for key, url in book_data.items():
            upper, lower = key.split('/')  # e.g. '0/1'
            if int(upper) > int(key_to) or int(upper) < int(key_from):
                continue
            if not util.is_valid(url) or os.path.exists(os.path.join(self.output_dir, upper, lower + '.body')):
                print(key, 'invalid')
                continue
            print('processing:', key)
            with open(os.path.join(self.base_dir, upper, lower), 'r', encoding='utf8') as f:
                soup = BeautifulSoup(f.read(), 'html5lib')
                if soup.title:
                    #print('-- title --')
                    tokens = Tokenizer.tokenize(soup.title.text)
                    #print(soup.title, tokens)
                    self.save_text(os.path.join(self.output_dir, upper, lower + '.title'), tokens)
                if soup.find_all('a'):
                    #print('-- a --')
                    link_data = Tokenizer.tokenize_link(url, soup.find_all('a'))
                    self.save_json(os.path.join(self.output_dir, upper, lower + '.link.json'), link_data)
                if soup.body:
                    #print('-- body --')
                    #print(soup.body)
                    txt = ' '.join([s for s in soup.body.stripped_strings])
                    #print(txt)
                    #print('---')
                    for script in soup.body.find_all('script'):
                        fragment = ' '.join([s for s in script.stripped_strings])
                        txt = txt.replace(fragment, '')
                    for style in soup.body.find_all('style'):
                        fragment = ' '.join([s for s in style.stripped_strings])
                        txt = txt.replace(fragment, '')
                    #print(txt)
                    tokens = Tokenizer.tokenize(txt)
                    #print('tokens:', tokens)
                    self.save_text(os.path.join(self.output_dir, upper, lower + '.body'), tokens)
            #input()

    def save_text(self, fname, t_list):
        with open(fname, 'w', encoding='utf8') as f:
            f.write(' '.join(t_list))

    def save_json(self, fname, data):
        with open(fname, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=True)

    def generate_anchor(self):
        with open(os.path.join(self.base_dir, self.book_file), 'r', encoding='utf8') as f:
            book_data = json.load(f)
        key_to_anchor = dict()
        for key in book_data.keys():
            key_to_anchor[key] = list()
        url_to_key = dict()
        for key, url in book_data.items():
            if url[-1] == '/':  # remove '/' in the end of url
                url = url[:-1]
            url_to_key[url] = key
        for key, url in book_data.items():
            print('processing', key)
            upper, lower = key.split('/')  # e.g. '0/1'
            if os.path.exists(os.path.join(self.output_dir, upper, lower + '.link.json')):
                with open(os.path.join(self.output_dir, upper, lower + '.link.json'), 'r') as f:
                    link_data = json.load(f)
                for link_url, link_text in link_data.items():
                    if link_url[-1] == '/':
                        link_url = link_url[:-1]
                    if link_url in url_to_key.keys():
                        key = url_to_key[link_url]
                        for token in link_text.split():
                            if token not in key_to_anchor[key]:
                                key_to_anchor[key].append(token)
        for key, url in book_data.items():
            if key in key_to_anchor.keys() and key_to_anchor[key]:
                print('generating anchor text for', key)
                upper, lower = key.split('/')  # e.g. '0/1'
                self.save_text(os.path.join(self.output_dir, upper, lower + '.anchor'), key_to_anchor[key])


if __name__ == '__main__':
    parser = Parser('C:\\Users\\Jun-Wei\\Desktop\\webpages_raw', 'C:\\Users\\Jun-Wei\\Desktop\\webpages_parsed_2', 'bookkeeping.json')
    #parser = Parser('/home/junwel1/ir-proj3-data/WEBPAGES_RAW', '/home/junwel1/ir-proj3-data/webpages_parsed_2', 'bookkeeping.json')
    #key_from = 0#sys.argv[1]
    #key_to = 74#sys.argv[2]
    #parser.preprocess(key_from, key_to)
    parser.generate_anchor()
