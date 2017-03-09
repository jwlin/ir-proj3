import json,sys

#inputValue = sys.argv[1]

data = [

    {'title' : 'title1',
    'link' : 'ics.uci.edu/111',
    'content' : 'content1'},

    {'title' : 'title2',
    'link' : 'ics.uci.edu/222',
    'content' : 'content2'},

    {'title' : 'title3',
    'link' : 'ics.uci.edu/333',
    'content' : 'content3'},

    {'title' : 'title4',
    'link' : 'ics.uci.edu/444',
    'content' : 'content4'},

    {'title' : 'title5',
    'link' : 'ics.uci.edu/555',
    'content' : 'content5'}
]

json_str = json.dumps(data)
print json_str