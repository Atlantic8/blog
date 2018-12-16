---
title: Partition
date: 2017-02-21 13:38:18
tags: [Sort, LeetCode]
categories: [OJ]
---

##### partition函数
`partition`函数是快速排序的核心部分，选定一个基准，然后将大于和小于基准的数分别放置于基准的两边，有多种实现方式，以下是参考

```java
// start, end表明作用范围
// pivotIndex表示基准的位置
int partition(vector<int> & A, int start, int end){
    int i = start, j = end;
    int pivotIndex = rand() % (end-start+1) + start; // 随机选择基准位置
    int pivot = A[pivotIndex];
    // 把基准换到最后
    swap<int>(A[end], A[pivotIndex]);
    while(i < j){
        while(i < j && A[i] < pivot) ++i;
        if (i > j) break;
        while(i < j && A[j] >= pivot) --j;
        if (i > j) break;
        if(i < j) swap<int>(A[i], A[j]);
    }
    swap<int>(A[end], A[i]);
    return i;
}
```

再提供另一种实现方式

```java
// arr[]为数组，start、end分别为数组第一个元素和最后一个元素的索引
// povitIndex为数组中任意选中的数的索引
int partition(int arr[], int start, int end, int pivotIndex) {
    int pivot = arr[pivotIndex];
    swap(arr[pivotIndex], arr[end]);
    int storeIndex = start;
    for(int i = start; i < end; ++i) {
        if(arr[i] < pivot) {
            swap(arr[i], arr[storeIndex]);
            ++storeIndex;
        }
    }
    swap(arr[storeIndex], arr[end]);
    return storeIndex;
}
```

##### Partition函数的应用
###### 快速排序
```java
void quick_sort(vector<int> &A, int start, int end) {
    int mid = partition(A, start, end);
    if (mid-start > 2) quick_sort(A, start, mid-1);
    if (end-mid > 2) quick_sort(A, mid+1, end);
}
```

###### Top K问题
给定未排序数组A，求排好序的数组中的第k个大个数。因为上面的`partition`函数是左小右大，所以我们考虑寻找第`A.size()-k`小的数。
思路是**调用partition函数，返回基准位置，如果基准位置正好是k，那么返回其对应的值
否则，如果基准在k左侧，则考虑基准右边的元素；否则考虑左边的元素。**
```java
int findKthLargest (vector<int> &A, int k) {
	int start=0, end=A.size()-1;
    while (start < end) {
    	int mid = partition(A, start, end);
    	if (mid == k-1) return A[k-1];
    	else if (mid < k-1) start = mid+1;
        else end = mid-1;
    }
}
```


