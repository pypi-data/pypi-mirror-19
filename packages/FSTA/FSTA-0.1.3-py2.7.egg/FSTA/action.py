#!/usr/bin/env python
# -*- coding:utf-8 -*
from FSTA.installation import *
from FSTA.group import *
from FSTA.scenario import *
from FUTIL.my_logging import *
import socket
import random

class action(object):
	"""action to be execute
	"""
	def __init__(self, callback = None, text = None):
		"""Initialisation
			- callback		function to be called
		"""
		self.callback = callback
		self._text = text
	
	def init(self, installation):
		''' Initialise the installation property
		'''
		self.installation = installation
	
	@property
	def text(self):
		if self._text:
			return self._text
		else:
			return "* "
	
	def run(self, text):
		"""Run the callback fonction
		- text		phrase dicted
		"""
		try:
			self.callback()
		except BaseException as e:
			logging.error("Error on %s callback: %s"%(self.text, e))
		
		
class action_mqtt(action):
	""" mqtt order
	"""
	def __init__(self, topic, payload = None, qos = 0, retain = False, text = None):
		"""Initialisation
			- topic			mqtt topic
			- payload		mqtt payload
			- qos			mqtt qos
			- retain		mqtt retain
		"""
		self.topic = topic
		self.payload = payload
		self.qos = qos
		self.retain = retain
		self.installation = None
		self._text = text
	
	
	def run(self, text):
		""" Send  a mqtt msg
			- text		phrase dicted (send in payload miss)
		"""
		logging.info("Running action : " + self.text)
		try:
			self.installation.mqtt_client.reconnect()
			self.installation.mqtt_client.publish(self.topic, self.payload or text, self.qos, self.retain)
		except socket.error:
			logging.error("Mqtt server : Connection refused")
			self.installation.show_message("X")
	
class action_mqtt_random(action_mqtt):
	'''mqtt order with random payload 
	'''
	def run(self, text):
		'''Send a mqtt msg with a random payload
		'''
		logging.info("Running random mqtt action : " + self.text)
		try:
			self.installation.mqtt_client.reconnect()
			self.installation.mqtt_client.publish(self.topic, random.choice(self.payload), self.qos, self.retain)
			self.installation.show_message(" ")
			self.installation.show_message(self.text)
		except Exception as e:
			logging.error("Error on running actio_mqtt_random : %s"%(e))
			self.installation.show_message(self.text | "X")
	
	
class random_action(action):
	'''Run randomize action
	'''
	def __init__(self, actions):
		'''Initialisation
			actions			:	list of actions
		'''
		self.actions = actions
	
	def init(self, installation):
		''' Initialise the installation property
		'''
		for action in self.actions:
			action.installation = installation
	
	def run(self, text):
		''' Run a action in actions
		'''
		random.choice(self.actions).run(text)