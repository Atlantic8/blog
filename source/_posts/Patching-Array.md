---
title: Patching Array
date: 2016-09-05 16:47:55
tags:
categories:
---

#### Problem
Given a sorted positive integer array nums and an integer n, add/patch elements to the array such that any number in range [1, n] inclusive can be formed by the sum of some elements in the array. Return the minimum number of patches required.

Example 1:
nums = [1, 3], n = 6
Return 1.

Combinations of nums are [1], [3], [1,3], which form possible sums of: 1, 3, 4.
Now if we add/patch 2 to nums, the combinations are: [1], [2], [3], [1,3], [2,3], [1,2,3].
Possible sums are 1, 2, 3, 4, 5, 6, which now covers the range [1, 6].
So we only need 1 patch.

Example 2:
nums = [1, 5, 10], n = 20
Return 2.
The two patches can be [2, 4].

Example 3:
nums = [1, 2, 2], n = 5
Return 0.


#### Solution
思路如下：设absent为当前缺失的最小的数，ind为nums的索引，count计数需要添加的数

- 如果存在一个nums[ind]小于absent，那么absent=nums[ind]+absent。这是因为[1,absent)都可以获得，现在又多了一个nums[ind]，所以当前可以得到的范围是[1,absent+nums[ind])，即absent=nums[ind]+absent
- 否则，我们需要引入absent，因为不引入它就没有办法继续，引入absent后，因为[1,absent-1]也是可以得到的，所以当前可以得到的集合是[1,absent+absent-1]，所以新的absent=2*absent
- 还需要注意的是数的表示范围，由于有一个例子n=2147483647，已经超出了int的表示范围，所以absent必须是long型的

```java
public class Solution {
    public int minPatches(int[] nums, int n) {
    	long count = 0, absent = 1, ind = 0;
    	while (absent <= n) {
    		if (ind < nums.length && nums[(int) ind] <= absent) {
    			absent += nums[(int) ind++];
    		} else {
    			++count;
    			absent += absent;
    		}
    	}
    	return (int) count;
    }
}
```
