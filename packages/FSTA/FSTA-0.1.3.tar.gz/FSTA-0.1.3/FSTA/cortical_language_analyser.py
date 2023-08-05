#!/usr/bin/env python
# -*- coding:utf-8 -*

import retinasdk
import json

from FSTA.language_analyser import *
from FUTIL.my_logging import *


class cortical_language_analyser(language_analyser):
	''' A syntaxic analyser based on Cortical.io's Retina API
	'''
	def __init__(self, api_key, api_server = "http://languages.cortical.io/rest", language = "fr_general"):
		'''Initialisation
			api_key		:	retina api key
			api_server	:	ex : "http://api.cortical.io/rest" or "http://languages.cortical.io/rest" or ...
			language	:	see self.fullClient.getRetinas()
		'''
		self.fullClient = retinasdk.FullClient(api_key, apiServer=api_server, retinaName= language)
	
	def getFingerprint(self,text):
		''' Get the Fingerprint of a list of texts
		'''
		return self.fullClient.getFingerprintsForTexts(json.dumps([{"text": text}]))
	
	def getFingerprints(self,texts):
		''' Get the Fingerprint of a text
		'''
		return self.fullClient.getFingerprintForText(texts)
		
	def compare(self, text1,text2):
		''' Compare two text ;
			0	:	low semantic similarity
			0.5	:	medium semantic similarity
			1	:	high semantic similarity
		'''
		return self.fullClient.compare(json.dumps([{"text": text1}, {"text":text2}])).cosineSimilarity

	def compare_texts(self, text, texts):
		'''Compare a text with a list of texts and return a tuple 
			(the index,  the cosine similarity) of the neerer text
			OBSOLETE
		'''
		list = []
		for t in texts:
			list.append([{"text":text},{"text":t}])
		cosines = [i.cosineSimilarity for i in self.fullClient.compareBulk(json.dumps(list))]
		logging.debug(cosines)
		max_cosine = max(cosines)
		max_index = [i for i, j in enumerate(cosines) if j == max_cosine][0]
		return (max_index, max_cosine)
	
	def get_cosines(self, text, texts):
		'''Compare a text with a list of texts and return the list a cosineSimilarity
		'''
		list = []
		for t in texts:
			list.append([{"text":text},{"text":t}])
		cosines = [i.cosineSimilarity for i in self.fullClient.compareBulk(json.dumps(list))]
		logging.debug(cosines)
		return cosines