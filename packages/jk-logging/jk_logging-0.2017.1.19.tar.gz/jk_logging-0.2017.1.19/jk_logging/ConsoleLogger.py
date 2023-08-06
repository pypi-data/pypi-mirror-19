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
class ConsoleLogger(AbstractLogger):



	def __init__(self, indentLevel = 0, prefix = ""):
		self.__level = indentLevel
		self.__prefix = prefix



	def _log(self,timeStamp,  logLevel, textOrException):
		lineOrLines = self._logEntryToStringOrStringList(timeStamp, logLevel, textOrException)
		if isinstance(lineOrLines, str):
			print(self.__prefix + lineOrLines)
		else:
			for line in lineOrLines:
				print(self.__prefix + line)



	def descend(self, text):
		self._log(time.time(), EnumLogLevel.INFO, text)
		return ConsoleLogger(self.__level + 1, self.__prefix + "\t")








