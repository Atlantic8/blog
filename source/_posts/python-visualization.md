---
title: python visualization
date: 2016-07-10 22:12:11
tags: [python, visualization]
---

## matplotlib
#### matplotlib配置
- 修改文件，位于.matplotlib目录中
- 使用rc方法,可以定义的有'figure','axes','xtick','ytick','grid','legend'等
```python
plt.rc('figure', figsize=(10,10)) # 设置图像默认大小
# 也可以
font_option = {'family':'monospace',
               'weight':'bold',
               'size':'small'}
plt.rc('font', **font_option)
```

#### matplotlib使用
```python
import matplotlib.pyplot as plt
import numpy as np
```

创建一个新的figure，所有图像都位于Figure对象中
```python
fig = plt.figure(2)  # 图像编号为2
```
无法通过空的Figure绘图，必须用add_subplot()创建subplot
创建4个子图，2x2
```python
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
fig.show() # 显示
```
分别对每个sub_figure画图
```python
ax1.plot(...)
ax2.scatter(...)
ax2.bar(...)
fig.show()
```
subplots，返回一个含有已创建subplot对象的numpy数组
axes可以使用axes[][]的形式访问
```python
fig, axes = plt.subplots(2,3)
axes
$-> array([[<matplotlib.axes._subplots.AxesSubplot object at 0x0A8B2EF0>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x0AA5F5D0>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x0AA9DD90>],
           [<matplotlib.axes._subplots.AxesSubplot object at 0x0AAD1E70>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x0AB1B810>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x0697C130>]], dtype=object)
```
subplots_adjust间距控制
wspace,hspace控制宽度和高度的百分比，可以用作subplot之间的距离
```python
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
```
<center><b>pyplot.subplots的选项</b></center>

|parameter|explaination|
|:-------:|:----------:|
|nrows|subplot的行数|
|ncols|subplot的列数|
|sharex|所有子图使用相同x轴刻度（xlim的影响）|
|sharey|所有子图使用相同y轴刻度（xlim的影响）|
|subplot_kw|用于创建各subplot的关键字字典|
|**fig_kw|创建fig时的其他关键字，如plt.subplot(2,2,figsize=(8,6))|

设置x、y轴的刻度
```python
ticks = axe1.set_xticks([0,200,400,600,800])
# 旋转45读，字体大小为9
labels = axe1.set_xtickslabels(['one','two','three','four','five'],rotation=45,fontsize=9)
# 将图例放在不错的位置，自动选择
ax.legend(loc='best')
```
注解，显示在(x,y)位置
```python
ax.text(x, y, 'hello world', family='consola', fontsize=10)
# annotate函数注解，既有箭头又有文字
# xy是箭头位置，xytext是注解位置，结果如下图：
ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
```
<center>![](http://matplotlib.org/_images/annotation_basic.png)</center>

图形中放入块patch
```python
rect = plt.Rectangle((0.2,0.75), 0.4, 0.15, color='r', alpha=0.3)
circ = plt.Circle((0.7,0.2), 0.15, color='b', alpha=0.3)
pgon = plt.Polygon([[0.15,0.15],[0.35,0.4],[0.2,0.6]], color='g', alpha=0.3)

ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)
```

<center><b>图形属性和说明</b></center>

|attribute|explaination|
|:-------:|:----------:|
|color|color='g' 颜色，可以指定'#555555'|
|linestyle|linestyle='--' 线性|
|marker|marker='o' 标记|
|label|label='algorithm 1' 图例|
|xlim,ylim|x轴、y轴的范围|

保存文件，参数设置如下表
```python
plt.savefig()
```

|params|introduction|
|:----:|:----------:|
|fname|文件名|
|dpi|分辨率（每英寸点数），默认为100|
|facecolor、edgecolor|背景色，默认为白色|
|format|设置文件格式，png、pdf等|
|bbox_inches|图标需要保存的部分。设为tight则尝试剪掉图标周围的空白部分|


### Pandas中的可视化方法
#### 普通的plot
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()
```
<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/series_plot_basic.png)</center>

<b>On DataFrame, plot() is a convenience to plot all of the columns with labels</b>
```python
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
df.plot()
plt.show()
# 其他关键字 subplots=True将不同列的图分别画在子图中
# layout=(2, 3) 两行三列
# sharex=False，sharey=False -> 不共享x、y轴
```
<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/frame_plot_basic.png)</center>

<b>You can plot one column versus another using the x and y keywords in plot()</b>
```python
df3 = pd.DataFrame(np.random.randn(1000, 2), columns=['B', 'C']).cumsum()
df3['A'] = pd.Series(list(range(len(df))))
df3.plot(x='A', y='B')
plt.show()
```

##### 使用第二个y轴
使用secondary_y关键字
```python
df.A.plot()
df.B.plot(secondary_y=True, style='g')
# 或者    mark_right默认是True
ax = df.plot(secondary_y=['A', 'B'], mark_right=True)
ax.set_ylabel('CD scale')
ax.right_ax.set_ylabel('AB scale')
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/frame_plot_secondary_y.png)</center>

