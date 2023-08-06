# -*- coding: UTF-8 -*-

from datetime import datetime, date, timedelta
#from ._opslogs import opsLogs.errorLog
from _opslogs import opsLogs
#from  ._opslogs.opsLogs import errorLog

class opsDate(object):
	"""
	custom date
	"""

	def __init__(self, mode=1, differ=None):
		self.mode = mode
		self.differ = differ

	def today(mode=1):
		"""
		return @str
		example: 2016-01-09
		"""
		if mode == 1:
			_today = date.today().strftime('%Y-%m-%d')
		elif mode == 2:
			_today = date.today().strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")
			#errorLog("wrong mode here!,mode is 1 or 2")

		return _today


	def yesterday(mode=1):
		"""
		return @str
		example: 2016-01-09
		"""
		if mode == 1:
			yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
		elif mode == 2:
			yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")
	
		return yesterday

	def tommorrow(mode=1):
		"""
		func: tommorrow
		return: the day after today
		"""
		if mode == 1:
			day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
		elif mode == 2:
			day = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")

		return day

	def dayBefore(differ=1, mode=1):
		"""
		return @str
		"""
		if mode == 1:
			day = (datetime.today() - timedelta(days=differ)).strftime('%Y-%m-%d')
		elif mode == 2:
			day = (datetime.today() - timedelta(days=differ)).strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")

		return day

	def dayAfter(differ=1, mode=1):
		"""
		return @str
		"""
		if mode == 1:
			day = (datetime.today() + timedelta(days=differ)).strftime('%Y-%m-%d')
		elif mode == 2:
			day = (datetime.today() + timedelta(days=differ)).strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")

		return day

	def daytime(mode=1):
		"""
		func: daytime
		return @str
		"""
		if mode == 1:
			daytime =  datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		elif mode == 2:
			daytime =  datetime.today().strftime('%Y%m%d %H:%M:%S')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")

		return daytime

	def firstAndLastDay(mode=1):
		"""
		func: firstAndLastDay
		desc: 得到上个月的第一天和最后一天
		return @str
		"""

		# result = []

		now = datetime.now()
		year = now.year
		month = now.month

		## 当月第一天
		cur_firstday = datetime(year, month, 1)
		print(type(cur_firstday))

		if month == 1:
			year -= 1
			month = 12
		else:
			month -= 1


		if mode == 1:
			## 上个月第一天
			last_firstday = datetime(year, month, 1).strftime('%Y-%m-%d')
			last_lastday = (cur_firstday - timedelta(days=1)).strftime('%Y-%m-%d')
		elif mode == 2:
			last_firstday = datetime(year, month, 1).strftime('%Y%m%d')
			last_lastday = (cur_firstday - timedelta(days=1)).strftime('%Y%m%d')
		else:
			opsLogs.errorLog("wrong mode here!,mode is 1 or 2")

		return last_firstday, last_lastday




