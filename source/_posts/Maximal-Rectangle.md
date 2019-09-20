---
title: Maximal Rectangle
date: 2016-09-03 18:54:38
tags: [DP, LeetCode]
categories: OJ
---

#### Problem
Given a 2D binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.

For example, given the following matrix:

1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

Return 6.


#### Solution
本题是DP题，为了能对所有情形考虑，每一列对应一个height值，表示从当前行开始一直向上的最大高度
所以具体的做法是：
- 每到一个位置，计算以这个位置所在列为最高的矩形面积
- 逐行处理，遇到0忽略，遇到1时，计算其height值
- 有了height，还要知道width才能计算数量，width的计算需要借助left、right和left_most、right_most
- 每一行的left、right到下一行才有用，因为要使用当前位置向上延伸的最高高度，所以在向两边延伸时需要上一行两边的情况
- 对于left，从左向右扫描，遇到0时left=0，否则left=max(left_last_row, 本行最近的0的下一位置序号)。（这里遇到0设置left=0是为了不影响下一行）
- 对于right，从右向左扫描，遇到0时right=行长度-1，否则，left=min(right_last_row, 本行最近的0的上一位置序号)
- 扫描这一行，多次计算(right-left+1)*height，并及时更新最大值
- 实现过程中，left、right和height可以分别用一维数组存储，详细见代码

```java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        int m=0, n=0, ret=0;
        if ((m=matrix.length)==0 || (n=matrix[0].length)==0) return 0;
        int[] height=new int[n], left=new int[n], right=new int[n];
        for (int j=0; j<n; j++) right[j] = n-1;
        for (int i=0; i<m; i++) {
            // left_most是当前点左侧最近0点的下一位
            // right_most是当前点右侧最近0点的前一个
            // 这两个变量可以确定以当前点为中心，连续为1的长度
            int left_most = 0, right_most = n-1;
            // 要想使用上一行的left值，本行的left_most必须小于等于上一行对应位的left值
            for (int j=0; j<n; j++) {
                if (matrix[i][j]=='0') {left_most=Math.max(left_most, j+1); left[j] = 0;}
                else left[j] = Math.max(left[j], left_most);
            }
            for (int j=n-1; j>=0; j--) {
                if (matrix[i][j]=='1') right[j] = Math.min(right[j], right_most);
                else {right_most = Math.min(right_most, j-1); right[j] = n-1;}
            }
            // 更新height值，并计算以本行中每个点为底，最高的矩形的面积
            for (int j=0; j<n; j++) {
                if (matrix[i][j]=='0') height[j] = 0;
                else height[j] += 1;
                ret = Math.max(ret, (right[j]-left[j]+1)*height[j]);
            }
        }
        return ret;
    }
}
```

