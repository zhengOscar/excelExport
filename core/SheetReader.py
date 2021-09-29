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

from Config import FRONT
from Config import BACKEND
from Config import IGNORE
from Config import FIELD_NAME_INDEX
from Config import DATA_TYPE_INDEX
from Config import DATA_START_INDEX

class SheetReader:
	fileName =None
	tableName=None

	datas=None
	rows = 0
	cols = 0
	
	keys = []
	typestr = []
	
	sheets = None

	fliter = {}#23 过滤不读取,  10前端专用 13后端专用
	
	mergedIndex =0
	mergedNum = 0
	mergedCells =[]#
	
	def __init__(self):
	
		self.fileName =None
	
	def load_data(self,filePath, fileName):
		self.fileName = fileName

		wb = xlrd.open_workbook(filePath, formatting_info=True)
		self.sheets = wb.sheets();
		return len(self.sheets);
		
	def load_sheet_data(self,index):
		self.reset();
		
		sheet = self.sheets[index]
		self.tableName= sheet.name.split("(")[0]
		
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
			if(type(self.datas[FIELD_NAME_INDEX][i]).__name__=='float'):
				self.keys.append( '['+str(int( self.datas[FIELD_NAME_INDEX][i] ) )+']' )
			else:
				self.keys.append( self.datas[FIELD_NAME_INDEX][i] )
			self.typestr.append( self.datas[DATA_TYPE_INDEX][i] )
			color =0;# wb.xf_list[  sheet.cell_xf_index(FIELD_NAME_INDEX,i)  ].background.pattern_colour_index
			if(color in self.fliter):
				self.fliter[color].append(i)
				
	def reset(self):
		self.tableName=None
		
		self.datas=None
		self.keys = []
		self.typestr = []
		
		self.mergedIndex =0
		self.mergedCells =[]#
		
		self.fliter[BACKEND] = []
		self.fliter[FRONT]   = []
		self.fliter[IGNORE]  = []

