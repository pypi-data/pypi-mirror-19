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
# This logger keeps track of how many log messages of what type have been issued.
#
class DetectionLogger(AbstractLogger):



	def __init__(self, logger):
		self.__logger = logger
		self.__protocol = {}
		self.__maxLogLevelSeen = 0



	def _log(self, timeStamp, logLevel, textOrException):
		nLogLevel = int(logLevel)
		n = self.__protocol.get(nLogLevel, 0)
		self.__protocol[nLogLevel] = n + 1
		if nLogLevel > self.__maxLogLevelSeen:
			self.__maxLogLevelSeen = nLogLevel
		self.__logger._log(timeStamp, logLevel, textOrException)



	#
	# Returns the number of log messages issued.
	#
	def getLogMsgCount(self, logLevel):
		return self.__protocol.get(int(logLevel), 0)



	#
	# Returns the number of log messages issued.
	#
	def getLogMsgCountsIntMap(self):
		return {
			int(EnumLogLevel.DEBUG) : self.__protocol.get(int(EnumLogLevel.DEBUG), 0),
			int(EnumLogLevel.NOTICE) : self.__protocol.get(int(EnumLogLevel.NOTICE), 0),
			int(EnumLogLevel.INFO) : self.__protocol.get(int(EnumLogLevel.INFO), 0),
			int(EnumLogLevel.STDOUT) : self.__protocol.get(int(EnumLogLevel.STDOUT), 0),
			int(EnumLogLevel.WARNING) : self.__protocol.get(int(EnumLogLevel.WARNING), 0),
			int(EnumLogLevel.ERROR) : self.__protocol.get(int(EnumLogLevel.ERROR), 0),
			int(EnumLogLevel.STDERR) : self.__protocol.get(int(EnumLogLevel.STDERR), 0),
			int(EnumLogLevel.EXCEPTION) : self.__protocol.get(int(EnumLogLevel.EXCEPTION), 0),
		}



	#
	# Returns the number of log messages issued.
	#
	def getLogMsgCountsStrMap(self):
		return {
			str(EnumLogLevel.DEBUG) : self.__protocol.get(int(EnumLogLevel.DEBUG), 0),
			str(EnumLogLevel.NOTICE) : self.__protocol.get(int(EnumLogLevel.NOTICE), 0),
			str(EnumLogLevel.INFO) : self.__protocol.get(int(EnumLogLevel.INFO), 0),
			str(EnumLogLevel.STDOUT) : self.__protocol.get(int(EnumLogLevel.STDOUT), 0),
			str(EnumLogLevel.WARNING) : self.__protocol.get(int(EnumLogLevel.WARNING), 0),
			str(EnumLogLevel.ERROR) : self.__protocol.get(int(EnumLogLevel.ERROR), 0),
			str(EnumLogLevel.STDERR) : self.__protocol.get(int(EnumLogLevel.STDERR), 0),
			str(EnumLogLevel.EXCEPTION) : self.__protocol.get(int(EnumLogLevel.EXCEPTION), 0),
		}



	#
	# Indicates if this logger has seen such a log message.
	#
	def hasLogMsg(self, logLevel):
		return self.__protocol.get(int(logLevel), 0) > 0



	def hasAtLeastWarning(self):
		return self.__maxLogLevelSeen >= int(EnumLogLevel.WARNING)

	def hasAtLeastError(self):
		return self.__maxLogLevelSeen >= int(EnumLogLevel.WARNING)

	def hasAtLeastException(self):
		return self.__maxLogLevelSeen >= int(EnumLogLevel.WARNING)

	def hasException(self):
		return self.hasLogMsg(EnumLogLevel.EXCEPTION)

	def hasStdErr(self):
		return self.hasLogMsg(EnumLogLevel.STDERR)

	def hasError(self):
		return self.hasLogMsg(EnumLogLevel.ERROR)

	def hasStdOut(self):
		return self.hasLogMsg(EnumLogLevel.STDOUT)

	def hasWarning(self):
		return self.hasLogMsg(EnumLogLevel.WARNING)

	def hasInfo(self):
		return self.hasLogMsg(EnumLogLevel.INFO)

	def hasNotice(self):
		return self.hasLogMsg(EnumLogLevel.NOTICE)

	def hasDebug(self):
		return self.hasLogMsg(EnumLogLevel.DEBUG)



	def descend(self, text):
		return self



	def clear(self):
		self.__protocol = {}
		self.__maxLogLevelSeen = 0
		self.__logger.clear()




