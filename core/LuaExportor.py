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
from Config import LIST_SPLIT_SYMBOL

from core.IExportor import IExportor as IExportor
from data import languageDB
from data import commonDB

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
					v = self.fliter_data( self.reader.typestr[j], self.reader.keys[j], self.reader.datas[i][j])
					if( v=="Error" ):
						raise TypeError("row:%s column:%s 数据格式不正确"%(i,j)) 

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
		
	def fliter_data(self,type,key, value):
		res = ''
		if(type=='int'):
			res = str(int(value))
		elif(type=='float'):
			res = str(value)
		elif(type=='str'):
			if(key in  languageDB.data ):
				if(value in  languageDB.data[key] ):
					
					res ="languageDB."+self.makeKey(key)+"["+ str( languageDB.data[key][value]  ) +"]"
				else:
					res = "''"
			else:
				res = "''"
				
		elif(type=='reward'):
			if(''==value):
				res = 'nil'
			else:
				r = value.split(':')
				if(len(r)==2):
					res += '{t=%s, id=0, n=%s, r=1 } ' %( str(r[0]) , str(r[1]) )
				elif(len(r)==3):
					res += '{t=%s, id=%s, n=%s, r=1 } ' %( str(r[0]) , str(r[1]) ,str(r[2]) )
				elif(len(r)==4):
					res += '{t=%s, id=%s, n=%s, r=%s } ' %( str(r[0]) , str(r[1]) ,str(r[2]) ,str(r[3]))
		elif(type=='list(int)'):
			if(''==value):
				res = 'nil'
			else:
				ds = value.split(LIST_SPLIT_SYMBOL)
				i = 1
				res = "{"
				for item in ds:
					res += '[%s]=%s,' %(str(i), str(item))
					i += 1
				res += "}"
				
		elif(type=='list(float)'):
			if(''==value):
				res = 'nil'
			else:
				ds = value.split(LIST_SPLIT_SYMBOL)
				i = 1
				res = "{"
				for item in ds:
					res += '[%s]=%s,' %(str(i), str(item))
					i += 1
				res += "}"
				
		elif(type=='list(str)'):
			if(''==value):
				res = 'nil'
			else:
				ds = value.split(LIST_SPLIT_SYMBOL)
				i = 1
				res = "{"
				for item in ds:
					res += '[%s]="%s",' %(str(i), str(item))
					i += 1
				res += "}"
		
		elif(type=='list(reward)'):
			if(''==value):
				res = 'nil'
			else:
				ds = value.split(LIST_SPLIT_SYMBOL)
				res = '{'
				i = 1
				for item in ds:
					r = item.split(':')
					if(len(r)==2):
						res += '[%s]={t=%s, id=0, n=%s, r=1 }, ' %( str(i) , str(r[0]) , str(r[1]) )
					elif(len(r)==3):
						res += '[%s]={t=%s, id=%s, n=%s, r=1 }, ' %( str(i) , str(r[0]) , str(r[1]) ,str(r[2]) )
					elif(len(r)==4):
						res += '[%s]={t=%s, id=%s, n=%s, r=%s }, ' %( str(i) , str(r[0]) , str(r[1]) ,str(r[2]) ,str(r[3]))
					elif(len(r)==5):
						res += '[%s]={t=%s, id=%s, n=%s, r=1, min=%s, max=%s }, ' %( str(i) , str(r[0]) , str(r[1]) ,str(r[2]) ,str(r[3]) , str(r[4]))
					elif(len(r)==6):
						res += '[%s]={t=%s, id=%s, n=%s, r=%s, min=%s, max=%s }, ' %( str(i) , str(r[0]) , str(r[1]) ,str(r[2]) ,str(r[3]) , str(r[4]) ,str(r[5]))
					i += 1
				res += '}'
		elif(type=='color'):
			res = commonDB.data['color'][  value  ]
		elif(type=='vector2'):
			res = "Vector2("+value+")"
		elif(type=='vector3'):
			res = "Vector3("+value+")"
		elif(type=='interval'):
			if(''==value):
				res = 'nil'
			elif("," in str(value)):
				r = value.split(',')
				res = '{min='+r[0]+', max='+r[1] +' }'
			else:
				res = "Error"
		return res

	def get_filepath(self, outputDir):
		return "%s%sDB.lua" %( outputDir , self.reader.tableName );
		
	def is_need(self, i):
		return (False ==( i in self.reader.fliter[IGNORE] ) and False==(i in self.reader.fliter[FRONT] ) )
		
	def mark(self):
		
		return ''
		
	def makeKey(self,k):
		ds = k.split('_')
		keys = []
		for d in ds:
			keys.append( d[0].upper()+d[1:len(d)] )
			
		return ''.join(keys)