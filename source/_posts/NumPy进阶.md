---
title: NumPy进阶
date: 2016-08-15 19:03:52
tags: [python, numpy]
categories: Dev
---

##### 数组重塑
```python
import numpy as np
from numpy.random import randn

# reshape函数
arr = np.arange(8)
arr.reshape((4, 2)).sahpe
$-> (4, 2)
arr.reshape((5,-1))

# 扁平化函数
# flatten函数返回数据副本，ravel则不是
# 这些函数可以带有指示顺序的参数：{'C':行有限, 'F':列优先}
arr = np.arange(15).reshape((5, 3))
arr.ravel()
$-> array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14])
arr.flatten()
$-> array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14])
arr.ravel('F')
$-> array([ 0,  3,  6,  9, 12,  1,  4,  7, 10, 13,  2,  5,  8, 11, 14])

# 拆分合并
arr1 = np.array([[1,2,3],[4,5,6]])
arr2 = np.array([[7,8,9],[10,11,12]])
np.concatenate([arr1, arr2], axis=0)
$-> array([[ 1,  2,  3],
              [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]])

np.concatenate([arr1, arr2], axis=1)
$-> array([[ 1,  2,  3,  7,  8,  9],
           [ 4,  5,  6, 10, 11, 12]])

# vstack(垂直方向的连接), hstack(水平方向的连接)
# 里面的圆括号也可以换成方括号
np.vstack((arr1, arr2))
$-> array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]])

np.hstack([arr1, arr2])
$-> array([[ 1,  2,  3,  7,  8,  9],
           [ 4,  5,  6, 10, 11, 12]])

# split
arr = randn(5, 2)
first, second, third = np.split(arr,[1,3])
first
$-> array([[-0.28435497,  0.71298716]])
second
$-> array([[ 0.48442513, -0.84460369],
           [-0.38289692, -1.11166995]])
third
$-> array([[-0.44724781,  0.52083756],
           [-0.39584687,  0.14325106]])

```

<center>数组连接函数</center>

|method|explanation|
|:----:|:---------:|
|concatenate|沿一条轴连接一组数组|
|vstack,hstack|垂直、水平连接|
|row_stack|按行连接，相当于vstack|
|column_stack|按列连接，相当于hstack|
|dstack|以面向‘深度’的方式堆叠，沿轴2|
|split|沿指定轴的指定位置拆分|
|hsplit,vsplit,dsplit|分别沿轴0、1、2切分|

元素重复操作
tile and repeat函数
tile沿指定轴向堆叠数组的副本
```python
arr = np.arange(3)
arr.repeat(3)
$-> array([0, 0, 0, 1, 1, 1, 2, 2, 2])
arr.repeat([2,3,4])
$-> array([0, 0, 1, 1, 1, 2, 2, 2, 2])

arr = np.arange(4).reshape((2,2))
arr.repeat([2,3], axis=0)
$-> array([[0, 1],
             [0, 1],
          [2, 3],
          [2, 3],
          [2, 3]])

np.tile(arr, 2)
$-> array([[0, 1, 0, 1],
           [2, 3, 2, 3]])
```

##### 广播
```python
np.arange(4) + 3
$-> array([3, 4, 5, 6])

# 每一行减去均值时，直接减
# 每一列减时需要维度变化
arr = np.arange(12).reshape((3,4))
# 参数为0计算每列的均值，1则计算每行的均值
arr.mean(0)
$-> array([ 4.,  5.,  6.,  7.])

arr - arr.mean(0)
$-> array([[-4., -4., -4., -4.],
           [ 0.,  0.,  0.,  0.],
           [ 4.,  4.,  4.,  4.]])

# arr - arr.mean(1)报错
# 沿其他轴广播，较小数组的‘广播维’必须为1，所以需要reshape()，把n变成(n,1)
arr - arr.mean(1).reshape((4,1))
$-> array([[-1.5, -0.5,  0.5,  1.5],
           [-1.5, -0.5,  0.5,  1.5],
           [-1.5, -0.5,  0.5,  1.5]])

# 一般解决方法是：专门为广播添加一个新轴
# 通过np.newaxis属性及全切片完成
arr = randn(3,4,5)
depth_mean = arr.mean(2)
demean = arr - depth_mean[:,np.newaxis,:]
demean.mean(2)
# 结果基本为0
$-> array([[  0.00000000e+00,  -2.22044605e-17,   1.11022302e-17,
              8.88178420e-17],
           [ -2.22044605e-17,  -1.11022302e-17,  -7.77156117e-17,
              2.77555756e-17],
           [  2.22044605e-17,  -5.55111512e-18,  -3.33066907e-17,
             -6.66133815e-17]])

# 通过广播设置数组的值
arr = randn(3,4)
arr[:] = 5
arr $->
array([[ 5.,  5.,  5.,  5.],
       [ 5.,  5.,  5.,  5.],
       [ 5.,  5.,  5.,  5.]])

```

