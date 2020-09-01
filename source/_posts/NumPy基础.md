---
title: NumPy基础
date: 2016-06-23 15:32:40
tags: [numpy, python]
categories: Dev
---

```python
import numpy as np
from numpy.random import randn
```

#### ndarray：一种对维数组对象
创建方法

|    函数    |    说明    |
|:----------:|:----------:|
|  array  |  将输入数据(列表、元组、数组或其他序列类型)转换为ndarray，可以指定dtype  |
|  asarray  |  将输入转换为ndarray，如果输入本身就是ndarray，则不进行复制  |
|  arange  |  同range，只是返回的是ndarray  |
|  ones,ones_like  |  前者根据指定形状和dtype创建一个全1数组。 后者以另一个数组为参照，copy其形状和dtype |
|  zeros,zeros_like  |  前者根据指定形状和dtype创建一个全0数组。 后者以另一个数组为参照，copy其形状和dtype  |
|  empty,empty_like  |  只分配内存，不填充任何值  |
|  eye,identity  |  单位矩阵  |

NumPy的精度dtype集合，实际使用应该加上np.前缀

|                 dtype         |             dtype            |
|:-----------------------------:|:----------------------------:|
|int8, uint8|int16,uint16|
|int32, uint32|int64,uint64|
|float16, float32|float64,float128|
|complex64|complex128|
|complex256|bool|

```python
# construct
arr1 = np.array([1,2,3,4,5])
arr1.ndim
$-> 1 # 一维数组
arr1.shape
$-> (1,5) # 1x5的数组
arr1.dtype
$-> dtype('int64')

# type convert，这里一定会常见一个新的数组，无论目标转换类型与原数组类型是否一致
float_arr = arr1.astype(np.float64)
```

#### 索引与切片
索引切片方法与list的对应方法相似，不同点在于：
<b>数组切片也是原始数组的视图，这意味着数据不会被复制，因此视图上的任何更改都会直接地反映到源数组上。而list不然</b>，请具体看下面的例子。
```python
a = [1,2,3,4,5,6]
b = a[2:5]
b[1] = 100
print(a)
$-> [1, 2, 3, 4, 5, 6]

arr = np.array([1,2,3,4,5,6])
br = arr[2:5]
br[1] = 99
arr
$-> array([ 1,  2,  3, 99,  5,  6])

# 如果需要ndarray的切片的副本而非视图，可以显示地复制
new_arr = arr[2:5].copy()
```
多维数组的切片
```python
arr2d = np.array([[1,2,3],[4,5,6],[7,8,9]])
arr2d[1][1]
$-> 1
arr2d[1,1]
$-> 1

# 沿着第0轴(第一个轴)切片
arr2d[:2]
$-> array([[1, 2, 3],
           [4, 5, 6]])
arr2d[:2,1:]
$-> array([[2, 3],
           [5, 6]])
arr2d[:,:1]
$-> array([[1],
           [4],
           [7]])

# bool索引与赋值
arr<4
$-> array([ True,  True,  True, False, False, False], dtype=bool)
arr[arr<4] = 4
arr
$-> array([ 4,  4,  4, 99,  5,  6])
```
<b>花式索引(fancy indexing)</b>,<b>花式索引总是将数据复制到新数组中</b>，切片得到的是视图。
```python
arr = np.empty((8,4))
for i in range(8):
    arr[i] = i
arr
$-> array([[ 0.,  0.,  0.,  0.],
           [ 1.,  1.,  1.,  1.],
           [ 2.,  2.,  2.,  2.],
             [ 3.,  3.,  3.,  3.],
           [ 4.,  4.,  4.,  4.],
           [ 5.,  5.,  5.,  5.],
           [ 6.,  6.,  6.,  6.],
           [ 7.,  7.,  7.,  7.]])

# 以特定顺序选取行子集，传入一个制定顺序的证书列表或者ndarray
arr[[4,2,6]]  # 打印第5、3、7行
$-> array([[ 4.,  4.,  4.,  4.],
           [ 2.,  2.,  2.,  2.],
           [ 6.,  6.,  6.,  6.]])
# 如果使用负数将从末尾计数
arr[[-2,-1,4]] # 倒数第二行、第一行和正数第5行
$-> array([[ 6.,  6.,  6.,  6.],
           [ 7.,  7.,  7.,  7.],
           [ 4.,  4.,  4.,  4.]])

arr = np.arange(32).reshape((8,4))
arr[[1,5,7,2],[0,3,1,2]]
$-> array([ 4, 23, 29, 10])
# 上面操作结果没有返回一个指示对应行列值得矩阵，方法如下：
arr[np.ix_([1,5,7,2],[0,3,1,2])]
$-> array([[ 4,  7,  5,  6],
           [20, 23, 21, 22],
           [28, 31, 29, 30],
           [ 8, 11,  9, 10]])
```
<b>数组轴对换和转置</b>
数组不仅有transpose方法(返回数据源视图，不复制)，还有T属性，二维的情况很容易理解，下面是高纬轴对换的例子。
```python
arr = np.arange(16).reshape((2,2,4))
arr
$-> array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7]],

           [[ 8,  9, 10, 11],
            [12, 13, 14, 15]]])
arr.transpose((1,0,2))
$-> array([[[ 0,  1,  2,  3],
            [ 8,  9, 10, 11]],

           [[ 4,  5,  6,  7],
            [12, 13, 14, 15]]])

# swapaxes,返回数据源视图，不复制
arr = np.arange(16).reshape((2,2,4))
arr.swapaxes(1,2)
Out[53]:
array([[[ 0,  4],
        [ 1,  5],
        [ 2,  6],
        [ 3,  7]],

       [[ 8, 12],
        [ 9, 13],
        [10, 14],
        [11, 15]]])
```

