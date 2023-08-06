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
# This logger serves as a filter. Logging events are passed on to other loggers if they are within the
# accepting range of the filter.
#
class FilterLogger(AbstractLogger):



	def __init__(self, logger, minLogLevel = EnumLogLevel.WARNING):
		self.__logger = logger
		self.__minLogLevel = int(minLogLevel)



	def _log(self, timeStamp, logLevel, textOrException):
		if int(logLevel) >= self.__minLogLevel:
			self.__logger._log(timeStamp, logLevel, textOrException)



	def descend(self, text):
		return self



	def clear(self):
		self.__logger.clear()








