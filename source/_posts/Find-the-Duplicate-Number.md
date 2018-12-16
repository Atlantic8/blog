---
title: Find the Duplicate Number
date: 2016-09-04 15:28:10
tags: LeetCode
categories: OJ
---

#### Problem
Description

Given an array nums containing n + 1 integers where each integer is between 1 and n (inclusive), prove that at least one duplicate number must exist. Assume that there is only one duplicate number, find the duplicate one.

Note:

- You must not modify the array (assume the array is read only).
- You must use only constant, O(1) extra space.
- Your runtime complexity should be less than O(n2).
- There is only one duplicate number in the array, but it could be repeated more than once.

#### Solution

- 题中给定的是数组，由于长度位n+1的数组只有1-n的整数，所以可以把数组看成静态链表，数组下标是节点值，对应的值指示下一节点的值
- 我们所要求的重复元素其实就是：不同的下标对应相同的值，在静态链表中也就是loop的入口节点的值
- 由于必然存在重复，所以这个静态链表肯定存在loop，查找loop入口节点的值方法和Linked List Cycle II一致

```java
public class Solution {
    public int findDuplicate(int[] nums) {
        int slow=nums[0], fast=nums[nums[0]];
        while (fast != slow) {
        	slow=nums[slow];
        	fast=nums[nums[fast]];
        }
        fast = 0;
        while (fast != slow) {
        	slow=nums[slow];
        	fast=nums[fast];
        }
        return fast;
    }
}
```

[相关问题：Linked List Cycle II](http://atlantic8.github.io/2016/09/04/Linked-List-Cycle/)