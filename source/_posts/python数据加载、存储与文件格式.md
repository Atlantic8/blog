---
title: python数据加载、存储与文件格式
date: 2016-06-23 15:37:19
tags: [python, 文件, pandas]
categories: Dev
---
##### csv

| 输入函数 | 说明 |
|:-------------:|:-------------:|
| read_csv | 从文件、URL、文件对象中加载带分隔符(,)的数据 |
| read_table | 从文件、URL、文件对象中加载带分隔符(默认为制表符:\t)的数据 |
| read_fwf | 读取顶宽列格式数据(没有分隔符) |
| read_clipboard | 读取剪贴板数据，read_table的剪贴板版 |
| from_csv | Series的方法，直接读出Series实例 |

###### 一些上述函数扩展用法
```python
import pandas as pd
from pandas import DataFrame,Series

# 指定分隔符，也可用delimiter，读取前10行数据
pd.read_table('filename', sep=',',nrows=10)
# 读取特定大小的文件块(byte)
pd.read_table('filename', chunksize=1000)

# 读入DataFrame时，指定列名
pd.read_csv('filename', header=None)
pd.read_csv('filename', names=['a','b','c','d'])

# 指定列为索引，列d设为索引
pd.read_csv('filename', names=['a','b','c','d'], index_col='d')
# 层次化索引的话，可以index_col指定多个列名
pd.read_csv('filename', names=['a','b','c','d'], index_col=['c','d'])

# 跳过文件的某些行
pd.read_csv('filename', skiprows=[1,3,6])
# 需要忽略的行数，从尾部算起
pd.read_csv('filename', skip_footer=10)

# 读文件缺失值处理，将文件中某些值设置为nan
pd.read_csv('filename', na_values=['NULL'])
# 将文件中满足box条件的值设置为nan
box = {'col1':['foo','NA'], 'col3':['two']}
pd.read_csv('filename', na_values=['NULL'])
# 写文件缺失值处理，将nan写成na_rep
pd.read_csv('filename', na_rep='NULL')

# 日期解析,解析所有列，也可以指定，默认为False;
# 冲突型日期，看成国际标准格式，28/6/2016, 默认为False
pd.read_csv('filename', parse_dates=True, dayfirst=True)

# 设置编码，数据解析后仅有一列返回Series
pd.read_csv('filename', encoding='utf-8', squeeze=True)
```

| 输出函数 | 说明 |
|:-------------:|:-------------:|
| to_csv | 把数据写入到文件、输出流中，分隔符为(,)，Series也有这个方法 |

```python
# 直接打印
data.to_csv(sys.stdout)
# 输出到文件，并且将nan用'NULL'替换
data.to_csv('filename', na_rep='NULL')
# 列名和index也可以禁用
data.to_csv('filename', index=False, header=False)
# 通过指定cols可以显示特定的列
data.to_csv('filename', index=False, cols=['a','b'])
```

##### 手工处理分隔符格式
对于任何单字符分隔符文件，可以直接使用python内置的csv模块，将任意已打开的文件或文件对象传递给csv.reader:
```python
import csv
f = open('filename')
reader = csv.reader(f)
# 对reader迭代会为每行产生一个元组
for line in reader:
    print(line)
```
csv文件的形式多样只需定义csv.Dialect的一个子类即可定义出新格式
```python
class my_dialect(csv.Dialect):
    lineterminator = '\n'
    delimiter = ';'
    quotechar = '"'

reader = csv.reader(f, dialect=my_dialect())
```
csv.Dialect的属性还包括：

| 属性 | 说明 |
|:-------------:|:-------------:|
| delimiter | 分隔字段的单字符字符串，默认为',' |
| lineterminator | 写操作的行终结符，默认为'\r\n'。读操作忽略，它能认出跨平台结束符 |
| quotechar | 用于带有特殊字符的字段的引用符号 |
| quoting | 引用约定。包括csv.QUOTE_ALL(引用所有字段)，csv.QUOTE_MINIMAL(只引用带有特殊字符的字段)，csv.QUOTE_NONNUMERIC(只引用非数值属性),csv.QUOTE_NON(不引用) |
| skipinitialspace | 忽略分隔符后面的空白符，默认为False |
| doublequote | 处理字段内的引用符号，如果为True则双写 |
| escapechar | 用于对分隔符进行转义的字符串，默认禁用 |

