---
title: Container With Most Water
date: 2016-09-07 21:43:54
tags: [LeetCode,Greedy]
categories: OJ
---

#### Problem
Given n non-negative integers a1, a2, ..., an, where each represents a point at coordinate (i, ai).
n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0).
Find two lines, which together with x-axis forms a container, such that the container contains the most water.

#### Solution
思路如下：假如已经计算了i和j之间的最大值
- 假如: height[i]<height[j]，因为对所有的k属于[i+1, j-1]，必然有m[i][j] 大于 m[i][k]，所以++i
- 反之：--j

```java
class Solution {
public:
    int maxArea(vector<int> &height) {
        int i=0, j=height.size()-1, maxArea=0;
        while (i < j) {
            maxArea = max(maxArea, (j-i)*min(height[i],height[j]));
            if (height[i] <= height[j])
                ++i;
            else
                --j;
        }
        return maxArea;
    }
}
```