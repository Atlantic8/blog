---
title: Remove Duplicate Letters
date: 2016-08-25 09:45:42
tags: [LeetCode, Greedy]
categories: OJ
---

##### Problem
Given a string which contains only lowercase letters, remove duplicate letters so that every letter appear once and only once. You must make sure your result is the smallest in lexicographical order among all possible results.

Example:
Given "bcabc"
Return "abc"

Given "cbacdcbc"
Return "acdb"

##### Solution
给定字符串s，使用贪心算法一定能得到最优解。需要稍微注意点的是，遇到只出现了一次的字符串的情况
1. 扫描一遍字符串，获取每个字符对应的出现次数
2. 扫描一遍字符串，寻找找到最小的字符对应的下标。每扫描到一个字符，其出现次数要-1，如果减完1后是0，表示这个字符是唯一的，所以要在此停顿，处理前面出现的最小字符。(下一次字符出现次数会重新计数)

```java
public class Solution {
    public String removeDuplicateLetters(String s) {
        if (s.length() == 0) return "";
    	int[] map = new int[26];
        for (int i=0; i<s.length(); i++)
        	map[s.charAt(i)-'a'] += 1;
        int pos = 0;
        for (int i=0; i<s.length(); i++) {
        	if (s.charAt(i) < s.charAt(pos)) pos = i;
        	if (--map[s.charAt(i)-'a'] == 0) break;
        }
        return s.charAt(pos)+removeDuplicateLetters(s.substring(pos+1).replaceAll(""+s.charAt(pos), ""));
    }
}
```