#### 通用函数，元素级数组函数

|      一元函数      |         说明         |     一元函数       |         说明         |
|:-----------------:|:--------------------:|:-----------------:|:--------------------:|
|   abs,fabs   | 求绝对值，实数用fabs更快  |  sqrt  |  计算各元素平方根,相当于arr**0.5  |
|  square  |  计算各元素平方,相当于arr**2  |  exp  |    计算e的元素次方   |
| log,log10,log2,log1p | 对数运算，最后一个是log(1+x) | sign | 指示符号，(1,0,-1) |
|  ceil  |   向上取整   |  floor  |  向下取整  |
|  rint   |  四舍五入到最近的整数，保留dtype  |  modf  |  将数组的整数和小数部分以两个独立数组的形式返回   |
|  isnan   |  返回哪些是NaN的bool数组   | isfinite,isinf | 返回哪些是有穷的/无穷的bool数组 |
| cos,cosh,sin,sinh,tan,tanh |  普通型和双曲型三角函数  |logical_not|  计算各元素not x的真值，相当于-arr |
|arccos,arccosh,arcsin,arcsinh,arctan,arctanh| 反三角函数  |

|      二元函数      |         说明         |     二元函数       |         说明         |
|:-----------------:|:--------------------:|:-----------------:|:--------------------:|
|   add   | 数值中对应元素相加  |  substract  |  第一个数组元素减去第二个数组元素  |
|  multiply  |  数组元素相乘  | divide,floor_divide |  除法，向下圆整除法  |
| power | 第一个数组元素为底，第二个数组元素为顶计算乘方 | maximum,fmax | 最大值，fmax忽略nan |
| minimum,fmin | fmin忽略nan  |  mod |  求模 |
|  copysign   |  将第二个数组元素的符号赋给第一个数组的元素  | greater,greater_equal,less,less_equal |  比较运算，产生bool数组  |
|  equal,not_equal  |  比较运算，产生bool数组   | logical_and,logical_or,logical_xor | 元素级真值逻辑运算 |

```python
arr = np.arange(10)
np.sqrt(arr)

x = randn(8)
y = randn(8)
np.maximum(x,y)

arr = randn(8)*5
np.modf(arr)
$-> (array([[-0.06742411, -0.37438428,  0.7491406 ,  0.63876896, -0.73629364,
           0.60505606, -0.38540241,  0.78968936]]),
 array([[-1., -1.,  0.,  0., -1.,  1., -1.,  0.]]))
```

