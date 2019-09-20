---
title: Majority Element
date: 2016-09-04 15:27:02
tags: [LeetCode]
categories: OJ
---
#### Problem
Given an integer array of size n, find all elements that appear more than ⌊n/3⌋(这是向下取整符号) times. The algorithm should run in linear time and in O(1) space.


#### Solution
这是主元素法的扩展，原主元素问题是：

设T[0:n-1]是n个元素的数组。对任一元素x，设S(x)={i|T[i]=x}。当|S(x)|>n/2时，称x为T的主元素。设计一个线性时间算法，确定T[0:n-1]是否有一个主元素。


解法为：如果每次删除两个不同的数字（不管是否包含主元素的数字），那么在剩下的数字中，主元素的出现的次数仍然超过总数的一半。可以通过不断的重复这个过程，转化为更小的问题，从而得到答案。

```java
master(A):
    n ← length[A]
    count ← 1
    seed ← A[0]
    找候选主元素，即数目最多的那个元素
    for i ← 1 to n – 1
        do if A[i] = seed
            then count ← count + 1
        else if count > 0
            then count ← count – 1
        else seed ← A[i]
    查找候选主元素是否是主元素
    count ← 0
    for i ← 0 to n – 1
        do if A[i] = seed
            then count ← count + 1
        if count > n/2
            then return seed and count
        else
            return null
```

在此基础上，本题的解题思路：

- 题目要求寻找个数大于⌊n/3⌋的元素，那么长度为n的数组中最多只有两个这样的元素。
- 使用两个标记，寻找出现次数最大和次大的元素
- 判断这两个元素是否满足：个数大于⌊n/3⌋

```java
public Class Solution {
    public List<Integer> majorityElement(int[] nums) {
        List<Integer> ret = new ArrayList<Integer>();
        if (nums.length == 0) return ret;
        int cand1=0,cand2=0,count1=0,count2=0;
        for (int i=0; i<nums.length; i++) {
            // if elseif可以防止cand1,cand2相同
            if (nums[i] == cand1) ++count1;
            else if (nums[i] == cand2) ++count2;
            else if (count1 == 0) { cand1 = nums[i]; count1 = 1; }
            else if (count2 == 0) { cand2 = nums[i]; count2 = 1; }
            else { --count1; --count2; }
        }
        count1=0; count2=0;
        // 判断候选元素数目是否满足条件
        for (int i=0; i < nums.length; i++) {
            if (nums[i] == cand1) ++count1;
            else if (nums[i] == cand2) ++count2;
        }
        if (count1 > nums.length/3) ret.add(cand1);
        if (count2 > nums.length/3) ret.add(cand2);
        return ret;
    }
}
```