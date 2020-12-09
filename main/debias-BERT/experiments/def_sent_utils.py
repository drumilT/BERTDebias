# standard library
from itertools import combinations
import numpy as np
import os, sys
from collections import defaultdict
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

np.random.seed(42)

words2 = [["spokesman", "spokeswoman"],["catholic_priest", "nun"], ["dad", "mom"], ["councilman", "councilwoman"], ["grandpa", "grandma"], 
["grandsons", "granddaughters"], ["uncle", "aunt"], ["He","She"], ["His","Her"], 
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
from nltk.tag import pos_tag
from tqdm import tqdm
import re

def get_pom():
	pom_loc = os.path.join(DIRECTORY, 'POM/')
	all_sent=[]
	for file in os.listdir(pom_loc):
		if file.endswith(".txt"):
			f = open(os.path.join(pom_loc, file), 'r')
			data = f.read()
			for sent in data.split('.'):
				sent = sent.strip()
				all_sent.append(sent)
				
	return all_sent
def get_rest(filename):

	all_sent =[]	
	f = open(os.path.join(DIRECTORY, filename), 'r')
	data = f.read()
	for sent in data.split('\n'):
		sent = sent.strip()
		all_sent.append(sent)
	return all_sent
def get_sst():
	all_sent = []
	for sent in open(os.path.join(DIRECTORY,'sst.txt'), 'r'):
		try:
			sent = sent.split('\t')[1:]
			sent = ' '.join(sent)
		except:
			pass
		all_sent.append(sent.splitlines()[0])

	return all_sent

def gen_check(sent, count):
	mc = []
	fc = []
	words = sent.split()
	if len(words) > 30:
		return [],-1
	for i in range(len(words)):
		word = words[i]
		if word in male_words.keys():
			mc.append(i)
		elif word in fmale_words.keys():
			fc.append(i)
	if len([word for word,pos in pos_tag(words) if pos == 'NNP'])!=0:
		return ([],-1)
	if len(mc)*len(fc) ==0 and (len(mc)+len(fc))>=1 and (len(mc)+len(fc))<=count:
		return (fc,0) if len(fc)!=0 else (mc,1)
	return ([],-1)

def work_on(sents):
	triples =[]
	for i in tqdm(range(len(sents))):
		sent = sents[i]
		sent = re.sub(r'[^\w\s]', '', sent) 
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
	domains =  ["yelp_review_10mb", "sst", "wikitext", "pom", "meld","news_200" ] # "news_200"]
	print("Get data from {}".format(domains))
	all_data = dict({})
	all_data['all'] = {'m':[],'f':[],'idx':[]}
	for domain in domains:
		
		triples = get_single_domain(domain)
		
		for x,y,z in triples:
			if x not in all_data['all']['m']: 
				all_data['all']['m'].append(x)
				all_data['all']['f'].append(y)
				all_data['all']['idx'].append(z)
		print(len(all_data['all']['m']))

	return all_data


if __name__ == '__main__':
	data = get_all()
	with open("all_data.json","w") as f:
		json.dump(data,f)
	
