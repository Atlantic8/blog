---
title: Count Complete Tree Nodes
date: 2016-07-19 16:21:35
tags: [Binary Tree, LeetCode]
categories: OJ
---

### Problem
count the total number of Binary Complete Tree nodes

### Solution
- traverse tree skill is not acceptable.

- The height of a tree can be found by just going left. Let a single node tree have height 0. Find the height h of the whole tree. If the whole tree is empty, i.e., has height -1, there are 0 nodes.

- Otherwise check whether the height of the right subtree is just one less than that of the whole tree, meaning left and right subtree have the same height.

- If yes, then the last node on the last tree row is in the right subtree and the left subtree is a full tree of height h-1. So we take the 2^h-1 nodes of the left subtree plus the 1 root node plus recursively the number of nodes in the right subtree.

- If no, then the last node on the last tree row is in the left subtree and the right subtree is a full tree of height h-2. So we take the 2^(h-1)-1 nodes of the right subtree plus the 1 root node plus recursively the number of nodes in the left subtree.

- Since I halve the tree in every recursive step, I have O(log(n)) steps. Finding a height costs O(log(n)). So overall O(log(n)^2).

recursive version:
```java
class Solution {
    int height(TreeNode root) {
        return root == null ? -1 : 1 + height(root.left);
    }
    public int countNodes(TreeNode root) {
        int h = height(root);
        return h < 0 ? 0 :
               height(root.right) == h-1 ? (1 << h) + countNodes(root.right)
                                         : (1 << h-1) + countNodes(root.left);
    }
}
```

iterative version:
```c++
class Solution {
public:
    int countNodes(TreeNode* root) {
        if(!root) return 0;
        int num=1;
        TreeNode *curR(root->left), *curL(root->left);
        // curR is the rightmost edge, which has a height equal to or less than the leftmost edge
        while(curR) {
            curL = curL->left;
            curR = curR->right;
            num = num<<1;
        }
        return  num + ( (!curL)?countNodes(root->right):countNodes(root->left) );
    }
};
```