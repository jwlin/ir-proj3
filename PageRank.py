import json
import operator
from collections import defaultdict

Hash_inversebook = {}
Hash_incominglink = {}
Hash_reputation = {}
Hash_PageRank = {}

"""
Create a hash table (Hash_incominglink) to map each URL with its incoming links
Create another hash table (Hash_reputation) to record each URL with its reputation score and number of outgoing link
"""
with open("C:/Users/Ken/Desktop/UCI Courses/CS 221 Information Retrieval/Project 3/bookkeeping.json") as bookkeeping:
	Hash_bookkeeping = json.load(bookkeeping)
	for item in Hash_bookkeeping: 
		Hash_inversebook[Hash_bookkeeping[item]] = item
		file_path = "C:/Users/Ken/Desktop/UCI Courses/CS 221 Information Retrieval/Project 3/webpages_parsed/" + item + ".link.json"
		try:
			with open(file_path) as file_link:
				data = json.load(file_link)
				for outlink in data:
					if outlink in Hash_incominglink:
						Hash_incominglink[outlink].append(Hash_bookkeeping[item])
					else:
						Hash_incominglink[outlink] = [Hash_bookkeeping[item]]
			Hash_reputation[Hash_bookkeeping[item]] = [len(data.keys()), 0.0]
		except:
			continue

iter = 1
max_score = 0
while iter <= 20:
	for item in Hash_reputation:
		if item in Hash_incominglink:
			score = 0
			for i in range(0,len(Hash_incominglink[item])):
				PR, C = Hash_reputation[Hash_incominglink[item][i]][iter], Hash_reputation[Hash_incominglink[item][i]][0]
				score += PR/C
			score = 1-0.85+0.85*score
			if iter == 20 and score > max_score:
				max_score = score
			Hash_reputation[item].append(score)
		else:
			Hash_reputation[item].append(0.15)
	iter += 1
	
for item in Hash_reputation:
	Hash_PageRank[Hash_inversebook[item]] = Hash_reputation[item][-1]/max_score
	
with open("C:/Users/Ken/Desktop/UCI Courses/CS 221 Information Retrieval/Project 3/webpages_parsed/PageRank.json", "w") as PageRank:
	json.dump(Hash_PageRank, PageRank)

sorted_PageRank = sorted(Hash_PageRank.items(), key = operator.itemgetter(1), reverse = True)
with open("C:/Users/Ken/Desktop/UCI Courses/CS 221 Information Retrieval/Project 3/webpages_parsed/sorted_PageRank.txt", "w") as PageRank:
	for i in range(0,len(sorted_PageRank)):
		PageRank.write(str(sorted_PageRank[i]) + "\n")