---
title: Insert Interval
date: 2016-09-07 22:20:10
tags: [LeetCode]
categories: OJ
---

#### Problem
Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).
You may assume that the intervals were initially sorted according to their start times.

Example 1:
Given intervals [1,3],[6,9], insert and merge [2,5] in as [1,5],[6,9].

Example 2:
Given [1,2],[3,5],[6,7],[8,10],[12,16], insert and merge [4,9] in as [1,2],[3,10],[12,16].

This is because the new interval [4,9] overlaps with [3,5],[6,7],[8,10].

#### Solution
题的意思比较直观，简洁的代码是最棒的

```java
public List<Interval> insert(List<Interval> intervals, Interval newInterval) {
    int i=0;
    // 把能合并的区间之前的区间skip
    while (i<intervals.size() && intervals.get(i).end<newInterval.start) i++;
    // 把能合并的区间删除
    while (i<intervals.size() && intervals.get(i).start<=newInterval.end) {
        newInterval = new Interval(Math.min(intervals.get(i).start, newInterval.start), Math.max(intervals.get(i).end, newInterval.end));
        intervals.remove(i);
    }
    // 添加合并完的集合
    intervals.add(i,newInterval);
    return intervals;
}
```
