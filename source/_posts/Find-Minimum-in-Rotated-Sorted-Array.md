---
title: Find Minimum in Rotated Sorted Array
date: 2016-11-09 09:27:53
tags: [LeetCode, Binary Search]
categories: OJ
---

##### Problem
Suppose a sorted array is rotated at some pivot unknown to you beforehand.

(i.e., 0 1 2 4 5 6 7 might become 4 5 6 7 0 1 2).

Find the minimum element.

You may assume no duplicate exists in the array.

##### Solution
将数组旋转，则会将小元素转到数组后面。
这是一个经典的二叉搜索问题，考虑如下：
对于位于下标[start,  end]范围内的元素，如果有
- a[start] < a[end]: 那么从start到end范围内的元素是有序的，第一个元素便是其最小值
- 否则，看mid = start+(end-start)/2
  - 如果a[start] < a[mid]，那么旋转位置在(mid, end)之间，这时设置 start = mid+1
  - 否则，旋转位置在(start, mid)之间, 这时设置 end = mid

```java
int findMin(vector<int> &num) {
	int start=0,end=num.size()-1;

	while (start<end) {
		if (num[start] < num[end])
        	return num[start];
        int mid = start+(end-start)/2;
        if (num[mid] > num[start]) {
			start = mid+1;
		} else {
			end = mid;
		}
	}

	return num[start];
}
```

##### Extension
###### 重复元素
如果存在元素重复现象怎么办。即有可能出现没法判断应该向左还是向右的情况，所以简单的做法是将end-1。

```java
class Solution {
public:
    int findMin(vector<int> &num) {
        int lo = 0;
        int hi = num.size() - 1;
        int mid = 0;

        while(lo < hi) {
            mid = lo + (hi - lo) / 2;

            if (num[mid] > num[hi]) {
                lo = mid + 1;
            }
            else if (num[mid] < num[hi]) {
                hi = mid;
            }
            else { // when num[mid] and num[hi] are same
                hi--;
            }
        }
        return num[lo];
    }
};
```

###### 二叉搜索的标准写法
```java
int binary_search(int *a, int left, int right, int target) {
	// 循环结束判断
    while (left <= right) {
    	int mid = left + (right-left)/2;
        if (a[mid] == target)
        	return mid;
        // 如果left=2, right=3,并且a[2]<target是将陷入死循环
        if (a[mid] < target)
        	left = mid+1;
        else
        	right = mid-1;
    }

}
```
