---
title: Palindrome Partitioning II
date: 2016-09-06 21:50:52
tags: [DP, LeetCode]
categories: OJ
---

#### Problem
Given a string s, partition s such that every substring of the partition is a palindrome.

Return the minimum cuts needed for a palindrome partitioning of s.

For example, given s = "aab",
Return 1 since the palindrome partitioning ["aa","b"] could be produced using 1 cut.


#### Solution
这题明显是DP题，因为满足最优子结构性质。
刚开始，我使用了如下的表达式
```java
num[i,j] = min(num[i,k]+num[k+1,j])
```
但是超时了，在例子很大的时候TLE，其复杂度达到: O(n^3)

下面介绍通过的代码思想：
- 用num[i]数组记录字符串s的[0~i-1]子串需要的最小切割次数
- 每到一个i，向两侧延伸寻找最长的回文子串，需要分别考虑回文子串的长度为奇数、偶数
- 比如考虑在i时的奇数长度回文子串，长度/2=k，则num[i+k]=min(num[i-k-1]+1, num[i+k])

```java
public class Solution {
    public int minCut(String s) {
        int[] num = new int[s.length()+1];
        for (int i = 0; i <= s.length(); i++) num[i] = i-1;
        for (int i = 0; i < s.length(); i++) {
            // 奇数回文子串
            for (int j=0; i-j>=0 && i+j<s.length() && s.charAt(i-j)==s.charAt(i+j); j++)
                num[i+j+1] = Math.min(num[i+j+1], num[i-j]+1);
            // 偶数回文子串
            for (int j=0; i-j>=0 && i+j+1<s.length() && s.charAt(i-j)==s.charAt(i+j+1); j++)
                num[i+j+2] = Math.min(num[i+j+2], num[i-j]+1);
        }
        return num[s.length()];
    }
}
```