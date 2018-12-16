---
title: Binary Tree Maximum Path Sum
date: 2016-07-19 15:01:56
tags: [Binary Tree, LeetCode]
categories: OJ
---
### Problem
Given a binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections. The path does not need to go through the root.

For example:
Given the below binary tree,

       1
      / \
     2   3
Return 6.

##### [Original Address](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

### Solution
function getMaxRoot(r) compute max value edged with node r
also, r is the highest node. for example:

       1
      / \
     2   3
getMaxRoot(1) returns 4.
each path has a highest node.
for a single node:
	maxPrice = max(maxPrice, getMaxRoot(r->left)+getMaxRoot(r->right)+r->val);
```java
class Solution {
public:
	int maxPrice;
public:
    int maxPathSum(TreeNode *root) {
        maxPrice=INT_MIN;
        getMaxRoot(root);
        return maxPrice;
    }
    // compute the maximum value of the path with hightest and edge node r.
    int getMaxRoot(TreeNode *r) {
    	if (r == NULL)
    		return 0;
   		int leftM  = max(0,getMaxRoot(r->left));
        int rightM = max(0,getMaxRoot(r->right));  
    	maxPrice = max(maxPrice, leftM+rightM+r->val);
    	return max(leftM,rightM)+r->val;
    }
};
```