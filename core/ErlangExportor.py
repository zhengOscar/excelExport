#-*- encoding:UTF-8 -*-  
#!/usr/bin/python3

from xml.dom import minidom
import os,sys 
import xlrd 
import xlwt
import string

from Config import FRONT
from Config import BACKEND
from Config import IGNORE
from Config import MARK_INDEX
from Config import DATA_START_INDEX

from core.IExportor import IExportor as IExportor
from core import function as func


class ErlangExportor(IExportor):


	def to_string(self,reader):
		self.reader = reader
		res = "";
		min,max = (-1,-1)
		q= False
		for i in range(DATA_START_INDEX, self.reader.rows):
			res +="{"+self.reader.tableName+"_temp, "
			
			if(self.reader.mergedNum>0):
				self.reader.mergedIndex = 0
				min,max = self.reader.mergedCells[self.reader.mergedIndex]
			
			for j in range(0, self.reader.cols):
				if( self.is_need(j) ):
					v = func.fliterDataForErl( self.reader.typestr[j], self.reader.keys[j], self.reader.datas[i][j])

					if(j==min ):
						if(self.reader.datas[0][min]=='props'):
							q = True
						res += '['
						if True == q:
							if(commonDB.data['props_key'].has_key( self.reader.keys[j] ) ):
								res += "("+ commonDB.data['props_key'][ self.reader.keys[j] ] +","+v   +"), "
						else:
							res +=  v   +", "
					elif(j==max):
						if True == q:
							if(commonDB.data['props_key'].has_key( self.reader.keys[j] ) ):
								res += "("+ commonDB.data['props_key'][ self.reader.keys[j] ] +","+v   +")"
						else:
							res +=  v 
						res += "], "
						
						if(self.reader.datas[0][min]=='props'):
							q = False
						if(self.reader.mergedIndex+1<self.reader.mergedNum):
							self.reader.mergedIndex+=1
							min,max = self.reader.mergedCells[self.reader.mergedIndex]
					else:
						if True == q:
							if(commonDB.data['props_key'].has_key( self.reader.keys[j] ) ):
								res += "("+ commonDB.data['props_key'][ self.reader.keys[j] ] +","+v   +"), "
						else:
							res +=  v   +", "
			
			res = res[:-2]
			res +="}.\n"
		return self.mark() + res
	
	def get_filepath(self,outputDir):
		return "%s%s_temp.config" %( outputDir , self.reader.tableName );

	def is_need(self, i):
		return (False ==( i in self.reader.fliter[IGNORE] ) and False==(i in self.reader.fliter[BACKEND] ) )
		

	def mark(self):
		res = '%'
		q = ''
		for i in range(0 , self.reader.cols ):
			if( self.is_need(i) ):
				res += q+ self.reader.datas[MARK_INDEX][i]
				q = ', '
		if( False==( '%'== res ) ):
			res += '\n'
		return  res