#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.scenario import *
from FUTIL.my_logging import *
import socket

class group(object):
	"""A group of scenarios with a unique hotword
	"""
	max_distance = 5
	min_cosine = 0.4
	def __init__(self, 
					name, 
					hotword = "./resources/hotwords/snowboy.umdl", 
					mqtt_hotword_topic = None, 
					scenarios = [],
					always_actions = []):
		"""Initialisation
			- hotword			string containing path to a umdl or pmdl file as "Ok google" 
			- orders			list of order object
		"""
		self.name = name
		self.hotword = hotword
		# if isinstance(scenarios, list):
			# self.scenarios = scenarios
		# else:
			# self.scenarios = [scenarios]
		self.scenarios = {}
		self.installation = None
		self.mqtt_hotword_topic = mqtt_hotword_topic
		self.always_actions = always_actions
	
	@property
	def always_actions(self):
		return self._always_actions
	@always_actions.setter
	def always_actions(self, actions):
		if isinstance(actions, list):
			self._always_actions = actions
		else:
			self._always_actions = [actions]
	
	def init(self, installation):
		'''Initialise the group with installation datas
		'''
		self.installation = installation
		for scenario in self.scenarios.values():
			scenario.init(self)
		if self.mqtt_hotword_topic == None and installation.mqtt_base_topic :
			self.mqtt_hotword_topic = installation.mqtt_base_topic + self.name
		for action in self.always_actions:
			action.init(self.installation)
	
	def callback(self):
		""" Function called when the hotword match
		"""
		logging.info(self.name + " : I listen ...")
		if self.mqtt_hotword_topic:
			try:
				self.installation.mqtt_client.reconnect()
				self.installation.mqtt_client.publish(self.mqtt_hotword_topic, self.name)
			except socket.error:
				logging.error("Mqtt server : Connection refused")
				logging.error("Mqtt server : Connection refused")
		self.installation.on_action = True
		self.installation.detector.terminate()
		self.installation.show_message("^")
		self.installation.calibrate()
		self.installation.show_message("O")
		time.sleep(0.1)
		text = None
		try:
			with sr.Microphone() as source:
				audio = self.installation.reconizer.listen(source, self.installation.listen_timeout)
			logging.info("Audio captured")
			self.installation.show_message("@")
			#Google API
			try:
				text =  self.installation.reconizer.recognize_google(audio, key=self.installation.google_API_key, language = self.installation.language)
				logging.info("Text found with Google API: " + text)
			except sr.UnknownValueError:
				logging.warning("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
			#TODO : utiliser d'autres API
		except Exception as e:
			logging.warning("Audio capture error : %s"%(e.message))
		if text:
			self.run_always_actions(text)
			#Calculate the syntaxic distances
			#for scenario in self.scenarios.values():
			#	scenario.test(text)
			#Tri des résultats
			#results = sorted(self.scenarios.values(), key = lambda scenario:scenario.distance)
			#for i in range(min(5,len(results))):
			#	logging.debug("Distance à %s : %s"%(results[i].name, results[i].distance_syntaxique(text)))
			#if results[0].distance<self.max_distance:
			#	results[0].run(text)
			best_scenario = self.get_best_scenario(text)
			if best_scenario:
				self.scenarios[best_scenario].run(text)
			else:
				self.installation.show_message("?")
				logging.info("The text no math with scenarios.")
				time.sleep(0.5)
		else:
			self.installation.show_message("#")
			logging.info("None text captured.")
			time.sleep(0.5)
		self.installation.show_message(" ")
		
	def add_scenario(self,name, phrases = [], actions = [], min_cosine = 0.4, text = None):
		'''add or update a scenario
		'''
		if name in self.scenarios:
			self.scenarios[name].phrases = phrases
			self.scenarios[name].actions = actions
			self.scenario[name].min_cosine = min_cosine
			self.scenario[name].text = text
		else:
			self.scenarios[name] = scenario(name, phrases, actions, min_cosine, text)
	
	def allphrases(self):
		''' return a list of tuple : [(text,scenario_name),(..),...]
		'''
		phrases = []
		for index in self.scenarios:
			for text in self.scenarios[index].phrases:
				phrases.append((text, index))
		return phrases
	
	def run_always_actions(self, text):
		'''Run all the always_actions
		'''
		for action in self.always_actions:
			action.run(text)
		
	def get_best_scenario(self, text):
		''' return the name of the best scenario or False
		'''
		texts, scenario_names = zip(*self.allphrases())
		logging.debug(texts)
		logging.debug(scenario_names)
		try:
			cosines = self.installation.language_analyser.get_cosines(text, texts)
		except Exception as e:
			logging.warning("cortical error : %s"%(e.message))
		best_cosine = 0
		best_scenario = False
		for i in range(0,len(cosines)):
			if cosines[i]>self.scenarios[scenario_names[i]].min_cosine:
				if cosines[i]>best_cosine:
					best_scenario = scenario_names[i]
					best_cosine = cosines[i]
		logging.info("Best scénario found : %s with cosine=%s"%(best_scenario, best_cosine))
		return best_scenario