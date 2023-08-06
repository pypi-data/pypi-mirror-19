#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Customize log functions"""

class colinLogs(object):
	"""customize log"""
	def __init__(self, string):
		self.string = string

	def printLog(string):
		"""
		func: greenPrint
		return: log with green color
		"""
		print("\033[32m " + string + "\033[0m")

	def warnLog(string):
		"""
		func: warnLog
		return: log with yellow color for warning message show
		"""
		print("\033[33m " + string + "\033[0m")

	def errorLog(string):
		"""
		func: warnLog
		return: log with yellow color for warning message show
		"""
		print("\033[31m " + string + "\033[0m")

