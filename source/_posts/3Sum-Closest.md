---
title: 3Sum Closest
date: 2016-11-09 10:21:26
tags: [LeetCode]
categories: OJ
---

##### Problem
Given an array S of n integers, find three integers in S such that the sum is closest to a given number, target. Return the sum of the three integers. You may assume that each input would have exactly one solution.

    For example, given array S = {-1 2 1 -4}, and target = 1.

    The sum that is closest to the target is 2. (-1 + 2 + 1 = 2)

##### Solution
最简单的莫过于O(n^3)的遍历算法了。
这里介绍一个O(n^2)的方法：
- 设置first,second和third三个下标。将数组先排序
- 第一层循环固定住first，将second放在first+1，将third放在最后
- 计算当前和curSum
  - 如果curSum等于目标值target，直接返回
  - 如果curSum比记录值更好，更新记录值
  - 然后更改second或third。如果curSum大于target，则third--，否则second++
  - 当second和third相遇，内层循环结束。first++迭代

由于second和third这样移动的复杂度为O(n)，所以整体的复杂度为O(n^2).

```java
int threeSumClosest(vector<int>& nums, int target) {
    if(nums.size() < 3) return 0;
    int closest = nums[0]+nums[1]+nums[2];
    sort(nums.begin(), nums.end());
    for(int first = 0 ; first < nums.size()-2 ; ++first) {
        if(first > 0 && nums[first] == nums[first-1]) continue;
        int second = first+1;
        int third = nums.size()-1;
        while(second < third) {
            int curSum = nums[first]+nums[second]+nums[third];
            if(curSum == target) return curSum;
            if(abs(target-curSum)<abs(target-closest)) {
                closest = curSum;
            }
            if(curSum > target) {
                --third;
            } else {
                ++second;
            }
        }
    }
    return closest;
}
```
