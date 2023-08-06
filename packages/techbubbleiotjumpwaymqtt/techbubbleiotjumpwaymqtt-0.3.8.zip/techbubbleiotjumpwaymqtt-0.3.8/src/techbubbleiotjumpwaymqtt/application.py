# *****************************************************************************
# Copyright (c) 2016 TechBubble Technologies and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html 
#
# Contributors:
#   Adam Milton-Barker - TechBubble Technologies Limited
#   Irene Naya  - TechBubble Technologies Limited
# *****************************************************************************

import inspect
import json
import os
import paho.mqtt.client as mqtt
import sys
import time

class JumpWayPythonMQTTApplicationConnection():
	
	def __init__(self, configs):	
		self._configs = configs
		self.mqttClient = None
		self.mqttTLS =  os.path.dirname(os.path.abspath(__file__)) + "/ca.pem"
		self.mqttHost = 'iot.techbubbletechnologies.com'
		self.mqttPort = 8883	
		self.applicationStatusCallback = None
		self.deviceStatusCallback = None	
		self.deviceSensorCallback = None
		self.deviceCommandsCallback = None
		if self._configs['locationID'] == None:
			raise ConfigurationException("locationID property is required")
		elif self._configs['applicationID'] == None:
			raise ConfigurationException("applicationID property is required")
		elif self._configs['applicationName'] == None:
			raise ConfigurationException("applicationName property is required")
		elif self._configs['username'] == None: 
			raise ConfigurationException("username property is required")
		elif self._configs['password'] == None: 
			raise ConfigurationException("password property is required")
	
	
	def connectToApplication(self):
		self.mqttClient = mqtt.Client(client_id=self._configs['applicationName'], clean_session=True)
		applicationStatusTopic = '%s/Applications/%s/Status' % (self._configs['locationID'], self._configs['applicationID'])
		self.mqttClient.will_set(applicationStatusTopic, "OFFLINE", 0, False)
		self.mqttClient.tls_set(self.mqttTLS, certfile=None, keyfile=None)
		self.mqttClient.on_connect = self.on_connect
		self.mqttClient.on_message = self.on_message
		self.mqttClient.on_publish = self.on_publish
		self.mqttClient.on_subscribe = self.on_subscribe
		self.mqttClient.username_pw_set(str(self._configs['username']),str(self._configs['password']))
		self.mqttClient.connect(self.mqttHost,self.mqttPort,10)
		self.mqttClient.loop_start()

	def on_connect(self, client, obj, flags, rc):
			self.publishToApplicationStatus("ONLINE")
			print("rc: "+str(rc))

	def on_subscribe(self, client, obj, mid, granted_qos):
			print("Subscribed: "+str(obj))

	def on_message(self, client, obj, msg):
		splitTopic=msg.topic.split("/")
		if splitTopic[1]=='Applications':
			if splitTopic[2]=='Status':
				if self.applicationStatusCallback == None:
					print("No applicationStatusCallback set")
				else:
					self.applicationStatusCallback(msg.topic,msg.payload)
		elif splitTopic[1]=='Devices':
			if splitTopic[4]=='Status':
				if self.deviceStatusCallback == None:
					print("No deviceStatusCallback set")
				else:
					self.deviceStatusCallback(msg.topic,msg.payload)
			elif splitTopic[4]=='Sensors':
				if self.deviceSensorCallback == None:
					print("No deviceSensorCallback set")
				else:
					self.deviceSensorCallback(msg.topic,msg.payload)
			elif splitTopic[4]=='Actuators':
				if self.deviceActuatorCallback == None:
					print("No deviceActuatorCallback set")
				else:
					self.deviceActuatorCallback(msg.topic,msg.payload)
			elif splitTopic[4]=='Commands':
				if self.deviceCommandsCallback == None:
					print("No deviceCommandsCallback set")
				else:
					self.deviceCommandsCallback(msg.topic,msg.payload)
			elif splitTopic[4]=='Warnings':
				if self.deviceWarningsCallback == None:
					print("No deviceWarningsCallback set")
				else:
					self.deviceWarningsCallback(msg.topic,msg.payload)
	
	def subscribeToApplicationChannel(self, channel, qos=0):
		if self._configs['locationID'] == None:
			print("locationID is required!")
			return False
		elif self._configs['applicationID'] == None:
			print("applicationID is required!")
			return False
		else:
			applicationChannel = '%s/Applications/%s/%s' % (self._configs['locationID'], applicationID, channel)
			self.mqttClient.subscribe(applicationChannel, qos=qos)
			print("Subscribed to Application "+channel+" Channel")
			return True
	
	def subscribeToDeviceChannel(self, channel, zone, device, qos=0):
		if self._configs['locationID'] == None:
			print("locationID is required!")
			return False
		elif zone == None:
			print("zoneID is required!")
			return False
		elif device == None:
			print("deviceId is required!")
			return False
		else:
			deviceChannel = '%s/Devices/%s/%s/%s' % (self._configs['locationID'], zone, device, channel)
			self.mqttClient.subscribe(deviceChannel, qos=qos)
			print("Subscribed to Device "+channel+" Channel")
			return True
	
	def publishToApplicationStatus(self, data):
		if self._configs['locationID'] == None:
			print("locationName is required!")
			return False
		elif self._configs['applicationID'] == None:
			print("applicationID is required!")
			return False
		else:
			deviceStatusTopic = '%s/Applications/%s/Status' % (self._configs['locationID'], self._configs['applicationID'])
			self.mqttClient.publish(deviceStatusTopic,data)
			print("Published to Application Status "+deviceStatusTopic)
	
	def publishToDeviceChannel(self, channel, data):
		if self._configs['locationID'] == None:
			print("locationID is required!")
			return False
		elif self._configs['zoneID'] == None:
			print("zoneID is required!")
			return False
		elif self._configs['deviceId'] == None:
			print("deviceId is required!")
			return False
		else:
			deviceChannel = '%s/Devices/%s/%s/%s' % (self._configs['locationID'], self._configs['zoneID'], self._configs['deviceId'], channel)
			self.mqttClient.publish(deviceChannel,json.dumps(data))
			print("Published to Device "+channel+" Channel")

	def on_publish(self, client, obj, mid):
			print("Published: "+str(mid))

	def on_log(self, client, obj, level, string):
			print(string)
	
	def disconnectFromApplication(self):
		self.publishToApplicationStatus("OFFLINE")
		self.mqttClient.disconnect()	
		self.mqttClient.loop_stop()
	
			
