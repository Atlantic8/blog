---
title: Sliding Window Median
date: 2017-06-17 10:03:17
tags: [Sliding window, LeetCode]
categories: OJ
---

###### 题目描述
给定数组nums和滑动窗口长度k，求滑动窗口由左向右滑动时**窗口内元素的中位数**。

    Given nums = [1,3,-1,-3,5,3,6,7], and k = 3.

    Window position                Median
    ---------------               -----
    [1  3  -1] -3  5  3  6  7       1
     1 [3  -1  -3] 5  3  6  7       -1
     1  3 [-1  -3  5] 3  6  7       -1
     1  3  -1 [-3  5  3] 6  7       3
     1  3  -1  -3 [5  3  6] 7       5
     1  3  -1  -3  5 [3  6  7]      6

###### 解题思路
容易想到用set的思想，由于数组可能会有重复，所以使用的数据结构为`multiset`。思想如下：
- 维护一个名为window的multiset
- 每次通过迭代器获取中位数

```java
vector<double> medianSlidingWindow(vector<int>& nums, int k) {
    multiset<int> ms(nums.begin(), nums.begin()+k);
    vector<double> ret;
    for (int i=k; i<=nums.size(); i++) {
        // k/2处，基数数组正好是中位数，偶数数组则是中间偏右的那一个
        auto mid = next(ms.begin(), k/2);
        if (k % 2 == 0) ret.push_back((double(*mid) + *prev(mid))/2.0);
        else ret.push_back(*mid);
        if (i == nums.size()) break;
        ms.insert(nums[i]);
        // 删除要用迭代器，否则将会删除所有值相同的元素
        // lower_bound取到值相同的最左边的元素
        ms.erase(ms.lower_bound(nums[i-k]));
    }
    return ret;
}
```
时间复杂度为`O(kn)`。

---

**更好的方法**
- 使用一个指针mid用以指向median值（基数指向中间那个元素、偶数指向中间两个元素的后一个）。
- 向window中加入/删除元素时，考虑两边比较麻烦（没做对==!）。这里的做法是**保证mid左边的元素个数不变，不管右侧如何**，这样结束后还是mid该在的位置
    - 添加元素时，如果添加的元素在mid左边，mid左移一位
    - 删除元素时，如果删除的元素在mid左边，mid右移一位


```java
vector<double> medianSlidingWindow(vector<int>& nums, int k) {
    multiset<int> window(nums.begin(), nums.begin() + k);
    auto mid = next(window.begin(), k / 2);
    vector<double> medians;
    for (int i=k; ; i++) {

        // Push the current median.
        medians.push_back((double(*mid) + *prev(mid, 1 - k%2)) / 2);

        // If all done, return.
        if (i == nums.size())
            return medians;

        // Insert nums[i].
        window.insert(nums[i]);
        // 只保证左边的元素个数不变，右边不用管
        // 如果新插入的在左边，则左移一位，保证左边元素数量不变
        if (nums[i] < *mid)
            mid--;

        // Erase nums[i-k].
        // 只保证左边的元素个数不变，右边不用管
        // 如果删除的在左边，右移一位保证左边的元素个数不变
        if (nums[i-k] <= *mid)
            mid++;
        window.erase(window.lower_bound(nums[i-k]));
    }
}
```

###### Find Median from Data Stream
实现一个数据结构，满足两种操作：
1. 加入元素
2. 计算结构中元素的中位数

###### 解题思路
- 使用两个优先队列（大根堆），将数据分成两部分，左边存较小的一部分，右边存较大一部分的相反数
- 计算中位数时，如果左边的个数大于右边，则左边的堆顶就是中位数；否则，两个堆的堆顶元素计算中位数
- 需要加入一个新的数时，先push进左边的堆，然后从左边的堆中pop出最大值到右边的堆
- 如果左侧堆的数量小于右侧的数量，右侧弹出一个元素并将其相反数放入左侧堆

```java
priority_queue<int> left;
priority_queue<int> right;
MedianFinder() {}
    
void addNum(int num) {
    left.push(num); // push到左侧
    right.push(-left.top()); // 左侧的最大值push到右侧
    left.pop();
    if (left.size() < right.size()) { // 确保左右两边的数量关系
        int tmp = -right.top();
        right.pop();
        left.push(tmp);
    }
}
    
double findMedian() {
    return left.size()>right.size()?double(left.top()) : (double(left.top())-right.top())/2;
}
```
