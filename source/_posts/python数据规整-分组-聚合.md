---
title: python数据规整_分组_聚合
date: 2016-08-15 19:09:26
tags: [python, 数据分析]
categories:
---

#### 数据合并
##### DataFrame合并
```python
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
pd.merge(***)
```
###### merge方法
<center>merge函数的参数</center>

|param|explanation|param|explanation|
|:---:|:---------:|:---:|:---------:|
|left|左侧的DataFrame|right|右侧的DataFrame|
|how|连接方式，inner、outer、left、right，默认为inner|on|指定连接的列名|
|left_on|左侧DataFrame用于连接的键名|right_on|右侧DataFrame用于连接的键名|
|left_index|将左侧的行索引用作其连接键|right_index|将右侧的行索引用作其连接键|
|sort|对合并后的数据在连接键上排序，默认为True|suffixes|重叠列名后缀，用于重复列名区分|
|copy|默认为True，设置为False可以避免将数据复制到结果数据结构中|--------|---------|

```python
left1 = DataFrame({'key':['a','b','a','a','b','c'], 'value':range(6)})
$-> key  value
0   a      0
1   b      1
2   a      2
3   a      3
4   b      4
5   c      5

right1 = DataFrame({'group_val':[2,5]},index=['a','b'])
$-> group_val
a          2
b          5

pd.merge(left1, right1, left_on='key', right_index=True)
$-> key  value  group_val
0   a      0          2
2   a      2          2
3   a      3          2
1   b      1          5
4   b      4          5
```
<b>层次化索引应当以列表的形式指明用作合并键的多个列<b>

###### join方法
- join方法可以更为方便地实现按索引合并
- 可以合并多个带有相同或相似索引的DataFrame对象

```python
# on指定调用者的连接键
left.join(right, how='', on='')

# 多个DataFrame合并
another = DataFrame(....)
left2.join([right2, another])
```

###### concat方法
concat方法用于轴向连接、绑定、堆叠操作
numpy有一个合并原始NumPy数组的concatenate的函数

```python
arr = np.arange(12).reshape((3,4))
# axis=1水平连接，axis=0垂直连接
np.concatenate([arr, arr], axis=1)
```

```python
s1 = Series([0,1], index=['a', 'b'])
s2 = Series([2,3,4], index=['c','d', 'e'])
s3 = Series([5,6], index=['f', 'g'])
# 默认 axis=0
pd.concat([s1, s2, s3])
$-> a    0
	b    1
	c    2
	d    3
	e    4
	f    5
	g    6
	dtype: int64

pd.concat([s1, s2, s3], axis=1)
$-> 0    1    2
a  0.0  NaN  NaN
b  1.0  NaN  NaN
c  NaN  2.0  NaN
d  NaN  3.0  NaN
e  NaN  4.0  NaN
f  NaN  NaN  5.0
g  NaN  NaN  6.0
```
<center>concat函数的参数</center>

|param|explanation|param|explanation|
|:---:|:---------:|:---:|:---------:|
|objs|参与连接的pandas对象的列表或字典，必需参数|axis|指明连接轴向，默认为0，参考上面示例|
|join|连接方式，inner、outer，默认为outer|join_axes|指明其他n-1条轴的索引，不执行并集、交集运算|
|keys|用于形成连接轴上的层次化索引|levels|指定层次化索引上各级别的索引|
|names|用于创建分层级别的索引，如果设置了keys和levels的话|verify_integrity|检查结果对象新轴上的重复对象|
|ignore_index|不保留连接轴上的索引，产生新索引range()|-----|---------------|

<b>重塑层次化索引</b>
- stack 将数据的列‘旋转’为行
- unstack 将数据的行‘旋转’为列

