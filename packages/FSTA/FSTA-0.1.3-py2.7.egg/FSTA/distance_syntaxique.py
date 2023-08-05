#!/usr/bin/env python
# -*- coding:utf-8 -*

from nltk.tokenize import WordPunctTokenizer
tokenizer = WordPunctTokenizer()
from nltk.corpus import stopwords
french_stopwords = set(stopwords.words('french'))
french_stopwords.add(u"'")
from nltk.metrics import *
import itertools

#TODO : optimisation!!!

def text_to_vector(text):
	 tokens = tokenizer.tokenize(text)
	 tokens = [token for token in tokens if token.lower() not in french_stopwords]
	 return tokens

	 
def distance_syntaxique(text1, text2):
	v1 = text_to_vector(text1)
	v2 = text_to_vector(text2)
	#En attendant l'optimisation, on limite à 6 mots
	v1 = v1[0:6]
	v2 = v2[0:6]
	n = max(len(v1),len(v2))
	if len(v1)>len(v2):
		v1,v2 = v2,v1
	v1_1 = v1 + [None]*(n-len(v1))
	distance = 99
	for v1_2 in itertools.permutations(v1_1):#un peu boeuf : on permutte aussi les None avec les None
		#Distance entre les mots
		d_mot=0
		for i in range(n):
			try:
				d_mot += (6-min(6,edit_distance(v1_2[i],v2[i])))**2
			except:
				d_mot += 1 #si None
		d_mot = 6*(n**0.5)-d_mot**0.5
		#distance de la permuttation
		#Nb de Non insérés = nb de None pas au début ni à la fin
		v1_3 = []
		debut = True
		for m in v1_2:
			if m or not debut:
				debut = False
				v1_3.append(m)
		v1_4 = []
		debut = True
		for i in range(len(v1_3)-1,-1,-1):
			if v1_3[i] or not debut:
				debut = False
				v1_4.append(v1_3[i])
		d_perm = len(v1_4)-len(v1)
		#Les permutation de mot : 3 par permutation
		l=[]
		for m in list(filter(lambda x:x,v1_4)):
			l.append(v1.index(m))
		for i in range(len(l)-1):
			if l[i]<l[i+1]:
				d_perm +=3
		distance = min(distance, (d_mot**2+d_perm**2)**0.5)
	return distance


#print(distance(u'allume la lumière',u"Merci d'allumer la lumière s'il te plait"))

			
	
	
	
