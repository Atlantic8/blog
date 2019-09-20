---
title: Maximum Gap
date: 2016-09-10 09:34:02
tags: [Sort, LeetCode]
categories: OJ
---

#### Problem
<b>Given an unsorted array, find the maximum difference between the successive elements in its sorted form</b>.

Try to solve it in <b>linear time/space</b>.

Return 0 if the array contains less than 2 elements.

You may assume all elements in the array are non-negative integers and fit in the 32-bit signed integer range.

#### Solution
解题思路：由于需要在O(n)的时间复杂度完成，一般的比较排序都不行了，这里考虑使用<b>Bucket sort</b>方法，主要的思想是将元素分配到bucket中

- 扫描一遍数组，得到最大、最小值max、min
- 创建n-1个bucket，从min到max，长度向上取整
- 将数组中除min、max之外的n-2个元素放入n-1个bucket中，所以必然有一个为空
- 每个bucket维护一个最大最小值，其他值忽略，因为最大间距必然出现在bucket之间
- 注意也要考虑min和max与临近数的gap
- 如果设置n+1个bucket的话，就可以把min、max也加入，而寻找最大gap时就不需要单独考虑min、max了

```java
public class Solution {
    public int maximumGap(int[] num) {
        if (num.length < 2) return 0;
        int N=num.length,bucketSize=0,bucketNum=0,minElement=Integer.MAX_VALUE,maxElement=0;
        // 确定最值
        for (int i=0; i<N; i++) {
            minElement = Math.min(minElement, num[i]);
            maxElement = Math.max(maxElement, num[i]);
        }
        bucketSize = (int)Math.ceil(((double)(maxElement-minElement))/(N-1)); // bucket的大小
        bucketNum  = (int)Math.ceil(((double)(maxElement-minElement))/bucketSize); // bucket数量
        int[] bucketMax = new int[bucketNum+1],bucketMin = new int[bucketNum+1];
        for (int i=0; i<=bucketNum; i++) {
            bucketMax[i]=Integer.MIN_VALUE;
            bucketMin[i]=Integer.MAX_VALUE;
        }
        for (int i=0; i<N; i++) {  //put elements in buckets
            if (num[i]==minElement || num[i]==maxElement) // 不加入最值
                continue;
            int bucketId = (int) Math.ceil(((double)(num[i]-minElement))/bucketSize); // 计算bucket编号
            bucketMax[bucketId] = Math.max(num[i], bucketMax[bucketId]);
            bucketMin[bucketId] = Math.min(num[i], bucketMin[bucketId]);
        }
        int maxGap=0, temp=minElement; // temp设置为最小值，可以捕捉最小值和第二小值之间的gap
        // 在bucket之间寻找最大gap
        for (int i=1; i<=bucketNum; i++) {
            if (bucketMin[i]==Integer.MAX_VALUE)
                continue;
            if (maxGap < bucketMin[i]-temp) {
                maxGap = bucketMin[i]-temp;
            }
            temp = bucketMax[i];
        }
        maxGap = Math.max(maxGap, maxElement-temp); 捕捉最大和第二大值之间的gap
        return maxGap;
    }
}
```