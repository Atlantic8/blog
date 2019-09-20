---
title: pandas初步
date: 2016-05-17 22:34:11
tags: [pandas, python]
---
#### Series
Series类似于一维数组对象，由一组数据和其对应的标签组成，仅由一组数据即可产生简单的Series：
```python
from pandas import Series, DataFrame
import pandas as pd

obj = Series([4,7,-5,3])
obj.index
$-> RangeIndex(start=0, stop=4, step=1)
obj.values
$-> array([ 4,  7, -5,  3], dtype=int64)

obj2 = Series([4,7,-5,3], index=['a','b','c','d'])
# a 4, b 7, c -5, d 3
obj2['a']
$-> 4
obj2[['a','b']]
$-> {'a':4, 'b':7}
obj2[obj2 > 3]
$-> {'a':4, 'b':7}

#也可以将Series看成一个字典， index是key， values是value
'b' in obj2
$-> true
#可以通过字典建立Series
obj3 = Series({'a':4, 'b':7, 'c':-5, 'd':3})

sdata = {'Ohio':35000,'Texas':71000,'Oregon':16000,'Utah':5000}
states=['California','Ohio','Oregon','Texas']
obj4=Series(sdata,index=states)
$-> California        NaN
    Ohio          35000.0
    Oregon        16000.0
    Texas         71000.0
obj4.isnull()
$-> California     True
    Ohio          False
    Oregon        False
    Texas         False

#Series对象有一个name属性
obj4.name = 'population'
```

#### DataFrame
表格型数据，有行索引和列索引
```python
data = {'state':['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year':[200,2001,2002,2001,2002],
        'pop':[1.5,1.7,3.6,2.4,2.9]}
frame = DataFrame(data)
$->   pop   state  year
   0  1.5    Ohio   200
   1  1.7    Ohio  2001
   2  3.6    Ohio  2002
   3  2.4  Nevada  2001
   4  2.9  Nevada  2002
```
指定列名，列会按照columns制定的顺序排列
```python
DataFrame(data, columns=['year', 'state', 'pop'])
```
指定index，如果index元素不在columns中，产生一列 NaN 值
```python
DataFrame(data, columns=['year','state','pop'], index=['year','state','pop','A'])

# 获取DataFrame的一个列，成为一个Series
# 相同的index，name属性就是对应的列名
frame['year']  &  frame.year

# 获取列名，删除一列
frame.columns
$->  Index([u'pop', u'state', u'year'], dtype='object')
del frame.year
```
嵌套字典构造DataFrame，外层的key作为列属性，里层的key作为行属性
```python
pop = {'Nvidia':{2001:2.4, 2002:2.9}, 'AMD':{2000:1.5,2001:1.7,2002:3.6}}
frame3 = DataFrame(pop)，加上index=[],重新设置index值
$->       AMD  Nvidia
    2000  1.5     NaN
    2001  1.7     2.4
    2002  3.6     2.9
frame3.T
$->         2000  2001  2002
    AMD      1.5   1.7   3.6
    Nvidia   NaN   2.4   2.9

# 设置行、列属性的name,设置完了也会打印出来
frame3.index.name = 'year'
frame3.columns.name = 'state'
# 显示DataFrame中的数据，ndarray形式
frame3.values
$-> array([[ 1.5,  nan],
          [ 1.7,  2.4],
          [ 3.6,  2.9]])
```
##### DataFrame构造器

|    data type    |        explain        |
|:---------------:|:----------------------------------:|
| 二维ndarray | 数据矩阵，还可以传入行标和列标 |
| 由数组、列表或元组组成的字典 | 每个序列会变成DataFrame的一列，所有序列长度必须相同 |
| NumPy的结构化/记录数据 | 类似于由数组组成的字典 |
| 由Series组成的字典 | 每个Series组成一列。没有显示指定index的话，各Series的index会被合并成结果的行index |
| 由字典组成的字典 | 各内层字典组成一列，键合并成行index |
| 字典或Series的列表 | 各项成为DataFrame的一行，字典键或Series索引的并集将成为列index |
| 由列表或元组组成的列表 | 类似于ndarray |
| 另一个DataFrame | 原来DataFrame的索引会被保留，除非显示指定 |
| NumPy的MaskedArray | 类似于ndarray，只是掩码值在结果DataFrame会变成NaN/缺失值 |

