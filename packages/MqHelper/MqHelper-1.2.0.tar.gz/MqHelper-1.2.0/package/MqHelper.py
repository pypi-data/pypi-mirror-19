#!/usr/bin/python
# -*- coding: UTF-8 -*-

# support both old and new python package ( http://mosquitto.org/documentation/python/ )
try: from paho.mqtt.client import Client as Mosquitto
except ImportError: from mosquitto import Mosquitto

import logging
logger = logging.getLogger('MqHelper')

class MqHelper(object):

	def __init__(self, name=None, host=None, **kwargs):
		self.client = None
		self.pending = None
		self.host = host or '127.0.0.1'
		self.clientName = name or 'testClient'
		self.subscriptions = {}
		self.kwargs = kwargs

	def loop(self):
		if self.client == None:
			self.reconnect()
		ret = self.client.loop()
		if ret != 0:
			logger.info("mosquitto client error")
			try:
				self.client.disconnect()
			except:
				pass
			self.client = None

	def send(self, topic, msg):
		if self.client:
			ret = -1
			try:
				ret = self.client.publish(topic, msg, 1)
			except:
				logger.info("error sending msg")
			if ret == 0 or hasattr(ret, '__getitem__') and ret[0] == 0:
				# sending success
				self.pending = None
			else:
				logger.info("returned %s"%str(ret))
				logger.info("saving pending msg %s %s"%(topic, msg))
				self.pending = (topic, msg)
				self.reconnect()				
		else:
			logger.info("client not available, saving as pending")
			self.pending = (topic, msg)
			self.reconnect()

	def onConnect(self):
		def callback(mosq, obj, rc):
			if rc != 0:
				self.client = None
				logger.info("connecting failed")
			else:
				self.client.on_message = self.createMsgCallback()
				self.__subscribeAll()
				logger.info("connected")
				if self.pending:
					logger.info("sending pending message %s"%self.pending[1])
					self.send(self.pending[0], self.pending[1])
		return callback

	def __subscribeAll(self):
		for topic in self.subscriptions.keys():
			self.client.subscribe(topic, 0)

	def subscribe(self, topic, callback):
		self.subscriptions[topic] = callback
		if self.client != None:
			self.client.subscribe(topic, 0)

	def createMsgCallback(self):
		def callback(mosq, obj, msg):
			logger.info("received msg on %s"%msg.topic)
			if self.subscriptions.has_key(msg.topic):
				self.subscriptions[msg.topic](msg.topic, msg.payload)
		return callback

	def reconnect(self):
		logger.info("reconnecting...")
		try:
			self.client = Mosquitto(self.clientName, **self.kwargs)
			ret = self.client.connect(self.host)
			if ret == 0:
				self.client.on_connect = self.onConnect()
			else:
				self.client = None
		except:
			self.client = None
