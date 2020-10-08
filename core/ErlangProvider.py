#-*- encoding:UTF-8 -*-  
from xml.dom import minidom
import os,sys 
import xlrd 
import xlwt
import string

from core import function as func


class ErlangProvider:
	
	reader    = None
	outputDir = ''

	def __init__(self):

		self.outputDir = ''

	
	def do_init(self, reader, output):
		self.reader    = reader
		self.outputDir = output
		
		if(False == os.path.exists(self.outputDir) ):
			os.makedirs(self.outputDir);
		if(self.outputDir[-1:] != '/'):
			self.outputDir += '/'
	
	
	def to_string(self):
		res = ""
		
		min,max = (-1,-1)
		q= False
		for i in range(self.reader.dataStarIndex, self.reader.rows):
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
	
	def get_filepath(self):
		return "%s%s_temp.config" %( self.outputDir , self.reader.tableName );
		
	def is_need(self, i):
		return (False ==( i in self.reader.fliter[self.reader.ignore] ) and False==(i in self.reader.fliter[self.reader.backend] ) )
		

	def mark(self):
		res = '%'
		q = ''
		for i in range(0 , self.reader.cols ):
			if( self.is_need(i) ):
				res += q+ self.reader.datas[self.reader.markIndex][i]
				q = ', '
		if( False==( '%'== res ) ):
			res += '\n'
		return  res