##### 索引对象<immutable>
```python
obj = Series(range(3), index=['a','b','c'])
index = obj.index
index[1] = 'x'
$-> TypeError: Index does not support mutable operations
```
重新索引,如果某个索引值当前不存在，引入缺失值
```python
# 重新索引列index
obj = Series([1,2,3], index=['a','b','c'])
obj2 = obj.reindex(['a','b','c','d'], fill_value=0)
# 重新索引行/列index
obj2 = obj.reindex(['a','b','c','d'], fill_value=0, columns=['x','y','z'])
# 也可以使用
frame.ix[['a','b','c','d'], ['x','y','z']]
```
处理时间序列数据时，可能需要一些插值处理，method选项
ffill | pad      : 前向填充(搬运)
bfill | backfill : 后向填充(搬运)
```python
obj3=Series(['blue','red','yellow'], index=[0,2,3])
obj3.reindex(range(6), method='ffill')
$-> 0      blue
    1      blue
    2       red
    3    yellow
    4    yellow
    5    yellow
    dtype: object
```
丢弃指定轴上的项
```python
obj = Series([1,2,3], index=['a','b','c'])
obj.drop('c')
$-> a    1
    b    2
    dtype: int64
```
##### 索引、选取和过滤
```python
obj = Series(np.arange(4.), index=['a','b','c','d'])
obj[0]
$-> 0.0
obj['b':'d']
$-> b    1.0
    c    2.0
    d    3.0
    dtype: float64
# b c d 对应的都设置为5
obj['b':'d'] = 5

data = DataFrame(np.arange(16).reshape((4,4)), columns=['a','b','c','d'], index=['A','B','C','D'])
data > 5
$-> upper      a      b      c      d
    A      False  False  False  False
    B      False  False   True   True
    C       True   True   True   True
    D       True   True   True   True
data[data < 5] = 0
$-> upper   a   b   c   d
    A       0   0   0   0
    B       0   5   6   7
    C       8   9  10  11
    D      12  13  14  15
```

##### DataFrame的索引选项

|    data type    |        explain        |
|:---------------:|:----------------------------------:|
| obj[val] | 选取DataFrame的单个列或一组列 |
| obj.ix[val] | 选取DataFrame的单个行或一组行 |
| obj.ix[:,val] | 选取单个列或列子集 |
| obj.ix[val1,val2] | 同时选取行和列 |
| reindex方法 | 匹配一个或多个轴到新索引 |
| xs方法 | 根据标签选取当行或单列，返回一个Series |
| icol,irow方法 | 根据整数选取当行或单列，返回一个Series |
| get_value | 根据行列标签获取对应值 |
| set_value | 根据行列标签设置对应值 |

##### 算术运算和数据对齐
Series对象可以叠加，对应index相加，没有对应index相加的是 NaN
DataFrame对象也可以相加，行和列都相加
为了不得到NaN，可以使用add函数，设置fill_value
```python
df1.add(df2, fill_value=0)
# other operants
df1.sub(df2, fill_value=0)
df1.div(df2, fill_value=0)
df1.mul(df2, fill_value=0)
```

##### 函数应用和映射
NumPy的ufunc也可以用于操作pandas对象
```python
frame = DataFrame(np.random.randn(4,3),columns=list('bde'),index=list('xyzw'))
# 绝对值
np.abs(frame)
```
DataFrame的apply方法
```python
frame = DataFrame(np.random.randn(4,3),columns=list('bde'),index=list('xyzw'))
f = lambda x: x.max()-x.min()
frame.apply(f)
# 除标量外，传递给apply的函数还可以返回多个值组成的Series
def f(x):
    return Series([x.min(), x.max()], index=['min', 'max'])
frame.apply(f)
$->             b         d         e
    min -0.983954 -0.578884 -0.916169
    max  1.111333  0.982841  0.663686
```

##### 排序和排名
```python
obj = Series(range(4), index=['a','d',b','c'])
obj.sort_index() # order by index
$-> a    0.0
    b    1.0
    c    2.0
    d    3.0
    dtype: float64
obj.order() # 按值排序, NaN都放最后
$-> a    0.0
    b    1.0
    c    2.0
    d    3.0
    dtype: float64

# DataFrame对象也可以排序
frame.sort_index(axis=0)
frame = DataFrame({'a':[1,2,3], 'b':[4,5,6]})
# 按照a和b排序，降序
frame.sort_index(by=['a','b'],ascending=False)
```

##### 重复值轴索引
```python
obj = Series(range(5), index=['a','a','b','b','c'])
obj.index.is_unique
$-> False
```

##### 汇总和计算描述统计
```python
df = DataFrame([[1.4,np.nan],[7.1,-4.5],[np.nan,np.nan],[0.75,-1.3]],index=['a','b','c','d'],columns=['one','two'])
# ax=1时按行求和，ax=0时按列求和
# skipna=True会忽略NaN(默认)
df.sum(axis=ax, skipna=False)

# idxmin/idxmax返回间接统计索引
df.idxmax()
$-> one    b
    two    d
    dtype: object
df.cumsum()
$->     one  two
    a  1.40  NaN
    b  8.50 -4.5
    c   NaN  NaN
    d  9.25 -5.8
df.describe() # 一次性产生多个汇总统计
$->             one       two
    count  3.000000  2.000000
    mean   3.083333 -2.900000
    std    3.493685  2.262742
    min    0.750000 -4.500000
    25%         NaN       NaN
    50%         NaN       NaN
    75%         NaN       NaN
    max    7.100000 -1.300000
```

