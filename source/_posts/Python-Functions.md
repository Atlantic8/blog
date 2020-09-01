---
title: Python Functions
mathjax: true
date: 2020-09-01 23:15:14
tags: [python]
categories: Dev
---

常用的python函数

### sort
python的sort函数有两种
##### L.sort
原地排序
```python
l=[3, 2, 4, 1, 5]
l.sort(comp, key, reverse=False)
```
其中
- comp是列表元素的比较函数
- key指定排序的键值，可以是一个函数。指定key的方法比comp快
- dict没有这个函数，需要通过`items()`方法转换为list才行

##### sorted
返回一个排好序的列表，这是**稳定排序**方法
```python
new_list = sorted(iterable, cmp=None, key=None, reverse=False)

sorted(dict.items(), key=lambda d: d[0], reverse=True)
```
其中
- iterable是可迭代的类型，比如list，dict等


在**python3中，去掉了自定义比较函数cmp，这时可以将比较函数转化为key**
```
sorted(iterable, cmp_to_key(my_comp))
```

### enumerate
enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中

##### 定义
```python
enumerate(sequence, [start=0])
```
- sequence -- 一个序列、迭代器或其他支持迭代对象。
- start -- 下标起始位置
 
##### 示例
```python
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
list(enumerate(seasons))
> [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

list(enumerate(seasons, start=1)) # 下标从1开始
> [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

for i, season in enumerate(seasons):
    print(i, season)
```

### groupby
itertools.groupby函数用于**对按照key排好序多字段列表进行分组**，返回一个分组后的key和一个迭代器对象，迭代器对象包含对应key值的所有对象

##### 定义
```python
groupby(sequence, key=itemgetter())
```
- sequence是列表：其元素可以是列表、或者字典
- key是分组的key，列表需要指示是哪个，dict需要指出是哪个属性。可以用itemgetter指定

##### 示例
```python
from operator import itemgetter
from itertools import groupby

x = [[1, 'b', 3], [2, 'a', 4], [1, 'b', 5]]
# sort first
x.sort(key=itemgetter(1))
for key, iter in groupby(x, itemgetter(1)):
    for lst in iter:
        print(key, lst)

> ('a', [2, 'a', 4])
  ('b', [1, 'b', 3])
  ('b', [1, 'b', 5])


# apply for dict
y = [{'a': 'm', 'b': 2}, {'a': 'n', 'b': 1}, {'a': 'm', 'b': 3}]
y.sort(key=itemgetter('a'))
for key, iter in groupby(y, itemgetter('a')):
    for dict in iter:
        print(key, dict)

> ('m', {'a': 'm', 'b': 2})
  ('m', {'a': 'm', 'b': 3})
  ('n', {'a': 'n', 'b': 1})
```

