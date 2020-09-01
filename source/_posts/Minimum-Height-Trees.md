---
title: Minimum Height Trees
date: 2016-09-03 14:29:46
tags: [Leetcode]
categories: OJ
---

#### Problem
For a undirected graph with tree characteristics, we can choose any node as the root. The result graph is then a rooted tree. Among all possible rooted trees, those with minimum height are called minimum height trees (MHTs). Given such a graph, write a function to find all the MHTs and return a list of their root labels.

Format
The graph contains n nodes which are labeled from 0 to n - 1. You will be given the number n and a list of undirected edges (each edge is a pair of labels).

You can assume that no duplicate edges will appear in edges. Since all edges are undirected, [0, 1] is the same as [1, 0] and thus will not appear together in edges.

Example 1:

Given n = 4, edges = [[1, 0], [1, 2], [1, 3]]

        0
        |
        1
       / \
      2   3
return [1]

Example 2:

Given n = 6, edges = [[0, 3], [1, 3], [2, 3], [4, 3], [5, 4]]

     0  1  2
      \ | /
        3
        |
        4
        |
        5
return [3, 4]



#### Solution
解体思想是，维护图的每个度为1的节点为叶节点集合，loop：
- 每层循环，对每一个叶节点，从叶节点集合中去掉当前页节点，并去除该叶节点上的边(指向此叶节点的边也得去掉)
- 对于，每个去掉的叶节点，如果与其相连的节点也成为了叶节点，将其加入叶节点集合
- 每次删除一个叶节点，将节点总数-1
- 当节点总数<=2时，退出循环，此时叶节点集合即为所求

```java
public class Solution {
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        if (n == 1) return Collections.singletonList(0);
        HashMap<Integer, Set<Integer>> map = new HashMap<>();
        // 建立邻接表
        for (int[] edge : edges) {
            map.computeIfAbsent(edge[0], k->new HashSet<Integer>()).add(edge[1]);
            map.computeIfAbsent(edge[1], k->new HashSet<Integer>()).add(edge[0]);
        }
        // 叶节点集合
        List<Integer> leafs = new LinkedList<>();
        for (Integer key : map.keySet())
            if (map.get(key).size() == 1) leafs.add(key);
        while (n > 2) {
            n -= leafs.size();
            List<Integer> new_leafs = new LinkedList<>();
            for (Integer leaf : leafs) {
                // 删除指向此叶节点的边
                int box = map.get(leaf).iterator().next();
                map.get(box).remove(leaf);
                // 新的叶节点出现
                if (map.get(box).size() == 1) new_leafs.add(box);
            }
            leafs = new_leafs;
        }
        return leafs;
    }
}
```