|    method    |        explain        |
|:---------------:|:----------------------------------:|
| count | 非NaN值的数量 |
| describe | 汇总统计 |
| min,max | 最大、最小值 |
| argmin,argmax | 最小、最大值的索引位置 |
| idxmin,idxmax | 最小、最大值的索引 |
| quantile | 计算样本的分位数 |
| sum,mean,median | 总和、均值、中位数 |
| mad | 根据平均值计算平均绝对离差 |
| var,std | 样本方差、标准差 |
| skew | 样本值的偏度(三阶矩) |
| kurt | 样本值的峰度(四阶矩) |
| cumsum | 样本累计和 |
| cummin,cummax | 样本累计最小、最大值 |
| cumprod | 样本累计积 |
| diff | 计算一阶差分(时间序列数据) |
| pct_change | 计算百分数变化 |

相关系数和协方差
```python
# 列表之间的相关系数、协方差
frame.col1.corr(frame.col2)
frame.col1.cov(frame.col2)
# DataFrame的相关系数、协方差，是指各个列之间的相关系数、协方差
frame.corr()
$->           b         d         e
    b  1.000000 -0.911353  0.324945
    d -0.911353  1.000000 -0.252583
    e  0.324945 -0.252583  1.000000
frame.cov()
$->           b         d         e
    b  0.591176 -0.292541  0.347585
    d -0.292541  0.174294 -0.146703
    e  0.347585 -0.146703  1.935457
# x可以是Series或者是DataFrame
frame.corrwith(x)
```

##### 唯一值、值计数和成员资格
```python
obj = Series(['a','b','c','b','a','c','d','b'])
obj.unique()
$-> array(['a', 'b', 'c', 'd'], dtype=object)
obj.value_counts()
$-> b    3
    c    2
    a    2
    d    1
    dtype: int64
pd.value_counts(obj.values, sort=False)
# Series中的所有元素是否在参数中
mask = obj.isin(['b','c'])
$-> 0    False
    1     True
    2     True
    3     True
    4    False
    5     True
    6    False
    7     True
    dtype: bool
obj[mask]
$-> 1    b
    2    c
    3    b
    5    c
    7    b
    dtype: object
```

##### 缺失数据处理
|    method    |        explain        |
|:---------------:|:----------------------------------:|
| dropna | 根据标签值中是否存在缺失数据对轴标签进行过滤，可通过阈值调节容忍度 |
| fillna | 用指定值或插值方法填充缺失数据 |
| isnull | 布尔值列表，True表示缺失值/NA |
| notnull | 与isnull相反 |

```python
from numpy import nan as NA
data = Series([1,NA,3.5,NA,7])
# 舍弃包含NA的行或列，加上how='all'后舍弃全是NA的行或列
# 默认是行，设置axis=1变成列！
data.dropna()  data.dropna(how='all')
data.[data.notnull()]

# 替换NA，返回新对象
# 设置inplace=True对现有对象就地修改
data.fillna(0)
```

##### 层次化索引
```python
data = Series(np.random.randn(10),index=[['a','a','a','b','b','b','c','c','d','d'],[1,2,3,1,2,3,1,2,2,3]])
$-> a  1    0.506070
       2   -2.293016
       3    1.391751
    b  1   -1.218733
       2    0.390983
       3    1.462456
    c  1    0.162262
       2   -0.091724
    d  2    0.321799
       3    0.203933
```
取值方法
```python
data['b']
data['b':'c']
data[:,2] # 二层取值

# unstack可以将这种数据重新安装到DataFrame中
# stack是unstack的逆操作
data.unstack()
$->           1         2         3
    a  0.506070 -2.293016  1.391751
    b -1.218733  0.390983  1.462456
    c  0.162262 -0.091724       NaN
    d       NaN  0.321799  0.203933

# DataFrame可以使用分层索引
frame = DataFrame(np.arange(12).reshape((4,3)),index=[['a','a','b','b'],[1,2,1,2]],columns=[['Ohis','Ohis','Colorado'],['Green','Red','Green']])
frame.index.names=['key1','key2']
frame.columns.names=['state','color']
$-> state      Ohis     Colorado
    color     Green Red    Green
    key1 key2
    a    1        0   1        2
         2        3   4        5
    b    1        6   7        8
         2        9  10       11
```
重排分级顺序
```python
frame.swaplevel('key1','key2')
$-> state      Ohis     Colorado
    color     Green Red    Green
    key2 key1
    1    a        0   1        2
    2    a        3   4        5
    1    b        6   7        8
    2    b        9  10       11
```
根据级别汇总统计
```python
# 如果对列计数，需要设置axis=1
frame.sum(level='key2')
$-> state  Ohis     Colorado
    color Green Red    Green
    key2
    1         6   8       10
    2        12  14       16
frame.sum(level='color',axis=1)
$-> color      Green  Red
    key1 key2
    a    1         2    1
         2         8    4
    b    1        14    7
         2        20   10
```










