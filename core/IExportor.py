#-*- encoding:UTF-8 -*-  
#!/usr/bin/python3
from abc import abstractmethod, ABCMeta

from Config import FRONT
from Config import BACKEND
from Config import IGNORE
from Config import DATA_START_INDEX

from data import languageDB
from data import commonDB

class IExportor(metaclass=ABCMeta):

	tableName = None
	reader    = None

	@abstractmethod
	def to_string(self,reader):
		pass


	@abstractmethod
	def fliter_data(self,type,key, value):
		pass


	@abstractmethod
	def get_filepath(self, outputDir):
		pass


	@abstractmethod
	def is_need(self, i):
		pass


	@abstractmethod
	def mark(self):
		pass