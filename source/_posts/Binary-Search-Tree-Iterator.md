---
title: Binary Search Tree Iterator
date: 2016-11-16 22:34:46
tags: [LeetCode, Binary Tree]
categories: OJ
---

##### Problem
Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.

Calling <b>next()</b> will return the next smallest number in the BST.

Note: next() and hasNext() should run in average O(1) time and uses O(h) memory, where h is the height of the tree.

##### Solution
思路是使用栈。
1. 给定根节点root，从root开始不断向左，将遇到的每个节点入栈
2. 使用next函数时，栈顶top节点出栈，将top节点设置为root，执行步骤1
3. hasNext函数：查看栈是否为空即可


```java
class BSTIterator {
    stack<TreeNode *> myStack;
public:
    BSTIterator(TreeNode *root) {
        pushAll(root);
    }

    /** @return whether we have a next smallest number */
    bool hasNext() {
        return !myStack.empty();
    }

    /** @return the next smallest number */
    int next() {
        TreeNode *tmpNode = myStack.top();
        myStack.pop();
        pushAll(tmpNode->right);
        return tmpNode->val;
    }

private:
    // 从root开始不断向左，将遇到的每个节点入栈
    void pushAll(TreeNode *node) {
        for (; node != NULL; myStack.push(node), node = node->left);
    }
};
```