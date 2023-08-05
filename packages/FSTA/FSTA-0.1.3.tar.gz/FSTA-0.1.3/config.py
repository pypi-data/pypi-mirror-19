#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.cortical_language_analyser import *

def get_installation():
	return installation(
		mqtt_host='192.168.10.155',
		led = led.matrix(),
		google_API_key = "AIzaSyDtizHAgEhUw5WjW9aRs84GUNk7o-fXwvA",
		mqtt_base_topic = 'T-HOME/SALON/LISTEN',
		language_analyser = cortical_language_analyser("84c53140-cdb1-11e6-a057-97f4c970893c")
		)