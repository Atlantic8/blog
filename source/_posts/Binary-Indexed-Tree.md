---
title: Binary Indexed Tree
date: 2016-09-23 20:43:51
tags: [Binary Tree, LeetCode]
categories: Algorithm
---

##### 定义
<b>树状数组(Binary Indexed Tree, BIT)用来求区间元素和，求一次区间元素和的时间效率为O(logn)</b>
树状数组是一个可以很高效的进行区间统计的数据结构。在思想上类似于线段树，比线段树节省空间，编程复杂度比线段树低，但适用范围比线段树小。

问题定义：

    有n个元素的数组。可能的操作为

    1.改变数组下标k的元素

    2.查询下标 i~j 的元素和

用树状数组，对操作1和2的时间复杂度都为O(logn)。


##### 算法内容
###### 利用树状数组求前i个元素的和S[i]
<b>![](http://ww4.sinaimg.cn/mw690/9bcfe727jw1f83t9l1oc3j20cu078jro.jpg)</b>
对给定序列：A[1]~A[8]，构建一个树状数组，如上图，其中，C[]是树状数组，S[k]表示从1-k的元素和。
分析C[]的组成如下：

    C[1]=A[1];
    C[2]=A[1]+A[2];
    C[3]=A[3];
    C[4]=A[1]+A[2]+A[3]+A[4];
    C[5]=A[5];
    C[6]=A[5]+A[6];
    C[7]=A[7];
    C[8]= A[1]+A[2]+A[3]+A[4]+A[5]+A[6]+A[7]+A[8];

将数组下标转换成二进制，可得：

    1 --> 00000001
    2 --> 00000010
    3 --> 00000011
    4 --> 00000100
    5 --> 00000101
    6 --> 00000110
    7 --> 00000111
    8 --> 00001000

结论：下标i的二进制中的从右往左数有连续的x个“0”，那么C[i]为序列A[]中的第i-2^x+1到第i个元素的和，即：

    C[i] = A[i-2^x+1] + … + A[i], 其中x为i的二进制中的从右往左数有连续“0”的个数

对于每个i，求x的方法是：<b>2^x = i & (-i)</b>

证明：设A’为A的二进制反码，i的二进制表示成A1B，其中A不管，B为全0序列。那么-i=A’0B’+1。由于B为全0序列，那么B’就是全1序列，所以-i=A’1B，所以：i&(-i)= A1B& A’1B=1B，即2^x的值。

所以，S[i]的方法是：
```java
//返回前i个元素和
int Sum(int i) {
    int s=0;
    while (i > 0) {
        s += C[i];
        i -= i & (-i);
    }
    return s;
}
```

###### 更新C[]
如果A[i]被改变了，那么所有包含A[i]的C[]都要更改，比如，A[3]被改变了，C[3], C[4], C[8]都得修改。
如果A[i]被改变了，那么C[i]必须要更改，并且假设C[k]是C[i]的直接父亲，那么C[k]包含的元素是C[i]包含的元素的2倍，所以：

    k = i + 2^x（x是i的元素数）。

所以更新的方法是：
```java
// A[i]的改变值为value
void Update(int i,int value)  {
    while(i<=n) {
        C[i] += value;
        i += i & (-i);
    }
}
```

##### 二维树状数组
BIT可用为二维数据结果。假设你有一个带有点的平面(有非负的坐标)。合理的操作有三种：

    1.在(x , y)设置点
    2.从(x , y)移除点
    3.在矩形(0 , 0), (x , y)计算点数 - 其中(0 , 0)为左下角，(x , y)为右上角，而边是平行于x轴和y轴。

对于1操作，在（x,y）处设置点，即Update(x,y,1)，因为x，y坐标是离散的，所以我们分别对x,y进行更新即可，函数如下
```java
void Update(int x,int y,int val) {
    while(x<=n) {
        int y1 = y;
         while (y1 <= n) {
            C[x][y1] += val;
            y1 += y1 & (-y1);
        }
        x += x & (-x);
    }
}
```
根据Update可以推得：GetSum函数为：
```java
int GetSum(int x,int y) {
    int sum=0;
    while (x > 0) {
        int y1 = y;
        while (y1 > 0) {
            sum += C[x][y1];
            y1 -= y1 & (-y1);
        }
        x -= x & (-x);
    }
    return sum;
}
```


##### 应用
###### POJ 2352 Stars
给定星星的坐标（y递增，若y相等，x递增），每个星星都有一个等级，规定它的<b>等级就是在它左下方的星星的个数</b>。
输入所有星星后，依次输出等级为0到n-1的星星的个数。

解法：
- 因为数据按y排序（y相等按x排序），所以对第i个星星，之前的星星没有y值大于当前y值的，如果之前的星星k的x值小于当前x值，那么星星k就是对星星i的等级贡献1。并且，星星i后面的星星不可能贡献星星i的等级。
- 所以，计算一个星星的等级就应该在这个星星没正式加入之前，计算之前哪些星星在它左下角，y值严格非递减就不用考虑了，只计数x坐标小于等于当前的个数，可以令A[i]的值是已经加入星星中x坐标为i的星星的数量，i的等级即为 Sum(i);
- 每次加入一个星星，加入星星i之前，计算星星i的贡献，即出现在星星i左下角的星星个数，也即数组A[]中小于等于i的元素和。

```java
#include<stdio.h>
#include<string.h>
#define n 32001
int c[n+5], total[n+5];
int Lowbit(int t) {
    return t&(t^(t-1));
}
int Sum(int end) {
    int sum = 0;
    while(end > 0) {
        sum += c[end];
        end -= Lowbit(end);
    }
    return sum;
}
void add(int li, int val) {
    while(li<=n) {
        c[li] += val;
        li += Lowbit(li);
    }
}
int main() {
    int i, j, x, y, nn;
    scanf("%d", &nn);
    memset(c, 0, sizeof(c));
    memset(total, 0, sizeof(total));
    for(i=1; i<=nn; i++) {
        scanf("%d%d", &x, &y);  //由于坐标x可能为0，因此输入坐标要+1，不然会超时0&(-0)=0;
        add(x+1, 1);
        total[Sum(x+1)-1]++;
    }
    for(i=0; i<nn; i++)
        printf("%d\n", total[i]);
}
```
本题用<b>线段树</b>也可以做，用静态数组结构，开始时就把所有的元素当成0，加入节点，就是一种更新操作。在把A[]抽象出来后，每次加入一个点时，计算Sum，然后更新节点。

```java
#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;
int sum[200000];
struct node {
    int x,y;
} p[20000];
void push_up(int root) {
    sum[root]=sum[root*2]+sum[root*2+1];
}
void update(int root,int l,int r,int p,int v) {
    int mid=(l+r)/2;
    if(l==r) {
        sum[root]++;
        return;
    }
    if(p<=mid)update(root*2,l,mid,p,v);
    else update(root*2+1,mid+1,r,p,v);
    push_up(root);
}
int q_sum(int root,int l,int r,int ql,int qr) {
    if(ql>r||qr<l)return 0;
    if(ql<=l&&r<=qr)return sum[root];
    int mid=(l+r)/2;
    return q_sum(root*2,l,mid,ql,qr)+q_sum(root*2+1,mid+1,r,ql,qr);
}
int main() {
    int n,i,j,m=32000;
    int _hash[20000];
    scanf("%d",&n);
    memset(_hash,0,sizeof(_hash));
    for(i=0; i<n; i++) {
        scanf("%d%d",&p[i].x,&p[i].y);
        _hash[q_sum(1,0,m,0,p[i].x)]++;
        update(1,0,m,p[i].x,1);
    }
    for(i=0; i<n; i++)
        printf("%d\n",_hash[i]);
    return 0;
}

```


##### 二维树状数组

问题描述：

    一个由数字构成的大矩阵，能进行两种操作
    1) 对矩阵里的某个数加上一个整数（可正可负）
    2) 查询某个子矩阵里所有数字的和,要求对每次查询，输出结果

