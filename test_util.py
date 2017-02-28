#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from util import merge_path, remove_trailing_junk, is_repeated_path, merge_href


class TestUtil(unittest.TestCase):
    @unittest.skip('skip')
    def test_merge_path(self):
        self.assertEqual('/about/annualreport/index.php', merge_path('/a/b/', '../../../about/annualreport/index.php'))
        self.assertEqual('/about/annualreport/index.php', merge_path('/', '../../../about/annualreport/index.php'))
        self.assertEqual('/about/annualreport/index.php', merge_path('/a/', '../about/annualreport/index.php'))
        self.assertEqual('/annualreport/index.php', merge_path('/', '../about/../../annualreport/index.php'))
        self.assertEqual('/annualreport/index.php', merge_path('/', 'about/../annualreport/index.php'))
        self.assertEqual('/a/about/annualreport/index.php', merge_path('/a/b/', '../about/annualreport/index.php'))

    @unittest.skip('skip')
    def test_remove_trailing_junk(self):
        self.assertEqual(
            'http://www.ics.uci.edu?p=2&c=igb-misc',
            remove_trailing_junk('http://www.ics.uci.edu?p=2&c=igb-misc/degrees/index/'))
        self.assertEqual(
            'http://www.ics.uci.edu/computing/linux/shell.php',
            remove_trailing_junk('http://www.ics.uci.edu/computing/linux/shell.php/computing/account/'))
        self.assertEqual(
            'http://www.ics.uci.edu/about/search/index.php',
            remove_trailing_junk('http://www.ics.uci.edu/about/search/index.php/about_safety.php/grad/index.php/search_payroll.php/search_graduate.php/search_sao.php/search_dean.php/search_dept_in4matx.php/search_business.php/search_dept_stats.php/search_support.php/search_facilities.php/search_payroll.php/ugrad/index.php/search_graduate.php/about_deanmsg.php/search_dean.php/ICS/ics/about/bren/index.php/about_contact.php/search_dept_stats.php/index.php/bren/index.php/ICS/ICS/search_dept_stats.php/search_business.php/search_external.php/ugrad/search_dept_cs.php/search_sao.php/search_dean.php/../about_safety.php/../about_meet_the_dean.php/../../grad/index.php'))
        self.assertEqual(
            'http://www.ics.uci.edu/about/visit/../bren/bren_advance.php',
            remove_trailing_junk('http://www.ics.uci.edu/about/visit/../bren/bren_advance.php'))
        self.assertEqual(remove_trailing_junk('http://www.ics.uci.edu/~pfbaldi?baldiPage=296'), 'http://www.ics.uci.edu/~pfbaldi?baldiPage=296')

    @unittest.skip('skip')
    def test_is_repeated_path(self):
        invalid_urls = [
            'http://www.ics.uci.edu/alumni/hall_of_fame/stayconnected/hall_of_fame/hall_of_fame/stayconnected/hall_of_fame/hall_of_fame/inductees.aspx.php',
            'http://www.ics.uci.edu/~mlearn/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/datasets/Abalone',
            'http://www.ics.uci.edu/alumni/hall_of_fame/stayconnected/stayconnected/stayconnected/hall_of_fame/stayconnected/stayconnected/hall_of_fame/index.php'
        ]
        for u in invalid_urls:
            self.assertTrue(is_repeated_path(u))
        valid_urls = [
            'http://www.ics.uci.edu/~pazzani/Publications/OldPublications.html',
            'http://www.ics.uci.edu/~theory/269/970103.html',
            'http://www.ics.uci.edu/~mlearn/datasets/datasets/CMU+Face+Images',
            'http://alderis.ics.uci.edu/files/AMBA_AHB_Functional_Verification_2Masters_Correct.out',
            'http://www.ics.uci.edu/~sharad',
            'http://www.ics.uci.edu/~sharad/students.html',
            'http://mhcid.ics.uci.edu',
            'http://www.ics.uci.edu/about/brenhall/index.php',
            'http://www.ics.uci.edu/~goodrich/pubs',
            'http://www.ics.uci.edu/alumni/stayconnected/hall_of_fame/inductees.aspx.php'
        ]
        for u in valid_urls:
            self.assertFalse(is_repeated_path(u))

    def test_bs4(self):
        from bs4 import BeautifulSoup
        import os
        from util import is_valid
        from tokenizer import Tokenizer
        import json

        base_path = 'C:\\Users\\Jun-Wei\\Desktop\\webpages_raw'
        book_file = 'bookkeeping.json'
        upper, lower = '20', '289'
        with open(os.path.join(base_path, book_file), 'r', encoding='utf8') as f:
            book_data = json.load(f)
        url = book_data[upper+'/'+lower]
        print(url)
        if not is_valid(url):
            print('invalid')
        else:
            with open(os.path.join(base_path, upper, lower), 'r', encoding='utf8') as f:
                soup = BeautifulSoup(f.read(), 'html5lib')
                #if soup.title:
                #    print('Title', soup.find('title').text)
                if soup.find_all('a'):
                    token_data = Tokenizer.tokenize_link(url, soup.find_all('a'))
                '''
                if soup.body:
                    print(soup.body)
                    print([s for s in soup.body.stripped_strings])
                    txt = ' '.join([s for s in soup.body.stripped_strings])
                    print(txt)
                    print('---')
                    for script in soup.body.find_all('script'):
                        fragment = ' '.join([s for s in script.stripped_strings])
                        txt = txt.replace(fragment, '')
                    for script in soup.body.find_all('style'):
                        fragment = ' '.join([s for s in script.stripped_strings])
                        txt = txt.replace(fragment, '')
                    print(txt)
                    print(Tokenizer.tokenize(txt))
                '''


if __name__ == '__main__':
    unittest.main()