##### Scales尺度
使用logy、logx、loglog关键字
```python
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = np.exp(ts.cumsum())
ts.plot(logy=True)
```

#### 其他plot，用kind指定

|value|function|value|function|
|:---:|:------:|:---:|:------:|
|bar|直方图|hist|统计直方图|
|kde, density|密度图|box|盒须图|
|area|面积图|scatter|散点图|
|hexbin|六边形箱图|pie|饼图|
|barh|横向的直方图|

```python
df.ix[5].plot(kind='bar')
plt.show()
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/bar_plot_ex.png)</center>

<b>其他用法</b>
```python
df = pd.DataFrame()
$-> df.plot.area    df.plot.box     df.plot.hist    df.plot.pie
	df.plot.bar     df.plot.density df.plot.kde     df.plot.scatter
	df.plot.barh    df.plot.hexbin  df.plot.line
```

##### bar plot
```python
df.ix[5].plot.bar()
plt.show()

df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
df2.plot.bar()
df2.plot.bar(stacked=True)  # 堆叠式
df2.plot.barh(stacked=True)  # 横向
```

##### histogram
Histogram can be drawn by using the <b>DataFrame.plot.hist()</b> and <b>Series.plot.hist()</b> methods
```python
df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000),'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
df4.plot.hist(stacked=True, bins=20) # 下图
df4['a'].plot.hist(orientation='horizontal', cumulative=True)
```
<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/hist_new_stacked.png)</center>

##### Box盒须图
Boxplot can be drawn calling <b>Series.plot.box()</b> and <b>DataFrame.plot.box()</b>, or <b>DataFrame.boxplot()</b> to visualize the distribution of values within each column
```python
df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
# 设置不同区域的颜色
color = dict(boxes='DarkGreen', whiskers='DarkOrange', medians='DarkBlue', caps='Gray')
# sym keyword, vert表示是否横向显示
# 另外还有positions=[1, 4, 5, 6, 8]参数指示盒图的位置
df.plot.box(color=color, sym='r+', vert=False)
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/box_new_colorize.png)</center>


##### Area面积图
<b>Series.plot.area()</b> and <b>DataFrame.plot.area()</b>

```python
df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
df.plot.area(stacked=True)
# 如果stacked=False，图形不堆叠
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/area_plot_stacked.png)</center>

##### Scatter散点图
using the <b>DataFrame.plot.scatter()</b> method
```python
df = pd.DataFrame(np.random.rand(50, 4), columns=['a', 'b', 'c', 'd'])
ax = df.plot.scatter(x='a', y='b', color='DarkBlue', label='Group 1')
# 两种不同颜色的组，注意ax=ax
df.plot.scatter(x='c', y='d', color='DarkGreen', label='Group 2', ax=ax)

df.plot.scatter(x='a', y='b', c='c', s=50)  # 下图
# 用c的值确定bubble大小
df.plot.scatter(x='a', y='b', s=df['c']*200)
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/scatter_plot_colored.png)</center>

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/scatter_plot_bubble.png)</center>

##### Hexagonal Bin Plot六边形箱图
数据过多，过于密集，无法显示出每一个数据，所以就显示<b>数据密度相关参数</b>
use<b> DataFrame.plot.hexbin()</b>
```python
df = pd.DataFrame(np.random.randn(1000, 2), columns=['a', 'b'])
df['b'] = df['b'] + np.arange(1000)
# gridsize决定网格能有多少个，默认值为100
df.plot.hexbin(x='a', y='b', gridsize=25)

# a和b作为二维坐标，C作为值，reduce_C_function是一个用于处理多个数据值的函数
# reduce_C_function包括：mean, max, sum, std等，下面有图
df.plot.hexbin(x='a', y='b', C='z', reduce_C_function=np.max, gridsize=25)
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/hexbin_plot_agg.png)</center>

##### Pie饼图
<b>DataFrame.plot.pie()</b> or <b>Series.plot.pie()</b>
```python
series = pd.Series(3 * np.random.rand(4), index=['a', 'b', 'c', 'd'], name='series')
# Series的饼状图
series.plot.pie(figsize=(6, 6))
# 使用subplot，每一列都是一个饼图，subplots=True要有
df = pd.DataFrame(3 * np.random.rand(4, 2), index=['a', 'b', 'c', 'd'], columns=['x', 'y'])
df.plot.pie(subplots=True, figsize=(8, 4))
# labels=['AA', 'BB', 'CC', 'DD']   每个扇形的标签
# colors=['r', 'g', 'b', 'c']    每个扇形的颜色
# autopct='%.2f'    显示比例、显示精度
# fontsize=20       字体大小
```

##### Density plot
```python
ser = pd.Series(np.random.randn(1000))
ser.plot.kde()  # 数量越多就越接近高斯分布
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/kde_plot.png)</center>