##### ufunc高级应用
<center>ufunc方法</center>

|method|explanation|
|:----:|:---------:|
|reduce(x)|通过连续执行原始运算的方式对值进行聚合|
|accumulate(x)|聚合值，保留所有局部聚合结果|
|reduceat(x,bin)|局部约简。约简数据的各个切片以产生聚合型数组|
|outer(x,y)|对x、y中的每个元素应用原始运算|

###### 自定义ufunc
- numpy.frompyfunc()函数接受一个python函数，以及两个分别表示输入输出参数数量的整数
- numpy.vectorize()函数用法类似
- 这两个函数速度较慢

```python
def add_elements(x, y):
    return x+y
# add_elements函数接受两个参数，返回一个参数
add_them = np.frompyfunc(add_elements, 2, 1)
add_them(np.arange(6), np.arange(6))
$-> array([0, 2, 4, 6, 8, 10], dtype=object)

add_them = np.vectorize(add_elements)
add_them(np.arange(6), np.arange(6))
$-> array([ 0,  2,  4,  6,  8, 10])
```

##### 更多的排序
- ndarray的排序是就地排序
- numpy.sort产生一个排好序的副本
- 两个函数都可以接受axis参数，0：对列排序，1：对行排序

###### 间接排序
对多个键排序时，可以使用这两个函数
```python
values = np.array([5,0,1,3,2])
index = values.argsort()
index
$-> array([1, 2, 4, 3, 0])
values[index]
$-> array([0, 1, 2, 3, 5])

first = np.array(['a','b','c','d','e'])
last = np.array(['z','y','x','v','u'])
# 键的应用是从后往前，先last，再first
sorter = np.lexsort((first, last))
sorter $-> array([4, 3, 2, 1, 0])

zip(last[sorter], first[sorter])
$-> [('u', 'e'), ('v', 'd'), ('x', 'c'), ('y', 'b'), ('z', 'a')]

```

<center>排序算法的kind参数</center>

|param|speed|stability|space complexity|worst complexity|
|:---:|:---:|:-------:|:--------------:|:--------------:|
|quicksort|1|no|0|O(n^2)|
|mergesort|2|yes|n/2|O(nlogn)|
|heapsort|3|no|0|O(nlogn)|

###### numpy.searchsorted
- 有序数组中的查找，使用二分查找
- 存在待查找的元素，返回其序号，否则返回插入该元素后该元素的序号

```python
arr = np.array([1,2,4,5,6,8,9])
arr.searchsorted(5)
$-> 3
arr.searchsorted(7)
$-> 5

arr = np.array([0,0,0,1,1,1])
arr.searchsorted([0,1])
$-> array([0, 3])
# 从右边数
arr.searchsorted([0,1], side='right')
$-> array([3, 6])
```

##### NumPy的matrix类
- np.matrix()接受参数：二维数组，构建一个矩阵对象
- 支持使用直接的 * 运算
- X.I返回矩阵X的逆
- 可用X.asarray将其转化为正规的ndarray对象

##### 输出输入
###### 内存映像文件
- 内存映像文件是一种将磁盘上的非常大的二进制文件当作文件中的数组进行处理的方式，实际上就是放在磁盘上的ndarray
- NumPy中的memmap对象允许将大文件分成小段进行读写
- np.memmap()函数接受(文件路径,数据类型,文件模式,模式)
- 对memmap对象切片会返回磁盘上的数据视图，如果对这些视图赋值，数据会被存储在内存中，调用flush就可以写入磁盘
- 如果某个内存映像超出作用域，他就会被垃圾回收器回收，之前的修改都会被写入磁盘

```python
mmap = memmap('mymmap', dtype='float64', mode='w+', shape=(10000,10000))
section = mmap[:5]
section[:] = randn(5,10000)

mmap.flush()
del mmap
```

###### HDF5
- PyTables和h5py用于处理高效、可压缩的HDF5格式的数据
- PyTables提供了一些用于结构化数组的高级查询功能

##### 性能加速
- 避免复制
- 使用广播
- 使用ufunc方法
- 使用连续内存
- Cython加速

```python
arr_c = np.ones((1000,1000), order='C')
arr_f = np.ones((1000,1000), order='F')
# 对前者的操作要快于后者的操作，前者数据按照C语言的连续方式存储
```