```python
data = DataFrame(np.arange(6).reshape((2,3)), index=pd.Index(['Ohio','Colorado'],name='state'), columns=pd.Index(['one','two','three'],name='number'))
$-> data
number    one  two  three
state
Ohio        0    1      2
Colorado    3    4      5

result = data.stack()
result
$-> state     number
	Ohio      one       0
          	  two       1
              three     2
	Colorado  one       3
              two       4
              three     5
	dtype: int32

result.unstack()
$-> number    one  two  three
	state
	Ohio        0    1      2
	Colorado    3    4      5

# unstack(和stack一样)默认操作的是最内层地址，给函数传入层次级别的编号或者名称即可在不同级别操作。
result.unstack(0)
$-> state   Ohio  Colorado
	number
	one        0         3
	two        1         4
	three      2         5
result.unstack('state')  # 效果同上
```
unstack操作可能会产生缺失值，而stack操作默认会过滤缺失值，可以设置参数dropna=False取消。


#### 数据转换
##### 去重
- DataFrame的duplicated()方法返回一个bool型Series实例，指示每一行是否是重复行
- DataFrame的drop_duplicates()方法返回一个移除重复行的DataFrame
- drop_duplicates()默认保留第一个出现的值组合，设置take_last=True则保留最后一个
- 指定部分列进行重复项判断，drop_duplicates(['a1', 'a2'])

##### 替换
- Series中的replace函数可以进行替换操作
- data.replace(a, b)
- data.replace([a1, a2], b)
- data.replace([a1, a2], [b1, b2])

##### 映射
- Series的map方法接受一个函数，或者含有映射关系的字典对象，返回一个映射后的Series对象
- data.map(str.lower)
- data.map(lambda x : str.lower(x))

##### 离散化与bin划分
- cut函数

```python
ages = [20,22,25,27,21,23,37,31,61,45,41,32]
bins = [18, 25, 35, 60 ,100]

# 将ages按照bins划分进行切割
# 直接切割得到的区间是左开右闭的，设置right=False可以得到左闭右开区间
# 设置参数labels=['a1','a2',...,'an']可以更改区间名称
# 也可以不传入bins，直接传入整数n表示分成n个区间，函数会根据最值等间距划分

cats = pd.cut(ages, bins)
cats
$-> [(18, 25], (18, 25], (18, 25], (25, 35], (18, 25], ..., (25, 35], (
	  60, 100], (35, 60], (35, 60], (25, 35]]
	Length: 12
	Categories (4, object): [(18, 25] < (25, 35] < (35, 60] < (60, 100]
	]

cats.codes   #每个数据的标签
$-> array([0, 0, 0, 1, 0, 0, 2, 1, 3, 2, 2, 1], dtype=int8)
cats.categories  #区间信息
$-> Index([u'(18, 25]', u'(25, 35]', u'(35, 60]', u'(60, 100]'], dtype='object')

# 简单统计
pd.value_count(cats)
$-> (18, 25]     5
	(35, 60]     3
	(25, 35]     3
	(60, 100]    1
	dtype: int64
```

- qcut函数根据样本分位数对样本进行划分，可以使得每个bin中的数据数量比较接近

```python
data = np.random.rand(1000)
# 5分位数
cats = pd.qcut(data, 5)
pd.value_counts(cats)
$-> (0.813, 1]           200
	(0.628, 0.813]       200
	(0.421, 0.628]       200
	(0.223, 0.421]       200
	[0.000386, 0.223]    200

# 自定义的分位数
cats = pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.0])
pd.value_counts(cats)
$-> (0.539, 0.901]       400
	(0.127, 0.539]       400
	(0.901, 1]           100
	[0.000386, 0.127]    100
	dtype: int64
```

##### 检测和过滤异常值
```python
data = DataFrame(np.random.randn(1000,4))
col = data[3]
# 找出某一列中绝对值大于3的值
col[np.abs(col) > 3]
# 找出data中全部大于3的值
data[(np.abs(data) > 3).any(1)]

# 替换异常值
data[np.abs(data) > 3] = 1
```

##### 排列和随机采样
```python
np.random.permutation(5)
# 整数采样，从[0,5)区间上采，样本空间为20
np.random.randint(0,5,20)
```

