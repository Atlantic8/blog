---
title: Floyd Cycle Detection
date: 2016-12-01 09:06:54
tags: 
categories: Algorithm
---

###### 定义
Floyd判圈算法(Floyd Cycle Detection Algorithm)，又称龟兔赛跑算法(Tortoise and Hare Algorithm)。该算法由美国科学家罗伯特·弗洛伊德发明，是一个可以在有限状态机、迭代函数或者链表上判断是否存在环，求出该环的起点与长度的算法。


	如果有限状态机、迭代函数或者链表上存在环，那么在某个环上以不同速度前进的2个指针必定会在某个时刻相遇
	如果从同一个起点(即使这个起点不在某个环上)同时开始以不同速度前进的2个指针最终相遇，那么可以判定存在一个环，且可以求出2者相遇处所在的环的起点与长度

###### 算法描述

	假设已知某个起点节点为节点S。现设两个指针t和h，将它们均指向S
	同时让t和h往前推进，但是二者的速度不同：t每前进1步，h前进2步
		当h无法前进，即到达某个没有后继的节点时，就可以确定从S出发不会遇到环
		当t与h再次相遇(在点M)时，就可以确定从S出发一定会进入某个环，设其为环C
			令h仍均位于节点M，而令t返回起点节点S
			让t和h往前推进，且保持二者的速度都为1
			t和h相遇的地方即为环C的入口

###### 相关问题

[Linked List Cycle](http://atlantic8.github.io/2016/09/04/Linked-List-Cycle/)

[Happy Number](http://atlantic8.github.io/2016/12/01/Happy-Number/)
