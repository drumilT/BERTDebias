# standard library
from itertools import combinations
import numpy as np
import os, sys
from collections import defaultdict
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

np.random.seed(42)

words2 = [["spokesman", "spokeswoman"],["catholic_priest", "nun"], ["dad", "mom"], ["men", "women"], ["councilman", "councilwoman"], ["grandpa", "grandma"], 
["grandsons", "granddaughters"], ["uncle", "aunt"], 
["wives", "husbands"], ["father", "mother"], ["grandpa", "grandma"], ["he", "she"], ["boy", "girl"], ["boys", "girls"], 
["brother", "sister"], ["brothers", "sisters"], ["businessman", "businesswoman"], ["chairman", "chairwoman"],
["congressman", "congresswoman"], ["dad", "mom"], ["dads", "moms"], ["dudes", "gals"], ["ex_girlfriend", "ex_boyfriend"], 
["fatherhood", "motherhood"], ["fathers", "mothers"], ["fraternity", "sorority"], ["gentleman", "lady"], 
["gentlemen", "ladies"], ["grandfather", "grandmother"], ["grandson", "granddaughter"], ["he", "she"], ["himself", "herself"], ["his", "her"], ["king", "queen"],
["kings", "queens"], ["male", "female"], ["males", "females"], ["man", "woman"], ["men", "women"], ["nephew", "niece"], ["prince", "princess"],
["schoolboy", "schoolgirl"], ["son", "daughter"], ["sons", "daughters"], ["twin_brother", "twin_sister"]]

male_words = {x[0]:x[1] for x in words2}
fmale_words ={x[1]:x[0] for x in words2}
words3 = [
    ["jewish", "christian", "muslim"],
    ["jews", "christians", "muslims"],
    ["torah", "bible", "quran"],
    ["synagogue", "church", "mosque"],
    ["rabbi", "priest", "imam"],
    ["judaism", "christianity", "islam"],
]

DIRECTORY = '../text_corpus/'

GENDER = 0
RACE = 1

def get_pom():
	pom_loc = os.path.join(DIRECTORY, 'POM/')
	all_sent=[]
	for file in os.listdir(pom_loc):
		if file.endswith(".txt"):
			f = open(os.path.join(pom_loc, file), 'r')
			data = f.read()
			for sent in data.lower().split('.'):
				sent = sent.strip()
				all_sent.append(sent.lower())
				
	return all_sent
def get_rest(filename):

	all_sent =[]	
	f = open(os.path.join(DIRECTORY, filename), 'r')
	data = f.read()
	for sent in data.lower().split('\n'):
		sent = sent.strip()
		all_sent.append(sent.lower())
	return all_sent
def get_sst():
	all_sent = []
	for sent in open(os.path.join(DIRECTORY,'sst.txt'), 'r'):
		try:
			sent = sent.split('\t')[1:]
			sent = ' '.join(sent)
		except:
			pass
		all_sent.append(sent.lower())

	return all_sent

def gen_check(sent, count):
	mc = []
	fc = []
	words = sent.split()
	for i in range(len(words)):
		word = words[i]
		if word in male_words.keys():
			mc.append(i)
		elif word in fmale_words.keys():
			fc.append(i)
	if len(mc)*len(fc) ==0 and (len(mc)+len(fc))==count:
		return (fc,0) if len(fc)!=0 else (mc,1)
	return ([],-1)

def work_on(sents):
	triples =[]
	for sent in sents:
		pos,gen = gen_check(sent,1)
		if gen==-1:
			continue
		sent_list = sent.split()
		for i in pos:
			sent_list[i] = fmale_words[sent_list[i]] if gen ==0 else male_words[sent_list[i]]
		new_sent = " ".join(sent_list)
		if gen ==0:
			triples.append((new_sent,sent,pos))
		else:
			triples.append((sent,new_sent,pos))
	return triples


# domain: news, reddit, sst, pom, wikitext
def get_single_domain(domain):
	if (domain == "pom"):
		sents = get_pom()
	elif (domain == "sst"):
		sents = get_sst()
	else:
		sents = get_rest("{}.txt".format(domain))
	gender= work_on(sents)
	return gender

def get_all():
	domains = ["reddit", "sst", "wikitext", "pom", "meld", "news_200"] #, "yelp_review_10mb"] # "news_200"]
	print("Get data from {}".format(domains))
	all_data = dict({})
	for domain in domains:
		all_data[domain] = {'m':[],'f':[],'idx':[]}
		triples = get_single_domain(domain)
		for x,y,z in triples:
			all_data[domain]['m'].append(x)
			all_data[domain]['f'].append(y)
			all_data[domain]['idx'].append(z)
	return all_data


if __name__ == '__main__':
	data = get_all()
	with open("all_data.json","w") as f:
		json.dump(data,f)
	