要手工输出分隔符文件，使用csv.writer
```python
with open('filename', 'w') as f:
writer = csv.writer(f, dialect=my_dialect)
writer.writerow(('one','two','three'))
writer.writerow(('1','2','3'))
```

#### JSON

```python
obj = """
{"name":"wes",
 "place":["usa","russia","china"],
 "pet": null,
 "siblings": [{"name":"scott","age":25, "pet":"Zuko"},{"name":"katie","age":33, "pet":"Cisco"}]
}
"""

import json
# 将json字符串转换成python形式
result = json.loads(obj)
$-> {u'name': u'wes',
      u'pet': None,
      u'place': [u'usa', u'russia', u'china'],
      u'siblings': [{u'age': 25, u'name': u'scott', u'pet': u'Zuko'},
     {u'age': 33, u'name': u'katie', u'pet': u'Cisco'}]}
# 将python字符串转换成json形式
asjson = json.dumps(result)
```
pandas团队正致力于开发原生的高效json导出(to_json)和解码(from_json)功能，待续.........

#### XML和HTML解析
使用lxml.html处理HTML内容

```python
from lxml.html import parse
from urllib2 import urlopen

parsed = parse(urlopen('http://finance.yahoo.com/xxxx/xxx/xxx///xxxx'))
doc = parsed.getroot()
# 通过doc可以获得特定类型的所有html标签(tag)，比如table等

links = doc.findall('.//a')   # 链接
links[0].get('href')
$-> 'http://baidu.com'
links[0].text_content()
$-> '百度一下'
```
处理表格，'.//table'
表格的每一行都是 './/tr'
表格的第一行是标题行，th表示单元格
余下的行是数据行，td表示单元格
```python
from pandas.io.parsers import TextParser
# 下面的是解析函数,解析一行数据
def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content() for val in elts]

# 解析整个表格，返回一个DataFrame对象
def parse_table(table):
    rows = table.findall('.//tr')
    header = _unpack(row[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    # TextParser将数值型的列进行类型转化
    return TextParser(data, names=header).get_chunk()

# 定位所有的表格
tables = doc.findall('.//table')
tab = tables[0]
parse_table(tab)
```

使用lxml.objectify处理XML内容
root.INDICATOR用于返回一个用于产生各个XML元素的生成器。
```python
from lxml import objectify

parsed = objectify.parse(open('hello.xml'))
root = parsed.getroot()
root.get('href')
$-> 'http://baidu.com'
root.text
$-> '百度一下'

data = []

for elt in root.INDICATOR:
    el_data = {}
    for child in elt.getchildren():
        el_data[child.tag] = child.pyval
    data.append(el_data)
# 转化成DataFrame
perf = DataFrame(data)
```

#### 二进制数据和Excel文件
pandas对象有一个将数据以pickle序列化形式保存到磁盘上的方法：save
```python
# 写入磁盘
frame.save('filename')
# 读入内存
frame = pd.load('filename')
```

使用xlrd包和openpyxl包(需要安装)读写xls或者xlsx文件
```python
# 创建ExcelFile示例
xls_file = pd.ExcelFile('data.xls')
# 存放在某个工作表中的数据可以通过parse读取到DataFrame中
table = xls_file.parse('sheet1')
```

#### 使用数据库
关系型数据库
```python
import sqlite3

# create table
query = """
create table test
(a varchar(20),
 b integer);"""
con = sqlite3.connect(':memory:')
con.execute(query)
con.commit()

# insert
data = [('tom',20),('jerry',15)]
stmt = "insert into test values(?,?)"
con.executemany(stmt, data)
con.commit

# query, select返回元组列表(大部分python SQL驱动器都这样)
cursor = con.execute('select * from test')
rows = cursor.fetchall()
print(rows)

# 由于这样产生DataFrame的方法比较复杂，所以有现成的方法
import pandas.io.sql as sql
sql.read_frame('select * from test', con)
```

非关系型数据库
非关系型数据库有多种方式，有些是字典键值对形式存在，另一些是基于文档的，这里不再赘述。
