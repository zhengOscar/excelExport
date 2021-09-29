#-*- encoding:UTF-8 -*-  
from xml.dom import minidom
import os,sys 
import xlrd 
import xlwt
import string

from Config import FRONT
from Config import BACKEND
from Config import IGNORE
from Config import DATA_START_INDEX

from core.IExportor import IExportor as IExportor
from core import function as func

class LuaExportor(IExportor):

	def to_string(self,reader):
		self.reader = reader
		lua = self.reader.tableName+"DB={\n"
		
		min,max = (-1,-1)
		for i in range(DATA_START_INDEX, self.reader.rows):
			lua +="\t[%d]={" %  int(self.reader.datas[i][0]) 
			
			if(self.reader.mergedNum>0):
				self.reader.mergedIndex = 0
				min,max = self.reader.mergedCells[self.reader.mergedIndex]
			
			for j in range(0, self.reader.cols):
				if( self.is_need(j) ):
					v = func.fliterData( self.reader.typestr[j], self.reader.keys[j], self.reader.datas[i][j])

					if(j==min ):
						lua += self.reader.datas[0][min]+'={'
						lua += "%s=%s, " % ( str(self.reader.keys[j]),  v )
					elif(j==max):
						lua += "%s=%s, " % ( str(self.reader.keys[j]),  v )
						lua += "}, "
						if(self.reader.mergedIndex+1<self.reader.mergedNum):
							self.reader.mergedIndex+=1
							min,max = self.reader.mergedCells[self.reader.mergedIndex]
					else:
						lua += "%s=%s, " % ( str(self.reader.keys[j]),  v )
						
			lua +="},\n"
		lua += "}"
		return self.mark() + lua
	
	def get_filepath(self, outputDir):
		return "%s%sDB.lua" %( outputDir , self.reader.tableName );
		
	def is_need(self, i):
		return (False ==( i in self.reader.fliter[IGNORE] ) and False==(i in self.reader.fliter[FRONT] ) )
		
	def mark(self):
		
		return ''