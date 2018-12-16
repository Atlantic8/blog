---
title: Super Washing Machines
date: 2017-04-02 10:08:53
tags: [LeetCode]
categories: OJ
---

###### 题目描述
You have $n$ super washing machines on a line. Initially, each washing machine has some dresses or is empty.

For each move, you could **choose any $m (1 ≤ m ≤ n)$ washing machines, and pass one dress of each washing machine to one of its adjacent washing machines at the same time** .

Given an integer array representing the number of dresses in each washing machine from left to right on the line, you should find the minimum number of moves to make all the washing machines have the same number of dresses. If it is not possible to do it, return -1.

	Example1

	Input: [1,0,5]
	Output: 3

	Explanation: 
	1st move:    1     0 <-- 5    =>    1     1     4
	2nd move:    1 <-- 1 <-- 4    =>    2     1     3    
	3rd move:    2     1 <-- 3    =>    2     2     2   
	Example2

	Input: [0,3,0]
	Output: 2

	Explanation: 
	1st move:    0 <-- 3     0    =>    1     2     0    
	2nd move:    1     2 --> 0    =>    1     1     1     
	Example3

	Input: [0,2,0]
	Output: -1

	Explanation: 
	It's impossible to make all the three washing machines have the same number of dresses. 
	Note:
	The range of n is [1, 10000].
	The range of dresses number in a super washing machine is [0, 1e5].


###### 解题思路
首先，如果所有洗衣机的衣服总和不能被$n$整除，返回-1.
然后对于每个洗衣机，计算它的`gain/lose`数组，表示还需要移除多少件衣服使得自己达到平衡状态。

举个栗子：
对于`[0,0,11,5]`，每个洗衣机应该有4件衣服，所以它的`gain/lose`数组为`[-4,-4,7,1]`。从第一个机器开始考虑，第一个要加入4件，得从第二个机器中过来，所以这个状态可以以4次移动的代价变成`[0,-8,7,1]`。同理第二个状态也可以以8次移动的代价变成状态三`[0,0,-1,1]`，最后以一次移动的代价变成`[0,0,0,0]`。

因为每一次移动可以选取任意个元素，并朝左边或者右边移动一个元素，所以总共需要的移动次数就是`gain/lose`数组中出现的最大值。

```java
int findMinMoves(vector<int>& machines) {
	int sum = accumulate(machines.begin(), machines.end(), 0);
	if (sum % machines.size() != 0) return -1;
	int ret=0, tmp=0, n=sum / machines.size();
	for (int num : machines) {
		tmp += num-n;
		ret = max(max(ret, num-n), abs(tmp));
	}
	return ret;
}
```
代码中`num-n`没加绝对值，我的理解是对于初始`gain/lose`数组的负数，可以从两边同时添加衣服，如果是正数，那么那么每次只能移除一件衣服。而`tmp`加了绝对值，是因为`tmp`表示左边一个缺少/多的衣服数，这些衣服得从右边过来，并且一个一个达到当前位置，所以得加绝对值。