一维扩展到二维的情况：(lowbit(x)=x&(-x))

    C[x][y] = ∑ a[i][j], 其中
        x-lowbit(x) + 1 <= i <= x
        y-lowbit(y) + 1 <= j <= y

在这样的定义下有：

    Sun(1,1)=C[1][1];  Sun(1,2)=C[1][2]; Sun(1,3)=C[1][3]+C[1][2];...
     Sun(2,1)=C[2][1];  Sun(2,2)=C[2][2]; Sun(2,3)=C[2][3]+C[2][2];...
     Sun(3,1)=C[3][1]+C[2][1]; Sun(3,2)=C[3][2]+C[2][2];

求和Sum：
```java
int Sum(int i, int j){
    int result = 0;
    for (int x = i; x > 0; x -= lowbit(x)) {
        for(int y = j; y > 0; y -= lowbit(y)) {
            result += C[x][y];
        }
    }
    return result;
}
```

更新update
```java
private void Modify(int i, int j, int delta){
    A[i][j]+=delta;
    for(int x = i; x< A.length; x += lowbit(x)) {
        for(int y = j; y <A[i].length; y += lowbit(y)) {
            C[x][y] += delta;
        }
    }
}
```

###### POJ 2155
给定MxN矩阵，每个元素取值{0, 1}，合法的操作如下：
- 将左上角坐标为(x1, y1)，右下角坐标为(x2, y2)的矩形区域内的所有元素反转（0->1, 1->0）
- 查询A[i][j]的值