#### 数据处理和统计
```python
points = np.arange(-5,5,0.01) # 1000个间隔相等的点
xs,ys = np.meshgrid(points, points)
z = np.sqrt(xs**2+ys**2)

xarr = np.array([1.1,1.2,1.3,1.4,1.5])
yarr = np.array([2.1,2.2,2.3,2.4,2.5])
cond = np.array([True,False,True,True,False])
# 根据cond的情况选取xarr或者yarr
result = [(x if c else x) for x,y,c in xarr,yarr,cond]

# 上述方法对大数组处理速度较慢，且无法用于多维数组
# np.where函数通常用于：根据一个数组产生另一个数组
result = np.where(cond, xarr, yarr)

arr = randn(4,4)
arr
$-> array([[ 1.52182545,  0.87451946,  1.04261881, -1.0087171 ],
            [-0.17748091, -0.11488603, -0.29951479,  0.67766543],
            [-0.21761354, -0.83476571,  1.69775644,  1.45229995],
            [ 0.1791336 ,  1.55750933,  0.23509194,  0.39716205]])
np.where(arr>0, 2, -2) # 把大于0的都换成2，小于0的换成-2
$-> array([[ 2,  2,  2, -2],
           [-2, -2, -2,  2],
           [-2, -2,  2,  2],
           [ 2,  2,  2,  2]])

```
<b>基本数组统计方法</b>
既是数组示例的方法，也是顶级方法。这类函数可以接受一个axis参数，表示轴向方向

|        方法        |        说明        |
|:------------------:|:----------------- :|
|sum|求和，对于bool值数组，sum计算True的个数|
|mean|均值，长度为0的均值为NaN|
|std,var|标准差和方差，自由度可调，默认为n|
|min,max|最小值，最大值|
|argmin,argmax|最小、最大元素的索引|
|cumsum|所有元素累计和|
|cumprod|所有元素累计积|

```python
arr.mean(axis=1)
arr = np.arange(9).reshape((3,3))
arr.cumsum(axis=0) # 列和
$-> array([[ 0,  1,  2],
           [ 3,  5,  7],
           [ 9, 12, 15]])
arr.cumprod(1)  #行积
$-> array([[  0,   0,   0],
           [  3,  12,  60],
           [  6,  42, 336]])
```
<b>用于bool数组的方法</b>
```python
(arr>0).sum()  #计算正值数量
bools = np.array([False, True, True, False])
# any用于检测数组中是否有True， all检查是否都是True
bools.any() -> True
bools.all() -> False
```
<b>排序</b>
顶级方法np.sort返回排序完的副本，就地排序则会修改数组本身
```python
arr = randn(8)
arr.sort()
np.array(arr)
$-> array([[ 0.4811325 ],
           [ 1.49888281],
           [ 0.71035914],
           [-1.24322946],
           [ 0.90270716],
           [ 1.29337938],
           [-0.29419419],
           [ 0.71318192]])
arr = randn(5,3)
arr.sort(axis=0)
```
<b>数组集合运算</b>

|    函数    |    说明    |
|  unique(x) | 计算x中的唯一元素，返回排序好的结果  |
|  intersect1d(x,y) |  计算x和y中的公共元素(交集)，返回排序好的结果 |
|  union1d(x,y) |  计算x和y中的并集，返回排序好的结果 |
|  in1d(x,y) | 返回表示x的元素是否在y中的bool数组  |
|  setdiff1d(x,y) | 差集，在x中，不在y中  |
|  setxor1d(x,y) | 对称差，找出只出现在一个数组中的元素  |

<b>线性代数基础</b>

|    函数    |    说明    |    函数    |    说明    |
|:----------:|:---------:|:----------:|:----------:|
|diag|给定矩阵，以一维数组的方式返回对角线元素；给定一维数组，返回以此数组为对角线的方阵|dot|矩阵乘法|
|trace|矩阵的迹|det|行列式的值|
|eig|方阵的特征值和特征向量|inv|方阵的逆|
|pinv|矩阵的Moore-Penrose伪逆|qr|计算矩阵的QR分解|
|svd|奇异值分解|solve|计算线性方程组Ax=b，A是方阵|
|lstsq|计算Ax=b的最小二乘解|

```python
from numpy.linalg import inv,qr

x = np.arange(6).reshape((3,2))
y = np.arange(6).reshape((2,3))
x.dot(y)  # 等同于np.dot(x,y)

q,r = pr(arr)
```
<b>随机数生成</b>
numpy.random中的部分函数

|    函数    |    说明    |    函数    |    说明    |
|:----------:|:---------:|:----------:|:----------:|
|seed|确定随机数生成器种子|permutation|序列的随机排列或一个随机排列的范围|
|shuffle|对一个序列就地随机排列|rand|产生均匀分布的样本值|
|randint|给定上下限的随机整数选取|randn|产生正态分布样本值(mean=0,std=1)|
|binomial|产生二项分布样本值|normal|产生正态分布样本值|
|beta|产生Beta分布样本值|chisqaure|产生卡方分布样本值|
|gama|产生Gamma分布样本值|uniform|产生[0,1]均匀分布样本值|








