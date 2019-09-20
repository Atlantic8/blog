---
title: Largest Rectangle in Histogram
date: 2016-09-08 10:20:14
tags: [LeetCode]
categories: OJ
---

#### Problem
Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.

<center>![](http://ww4.sinaimg.cn/mw690/9bcfe727jw1f7lz38exq2j205805oaab.jpg)</center>

Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].
The largest rectangle is shown in the shaded area, which has area = 10 unit.

For example,
Given heights = [2,1,5,6,2,3],
return 10.

#### Solution
解题思路是：每到一个柱子i，计算以柱子i为最矮柱子的矩形面积，所以需要知道i左侧第一个小于h[i]的序号left，和i右侧第一个小于h[i]的序号right。做法是从左向右遍历，维护一个栈，每个柱子都会入栈一次。当一个比栈顶柱子更小的柱子出现时，栈顶柱子出栈，此时计算以这个出栈的柱子为最矮柱子的矩形面积。此时，当前循环的序号为right，栈里之前的元素是left，算法具体思路如下：
- 创建空的栈
- 从第一个柱子开始——>最后一个柱子
  - 如果栈为空或者h[i]大于栈顶的柱子高度，则将i入栈
  - 如果h[i]小于栈顶的柱子高度，持续从栈顶移除元素直到栈顶对应的柱子的值大于h[i]为止。设被移除的柱子为h[tp]，将h[tp]当作最矮的柱子并计算对应的面积，此时，left为栈中tp之前的元素，right是当前的i
- 如果栈不为空，那么逐个移除其元素，并且按上面的步骤计算对应的面积

因为每个柱子仅入栈、出栈一次，所以算法的复杂度为O(n)。
```java
class Solution {
public:
    int largestRectangleArea(vector<int> &height) {
        vector<int> s;
        int ret = 0;
        height.push_back(0);
        for (int i=0; i<height.size(); i++) {
            while (s.size()>0 && height[s.back()]>=height[i]) {
                int h = height[s.back()], sid=0;
                s.pop_back();
                if (s.size() == 0)
                    sid = 0;
                else
                    sid = s.back()+1;
                if (ret < h*(i-sid))
                    ret = h*(i-sid);
            }
            s.push_back(i);
        }
        return ret;
    }
}
```