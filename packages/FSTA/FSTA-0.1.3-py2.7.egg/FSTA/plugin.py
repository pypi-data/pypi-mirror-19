#!/usr/bin/env python
# -*- coding:utf-8 -*

import time
import logging

class plugin(object):
	'''Plugin for FSTA
	'''
	def __init__(self, file_name):
		'''Initialisation
			- file_name
			- modified_date
		'''
		self.file_name = file_name
		self.loaded_date = time.time()
	
	def load(self, maison):
		'''Load the plugin with 'maison' as installation name
		'''
		logging.info("Load the plugin %s ..."%(self.file_name))
		try:
			execfile(maison.plugin_path+'/'+self.file_name,globals(),locals())
			logging.info("	plugin loaded.")
		except Exception as e:
			logging.error("	Error on plugin %s : %s"%(self.file_name, e))