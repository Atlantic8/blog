---
title: Longest Substring
date: 2016-08-27 10:55:20
tags: [String, Sliding window, LeetCode]
categories: OJ
---
#### Longest Substring
##### Problem -- Without Repeating Characters
Given a string, find the length of the longest substring without repeating characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

##### Solution
- 双指针思想，滑动窗口
- 没找到T包含所有字符时，end指针移动，找到时移动start指针
- 注意滑动窗口、双指针类的题目一般都是这么解的

```c++
int lengthOfLongestSubstring(string s) {
    vector<int> map(128,0);
    int counter=0, begin=0, end=0, d=0;
    while(end<s.size()){
        if(map[s[end++]]++>0) counter++;
        while(counter>0) if(map[s[begin++]]-->1) counter--;
        d=max(d, end-begin); //while valid, update d
    }
    return d;
}
```

##### Problem -- At Most Two Distinct Characters
Given a string, find the length of the longest substring T that contains at most 2 distinct characters.

For example, Given s = “eceba”,

T is "ece" which its length is 3.

##### Solution
- 子串只能包含最多2个不同的字符，所以扫描的时候，count表示子串不同字符的数量
- 需要记录子串中每个字符出现的次数，第一次出现时count+1，第二次、三次等不需要
- 加入字符后，如果count>2，需要从子串的头部删除元素，直到满足count<=2为止

```c++
int lengthOfLongestSubstringTwoDistinct(string s) {
    vector<int> map(128, 0);
    int counter=0, begin=0, end=0, d=0;
    while(end<s.size()){
    	// add a new character
        if(map[s[end++]]++==0) counter++;
        // at most 2 distinct characters, so, count <= 2
        // only when map[s[begin]]--==1, we get rid of s[begin] completely
        while(counter>2) if(map[s[begin++]]--==1) counter--;
        // update d
        d=max(d, end-begin);
    }
    return d;
}
```

##### Problem -- At Most k Distinct Characters
Given a string s, find the length of the longest substring T that contains at most k distinct characters.

Example
For example, Given s = "eceba", k = 3,

T is "eceb" which its length is 4

##### Solution
思路同上一题，只需要将2变成k即可

```c++
int lengthOfLongestSubstringKDistinct(string s, int k) {
    vector<int> map(128, 0);
    int counter=0, begin=0, end=0, d=0;
    while(end<s.size()){
    	// add a new character
        if(map[s[end++]]++==0) counter++;
        // at most k distinct characters, so, count <= k
        // only when map[s[begin]]--==1, we get rid of s[begin] completely
        while(counter>k) if(map[s[begin++]]--==1) counter--;
        // update d
        d=max(d, end-begin);
    }
    return d;
}
```

#### Generalization
对于要求寻找特定要求的子串的问题，通用解法就是滑动窗口的思想，使用哈希表和双指针，可以有如下模板：
```c++
int findSubstring(string s){
    vector<int> map(128,0);
    int counter; // check whether the substring is valid
    int begin=0, end=0; //two pointers, one point to tail and one  head
    int d; //the length of substring

    for() { /* initialize the hash map here */ }

    while(end<s.size()){

        if(map[s[end++]]-- ?){  /* modify counter here */ }

        while(/* counter condition */){

            /* update d here if finding minimum*/

            //increase begin to make it invalid/valid again

            if(map[s[begin++]]++ ?){ /*modify counter here*/ }
        }

        /* update d here if finding maximum*/
    }
    return d;
}
```
[原文地址](https://discuss.leetcode.com/topic/30941/here-is-a-10-line-template-that-can-solve-most-substring-problems)，感谢作者