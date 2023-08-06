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
class MulticastLogger(AbstractLogger):



	def __init__(self, loggerList = None):
		self.__loggerList = []
		if loggerList is not None:
			if isinstance(loggerList, AbstractLogger):
				self.__loggerList.append(loggerList)
			elif isinstance(loggerList, list):
				for item in loggerList:
					if isinstance(item, AbstractLogger):
						self.__loggerList.append(item)
					else:
						raise Exception("Invalid object found in logger list!")
			else:
				raise Exception("Invalid object found in logger list!")



	def addLogger(self, logger):
		assert isinstance(logger, AbstractLogger)
		self.__loggerList.append(logger)



	def removeLogger(self, logger):
		assert isinstance(logger, AbstractLogger)
		self.__loggerList.remove(logger)



	def _log(self, timeStamp, logLevel, textOrException):
		for logger in self.__loggerList:
			logger._log(timeStamp, logLevel, textOrException)



	def descend(self, text):
		newList = []
		for logger in self.__loggerList:
			newList.append(logger.descend(text))
		return MulticastLogger(newList)



	def clear(self):
		for logger in self.__loggerList:
			logger.clear()






