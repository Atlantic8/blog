---
title: H-Index
date: 2017-02-21 20:30:46
tags: [LeetCode]
categories: OJ
---

##### H-Index I
###### H-Index
维基百科上H-Index的定义如下

    一个科学家的H-Index为h，如果他一共有N篇文章，其中有h篇文章每一篇都至少有h次引用，其他N-h篇论文每一篇都不超过h次引用

比如给定`citations = [3, 0, 6, 1, 5]`，表示当前研究者有5篇论文，其引用为`citations`中。因为这些论文中有3篇论文每篇都至少有3次引用，其他2篇都没有3次应用，所以他的H-Index为3。
###### 题目描述
给定某个科学家论文引用数目的数组（非负），输出他的H-Index
###### 解题方案
首先，一个拥有N篇论文的科学家，他的H-Index不可能会超过N，最大就是N，最小是0。所以如果一篇论文的引用超过N，那么这篇论文的引用在计算H-Index时和N个引用是一样的；如果引用小于N，不妨设置为t，这篇论文只在H-Index小于等于t时有用，如果H-Index大于t，这篇论文不能被计数。

所以，设置一个长度为N+1的辅助数组`array`，扫描`citations`数组，对于每个引用t，如果
- t < N   : array[t]++
- t >= N : array[N]++

得到数组`array`数组，从后向前，判断方式为如果$ \sum_{k=i}^{N} array[k] >= i $，那么返回$i$，否则继续向前寻找。
```java
int hIndex(vector<int> & citations) {
    int N = citations.size();
    if (N == 0) return 0;
    vector<int> array(N+1, 0);
    for (int i=0; i<N; i++) {
        if (citations[i] > N) array[N]++;
        else array[citations[i]]++;
    }
    int sum = 0;
    for (int i=N; i>0; i--) {
        sum += array[i];
        if (sum >= i) return i;
    }
    return 0;
}
```

##### H-Index II
###### 题目描述
在H-Index的基础上，假设给定的`citations`数据是按升序排序的。求H-Index
###### 解题方案
对于第k篇论文，其引用为`citations[k]`，引用数大于等于`citations[k]`的论文数量为`N-k`，所以对应的H-Index为`min(N-k, citations[k])`。从前向后考虑，开始时始终有`citations[k]<N-k`，对应的候选H-Index为`citations[k]`，到后面有`citations[k]>N-k`，对应的H-Index为`N-k`。也就是说候选H-Index经历了先增大后减小的过程，转折过程就是`citations[k]`第一次大于等于`N-k`的时候。由于H-Index也限制“其他N-h篇论文每一篇都不超过h次引用”，所以我们的目标就是找到第一个`citations[k]>=N-k`的序号k，因为此时k对应的候选H-Index为`N-k`，而k-1对应的候选H-Index肯定小于`N-k+1`，所以k必对应着最优解。

现在有了O(n)复杂度的算法，考虑到引用数据是严格有序的，所以可以使用类似于二分搜索的方法。此时，可以稍微换个角度思考。对于第k篇论文，其引用为`citations[k]`，如果`N-k>=citations[k]`，那么`citations[k]`就是合格的H-Index，此时应该向右尝试寻找更大的H-Index（因为左边的`citations`小）；如果`N-k<citations[k]`，那么`citations[k]`就不是一个当前合法的H-Index（N-k是），所以要向左尝试寻找。

出现`N-k=citations[k]`直接结束了。否则必然存在k满足`citations[k]<N-k && citations[k+1]>N-k-1`，现在考虑`k,k+1,left,right`最终的可能关系，如下

    | k       k+1    |            k     k+1 |  k    k+1            |  k   k+1                   |                   k    k+1  |
    | left     right | left    right        |       left     right |              left    right |  left    right               |
    后面两种情况不可能出现，前三种情况的最终结果都是 `N-left`

再来考虑停止条件，两种情况`left=right`或者`left+1=right`。
1. 当第一种情况出现，`mid=left`，此时如果`citations[mid] > N-mid`，那么`mid=left`就是最佳位置，H-Index为`N-mid`；否则最佳位置在left后一位，此时将`left=mid+1`后，`N-left`就是最佳H-Index。
2. 当第二种情况出现，`left+1=right`，`mid=left`，此时如果`citations[mid] > N-mid`，那么`mid=left`就是最佳位置，H-Index为`N-mid`；否则，设置`left=mid+1`，回到了第一种情况。

```java
int hIndex(vector<int>& citations) {
    int N=citations.size(), left=0, right=N-1, ret=0;
    if (N == 0) return 0;
    while (left <= right) {
        int mid = left + (right-left)/2;
        if (citations[mid] == N-mid) return N-mid;
        else if (citations[mid] > N-mid) right = mid-1; // 向左寻找
        else left = mid+1;                                     // 向右寻找
    }
    return N-left;
}
```