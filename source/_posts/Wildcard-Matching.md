---
title: Wildcard Matching
date: 2016-09-24 22:59:35
tags: [LeetCode, Greedy]
categories: OJ
---

##### Problem
Implement wildcard pattern matching with support for '?' and '*'.

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

The function prototype should be:
bool isMatch(const char *s, const char *p)

	Some examples:
	isMatch("aa","a") → false
	isMatch("aa","aa") → true
	isMatch("aaa","aa") → false
	isMatch("aa", "*") → true
	isMatch("aa", "a*") → true
	isMatch("ab", "?*") → true
	isMatch("aab", "c*a*b") → false

##### Solution
C++的DP方法超时（好像java可以）。
线性时间算法的基本思想是维护两个指针p1、p2，分别指向s和p，分以下几种情况：

- p[p2] == '?' 说明匹配，那么 ++p1，++p2
- p[p2] == '*' 这也是一种匹配，但是可能的情况很多，用start保存此星号的位置，用matched保存与当前星号匹配的s的位置，p2++，p1不移动，先把与星号匹配的设为空，因为如果后面不匹配的话，还会回来给星号匹配字符
- 否则，当前已经不能匹配了，找到上一个星号位置
	- 上一个星号存在，则p回退到上一个星号后一位，把matched对应的字符串匹配给星号，s回退到matched下一位，matched++，p2=star+1，p1=++matched
	- 否则，没有可能的匹配了，返回 false
- 最后，如果p2还没到结尾，如果p2及其后面都是'*'，那么匹配成功，否则失败

```java
bool isMatch(string s, string p) {
	int star=-1, s1=0, p1=0, matched=0;
	while (s1 < s.length()) {
		if (p[p1]=='?' || s[s1]==p[p1]) {++s1, ++p1;}
		else if (p[p1] == '*') {star = p1++; matched = s1;}
		else if (star>=0) {p1 = star+1; s1 = ++matched;}
		else return false;
	}
	while (p1<p.length() && p[p1]=='*') ++p1;
	return p1==p.length();
}
```