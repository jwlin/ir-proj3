#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import re
from urllib.parse import urlparse, parse_qs
from shutil import copyfile
from collections import Counter


def remove_trailing_junk(url):
    # remove trailing string after parameters
    # e.g. http://www.ics.uci.edu?p=2&c=igb-misc/degrees/index/... ->  http://www.ics.uci.edu?p=2&c=igb-misc
    # http://www.ics.uci.edu/computing/linux/shell.php/computing/account/ ->  http://www.ics.uci.edu/computing/linux/shell.php
    sub_names = ['?', '.htm', '.html', '.php', '.jsp']
    for sub_name in sub_names:
        if sub_name in url and '/' in url[url.index(sub_name):]:
            return url[:
                url.index(sub_name) +
                url[url.index(sub_name):].index('/')
            ]
    return url


def merge_path(parent_path, href):
    parent_dirs = [d for d in parent_path.split('/') if d]
    children_dirs = [c for c in href.split('/') if c]
    total_dirs = parent_dirs + children_dirs
    parsed_dirs = []
    for d in total_dirs:
        if d == '..' and parsed_dirs:
            parsed_dirs = parsed_dirs[:-1]
        elif d != '..':
            parsed_dirs.append(d)
    return '/' + '/'.join(parsed_dirs)


def is_repeated_path(url):
    # detect invalid urls like:
    # http://www.ics.uci.edu/~mlearn/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/Abalone
    # http://www.ics.uci.edu/alumni/hall_of_fame/stayconnected/stayconnected/stayconnected/hall_of_fame/stayconnected/stayconnected/hall_of_fame/index.php
    return max(Counter(urlparse(url).path.split('/')).values()) > 3


def is_valid(url):
    try:
        if re.match(".*\.(css|js|bmp|gif|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ppsx" \
                            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                            + "|thmx|mso|arff|rtf|jar|csv|txt|py|lif|h5|ply|bed|flv" \
                            + "|rm|smil|wmv|swf|wma|zip|rar|gz|txt|java|c|cc|cpp|m|out|edelsbrunner)$", url.lower()):
            return False
    except TypeError:
        print("TypeError for ", url)

    '''
    if is_repeated_path(url):
        return False

    if url != remove_trailing_junk(url):
        return False
    '''
    return True


def merge_href(orig_url, href):
    #print('orig_url:', orig_url)
    parsed = urlparse(orig_url)
    #print('parsed', parsed)

    # path: 'abc.ics.uci.edu/b/c.html' -> '/b/'
    path = parsed.path.split('/')[:-1][1:]
    path = '/' + '/'.join(path) + '/'
    assert not parsed.hostname
    url_prefix = parsed.path.split('/')[0]

    if '#' in href:
        href = re.sub(r'#.*', '', href)
    if href.startswith('./'):
        href = href[2:]
    if href.startswith('mailto') or not href:
        return None
    elif href.startswith('/'):
        return url_prefix + href
    elif href.startswith('http'):
        return re.sub('^https?://', '', href)
    elif '../' in href:
        return url_prefix + merge_path(path, href)
    else:
        return url_prefix + path + href

'''
def is_not_trap(url, trapCheckTable={}):
    value = set(parse_qs(urlparse(url).query))
    key = urlparse(url).hostname + urlparse(url).path
    if len(value) < 2 or 'id' in value:
        return True

    # check the incoming url with the url hash table. If there are more than 5 urls having exactly the same queries with the incoming url,
    # the incoming url will be identified as a trap and therefore return False.
    if key in trapCheckTable and len(trapCheckTable[key]) >= 5:
        count = 0
        for item in trapCheckTable[key]:
            if value == item:
                count += 1
                if count >= 5:
                    return False
        trapCheckTable[key].append(value)
    elif key in trapCheckTable and len(trapCheckTable[key]) < 5:
        trapCheckTable[key].append(value)
    else:
        trapCheckTable[key] = [value]
    if trapCheckTable:
        print 'trapCheckTable inside', trapCheckTable
    return True
'''