##### 计算指示变量、哑变量
本节的作用是将分类变量转换为‘哑变量矩阵’（dummy matrix）或‘指示变量矩阵0-1’（indicator matrix）.如果DataFrame中的某一列有k个不同的值，则可以派生出一个k列矩阵或DataFrame
```python
data = DataFrame({'key':['a','b','a','c','d'],'value':range(5)})
pd.get_dummies(data['key'])
$-> a    b    c    d
0  1.0  0.0  0.0  0.0
1  0.0  1.0  0.0  0.0
2  1.0  0.0  0.0  0.0
3  0.0  0.0  1.0  0.0
4  0.0  0.0  0.0  1.0
# 为新生成的列名添加前缀
pd.get_dummies(data['key'], prefix='new_')
```

##### 字符串操作
###### python内置的字符串库
- strip() 修剪空白符、换行符
- split('xx') 字符串分割
- a.join(list): 在字符串a后面接上列表list（或元组）里所有的元素
- str.index(',') 在字符串str中找到','的位置，如果找不到则抛出异常
- str.find(',') 在字符串str中找','，找到返回第一个位置，找不到返回-1
- str.rfind(',') 在字符串str中找','，找到返回最后一个位置，找不到返回-1
- str.count(',') 统计str中','的个数
- str.replace('aa','a') 替换
- str.lower(), upper()  大小写转换
- str.ljust(n), rjust(n) 用空白字符填充以满足最小长度n

