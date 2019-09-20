---
title: Reservoir Sampling
date: 2016-09-12 18:59:35
tags: [ LeetCode, random algorithm]
categories: Algorithm
---

##### 算法介绍
Reservoir Sampling（水塘抽样）是一系列的随机算法，其目的在于从包含n个项目的集合S中选取k个样本，其中n为一很大或未知的数量，尤其适用于<b>不能把所有n个项目都存放到主内存</b>的情况。
算法思路如下：

    从S中抽取首k项放入「水塘」中
    对于每一个S[j]项（j ≥ k）：
        随机产生一个范围从0到j的整數r
        若 r < k 则把水塘中的第r项换成S[j]项

##### 相关问题
###### 可否在一未知大小的集合中，随机取出一元素？
第一次直接以第一行作为取出行 choice
第二次以二分之一概率决定是否用第二行替换 choice
第三次以三分之一的概率决定是否以第三行替换 choice
以此类推。
Generally，在取第n个数据的时候，我们生成一个0到1的随机数p，如果p小于1/n，保留第n个数。大于1/n，继续保留前面的数。直到数据流结束，返回此数，算法结束。

证明思路：最后一个数留下的概率是1/N，第一个数留下的概率是1x1/2x2/3x...x(N-1)/N = 1/N，其他元素证明类似，所以每个数被选中的概率是一样的，即这种方法是等概率的。

###### 在一个长度很大但未知的链表中，如何最高效地取出k个元素？
道理同上，在取第n个数据的时候，我们生成一个0到1的随机数p
如果p小于k/n，替换池中任意一个为第n个数
大于k/n，继续保留前面的数
直到数据流结束，返回此k个数
<b>但是为了保证计算机计算分数额准确性，一般是生成一个0到n的随机数，跟k相比，小于k就替换第k项</b>。

###### Random Pick Index <LeetCode>
Given an array of integers with possible duplicates, randomly output the index of a given target number. You can assume that the given target number must exist in the array.

Note:
The <b>array size can be very large</b>. Solution that uses too much extra space will not pass the judge.

    Example:

    int[] nums = new int[] {1,2,3,3,3};
    Solution solution = new Solution(nums);

    // pick(3) should return either index 2, 3, or 4 randomly. Each index should have equal     probability of returning.
    solution.pick(3);

    // pick(1) should return 0. Since in the array only nums[0] is equal to 1.
    solution.pick(1);


解体思想：用简单的map思路来做会超出空间限制，水塘抽样是比较好的方法
- 扫描每一个元素，不是当前要求的忽略
- 遇到第k个目标元素，以1/k的概率替换ret值
- 直到扫描完整个字符串

```java
vector<int> data;
void Solution(vector<int> nums) {
    srand((int)time(NULL)); // 设置时间种子，放在pick里面会导致之间间隔太短而使得随机数不随机
    data = nums;
}

int pick(int target) {
    int ret = 0, n = 1;
    for (int i=0; i<data.size(); i++) {
        if (data.at(i) != target) continue;
        else if (rand()%n++ == 0) ret = i;  // 以以1/k的概率使用第k个target值
    }
    return ret;
}
```