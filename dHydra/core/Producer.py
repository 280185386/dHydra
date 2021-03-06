# -*- coding: utf8 -*-
"""
Producer类（生产者类，负责把数据推送进消息队列）
所有producer需要继承这个类
Created on 03/27/2016
@author: Wen Gu
@contact: emptyset110@gmail.com
"""
import multiprocessing
from dHydra.app import PRODUCER_NAME, PRODUCER_HASH
import time
from abc import ABCMeta
import threading

class Producer(threading.Thread):
	__metaclass__ = ABCMeta
	def __init__(self, name, **kwargs):
		super().__init__()
		self._name = name
		self._subscriber = set()
		self._active = False
		self._running = False

	def _activate(self):
		self._active = True

	def _deactivate(self):
		self._active = False
		print(self._name,self._active)

	def run(self):
		print('[开启生产者]\t', self._name)
		self._running = True
		while self._running:
			self.handler()
			time.sleep(0.5)
		self._end()

	def is_active(self):
		return self._active

	def is_running(self):
		return self._running

	def handler(self):
		pass

	def _end(self):
		print("[Producer结束]", self._name)
		pass

	# 添加订阅者
	def _add_subscriber(self, queue):
		self._subscriber.add(queue)
		self._activate()

	# 删除订阅者
	def _remove_subscriber(self, queue):
		self._subscriber.remove(queue)
		if ( len(self._subscriber) == 0 ):
			print("暂停Producer", self._name)
			self._deactivate()