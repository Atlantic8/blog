---
title: Longest Palindromic Substring
date: 2016-09-09 20:21:53
tags: [LeetCode, DP]
categories: OJ
---

#### Problem
Given a string S, find the longest palindromic substring in S. You may assume that the maximum length of S is 1000, and there exists one unique longest palindromic substring.

#### Solution
本题的解法不止一种。
###### DP解法
- 维护一个二维数组，p[i][j]表示子串substring(i,j+1)是否为回文
- p[i][j] = s[i]==s[j] ? p[i+1][j-1] : false;
- 时间复杂度O(n^2)

具体代码就不贴了

###### 扩展式解法
- 循环扫描每一位
- 以当前为基准，向左右扩展寻找回文子串，要注意的是奇数、偶数长度子串的不同
- 最坏情况的时间复杂度O(n*len)，len为最长回文子串的长度

```java
public class Solution {
private int lo, maxLen;

public String longestPalindrome(String s) {
    int len = s.length();
    if (len < 2)
        return s;
    for (int i = 0; i < len-1; i++) {
         extendPalindrome(s, i, i);  //assume odd length
         extendPalindrome(s, i, i+1); //assume even length
    }
    return s.substring(lo, lo + maxLen);
}

private void extendPalindrome(String s, int j, int k) {
    while (j >= 0 && k < s.length() && s.charAt(j) == s.charAt(k)) {
        j--;
        k++;
    }
    if (maxLen < k - j - 1) {
        lo = j + 1;
        maxLen = k - j - 1;
    }
}}
```

###### Manacher算法
Manacher算法是上面解法思想的延伸，主要除去了一些不必要的比较。

首先用一个非常巧妙的方式，将所有可能的奇数/偶数长度的回文子串都转换成了奇数长度：在每个字符的两边都插入一个特殊的符号。比如 abba 变成 #a#b#b#a#， aba变成 #a#b#a#。 为了进一步减少编码的复杂度，可以在字符串的开始加入另一个特殊字符，这样就不用特殊处理越界问题，比如$#a#b#a#

以字符串12212321为例，经过上一步，变成了 S[] = "$#1#2#2#1#2#3#2#1#";

然后用一个数组<b> P[i] 来记录以字符S[i]为中心的最长回文子串向左/右扩张的长度</b>（包括S[i]），比如S和P的对应关系：

```java
S     #  1  #  2  #  2  #  1  #  2  #  3  #  2  #  1  #
P     1   2  1  2  5   2  1  4   1  2  1  6   1  2   1  2  1
P[i]-1正好是原字符串中回文串的总长度
```

下面计算P[i]，该算法增加两个辅助变量id和mx，其中<b>id表示最大回文子串中心的位置，mx则为id+P[id]，也就是最大回文子串的边界</b>。

这个算法的关键点就在这里了：

当 mx - i > P[j] 的时候，以S[j]为中心的回文子串包含在以S[id]为中心的回文子串中，由于 i 和 j 对称，以S[i]为中心的回文子串必然包含在以S[id]为中心的回文子串中，所以必有 P[i] = P[j]，见下图。

![](http://pic002.cnblogs.com/images/2012/426620/2012100415402843.png)

当 P[j] > mx - i 的时候，以S[j]为中心的回文子串不完全包含于以S[id]为中心的回文子串中，但是基于对称性可知，下图中两个绿框所包围的部分是相同的，也就是说以S[i]为中心的回文子串，其向右至少会扩张到mx的位置，也就是说 P[i] >= mx - i。至于mx之后的部分是否对称，就只能一个一个匹配了。

![](http://pic002.cnblogs.com/images/2012/426620/2012100415431789.png)

对于 mx <= i 的情况，无法对 P[i]做更多的假设，只能P[i] = 1，然后再去匹配了

```java
#include <iostream>
#include <string>
#include<algorithm>
using namespace std;
// 将字符串处理，比如abcd变成：$#a#b#c#d#.
// 这样可以将奇数长度的回文和偶数长度回文一起处理。
string preProcess(string & str) {
    string ret="$#";
    for (int i=0; i<str.length(); i++) {
        ret += str[i];
        ret += "#";
    }
    return ret;
}
int p[2000009]={0};
void getMaxLength(string str) {
    // mostFar记录了i之前回文到达的最右坐标
    // id是与之对应的中心坐标。 p记录的是以i为中心的回文半价，单个字母为1. 
    int id=0, mostFar=0, maxL=0;
    p[0] = 0;
    for (int i=1; i<str.length(); i++) {
        if (mostFar > i) {
            int j=2*id-i; // j and i are symmetric by id.
            if (p[j] < mostFar-i) // extension needed
                p[i] = p[j];
            else
                p[i] = mostFar-i; // extension needed
        } else
            p[i] = 1;
        // extension
        while ((i+p[i]<str.length()) && (i-p[i]>=0) && str.at(i+p[i]) == str.at(i-p[i]))
            ++p[i];
        if (p[i]+i > mostFar) { // update mostFar and id.
            mostFar = (p[i]+i);
            id = i;
        }
    }
    for (int i=0; i<str.length(); i++)
        maxL = max(maxL, p[i]);
    cout<<maxL-1<<endl;
}
int main() {
    int n=0;
    cin>>n;
    string str="";
    for (int i=0; i<n; i++) {
        cin>>str;
        if (str.length() < 2)
            cout<<str.length()<<endl;
        else {
            str = preProcess(str);
            getMaxLength(str);
        }
    }
    return 0;
}

```
