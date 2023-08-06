#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc

import sh

from .AbstractLogger import *





#
# This logger will broadcast log messages to additional loggers.
#
class NamedMulticastLogger(AbstractLogger):



	def __init__(self, loggerMap = None):
		if loggerMap is not None:
			assert isinstance(loggerMap, dict)
			self.__loggerMap = loggerMap
		else:
			self.__loggerMap = {}



	def addLogger(self, loggerName, logger):
		assert isinstance(loggerName, str)
		assert isinstance(logger, AbstractLogger)
		if self.__loggerMap.get(loggerName, None) is not None:
			del self.__loggerMap[loggerName]
		self.__loggerMap[loggerName] = logger



	def removeLogger(self, loggerName):
		assert isinstance(loggerName, str)
		if self.__loggerMap.get(loggerName, None) is not None:
			del self.__loggerMap[loggerName]



	def _log(self, timeStamp, logLevel, textOrException):
		for logger in self.__loggerMap.values():
			logger._log(timeStamp, logLevel, textOrException)



	def descend(self, text):
		newMap = {}
		for loggerName in self.__loggerMap:
			logger = self.__loggerMap[loggerName]
			newMap[loggerName] = logger.descend(text)
		return NamedMulticastLogger(newMap)



	def clear(self):
		for logger in self.__loggerMap.values():
			logger.clear()