在树状数组中存储该节点的变换次数，因为数值只是0或1，所以奇数次的效果是一样的，偶数次的效果也是一样的。如下图所示：
    反转[(x1, y1), (x2, y2)]等价于：
    分别反转 [(x1, y1), (n,n)], [(x2+1, y2+1), (n,n)], [(x1, y2+1), (n,n)], [(x1+1, y2), (n,n)]
<b>![](http://ww2.sinaimg.cn/mw690/9bcfe727jw1f84ijeapf1j20dw0gotbu.jpg)</b>

```java
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
using namespace std;
const int MAX = 1010;
int c[MAX][MAX];
int n;
int Lowbit(int x) {
    return x & (-x);
}

// 是将以(n,n)为右下角，(x,y)为左上角的矩形区域反转
// 需要把所有包含(x, y)的c数组元素更新
void Updata(int x,int y) {
    int i,k;
    for(i=x; i<=n; i+=Lowbit(i))
        for(k=y; k<=n; k+=Lowbit(k))
            c[i][k]++;
}

// 包含点(x, y)的所有区间的总反转次数
// 因为反转都是左上->右下，所以包含点(x, y)的区间端点不会在(x, y)右、下角
int Get(int x,int y) {
    int i,k,sum = 0;
    for(i=x; i>0; i-=Lowbit(i))
        for(k=y; k>0; k-=Lowbit(k))
            sum += c[i][k];
    return sum;
}
int main() {
    int ncases,m;
    int x1,y1,x2,y2;
    char ch[2];
    scanf("%d",&ncases);
    while( ncases-- ) {
        memset(c,0,sizeof(c));
        scanf("%d%d",&n,&m);
        while( m-- ) {
            scanf("%s",ch);
            if( ch[0] == 'C' ) {
                scanf("%d%d%d%d",&x1,&y1,&x2,&y2);
                x1++; y1++; x2++; y2++;
                Updata(x2,y2);
                Updata(x1-1,y1-1);
                Updata(x1-1,y2);
                Updata(x2,y1-1);
            } else {
                scanf("%d%d",&x1,&y1);
                printf("%d/n",Get(x1,y1)%2);
            }
        }
        printf("/n");
    }
return 0;
}

```






