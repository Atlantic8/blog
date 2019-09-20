---
title: Remove Boxes
date: 2017-04-01 10:17:56
tags: [LeetCode, DP]
categories: OJ
---

###### 题目描述
Given several boxes with different colors represented by different positive numbers.
You may experience several rounds to remove boxes until there is no box left. Each time you can choose some continuous boxes with the same color (composed of k boxes, k >= 1), remove them and get k*k points.
Find the maximum points you can get.

`Example 1`

    Input:
    [1, 3, 2, 2, 2, 3, 4, 3, 1]
    Output:
    23
    Explanation:
    [1, 3, 2, 2, 2, 3, 4, 3, 1] 
    ----> [1, 3, 3, 4, 3, 1] (3*3=9 points) 
    ----> [1, 3, 3, 3, 1] (1*1=1 points) 
    ----> [1, 1] (3*3=9 points) 
    ----> [] (2*2=4 points)

`Note: The number of boxes n would not exceed 100.`

###### 解题思路
本题可以采用递归+memory（DP）的方法解决，思路是：使用数组map[i][j][k]表示从第i个元素到第j个元素，并且后面还有k个boxes[j]，也就是说现在至少有k+1个boxes[j]。对于i-j之间的满足boxes[p]=boxes[j]的元素，满足一下条件
$$
\begin{aligned}
for\;& p\; with\;boxes[p]==boxes[j]: \\ 
&map[i][j][k]=\max_p(map[i][j][k], map[i][p][k+1]+map[p+1][r-1][0])
\end{aligned}
$$
代码为：
```java
int dfs(vector<int>& boxes, int start, int end, int k, int map[100][100][100]) {
    int ret=0;
    if (start > end) return 0;
    if (map[start][end][k] > 0) return map[start][end][k];
    // 记录后面连续boxes[end]的数量
    while (start<end && boxes[end-1]==boxes[end]) {--end; ++k;}
    map[start][end][k] = dfs(boxes, start, end-1, 0, map)+(k+1)*(k+1);
    for (int i=start; i<end; i++) {
        if (boxes[i] == boxes[end]) {
            map[start][end][k]=max(map[start][end][k], dfs(boxes, start, i, k+1, map)+dfs(boxes, i+1, end-1, 0, map));
        }
    }
    return map[start][end][k];
}
int removeBoxes(vector<int>& boxes) {
    int map[100][100][100]={0};
    return dfs(boxes, 0, boxes.size()-1, 0, map);
}
```