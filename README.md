excel配置及导出(目前实现lua,erlang导出)
================

*本地安装python 3.10.0rc2版本
*安装excel处理插件
*pip3 install xlrd
*pip3 install xlwt

*安装完python 配置环境变量到python 目录和python/scripts目录
*tool目录下有32位/64位版本，根据系统安装一个版本

操作命令
---------------

```go
	python run.py -a
	python run.py -f 指定文件
```

excel配置说明
---------------

### 前4行为表头
```go
	R1 多数情况下不用到,比如设置属性时要导出为一个单元，可设置该行，合并单元格
	R2 中文字段备注
	R3 字段名称
	R4 数值类型
```

### 数值类型
```go
	int      整型数据
	float    浮点数据
	str     文本字段
	istr    自定义枚举类型
	bstr    布尔值文本  是/否  导出时直接转为true/false
	vector2  二维坐标 0,0
	vector3  三维坐标 0,0,0
	reward   奖励配置
```
*列表类型 list(type) type  为上述类型
*数据除开几个几本类型，像reward 可以根据需求自行做解析。解析处理在function.py文件中

配置导出扩展
---------------
	
*目前导出只实现了lua,erl导出，若要扩展处理json,xml可在代码做新增exportor，在Main.py添加实例
```go
providers = {
	"lua": LuaExportor(),
	"erl": ErlangExportor(),
	"json": JsonExportor(),
	"xml": XmlExportor()
}
```

## 打赏作者

![](https://inews.gtimg.com/newsapp_bt/0/12589884703/641)