#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc
from enum import Enum
import datetime
import re

import sh



class EnumLogLevel(Enum):
	DEBUG = 10, 'DEBUG'
	NOTICE = 20, 'NOTICE'
	INFO = 30, 'INFO'
	STDOUT = 31, 'STDOUT'
	WARNING = 40, 'WARNING'
	ERROR = 50, 'ERROR'
	STDERR = 51, 'STDERR'
	EXCEPTION = 60, 'EXCEPTION'

	def __new__(cls, value, name):
		member = object.__new__(cls)
		member._value_ = value
		member.fullname = name
		return member

	def __int__(self):
		return self.value





def _getLogLevelStrMap(bPrefixWithSpacesToSameLength = False):
	maxLogLevelLength = len("STACKTRACE")
	for logLevel in EnumLogLevel:
		s = _getLogLevelStr(logLevel)
		if len(s) > maxLogLevelLength:
			maxLogLevelLength = len(s)
	logLevelToStrDict = {}
	for logLevel in EnumLogLevel:
		s = _getLogLevelStr(logLevel)
		if bPrefixWithSpacesToSameLength:
			while len(s) < maxLogLevelLength:
				s = " " + s
		logLevelToStrDict[logLevel] = s
	return logLevelToStrDict





def _getLogLevelStr(logLevel):
	s = str(logLevel)
	pos = s.rfind(".")
	if pos >= 0:
		s = s[pos+1:]
	return s





_PATTERN = re.compile("^File\\s\"" + "(?P<path>.+?)" + "\",\\sline\\s" + "(?P<line>[0-9]+?)" + ",\\sin " + "(?P<module>.+?)" + "$")

#
# Parse an exception line such as: "File \"./test.py\", line 33, in <module>"
#
def _parseExceptionLine(line):
	match = _PATTERN.match(line)

	path = match.group("path")
	sLineNo = match.group("line")
	module = match.group("module")

	return (path, sLineNo, module)








class AbstractLogger(object):
	__metaclass__ = abc.ABCMeta



	_logLevelToStrDict = _getLogLevelStrMap(True)



	@abc.abstractmethod
	def _log(self, timeStamp, logLevel, textOrException):
		raise NotImplementedError('subclasses must override log()!')



	def _logAll(self, logEntryList):
		for (timeStamp, logLevel, textOrException) in logEntryList:
			self._log(timeStamp, logLevel, textOrException)



	#
	# Converts the specified log data to a single string or a list of strings.
	#
	def _logEntryToStringOrStringList(self, timeStamp, logLevel, textOrException):
		sTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
		sTimeStamp = "[" + sTimeStamp + "] "

		logLevelStr = self._logLevelToStrDict[logLevel]

		if isinstance(textOrException, str):
			textOrException = textOrException.rstrip('\n')
			return sTimeStamp + logLevelStr + ":  " + textOrException

		if isinstance(textOrException, Exception):
			outputLines = []

			exceptionLines = []
			for line in str(textOrException).splitlines():
				line = line.strip()
				if len(line) > 0:
					exceptionLines.append(line)
			bFirstLine = True
			for line in exceptionLines:
				if bFirstLine:
					outputLines.append(sTimeStamp + logLevelStr + ":  " + textOrException.__class__.__name__ + ": " + line)
					bFirstLine = False
				else:
					outputLines.append(sTimeStamp + logLevelStr + ":  " + line)

			exceptionLines1 = []
			exceptionLines2 = []
			maxExceptionLineLength = 0
			tempLine = ""
			exceptionText = traceback.format_exc()
			for line in exceptionText.splitlines():
				line = line.strip()
				if line.startswith("Traceback "):
					continue
				if len(tempLine) > 0:
					(filePath, sLineNo, moduleName) = _parseExceptionLine(tempLine)
					exceptionLines1.append(filePath + ":" + sLineNo + " " + moduleName)
					if len(tempLine) > maxExceptionLineLength:
						maxExceptionLineLength = len(tempLine)
					tempLine = ""
					exceptionLines2.append("   # " + line)
				else:
					if line.startswith("File "):
						tempLine = line
					else:
						break

			for i in range(0, len(exceptionLines1)):
				s = exceptionLines1[i]
				while len(s) < maxExceptionLineLength:
					s += " "
				outputLines.append(sTimeStamp + "STACKTRACE:  " + s + exceptionLines2[i])

			return outputLines

		s = str(textOrException).rstrip('\n')
		return sTimeStamp + logLevelStr + ":  " + s



	#
	# Perform logging with log level ERROR.
	#
	# @param	string text		The text to write to this logger.
	#
	def error(self, text):
		self._log(time.time(), EnumLogLevel.ERROR, text)

	#
	# Perform logging with log level EXCEPTION.
	#
	# @param	Exception exception		The exception to write to this logger.
	#
	def exception(self, exception):
		self._log(time.time(), EnumLogLevel.EXCEPTION, exception)

	#
	# Perform logging with log level ERROR.
	# This method is intended to be used in conjunction with STDERR handlers.
	#
	# @param	string text		The text to write to this logger.
	#
	def stderr(self, text):
		text = text.rstrip('\n')
		self._log(time.time(), EnumLogLevel.STDERR, text)

	#
	# Perform logging with log level STDOUT.
	# This method is intended to be used in conjunction with STDOUT handlers.
	#
	# @param	string text		The text to write to this logger.
	#
	def stdout(self, text):
		text = text.rstrip('\n')
		self._log(time.time(), EnumLogLevel.STDOUT, text)

	#
	# Perform logging with log level WARNING.
	#
	# @param	string text		The text to write to this logger.
	#
	def warning(self, text):
		self._log(time.time(), EnumLogLevel.WARNING, text)

	#
	# Perform logging with log level INFO.
	#
	# @param	string text		The text to write to this logger.
	#
	def info(self, text):
		self._log(time.time(), EnumLogLevel.INFO, text)

	#
	# Perform logging with log level NOTICE.
	#
	# @param	string text		The text to write to this logger.
	#
	def notice(self, text):
		self._log(time.time(), EnumLogLevel.NOTICE, text)

	#
	# Perform logging with log level DEBUG.
	#
	# @param	string text		The text to write to this logger.
	#
	def debug(self, text):
		self._log(time.time(), EnumLogLevel.DEBUG, text)



	#
	# (Work in progress. Do not use this method yet.)
	#
	@abc.abstractmethod
	def descend(self, text):
		return None



	#
	# If this logger is buffering log messages, clear all log messages from this buffer.
	# If this logger has references to other loggers, such as a <c>FilterLogger</c>
	# or a <c>MulticastLogger</c>
	#
	def clear(self):
		pass




