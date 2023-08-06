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
# This logger just consumes all loggin output without doing anyting with it.
#
class SimpleFileLogger(AbstractLogger):



	def __init__(self, filePath, bAppendToExistingFile = True, bFlushAfterEveryLogMessage = True, fileMode = 0o0500):
		self.__filePath = filePath
		self.__bAppendToExistingFile = bAppendToExistingFile
		self.__bFlushAfterEveryLogMessage = bFlushAfterEveryLogMessage
		if not bAppendToExistingFile:
			if os.path.isfile(filePath):
				os.unlink(filePath)
		self.__f = open(filePath, "a+")
		if fileMode is not None:
			os.chmod(filePath, fileMode)



	def _log(self, timeStamp, logLevel, textOrException):
		if self.__f == None:
			raise Exception("Logger already closed.")

		lineOrLines = self._logEntryToStringOrStringList(timeStamp, logLevel, textOrException)
		if isinstance(lineOrLines, str):
			self.__f.write(lineOrLines + "\n")
		else:
			for line in lineOrLines:
				self.__f.write(line + "\n")
		if self.__bFlushAfterEveryLogMessage:
			self.__f.flush()



	def _logAll(self, logEntryList):
		if self.__f == None:
			raise Exception("Logger already closed.")

		for (timeStamp, logLevel, textOrException) in logEntryList:
			lineOrLines = self._logEntryToStringOrStringList(timeStamp, logLevel, textOrException)
			if isinstance(lineOrLines, str):
				self.__f.write(lineOrLines + "\n")
			else:
				for line in lineOrLines:
					self.__f.write(line + "\n")
		if self.__bFlushAfterEveryLogMessage:
			self.__f.flush()



	def descend(self, text):
		return self



	def close(self):
		if self.__f is not None:
			self.__f.close()
			self.__f = None