##### Scatter Matrix Plot
```python
from pandas.tools.plotting import scatter_matrix
df = pd.DataFrame(np.random.randn(1000, 4), columns=['a', 'b', 'c', 'd'])
scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/scatter_matrix_kde.png)</center>

##### 多元数据可视化
###### Andrews曲线
可以应用于多元数据，将其绘制成使用样本属性作为傅里叶级数参数的大量曲线。
```python
from pandas.tools.plotting import andrews_curves
data = pd.read_csv('data/iris.data')
andrews_curves(data, 'Name')   # Name是类别属性，根据类别划分
```
<center>iris.data中的数据</center>

|SepalLength|SepalWidth|PetalLength|PetalWidth|Name|
|:---------:|:--------:|:---------:|:--------:|:--:|
|5.1|3.5|1.4|0.2|Iris-setosa|

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/andrews_curves.png)</center>

###### Parallel Coordinates平行坐标系
可以应用于多元数据,每个垂直的线都对应一个属性
```python
from pandas.tools.plotting import parallel_coordinates
data = pd.read_csv('data/iris.data')
parallel_coordinates(data, 'Name')
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/parallel_coordinates.png)</center>

##### 随机性检测
###### Lag Plot
用于检测数据集或者是时间序列数据是否是随机数据,显示data[t]和data[t+1]的关系。
如果plot出的图形是无规则的，那么数据有极大的可能性是随机的。
```python
from pandas.tools.plotting import lag_plot
data = pd.Series(np.arange(1000))  # 有规则
data = pd.Series(np.random.rand(1000)) # 无规则
data = pd.Series(0.1 * np.random.rand(1000) + 0.9 * np.sin(np.linspace(-99 * np.pi, 99 * np.pi, num=1000)))  # 有规则， 有图
lag_plot(data)
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/lag_plot.png)</center>

###### Autocorrelation Plot
用于检测时序数据的随机性，通过计算不同的时间延迟（步长）下数据的自相关系数
如果这个序列是随机的，那么对于所有的延迟，其自相关系数都应该接近于0。否则，必然存在至少一个延迟对应的自相关系数远大于/小于0
```python
from pandas.tools.plotting import autocorrelation_plot
data = pd.Series(0.7 * np.random.rand(1000) + 0.3 * np.sin(np.linspace(-9 * np.pi, 9 * np.pi, num=1000)))
autocorrelation_plot(data)
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/autocorrelation_plot.png)</center>

其中，中间黑线的0值线，向外的实线和虚线分别是95%、99%置信带，有颜色的线是不同延迟对应的自相关系数。

###### Bootstrap Plot
可视化地评估统计信息的不确定性，比如说均值、中值、中距等
方法：从数据集中随机选取特定长度的子集并计算其相应的统计信息，重复特定次数
```python
from pandas.tools.plotting import bootstrap_plot
data = pd.Series(np.random.rand(1000))
bootstrap_plot(data, size=50, samples=500, color='grey')
```

<center>![](http://pandas.pydata.org/pandas-docs/stable/_images/bootstrap_plot.png)</center>

##### Colormaps
```python
from matplotlib import cm
# df.plot(colormap='cubehelix')
# df.plot(colormap=cm.cubehelix)
# colormap='Greens'
# colormap='gist_rainbow'
# colormap='winter'
dd = pd.DataFrame(np.random.randn(10, 10)).applymap(abs)
dd = dd.cumsum()
dd.plot.bar(colormap='Greens')
```

![](http://pandas.pydata.org/pandas-docs/stable/_images/greens.png)

##### Plotting Tables
关键字table=True，table关键字也可以使用DataFrame或者Series作为值
```python
fig, ax = plt.subplots(1, 1)
df = pd.DataFrame(np.random.rand(5, 3), columns=['a', 'b', 'c'])
ax.get_xaxis().set_visible(False)   # Hide Ticks
df.plot(table=True, ax=ax)
```

![](http://pandas.pydata.org/pandas-docs/stable/_images/line_plot_table_data.png)













