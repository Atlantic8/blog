---
title: Monotonous Sequence
mathjax: true
date: 2021-01-02 16:12:40
tags: 
categories: OJ
---

单调序列结构，这里不仅仅指的是数组，指的是用于加速检索结果的线性数据结构（vector、队列、栈等）。
用例题解释~

#### Minimum Number in Sliding Window
> 有一个长为 n 的序列 nums，以及一个大小为 k 的窗口。现在这个从左边开始向右滑动，每次滑动一个单位，求出每次滑动后窗口中的最小值

这里介绍一个`O(n)`复杂度的算法。

我们可以把关键的数据存储起来，利用第 i 个位置的信息计算第 i+1 位置的任务。方法如下：
- 建立一个队列，这个队列需要满足：
  - 新进入队列的数要大于等于队尾的数字，也就是说任何时刻**队列都是单调递增**的
  - 所以如果当前数小于等于队尾的数据，队尾的数据就不可能是窗口最小值。【等于是考虑了位置，位置约靠后越好】
- 对于当前的位置，如果大于k，需要将队列中不满足窗口位置的从队头去掉
  - 所以队列中存储的应该是下标志，而不是元素本身
- 然后将队尾大于当前数字的元素pop出去
- 这时候**队头的元素就是当前窗口中的最小值**

代码实现如下：
```c++
// #include <deque>

vector<int> function(const vector<int>& nums, int k) {
    vector<int> ret;
    if (nums.size() == 0 || k < 1) {
        return ret;
    }
    deque<int> qu; // monotonous queue
    for (int i = 0; i < nums.size(); ++i) {
        if (qu.size() > 0 && i - qu.front() == k) { // window size
            qu.pop_front();
        }
        while(qu.size() > 0) {
            // 队尾大于当前数字的元素pop出去, 保持递增
            if (nums[i] <= nums[qu.back()]) {
                qu.pop_back();
            }
        }
        qu.push_back(i); // 入队
        ret.push_back(nums[qu.front()]); // 对头是最小值
    }
    return ret;
}
```

时间复杂度：因为每个元素入队、出队只有一次，所以整体的复杂度是`O(N)`.


#### 右侧大数
> 有一个长为 n 的整数序列 nums，对于每个元素找到这个元素右侧第一个大于它的值（不存在就-1），返回这个值序列

如果当前元素小于下一个，那么直接就有结果了。如果不是，将当前元素的位置存到栈里面，所以在搜索到新位置时也需要看栈顶元素。所以整体的步骤如下：
- 初始化结果数组ret，新建一个栈stack
- 对于位置i
  - while(nums[i] > nums[stack.top()]):
    - 更新stack.top()位置的值: ret[stack.top()] < nums[i]
    - 栈顶pop：这能保证堆栈从上到下是递增的（栈顶最小）
    - i入栈

```c++
// #include<stack>

vector<int> function(const vector<int>& nums) {
    vector<int> ret(nums.size(), -1);
    if (nums.size() < 2) {
        return ret;
    }
    stack<int> st;
    st.push(nums[0])
    for (int i = 1; i < nums.size(); ++i) {
        while(!st.empty() && nums[st.top()] < nums[i]) {
            ret[st.top()] = nums[i];
            st.pop();
        }
    }
    return ret;
}
```

#### 最长递增子序列
> 有一个长为 n 的整数序列 nums，找到这个序列中最长的递增序列，返回长度

DP思路的复杂度为`O(N^2)`，下面介绍一个复杂度为`O(N*logN)`的算法

维护一个数组vec，位置i的元素表示**长度为i的递增子序列最后一个元素值的最小值**，也就是子序列最大值中的最小值。这样一个数组有一个特点：**数组的元素是递增的**，证明就反证法就好

对于nums中的一个新元素num，我们可以找到vec中m的位置k满足
- `vec[k] < num <= vec[k+1]`，表示最优子序列中，长度k子序列的最大值小于num，但是长度k+1子序列的最大值不小于num，所以我们更新k+1子序列的最大值为num，但是k+2及以后的不行
- 上述操作可以线性搜索，但是因为vec数组是有序的，所以可以通过二分搜索的思想来做

```c++
int function(const vector<int>& nums) {
    if (nums.size() < 2) {
        return nums.size();
    }
    vector<int> vec;
    for (int i = 0; i < nums.size(); ++i) {
        // vec[k] < num <= vec[k+1]，找到位置
        auto idx = upper_bound(vec.begin(), vec.end(), nums[i]);
        if (idx == vec.end()) {
            vec.push_back(nums[i]);
        } else {
            *idx = nums[i];
        }
    }
    return vec.size();
}
```

#### Largest Rectangle in Histogram
见[Largest Rectangle in Histogram](http://atlantic8.github.io/2016/09/08/Largest-Rectangle-in-Histogram/)

