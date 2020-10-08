#-*- encoding:UTF-8 -*- 
"""
excel sheet读取

@author: Oscar
"""
 
from xml.dom import minidom
import os,sys 
import xlrd 
import xlwt
import string

class SheetReader:
	fileName =None
	tableName=None

	datas=None
	rows = 0
	cols = 0
	markIndex = 1
	keyIndex = 2
	typeIndex = 3
	dataStarIndex= 4
	keys = []
	typestr = []
	
	front  = 10;#黄色
	backend= 13;#红色
	ignore = 23;#灰色
	
	fliter = {}#23 过滤不读取,  10前端专用 13后端专用
	
	mergedIndex =0
	mergedNum = 0
	mergedCells =[]#
	
	def __init__(self):
	
		self.fileName =None
		self.tableName=None
		
		self.datas=None
		self.keys = []
		self.typestr = []
		
		self.mergedIndex =0
		self.mergedCells =[]#
		
		self.fliter[self.backend] = []
		self.fliter[self.front]   = []
		self.fliter[self.ignore]  = []
	
	def load_data(self,filePath, fileName, tableName):
	
		self.fileName = fileName
		self.tableName = tableName

		wb = xlrd.open_workbook(filePath, formatting_info=1)
		sheet = wb.sheet_by_name(self.tableName)
		self.rows = sheet.nrows
		self.cols = sheet.ncols
		self.datas = [[0 for i in range(self.cols)] for i in range(self.rows) ]
		
		self.mergedNum = len(sheet.merged_cells)
		for i in range(0, self.mergedNum):
			_,_,a,b = sheet.merged_cells[i]
			self.mergedCells.append( (a, b-1) )

		for i in range(0, self.rows):
			for j in range(0, self.cols):
				self.datas[i][j] = sheet.cell(i,j).value

		self.mergedCells =sorted(self.mergedCells)

		color = 0
		for i in range(0 , self.cols ):
			if(type(self.datas[self.keyIndex][i]).__name__=='float'):
				self.keys.append( '['+str(int( self.datas[self.keyIndex][i] ) )+']' )
			else:
				self.keys.append( self.datas[self.keyIndex][i] )
			self.typestr.append( self.datas[self.typeIndex][i] )
			color = wb.xf_list[  sheet.cell_xf_index(self.keyIndex,i)  ].background.pattern_colour_index
			if(self.fliter.has_key(color)):
				self.fliter[color].append(i)

	def WriteFile(self, name , data):
		f = open(name,'w' )
		f.write(data.encode('utf-8'));
		f.close();