#-*- encoding:UTF-8 -*-
#!/usr/bin/python3

"""
工具
@author: Oscar
"""
import getopt
import os,sys 
import string

from Config import EXCEL_DIR
from Config import EXCEL_EXT
from Config import EXPORT_MODE
from Config import CONFIG_OUTPUT_PATH
from Config import LUA_File_FOLDER
from Config import ERL_File_FOLDER


from core.SheetReader import SheetReader as Reader
from core.LuaExportor import LuaExportor as LuaExportor
from core.ErlangExportor import ErlangExportor as ErlangExportor

exportors = {
	"lua": LuaExportor(),
	"erl": ErlangExportor(),
}

shortArgv = "ahf:l:";
#file:指定文件  help:指令说明 all:导出所有  lang:导出格式
argv = ['file=','help','all','lang=',];
			
config = {
	"lang":[LUA_File_FOLDER,ERL_File_FOLDER],
	"file":None
}

def showHelp():
	print(u"***********************************************************************************************")
	print(u"*   -h or --help    显示帮助信息                                                              *")
	print(u"*   -a or --all     导出所有                                                                  *")
	print(u"*   -f or --file    指定文件输出                                                              *")
	print(u"*   -l or --lang    导出格式 ['lua','erl']                                                    *")
	print(u"***********************************************************************************************")


def main():
	res = False
	cmd = None;
	try:
	
		opts, args = getopt.getopt(sys.argv[1:], shortArgv, argv)
		res = True;
	except getopt.GetoptError as e:
		print("argv error,please input %s" % e)
		res = False;
	
	if res == True:
		for option, value in opts:
			if option in ['-h', '--help']:
				cmd = "help"
			elif option in ['-a', '--all']:
				cmd = "all"
			elif option in ['-f', '--file']:
				cmd = "single"
				config['file']=value;
			elif option in ['-l','--lang']:
				config['lang'] = eval(value);
			
	return cmd != None, cmd;

#导出目录下所有
def exportAll():
	files= [];

	recursiveSearch(EXCEL_DIR,files)
	if(False == os.path.exists(EXCEL_DIR) ):
		print('目录不存在')
	else:
		file_name = ''
		num = len(files)
		for index in range(0, num):
			#print(files[index])
			export(files[index])

#导出指定单个文件
def exportSingle():
	if(None== config['file']):
		print( '未指定文件!! ')
	else:
		filePath = ''
		fileName = ''

		if(EXCEL_DIR[-1:] != '/'):
			EXCEL_DIR = EXCEL_DIR+'/'
		
		strs = os.path.splitext(config['file'])
		if(strs[1] == EXCEL_EXT):
			filePath= "%s%s" % ( EXCEL_DIR, config['file'])
		else:
			filePath= "%s%s%s" % ( EXCEL_DIR, config['file'], EXCEL_EXT)
			
		export(filePath)

def export(filePath):
	if(True ==os.path.exists(filePath) ):
		path,fileName= os.path.split(filePath)
		tableName = fileName.split("(")[0]
		
		reader = Reader()
		sheetCount= reader.load_data(filePath, fileName)
		
		isSingle = sheetCount ==1
		#导出语言
		num = len(config['lang'])
		exportor = None
		data = ""
		outputPath = ""
		for index in range(0, num):
			data =""
			
			outputPath = CONFIG_OUTPUT_PATH+ config['lang'][index]
			if(False == os.path.exists(outputPath) ):
				os.makedirs(outputPath);
			if(outputPath != '/'):
				outputPath += '/'
			
			if(config['lang'][index] in exportors ):
				exportor = exportors[ config['lang'][index] ]
				for k in range(0, sheetCount):
					reader.load_sheet_data(k)
					reader.tableName = "%s_%s"% (tableName,reader.tableName)
					#one sheet one file
					if(EXPORT_MODE == 1):
						data = exportor.to_string(reader)
						
						writeFile(exportor.get_filepath(outputPath) , data)
					else:
						data += "\n\r"+exportor.to_string(reader)
				if(EXPORT_MODE == 2):
					reader.tableName = tableName
					writeFile(exportor.get_filepath(outputPath) , data)
			else:
				print( 'no found exportor :'+  config['lang'][index])

	else:
		print( '%s no found!! '% filePath)

# 递归查找文件
def recursiveSearch(path,files):
	contents = os.listdir(path)
	for pathdir in contents:  # 遍历当前目录
		fullpath = os.path.join(path, pathdir)

		if os.path.isdir(fullpath):
			recursiveSearch(fullpath,files)
		elif os.path.isfile(fullpath):
			if os.path.splitext(fullpath)[1] == EXCEL_EXT:
				files.append(fullpath);


def loadData(file_name,tab_name , p):
	package = 'module'
	
	module = __import__(package+".tab_"+tab_name,fromlist=True)
	parser = getattr(module, 'tab_'+tab_name)()
	parser.loadData(os.path.realpath(p) ,file_name , tab_name)


def writeFile(name , data):
	with open(name, "w", encoding="utf-8") as f:
		f.write(data)

if __name__ == '__main__':

	if len(sys.argv)==0:
		print(u'请输入参数-h 查看帮助')
		sys.exit()
	
	res = True
	cmd = ""
	if res == True:
		res,cmd = main();
	
	if res == True:
		if cmd == "help":
			showHelp()
		elif cmd == "all":
			exportAll()
		elif cmd == "single":
			exportSingle()
		print(u'处理完成！')
	else :
		print(u'请输入参数-h 查看帮助')