###### 正则表达式
- 正则表达式是用于处理字符串的强大工具，拥有自己独特的语法以及一个独立的处理引擎，效率上可能不如str自带的方法，但功能十分强大。得益于这一点，在提供了正则表达式的语言里，正则表达式的语法都是一样的，区别只在于不同的编程语言实现支持的语法数量不同。下图展示了使用正则表达式进行匹配的流程：
<center>![](http://ww4.sinaimg.cn/mw690/9bcfe727jw1f6unc8s9fzj20d605w0ue.jpg)</center>

- 下图列出了Python支持的正则表达式元字符和语法：
<center>![](http://ww3.sinaimg.cn/mw690/9bcfe727jw1f6unc85kmxj20m71brniv.jpg)</center>

- 正则表达式通常用于在文本中查找匹配的字符串。Python里数量词默认是贪婪的（在少数语言里也可能是默认非贪婪），总是尝试匹配尽可能多的字符；非贪婪的则相反，总是尝试匹配尽可能少的字符。例如：正则表达式"ab*"如果用于查找"abbbc"，将找到"abbb"。

- 与大多数编程语言相同，正则表达式里使用"\"作为转义字符，这就可能造成反斜杠困扰。假如你需要匹配文本中的字符"\"，那么使用编程语言表示的正则表达式里将需要4个反斜杠"\\\\"：前两个和后两个分别用于在编程语言里转义成反斜杠，转换成两个反斜杠后再在正则表达式里转义成一个反斜杠。Python里的原生字符串很好地解决了这个问题，这个例子中的正则表达式可以使用r"\\"表示。同样，匹配一个数字的"\\d"可以写成r"\d"。

- re模块。Python通过re模块提供对正则表达式的支持。使用re的一般步骤是先将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果（一个Match实例），最后使用Match实例获得信息，进行其他的操作。

```python
import re
```

1. compile
re.compile(strPattern[, flag])
用于将字符串形式的正则表达式编译为Pattern对象,第二个参数flag是匹配模式，取值可以使用按位或运算符'|'表示同时生效。flag的可选值有：
re.I(re.IGNORECASE): 忽略大小写（括号内是完整写法，下同）
M(MULTILINE): 多行模式，改变'^'和'$'的行为（参见上图）
S(DOTALL): 点任意匹配模式，改变'.'的行为
L(LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
U(UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
X(VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释

2. match
match(string[, pos[, endpos]]) | re.match(pattern, string[, flags])
这个方法将从string的pos下标处起尝试匹配pattern；如果pattern结束时仍可匹配，则返回一个Match对象；如果匹配过程中pattern无法匹配，或者匹配未结束就已到达endpos，则返回None。
pos和endpos的默认值分别为0和len(string)；re.match()无法指定这两个参数，参数flags用于编译pattern时指定匹配模式。 注意：这个方法并不是完全匹配。当pattern结束时若string还有剩余字符，仍然视为成功。想要完全匹配，可以在表达式末尾加上边界匹配符'$'。
3. split
split(string[, maxsplit]) | re.split(pattern, string[, maxsplit])
按照能够匹配的子串将string分割后返回列表。maxsplit用于指定最大分割次数，不指定将全部分割。
4. findall
findall(string[, pos[, endpos]]) | re.findall(pattern, string[, flags])
搜索string，以列表形式返回全部能匹配的子串
5. finditer
finditer(string[, pos[, endpos]]) | re.finditer(pattern, string[, flags])
搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器
6. sub
sub(repl, string[, count]) | re.sub(pattern, repl, string[, count])
使用repl替换string中每一个匹配的子串后返回替换后的字符串。
当repl是一个字符串时，可以使用\id或\g<id>、\g<name>引用分组，但不能使用编号0。
当repl是一个方法时，这个方法应当只接受一个参数（Match对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
count用于指定最多替换次数，不指定时全部替换。
7. subn
subn(repl, string[, count]) |re.sub(pattern, repl, string[, count])
返回 (sub(repl, string[, count]), 替换次数)

<b>[原文地址与示例](http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html)<b>

###### pandas中矢量化的字符串操作
通过Series的str方法获取Series中值得字符串内容，函数示例
- data.str.constins('hello'), 返回一个bool型的Series对象
- data.str.findall(pattern,flags=re.IGNORECASE)
- matches = data.str.match(pattern, flags=re.IGNORECASE)
- matches.str.get(1) 矢量化元素获取
- matches.str[1] 矢量化元素获取(效果和上一个一致),也支持分片操作

<center>矢量化的字符串方法</center>

|method|explanation|method|explanation|
|:----:|:---------:|:----:|:---------:|
| cat |元素级的字符串连接操作，可指定分隔符| contains |返回各字符串是否包含指定模式的bool数组|
| count |模式出现的次数| endswith,startswith |各元素是否以指定的模式开头、结尾，返回bool数组|
| findall |计算各字符串的模式列表| get |获取各元素的第i个字符|
| join |根据指定的分隔符将各元素的字符串连接起来| len |计算各字符串的长度|
| lower,upper |大小写转换| match |根据给定模式，执行re.match()|
| pad |在字符串左边/右边或两边添加空白符| center |相当于pad(side='both')|
| repeat |重复操作，在字符串上就是多个相同的拼接| replace |替换指定模式|
| slice |对各个字符串进行子串分片操作|split |根据指定模式，对字符串切割|
|strip,rstrip,lstrip |去空白符，换行符| | |


#### 数据聚合
```python
df
$->   data1     data2 key1 key2
0  2.128648  0.552487    a  one
1  2.040146 -0.974248    a  two
2 -1.442976 -0.404534    b  one
3  1.796789 -1.413561    b  two
4  0.429355  0.604959    a  one

```
##### GroupBy
- groupby用于DataFrame上，假定要按‘key’进行分组，并计算‘value’列的值，默认在axis=0上分组
- grouped = df['value'].groupby(df['key'])   grouped是一个GroupBy对象，只包含一些有关分组建的中间数据
- 上面的等价语法为：df.groupby(df['key'])['value']或者df.groupby(df['key'])[['value']]
- grouped.mean()  使用GroupBy的方法进行计算
- 分组键可以不止一个，groupby(df['key1','key2'])，得到层次索引结果
- 分组键可是任意长度适当的数组，可以是字符串、数字或其他python对象，比如'key1'，也可以按照列的类型dtype进行分组: df.groupby(df.dtypes, axis=1)
- df.groupby(df['key']).mean() 对df的所有数值列求值，非数值列自动忽略
- df.groupby(df['key']).size() 返回含有分组大小的Series
- grouped.describe()等方法也是可以用在这里的

##### 分组迭代
- GroupBy对象支持迭代，可以产生一组二元分组（由分组名和数据块组成）
- for name,group in df.groupby(df['key']) 将返回df['key']每一种可能的值以及其对应的df行集合
- for (k1, k2),group in df.groupby(df['key1', 'key2'])

groupby对象字典化
```python
grouped = df.groupby('key1')

glist = list(grouped)  # glist中包含的是(分组名, 数据块)组成的元组
$-> [('a',
	    data1     data2 key1 key2
  0  2.128648  0.552487    a  one
  1  2.040146 -0.974248    a  two
  4  0.429355  0.604959    a  one),
     ('b',
        data1     data2 key1 key2
  2 -1.442976 -0.404534    b  one
  3  1.796789 -1.413561    b  two)]

gdict = dict(glist)  # 字典化
$-> {'a':       data1     data2 key1 key2
 		0  2.128648  0.552487    a  one
 		1  2.040146 -0.974248    a  two
 		4  0.429355  0.604959    a  one,
     'b':       data1     data2 key1 key2
 		2 -1.442976 -0.404534    b  one
 		3  1.796789 -1.413561    b  two}

dict(list(df.groupby(df.dtypes, axis=1)))
```

##### 分组
###### 通过字典或者Series进行分组
比如说现在dataframe有列'a','b','c','d','e'，通过如下代码
```python
mapping = {'a':'red','b':'blue','c':'red','d':'red','e':'blue'}
# 将字典传给groupby函数，设置axis=1（这是合并列）
by_column = df.groupby(mapping, axis=1)
by_column.sum()  # 对映射到相同名称的列求和，结果的列只有'red'和'blue'

# Series也有同样的功能
map_series(mapping)
df.groupby(map_series, axis=1).sum()
```
###### 通过函数进行分组
比如说索引为字符串，若想按照字符串长度进行分组，则可以：
```python
df.groupby(len).sum()

# 将函数跟数组、列表、字典等结合起来使用也可以
key_list = ['one','one','one','two','two']
df.groupby([len, key_list]).sum() # 得到一个层次化索引的结果
```
###### 通过索引级别进行分组
通过level关键字传入级别编号或名称，按照索引级别进行分组
```python
columns = pd.MultiIndex.from_arrays([['US','US','US','JP','JP'],[1,3,5,1,3]], names=['country','tenor'])
df = DataFrame(np.random.randn(4,5), columns=columns)
df.groupby(level='country', axis=1).count()
$->
country  JP  US
0         2   3
1         2   3
2         2   3
3         2   3
```

##### 聚合方法
自定义聚合函数，将其传入<b>agg或者aggregate方法</b>即可
<center>经过优化的groupby方法，可以传入函数名字符串进行调用</center>

|method|explanation|method|explanation|
|:----:|:---------:|:----:|:---------:|
|count|分组中非NAN值的数量|sum|非NAN值的和|
|mean|非NAN值的均值|median|非NAN值的中值|
|std,var|无偏(分母n-1)标准差和方差|min,max|非NAN值的最值|
|prod|非NAN值的乘积|first,last|第一个、最后一个非NAN值|

###### 面向列的多函数应用
```python
# 传入一个函数列表执行多个函数，每个函数的执行结果单成一列
grouped['data3'].agg(['mean', 'std', my_function])

# 传入由(name, function)元组组成的列表时，每个元组第一个元素成为结果DataFrame的列名，第二个元素是对应此列名上的函数
grouped.agg([('data1','mean'), ('data2','std')])

# 不同的列对应不同的函数，可传入字典
grouped.agg({'data1':['min','max'], 'data2':[np.max, 'std'])
```

###### 聚合结果索引变换
python聚合返回结果时，向groupby函数传入: <b>as_index=False<b> 取消由分组键形成索引，而是将分组键变成列，把简单数字作为索引。对结果调用reset_index()也能得到这样的结果。


#### 分组运算与转换
##### transform
transform函数接收一个函数，并将这个函数应用到各个分组，然后将每个分组的结果放置在这个分组对应的每一个元素上，最后显示它。
```python
people
$->
               a         b         c         d         e
Joe    -0.338386  0.849100 -1.951048 -1.153923 -1.672975
Steve  -0.490588  0.408497 -0.692801 -0.100917  0.970808
Wes    -1.603786       NaN       NaN -0.534380  0.847692
Jim     0.309432  2.768331 -0.454094 -1.026735 -0.679794
Travis -1.400938 -0.865599 -0.190541 -0.835916  0.315975

key=['one','two','one','two','one']
people.groupby(key).mean()
$->      a         b         c         d         e
one -1.114370 -0.008250 -1.070794 -0.841406 -0.169769
two -0.090578  1.588414 -0.573447 -0.563826  0.145507

people.groupby(key).transform(np.mean)
$->         a         b         c         d         e
Joe    -1.114370 -0.008250 -1.070794 -0.841406 -0.169769
Steve  -0.090578  1.588414 -0.573447 -0.563826  0.145507
Wes    -1.114370 -0.008250 -1.070794 -0.841406 -0.169769
Jim    -0.090578  1.588414 -0.573447 -0.563826  0.145507
Travis -1.114370 -0.008250 -1.070794 -0.841406 -0.169769

# 传入自定义的函数也可以，需要注意的是自定义函数的输入参数是已经分好组的各个分组
def my_function(arr):
	return arr-arr.mean()
```

##### apply：拆分-应用-合并
- apply 将待处理的对象拆成多个分段，然后对各分段调用传入的函数，最后尝试将各分段组合到一起
- 分段组合需要用到pandas.concat函数
- apply 传入函数名，这里传入的函数需要包括：分好组的DataFrame分段，也可以包括一些其他的参数


```python
# 取列'tip_pct'排前五的记录
def top(df, n=5, col='tip_pct'):
	return df.sort_index(by=col)[-n:]
df.groupby('smoker').apply(top)

# 禁止分组键
df.groupby('smoker', group_keys=False).apply(top)
```

###### 分位数和桶分析
- pandas中面元划分、样本分位数划分的函数cut和qcut可以和groupby结合起来
- 函数cut和qcut返回的对象可以作为groupby函数的参数

```python
def get_status(group):
	return {'min':group.min, 'max':group.max, 'count':group.count}

factor = pd.cut(df.data1, 4) # labels=False，只获取分位数编号
grouped = df.data2.groupby(factor)
grouped.apply(get_status).unstack()
```

##### 透视表与交叉表
###### 透视表
- 根据一个或多个键对数据进行聚合，并根据行和列上的分组键将数据分配到各个矩形区域中
- DataFrame有个pivot_table函数
- 顶级函数：pandas.pivot_table

<center>pivot_table的参数</center>

|method|explanation|method|explanation|
|:----:|:---------:|:----:|:---------:|
|values|待聚合列的名称，默认为所有数值列|rows|用于分组的列名或其他分组键，出现在结果透视图的行|
|cols|用于分组的列名或其他分组键，出现在结果透视图的列|aggfunc|聚合函数或函数列表，默认为mean。可以是任何对groupby有效的函数|
|fill_value|用于替换结果表中的缺失值|margin|添加行列小计，默认为False|

```python
# 第一个参数是表格内容，如果不设置，则默认为pivot_table中的默认聚合类型
# 设置参数 rows，设置行内容和索引，
# 设置参数 cols，设置列内容和索引
tips.pivot_table(['tip_pct','size'], rows=['sex','day'], cols='smoker')

# 设置：margins=True，添加分项小计，默认为平均值
tips.pivot_table(['tip_pct','size'], rows=['sex','day'], cols='smoker', margins=True)
# 要使用其他小计函数，可以使用：aggfunc参数
tips.pivot_table(['tip_pct','size'], rows=['sex','day'], cols='smoker', margins=True,aggfunc='sum')
```
###### 交叉表
- 交叉表是一种用于计算分组频率的特殊透视表
- pandas.crosstab函数可以统计交叉表

```python
# param1: 用于分组的列名或其他分组键，出现在结果透视图的行
# param2: 用于分组的列名或其他分组键，出现在结果透视图的列
# margins=True：行、列小计
pd.crosstab(param1, param2, margins=True)
```






