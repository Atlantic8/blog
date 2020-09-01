---
title: java-matlab2014a混合编程
date: 2016-05-05 15:16:47
tags: [Java, Matlab]
categories: Dev
---
## 第一步
- 编写需要调用的matlab函数，可以多个文件一起编译
- 在matlab的shell框中输入deploytool，回车
- 在弹出的菜单中选中library compiler(这个根据实际情况自己决定)
- 左上角选中java package。点击稍右侧的+号添加文件
- 修改Library Name和类名
- Runtime downloaded from web和runtime included in package视情况决定
- 点击右上角的Package按钮开始编译

## 第二步
- 首先需要将Matlab\R2014a\toolbox\javabuilder\jar中的javabuilder.jar放入java工程文件夹内(最好这么做)
- 将编译完成的xxx.jar包放入java工程文件夹内(最好这么做)
- 在eclipse的Package Explore中右键工程名
- Build path -> configure build path，然后点击Add External JARs添加上面的2个jar包

## 第三步
- 首先导入jar包
```java
import com.mathworks.toolbox.javabuilder.*;
import xxx.Class1;
```
- 使用函数时
```java
Class1 class = new Class1();
Object[] result = t = new Object[2]; //这里必须用数组形式，至少在matlab2014a里是这样的
result = class.functionName(2, argument1, srgument2, argument3); //2表示返回结果的个数为2
MWNumericArray temp = (MWNumericArray)result[0]; //第一个结果是数组                    
double[][] recv = (double[][]) temp.toDoubleArray(); //还有toInt/FloatArray以及toString等用法
int box = Integer.valueOf(result[0].toString()); //第二个结果是一个int型整数.
```