---
title: KMP
date: 2016-09-12 11:05:21
tags: [String]
categories: Algorithm
---

KMP算法是是一种在<b>线性时间</b>内对字符串进行匹配的经典算法.
待匹配的字符串是s，模式串为p
###### 匹配原理

![](http://ww2.sinaimg.cn/mw690/9bcfe727jw1f7qppqwfckj20g103m74h.jpg)

算法的出发点很直接，如上图所示，当匹配过程中出现不匹配时，不是简单地将模式串向右移动一位再从头匹配。而是利用匹配中的信息，比如上图，应该直接将模式串移动4位，到达下图的位置：

![](http://ww3.sinaimg.cn/mw690/9bcfe727jw1f7qppr0j6zj20g503tdg2.jpg)

那么算法如何确定应该移动几位呢？这样的信息其实隐藏在模式串p中。我们把这些信息放在数组中，称之为next数组。（后面再讨论next数组的求法）

    例子中模式串p的next数组位
    A B C D A B D
    0 0 0 0 1 2 0

所以当第k位匹配失败时，模式串向前移动的位数满足：

    移动位数 = 已匹配的字符数 - next[k-1]

###### next数组
<b>next数组就是"前缀"和"后缀"的最长的共有元素的长度
next[i]表示的是p的子串p[0,i]的"前缀"和"后缀"的最长的共有元素的长度</b>
next数组的计算方式依旧采用滑动匹配的方式，并且在计算next[j]时需要使用已经计算过的next值

1. 首先p的第一个字符的最大相同前后缀长度为0
2. 设next[q-1]=k，对于第q个
  - 如果：p[q]==p[k]，那么，next[q] = ++k，break;
  - 否则：因为此时p[q]和p[k]已经不匹配了，所以我们需要将匹配串右移next[k-1]=j位，此时p[0,j-1]和p[q-j,q-1]已经匹配上了，所以此时要看p[j]==p[q]?，所以回到第2步；

![](http://ww4.sinaimg.cn/mw690/9bcfe727jw1f7qppq928aj20bn0800td.jpg)
![](http://ww2.sinaimg.cn/mw690/9bcfe727jw1f7qppqs0frj20cj080js0.jpg)

###### 实现
```java
#include<stdio.h>
#include<string.h>
void makeNext(const char P[],int next[]) {
    int q,k;
    int m = strlen(P);
    next[0] = 0;
    for (q = 1,k = 0; q < m; ++q) {
        // k=0时，无论P[q]和P[k]是否匹配，next[q]都next[k-1]值无关
        // 不匹配时，根据next[k-1]=j右移，并且看P[q]和P[j]的匹配情况
        while(k > 0 && P[q] != P[k])
            k = next[k-1];
        if (P[q] == P[k]) { // next值增长一
            k++;
        }
        next[q] = k;
    }
}

int kmp(const char T[],const char P[],int next[]) {
    int n,m;
    int i,q; // i指示T的索引，q指示P的索引
    n = strlen(T);
    m = strlen(P);
    makeNext(P,next);
    for (i = 0,q = 0; i < n; ++i) {
        // 这里的原理和上面一致
        while(q > 0 && P[q] != T[i])
            q = next[q-1];
        if (P[q] == T[i]) {
            q++;
        }
        if (q == m) { // 找到一个匹配
            printf("Pattern occurs with shift:%d\n",(i-m+1));
            // count++; // 计算模式串出现的次数
            q = next[q-1]; // 找到一个匹配后，寻找下一个匹配，移动p
        }
    }
}

int main() {
    int i;
    int next[20]={0};
    char T[] = "ababxbababcadfdsss";
    char P[] = "abcdabd";
    printf("%s\n",T);
    printf("%s\n",P );
    // makeNext(P,next);
    kmp(T,P,next);
    for (i = 0; i < strlen(P); ++i) {
        printf("%d ",next[i]);
    }
    printf("\n");

    return 0;
}
```
