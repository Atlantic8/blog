---
title: Minimum Window Substring
date: 2016-08-27 10:26:59
tags: [Sliding window, LeetCode, String]
categories: OJ
---

#### Problem
Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).

For example,
S = "ADOBECODEBANC"
T = "ABC"
Minimum window is "BANC".

Note:
- If there is no such window in S that covers all characters in T, return the empty string "".
- If there are multiple such windows, you are guaranteed that there will always be only one unique minimum window in S.

#### Solution
- 使用滑动窗口、两个指针的思想，从前到后扫描
- 没找到T包含所有字符时，end指针移动，找到时移动start指针
- 注意滑动窗口、双指针类的题目一般都是这么解的

```C++
string minWindow(string s, string t) {
    vector<int> map(128,0);
    for(auto c: t) map[c]++;
    int counter=t.size(), begin=0, end=0, d=INT_MAX, head=0;
    while (end<s.size()) {
        if(map[s[end++]]-->0) counter--; //in t
        while(counter==0){ //valid
            if(end-begin<d)  d=end-(head=begin);
            if(map[s[begin++]]++==0) counter++;  //make it invalid
        }
    }
    return d==INT_MAX? "":s.substr(head, d);
}
```
别人写的精炼代码，拿来参考.
