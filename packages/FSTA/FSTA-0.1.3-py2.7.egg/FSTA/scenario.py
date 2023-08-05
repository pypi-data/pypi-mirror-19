#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.group import *
from FUTIL.my_logging import *
from FSTA.distance_syntaxique import *
import threading


class scenario(object):
	"""Scenario if * or * or ... then ...
	"""
	def __init__(self, name = "", phrases = [], actions = [], min_cosine = 0.4, text = None):
		"""Initialisation
			- name			explain the action (for logging)
			- phrases		list of unicode text
			- actions		list of actions obtect
			- text			text to show on leds
		"""
		self.phrases = phrases
		self.actions = actions
		self.name = name
		self.valide = False
		self.installation = None
		self.min_cosine = min_cosine
		self._text = text
	
	@property
	def phrases(self):
		return self._phrases
	@phrases.setter
	def phrases(self, phrases):
		if isinstance(phrases, list):
			self._phrases = phrases
		else:
			self._phrases = [phrases]
	
	@property
	def actions(self):
		return self._actions
	@actions.setter
	def actions(self, actions):
		if isinstance(actions, list):
			self._actions = actions
		else:
			self._actions = [actions]
	@property
	def text(self):
		if self._text:
			return self._text
		else:
			return self.name
	@text.setter
	def text(self, text):
		self._text = text
	
	def run(self, text):
		"""Function called if phrases match
		- text		phrase dicted
		"""
		logging.debug("Running scenario : %s"%(self.name))
		self.installation.show_message(text)
		for action in self.actions:
			action.run(text)
	
	def init(self, group):
		""" Initialisation of the order with the installation datas
		"""
		self.installation = group.installation
		for action in self.actions:
			action.init(group.installation)		
	
	def test(self, text):
		""" calculate self.distance, the smaller syntaxic distance between text and phrases
		"""	
		self.distance = 99
		try:
			for phrase in self.phrases:
				distance = self.installation.language_analyser.distance(text,phrase.lower())
				self.distance = min(self.distance, distance)
				logging.debug("%s : %s"%(phrase,distance))
		except Exception as e:
			logging.error("Error on test for scenario %s : %s"%(self.name,e)) 