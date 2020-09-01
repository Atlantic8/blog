---
title: matplotlib绘图基本方法
date: 2016-05-10 09:30:37
tags: [python]
categories: Dev
---
### 设置中文编码
```python
# -*- coding: utf-8 -*-
```
### 头文件
```python
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.legend import Legend
```

### 直方图(histogram)
```python
#N：表示横坐标点个数
#m：对比方案个数
def getHistogram(data, my_title):
    color = ['gray','green','blue','magenta']
    N = 6
    fs = 20 # font size
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2       # the width of the bars, 1/(m+1)
    pylab.grid(True)
    # pylab.title(my_title, fontsize = fs)
    pylab.ylim((-25,15))
    #plt.ylim((0,7.5))
    pylab.bar(ind-2*width, data[0], width, color=color[0],label='MBE3',edgecolor=color[0])
    pylab.bar(ind-1*width, data[1], width, color=color[1],label='PRIVATUS',edgecolor=color[1])
    pylab.bar(ind+0*width, data[2], width, color=color[2],label='OPPEMS',edgecolor=color[2])
    pylab.bar(ind+1*width, data[3], width, color=color[3],label='DPMRRS',edgecolor=color[3])
    
    # add some text for labels, title and axes ticks
    pylab.xlabel(r'$\epsilon$', fontsize = fs)
    #pylab.ylabel('mutual information', fontsize = fs)
    pylab.ylabel('extra cost/$', fontsize = fs)
    pylab.xticks(ind, ('0.15', '0.25', '0.35', '0.45', '0.55','0.65'), fontsize = fs)
    pylab.yticks(fontsize = fs)
    pylab.legend(ncol = 4, loc = 'upper left')
    pylab.show()
```

### 折线图(plot)
```python
def getLine(data,my_title):
    plt.grid(True)
    fs = 20
    X = [100, 200, 300, 400, 500]
    plt.xlabel('number of invalid noises', fontsize = fs)
    plt.ylabel('extra cost/$', fontsize = fs)
    # plt.ylabel('mutual information', fontsize = fs)
    plt.xlim((0,600))
    plt.xticks(fontsize = fs)
    plt.yticks(fontsize = fs)
    # plt.title(my_title, fontsize = fs)
    plt.plot(X, data, 'ro-',linewidth=4)
    plt.show()
```

### 散点图(dot)
```python 
def plotDots(data):
    plt.grid(True)
    fs = 20
    X = range(96)
    plt.xlabel('time', fontsize = fs)
    # plt.ylabel('price/($/kwh)', fontsize = fs)
    plt.ylabel('mutual information', fontsize = fs)
    plt.xlim((-4,100))
    plt.ylim((0,0.03))
    plt.xticks([])
    plt.yticks([])
    # plt.title(my_title, fontsize = fs)
    plt.plot(X, data, 'go',label='price')
    plt.plot(X,y1, 'b--',label='$p_l$')
    plt.plot(X,y2, 'k--',label='$p_h$')
    # plt.legend(fontsize = fs, ncol=3)
    plt.show()
```

### 饼图(pie)
```python
#sum(data)=1
def plotPie(data):
    plt.title('pie chart')
    labels = ['China', 'Japan', 'America']
    # labeldistance>1, label就在饼图外面
    plt.pie(x, labels=labels, autopct='%1.1f%%',labeldistance=1.2)
    plt.show()
```