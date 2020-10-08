#-*- encoding:UTF-8 -*-  
import os,sys 
import string

from data import languageDB
from data import commonDB

def fliterData(t, k, v):
	res = ''
	if(t=='text'):
		if( languageDB.data.has_key(k) ):
			if(  languageDB.data[k].has_key(v) ):
				
				res ="languageDB."+makeKey(k)+"["+ str( languageDB.data[k][v]  ) +"]"
			else:
				res = "''"
		else:
			res = "''"
			
	elif(t=='itext'):
		if(commonDB.data.has_key(k)):
			if( commonDB.data[k].has_key(v) ):
				res = str( commonDB.data[k][v] )
			else:
				res = "''"
		else:
		
			res = "''"
	elif(t=='btext'):
		if(v==u'是'):
			res = 'true'
		else:
			res = 'false'
	elif(t=='props'):
		if(v==''):
			res = 'nil'
		else:
			ds = v.split(',')
			res = '{'
			for item in ds:
				r = item.split(':')
				if(commonDB.data['props'].has_key( r[0] ) ):
					if(len(r)==2):
						res += commonDB.data['props'][ r[0] ] +'=' + str( r[1] ) +','
					elif(len(r)==3):
						res += commonDB.data['props'][ r[0] ] +'=' + str( r[2] ) +','
			res += '}'
	elif(t=='sstr'):
		if(type(v).__name__=='float'):
			res = '{[1]='+str(int(v)) + ' }'
		
		elif(v==''):
			res = 'nil'
		else:
			ds = v.split(',')
			res = '{'
			index = 1
			for item in ds:
				r = item.split(':')
				if(len(r)==1):
					res += '[' + str(index)  +']=' + item +','
					index +=1
				elif(len(r)==2):
					res += '[' + r[0]  +']=' + str( r[1] ) +','
				elif(len(r)==3):
					res += '[' + r[0]  +']=' + str( r[2] ) +','
			res += '}'
	elif(t=='fstr'):
		if(type(v).__name__=='float'):
			res = '{[1]=['+str(v) + '] }'
		
		elif(v==''):
			res = 'nil'
		else:
			ds = v.split(',')
			res = '{'
			index = 1
			for item in ds:
				r = item.split(':')
				if(len(r)==1):
					res += '[' + str(index)  +']=' + item +','
					index +=1
				elif(len(r)==2):
					res += '[' + r[0]  +']=' + str( r[1] ) +','
				elif(len(r)==3):
					res += '[' + r[0]  +']=' + str( r[2] ) +','
			res += '}'
	elif(t=='xstr'):
		if(v==''):
			res = 'nil'
		else:
			ds = v.split(',')
			res = '{'
			eds = {}
			for item in ds:
				r = item.split(':')
				if(False == eds.has_key( r[2] ) ):
					eds[  r[2]  ] = []
				
				eds[  r[2]  ].append( r[0] )
				
			for item in eds:
				res += '['+str(item) +']={'
				res += ','.join( eds[item] )
				res += '},'
			res += '}'
	elif(t=='qstr'):#区间数据
		ds = v.split('-')
		res = '{'
		res += 'min='+ds[0]+ ', max='+ ds[1]
		res += '}'
	elif(t=='rewards'):
		if(''==v):
			res = 'nil'
		else:
			ds = v.split(',')
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
	elif(t=='reward'):
		if(''==v):
			res = 'nil'
		else:
			r = v.split(':')
			if(len(r)==2):
				res += '{t=%s, id=0, n=%s, r=1 } ' %( str(r[0]) , str(r[1]) )
			elif(len(r)==3):
				res += '{t=%s, id=%s, n=%s, r=1 } ' %( str(r[0]) , str(r[1]) ,str(r[2]) )
			elif(len(r)==4):
				res += '{t=%s, id=%s, n=%s, r=%s } ' %( str(r[0]) , str(r[1]) ,str(r[2]) ,str(r[3]))
	elif(t=='str'):
		res = "'"+v+"'"
	elif(t=='color'):
		res = commonDB.data['color'][  v  ]
	elif(t=='vector2'):
		res = "Vector2("+v+")"
	elif(t=='vector3'):
		res = "Vector3("+v+")"
	elif(t=='interval'):
		if(type(v).__name__=='float'):
			res = '{min='+str(v) + ', max=99999 }'
		elif(''==v):
			res = 'nil'
		else:
			r = v.split(',')
			res = '{min='+r[0]+', max='+r[1] +' }'
	elif(t=='int'):
		res = str(int(v))
	elif(t=='float'):
		res = str(v)
		
	return res

def makeKey(k):
	ds = k.split('_')
	keys = []
	for d in ds:
		keys.append( d[0].upper()+d[1:len(d)] )
		
	return ''.join(keys)
	
def fliterDataForErl(t, k, v):
	res = ''
	
	if(t=='int'):
		res = str(int(v))
	elif(t=='float'):
		res = str(v)
	elif(t=='rewards'):
		res = '"'+ v +'"'
	elif(t=='reward'):
		res = '"'+ v +'"'
	elif(t=='str'):
		res = '"'+ v +'"'
	elif(t=='sstr'):
		if(type(v).__name__=='float'):
			res = '['+str(int(v)) + ']'
		else:
			res = '['+ str(v) +']'
	elif(t=='fstr'):
		if(type(v).__name__=='float'):
			res = '['+str(v) + ']'
		else:
			res = '['+ str(v) +']'
	elif(t=='props'):
		if(v==''):
			res = '""'
		else:
			ds = v.split(',')
			res = '['
			for item in ds:
				r = item.split(':')
				if(commonDB.data['props_flag'].has_key( r[0] ) ):
					if(len(r)==2):
						res += "("+commonDB.data['props_flag'][ r[0] ] +',' + str( r[1] ) +'),'
					elif(len(r)==3):
						res += "("+commonDB.data['props_flag'][ r[0] ] +',' + str( r[2] ) +'),'
			res = res[:-1]
			res += ']'
	elif(t=='itext'):
		if(commonDB.data.has_key(k)):
			if( commonDB.data[k].has_key(v) ):
				res = str( commonDB.data[k][v] )
			else:
				res = '""'
		else:
		
			res = "''"
	elif(t=='btext'):
		if(v==u'是'):
			res = 'true'
		else:
			res = 'false'
	elif(t=='interval'):
		if(type(v).__name__=='float'):
			res = '('+str(v) + ',  99999 )'
		elif(''==v):
			res = '(0, 99999)'
		else:
			r = v.split(',')
			res = '('+r[0]+', '+r[1] +' )'
	else:
		res = '"'+ v +'"'
	return res
	