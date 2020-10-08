#-*- encoding:UTF-8 -*-  
"""
工具

@author: Oscar
"""
import getopt
import os,sys 
import string

from core.SheetReader import SheetReader as Reader
from core.LuaProvider import LuaProvider as LuaProvider
from core.ErlangProvider import ErlangProvider as ErlangProvider


shortArgv = "ahf:o:p:l:";
argv = [
            'file=',
			'help',
			'all',
			'output=',
			'path=',
			'lang=',
            ];
			
config = {
	"suffix":".xls",
	"path":"./xls",
	"lang":["lua","erl"],
	"outputPath":["./output/lua","./output/erl"],
	"file":None
}

providers = {
	"lua": LuaProvider(),
	"erl": ErlangProvider(),
}

def getList(dir):
	return os.listdir(dir);

def getAllFile(dir,suffix,list,flist):	
	fileList = getList(dir);
	for k in fileList:
		if(os.path.isfile(dir+'/'+k)):
			l = len(suffix);
			if(k[(-1)*l:]==suffix):
				list.append(dir+'/'+k);
				flist.append(k[:(-1)*l]);
		else:
			#print(str(os.path.isdir(dir+'/'+k))+'::'+dir+'/'+k);
			if(os.path.isdir(dir+'/'+k)):
				getAllFile(dir+'/'+k,suffix,list,flist);

def loadData(file_name,tab_name , p):
	package = 'module'
	
	module = __import__(package+".tab_"+tab_name,fromlist=True)
	parser = getattr(module, 'tab_'+tab_name)()
	parser.loadData(os.path.realpath(p) ,file_name , tab_name)
				
def WriteFile(name , data):
	f = open(name,'w' )
	f.write(data.encode('utf-8'));
	f.close();

def nicePrint():
	#sys.setDefaultenCoding('utf-8')
	print ("                     _ooOoo_ ")
	print ("                    o8888888o ")
	print ("                    88  .  88 ")
	print ("                    (| -_- |) ")
	print ("                     O\ = /O ")
	print ("                 ____/`---'\____ ")
	print ("               .  '  \| |// `. ")
	print ("                / \||| : |||// \ ")
	print ("              / _||||| -:- |||||- \ ")
	print ("                | | \\\\\ - /// | | ")
	print ("              | \_| ''\---/'' | | ")
	print ("               \ .-\__ `-` ___/-. / ")
	print ("            ___`. .' /--.--\ `. . __ ")
	print ("         . '< `.___\_<|>_/___.' >'. ")
	print ("        | | : `- \`.;`\ _ /`;.`/ - ` : | | ")
	print ("          \ \ `-. \_ __\ /__ _/ .-` / / ")
	print ("  ======`-.____`-.___\_____/___.-`____.-'====== ")
	print ("                     `=---=' ")
	print (" ")
	print ("  ............................................. ")
	print (u"               佛祖镇楼   BUG辟易 ")
	print (u"     佛曰: ")
	print (u"          写字楼里写字间，写字间里程序员； ")
	print (u"          程序人员写程序，又拿程序换酒钱。 ")
	print (u"          酒醒只在网上坐，酒醉还来网下眠； ")
	print (u"          酒醉酒醒日复日，网上网下年复年。 ")
	print (u"          但愿老死电脑间，不愿鞠躬老板前； ")
	print (u"          奔驰宝马贵者趣，公交自行程序员。 ")
	print (u"          别人笑我忒疯癫，我笑自己命太贱； ")
	print (u"          不见满街漂亮妹，哪个归得程序员？")

def do_show_help():
	print u"***********************************************************************************************"
	print u"*   -h or --help    显示帮助信息                                                              *"
	print u"*   -a or --all     导出所有                                                                  *"
	print u"*   -f or --file    指定文件输出                                                              *"
	print u"*   -o or --output  导出路径 ['./lua','./erl']                                                *"
	print u"*   -l or --lang    导出格式 ['lua','erl']                                                    *"
	print u"***********************************************************************************************"


def do_run():
	res = False
	cmd = "help";
	try:
	
		opts, args = getopt.getopt(sys.argv[1:], shortArgv, argv)
		res = True;
	except getopt.GetoptError as e:
		print "argv error,please input %s" % e
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
			elif option in ['-o','--outputPath']:
				config['outputPath'] = eval(value);
			elif option in ['-p','--path']:
				config['path']=value;
			
	return res, cmd;
	
def do_all():
	list = [];
	flist= [];
	suffix = config['suffix']
	path = config['path']
	
	getAllFile(path, suffix,list,flist)
	if(False == os.path.exists(path) ):
		print('directory no found')
	else:
		file_name = ''
		num = len(list)
		for index in range(0, num):
			#print list[index].replace(flist[index]+suffix,""), flist[index]
			do_export(list[index].replace(flist[index]+suffix,""), list[index], flist[index])
	
def do_export(path, filePath, fileName):
	if(True ==os.path.exists(filePath) ):
		tableName = fileName.split("(")[0]
		reader = Reader()
		reader.load_data(filePath, fileName, tableName)
		
		num = len(config['lang'])
		provider = None
		for index in range(0, num):
			if(providers.has_key( config['lang'][index] ) ):
				provider = providers[ config['lang'][index] ]
				
				provider.do_init(reader, config['outputPath'][index])
				data = provider.to_string()
				WriteFile(provider.get_filepath() , data)
			else:
				print( 'no found provider :'+  config['lang'][index])
	else:
		print( 'file no found!! ('+(p +"/"+ real_path + suffix)+')' )

def do_single():
	suffix = config['suffix']

	if(None== config['file']):
		print( 'file no set!! ')
	else:
		filePath = ''
		fileName = ''
		path = config['path']
		if(path[-1:] != '/'):
			path = path+'/'
		
		if(config['file'][(-1)*len(suffix):] == suffix):
			filePath= "%s%s" % ( path, config['file'])
			fileName = config['file'][:(-1)*len(suffix)]
		else:
			filePath= "%s%s%s" % ( path, config['file'], suffix)
			fileName = config['file']
			
		do_export(path, filePath, fileName)

if __name__ == '__main__':
	nicePrint();
	
	if len(sys.argv)==0:
		
		sys.exit()
	
	res = True
	cmd = ""
	if res == True:
		res,cmd = do_run();
	
	if res == True:
		if cmd == "help":
			do_show_help()
		elif cmd == "all":
			do_all()
		elif cmd == "single":
			do_single()
		print(ur'处理完成！')