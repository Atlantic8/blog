---
title: Convex Hull
date: 2017-05-18 11:57:01
tags: [ LeetCode, Math ]
categories: OJ
---

###### 概念

凸包(Convex Hull)是一个计算几何（图形学）中的概念。凸包的求解方法之一是由葛立恒(Graham)发明的。给定二维平面上的点集，**凸包就是将最外层的点连接起来构成的凸多边型，它能包含点集中所有点**。

###### 求解方法
选取点集中**纵坐标最小**的点，如果纵坐标相同则选择**横坐标较小**的点，设为点H（如下图）

![凸包](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffpecd53h8j207l06a3yb.jpg)

考虑除H之外所有点和H构成的向量，按与向量$(1,0)$之间的夹角从小到大的顺序进行排序；对于夹角一样的点，则考虑其距离，如下图所示;夹角的大小由余弦值决定，因为`cos`函数在$[0,\pi]$上递减，所以`cos`值越大的点夹角越小，这里可能会遇到数值的精确度问题，开方精确度有差异的话最好比较平方大小。向量$a,b$的余弦值计算方法为
$$
\begin{aligned}
cos(a,b)=\frac{a\cdot b}{|a||b|}
\end{aligned}
$$


![](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffpf16x104j20fl0bot8s.jpg)

$(3,0)$即为基点，这里$(4,0),(5,0)$与基点共线，$(0,3),(1,2),(2,1)$与基点共线。但是这里的处理方法是不一样的。在逆时针扫描过程中，开始阶段，共线状态的点按距离远近进行排序，近的先；而对于最后的共线点，我们需要把距离远的点放前面，$(0,3)$先于$(1,2)$先于$(2,1)$。所以统一的处理方法是，**共线的点先按距离由小到大排序，然后看排在最后面的点，如果有共线的就按他们的顺序反转**。（不是最后的没关系，比如上图如果还有个$(1,1)$点，那么$(1,2),(2,1)$排在$(0,3)$前面没有影响）

最后一步，就是处理排好序的点集。逆时针扫描，基点和第一个点肯定在凸包中，然后逐个加入栈中。看第一个图，栈中点包括$(H,K)$时，向量$CK$相对于$KH$往逆时针方向偏，$C$入栈(方向不变也可以)，下一个点是$D$，由于$DC$相对于$CK$往顺时针方向偏，所以将$C$出栈；由于$DK$和$KH$满足条件，所以将$D$入栈，下一个点看$L$，以此类推。。。那么问题是如何判断两个向量是否是逆时针旋转关系呢？

可以通过向量的叉积，向量$a\times b$的方向通过右手定则判断，具体地，四指并拢指向$a$的方向，四指转动一定角度（小于180度）指向$b$的方向，大拇指的方向就是$a\times b$的方向，如下图所示

![右手定则](http://ww1.sinaimg.cn/mw690/9bcfe727ly1ffpgezlj08j204t064aa9.jpg)

那么如何通过计算得到方向呢？由于二维向量的叉积会产生第三个维度，所以可以假设$a=(a_1,a_2)=(a_1,a_2,0),b=(b_1,b_2)=(b_1,b_2,0)$，$a\times b$计算如下
$$
\begin{aligned}
a\times b = \left[
\begin{matrix}
i & j & k \\
a_1 & a_2 & 0 \\
b_1 & b_2 & 0
\end{matrix}
\right]=\left[0, 0, a_1b_2-a_2b_1\right]
\end{aligned}
$$
第三维的分量为$a_1b_2-a_2b_1$，举个栗子判断一下不难发现，逆时针方向转动的向量第三维分量大于0，顺时针转动的小于0.比如图中的$a\times b$指向z轴正向。所以通过计算$a_1b_2-a_2b_1$就可以知道转动方向了。

以下是c++实现
```java
vector<Point> outerTrees(vector<Point>& points) {
	if (points.size() < 4) return points;
	Point bottom = points[0];
	int index = 0;
	for (int i=0; i<points.size(); i++) { // search for lowest node 
		Point point = points[i];
		if (point.y==bottom.y && point.x<bottom.x) {bottom = point; index = i;}
		if (point.y < bottom.y) {bottom = point; index = i;}
	}
	swap(points[0], points[index]);
	sort(points.begin()+1, points.end(), [bottom](const Point &p1, const Point &p2){
		double d1 = (p1.x-bottom.x)*(p1.x-bottom.x)+(p1.y-bottom.y)*(p1.y-bottom.y);
		double d2 = (p2.x-bottom.x)*(p2.x-bottom.x)+(p2.y-bottom.y)*(p2.y-bottom.y);
		double x1 = 1.0*(p1.x-bottom.x)*abs(p1.x-bottom.x)/d1;
		double x2 = 1.0*(p2.x-bottom.x)*abs(p2.x-bottom.x)/d2;

		if (x1 != x2) return x1 > x2; // angle from small to big
		return d1 < d2; // distance from close to far
	});
	int rl = points.size()-2, rr = points.size()-1;
	while (rl >= 1) { // reverse co-linear nodes from behind if necessary
	    Point p1 = points[rl];
	    Point p2 = points[rr];
	    double d1 = (p1.x-bottom.x)*(p1.x-bottom.x)+(p1.y-bottom.y)*(p1.y-bottom.y);
		double d2 = (p2.x-bottom.x)*(p2.x-bottom.x)+(p2.y-bottom.y)*(p2.y-bottom.y);
	    double x1 = 1.0*(p1.x-bottom.x)*abs(p1.x-bottom.x)/d1;
		double x2 = 1.0*(p2.x-bottom.x)*abs(p2.x-bottom.x)/d2;
		if (x1 == x2) rl--;
		else break;
	}
	if (++rl < rr && rl >= 1)while (rl < rr) swap(points[rl++], points[rr--]);

	vector<Point> ret;
	ret.push_back(points[0]);
	ret.push_back(points[1]);
	for (int i=2; i<points.size(); i++) { remove clock-wize node
	    int num = 0;
		while (ret.size() > 2) {
			// last vector
			int v1x=ret[ret.size()-1].x-ret[ret.size()-2].x, v1y=ret[ret.size()-1].y-ret[ret.size()-2].y;
			// current vector
			int v2x=points[i].x-ret[ret.size()-1].x, v2y=points[i].y-ret[ret.size()-1].y;
			// cross product x1*y2-x2*y1, positive is ok
			if (v1x*v2y-v2x*v1y < 0) ret.pop_back();
			else break;
		}
		ret.push_back(points[i]);
	}
	return ret;
}
```

###### 类似题目
LeeCode题目[Erect the Fence](https://leetcode.com/problems/erect-the-fence/#/description)就是求点的凸包问题。

还有类似的题目：求二维平面上多个点构成的最大三角形。思路是先求多个点的凸包，然后枚举凸包中的点，找到最大三角形。（$S=\sqrt{p(p-a)(p-b)(p-c)},p=\frac{a+b+c}{2}$）.

**引用**
[1]. [Graham's Scan法求解凸包问题](http://www.cnblogs.com/devymex/archive/2010/08/09/1795392.html)
[2]. [百度百科-向量积](http://baike.baidu.com/link?url=xtFaaawZVn0sbpsumowTV-hIlzVBsUOUxoPL-czVqaqmEIFU3WnU7LcMkHy6FyYJ4etWIBK3u5bYXmEQ4vZW-cZw6fKT7Sj4iyl1IZzuHHBs0QxUru5Y5F_nGa2JazZk)
