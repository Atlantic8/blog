---
title: Minimum Spanning Tree
date: 2016-11-27 10:30:03
tags: [Tree]
categories: Algorithm
---

最小生成树（MST）算法是给定一个无向带权图（V, E），求解最小生成树。

##### 普里姆算法 Prim
Prim算法是逐渐加入点的算法

    输入：一个加权连通图，其中顶点集合为V，边集合为E；

    初始化：Vnew = {x}，其中x为集合V中的任一节点（起始点），Enew = {},为空；

    重复下列操作，直到Vnew = V：

    1. 在集合E中选取权值最小的边<u, v>，其中u为集合Vnew中的元素，而v不在Vnew集合当中，并且v∈V（如果存在有多条满足前述条件即具有相同权值的边，则可任意选取其中之一）；

    2. 将v加入集合Vnew中，将<u, v>边加入集合Enew中；

    输出：使用集合Vnew和Enew来描述所得到的最小生成树

```java
int Prim() {
    int sum=0;
    // dis数组维护的是已经找过的点集 到 每一个点 的最小距离
    // 每个点到第一个点的距离就是其直接距离
    for(int i=1; i<=n; i++)
        dis[i]=map[1][i];
    vis[1]=1;
    for(int i=1; i<n; i++) {
        int min=INF;
        // 找到最近的点
        for(int j=1; j<=n; j++)
            if(!vis[j]&&dis[j]<min) {
                min=dis[j];
                k=j;
            }
        sum+=min;
        vis[k]=1; //标记访问
        // 更新由于引入k点可能带来的距离变化
        for(int j=1; j<=n; j++) {
            if(!vis[j]&&map[k][j]<dis[j]) {
                dis[j]=map[k][j];
            }
        }
    }
    return sum;
}
```
复杂度：$O(n^2)$, 其中$n$为点的个数，适用于边稠密的图。


##### 克鲁斯卡尔算法 Kruskal
###### 并查集 Union-Find
并查集是解决动态连通性一类问题的一种算法，主要思想与树的思想类似，利用根来确定连通性。并查集本质上由两个操作组成，分别是find和join，其中find用于查找最顶层的节点（root），join将两个连通子集合并起来。
```java
int pre[1000 ]; // 存储每一个节点的前继

// 查找根节点
int find(int x) {
    int r=x;
    while ( pre[r ] != r )
        r=pre[r ];

    return r ;
}

// 连接根节点
void join(int x,int y) {
    int fx = find(x);
    int fy = find(y);
    // 设置根之间的关系
    if (fx != fy)
        pre[fx]=fy;
}
```

Kruskal是逐渐加入边的算法

    记Graph中有v个顶点，e个边

    新建图Graphnew，Graphnew中拥有原图中相同的e个顶点，但没有边

    将原图Graph中所有e个边按权值从小到大排序

    循环：从权值最小的边开始遍历每条边 直至图Graph中所有的节点都在同一个连通分量(并查集思想)中
            if 这条边连接的两个节点于图Graphnew中不在同一个连通分量中
                    添加这条边到图Graphnew中

```java
// 间接排序
int cmp(const int i,const int j) {
    return w[i]<w[j];
}
int find(int x) {
    return p[x]==x ? x : p[x]=find(p[x]);
}
int kruskal()
{
    int cou=0,x,y,i,ans=0;
    // 将每个点的前缀初始化为为自己
    for(i=0;i<n;i++) p[i]=i;
    for(i=0;i<m;i++) r[i]=i;
    // 间接排序，排序后第i小的边保存在r[i]中
    sort(r,r+m,cmp);
    // 从小到大取边
    for(i=0;i<m;i++) {
        int e=r[i];
        x=find(u[e]);
        y=find(v[e]);
        // 来自不同的连通分量就可以加入
        if(x!=y) {
            ans += w[e];
            p[x]=y;
            cou++;
        }
    }
    if(cou<n-1) ans=0;
    return ans;
}
```

复杂度：$O(elog_2^e)$，其中$e$为边的数量，适用于边稀疏的图。