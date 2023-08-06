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
class NullLogger(AbstractLogger):



	def _log(self, timeStamp, logLevel, textOrException):
		pass



	def descend(self, text):
		return self








