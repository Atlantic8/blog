---
title: Unique Binary Search Trees
date: 2016-11-30 13:48:00
tags: [LeetCode, Binary Tree, DP]
categories: OJ
---

##### Unique Binary Search Trees
###### 问题描述
Given n, how many structurally unique BST's (binary search trees) that store values 1...n?

For example,
Given n = 3, there are a total of 5 unique BST's.

    1         3     3      2      1
     \       /     /      / \      \
      3     2     1      1   3      2
     /     /       \                 \
    2     1         2                 3

###### 解题思路
使用DP的思想解题
定义两个函数：
- G(n)：n个数组成的序列能构成的BST的总数目
- F(i,n), 1<=i<=n：1-n序列以第i个节点为根节点的BST的数目
- G(n)由根节点分别为每个节点的BST组成。对每个F(i,n)，i是根，则左子树有i-1个节点，右子树有n-i个节点

显然，根据上面的定义有：$$G(n)=\sum_{i=1}^nF(i,n)$$ $$F(i,n)=G(i-1) \times G(n-i)$$初始条件：G(0)=1, G(1)=1
所以有：$$G(n)=\sum_{i=1}^nG(i-1)\times G(n-i)$$ 代码如下：
```java
public int numTrees(int n) {
    int [] G = new int[n+1];
    G[0] = G[1] = 1;

    for(int i=2; i<=n; ++i) {
        for(int j=1; j<=i; ++j) {
            G[i] += G[j-1] * G[i-j];
        }
    }
    return G[n];
}
```

##### Unique Binary Search Trees II
###### 问题描述
Given an integer n, generate all structurally unique BST's (binary search trees) that store values 1...n.

For example,
Given n = 3, there are a total of 5 unique BST's.

    1         3     3      2      1
     \       /     /      / \      \
      3     2     1      1   3      2
     /     /       \                 \
    2     1         2                 3

###### 解题思路
与上一题的区别在于本题需要返回所有的BST，而不是仅仅计算结果。
这题可以使用分治递归的思想，大致思想是：
- 对于1-n组成的节点，每个节点都可能是root
- 如果根结点是i，则分别求其左子树和右子树，然后所有左子树和右子树两两配对，加上根节点就是一棵树

```java
public List<TreeNode> generateTrees(int n) {
	return generateSubtrees(1, n);
}

private List<TreeNode> generateSubtrees(int s, int e) {
    List<TreeNode> res = new LinkedList<TreeNode>();
    if (s > e) {
        res.add(null); // empty tree
        return res;
    }

    for (int i = s; i <= e; ++i) {
        List<TreeNode> leftSubtrees = generateSubtrees(s, i - 1);
        List<TreeNode> rightSubtrees = generateSubtrees(i + 1, e);

        for (TreeNode left : leftSubtrees) {
            for (TreeNode right : rightSubtrees) {
                TreeNode root = new TreeNode(i);
                root.left = left;
                root.right = right;
                res.add(root);
            }
        }
    }
    return res;
}
```