---
title: Next Right Pointers in Each Node
date: 2016-09-10 15:04:17
tags: [LeetCode, Binary Tree]
categories: OJ
---

#### Problem 1
Given a binary tree

    struct TreeLinkNode {
      TreeLinkNode *left;
      TreeLinkNode *right;
      TreeLinkNode *next;
    }
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

Note:

You may only use constant extra space.
You may assume that it is a <b>perfect binary tree</b> (ie, all leaves are at the same level, and every parent has two children).
For example,
Given the following perfect binary tree,

         1
       /  \
      2    3
     / \  / \
    4  5  6  7
After calling your function, the tree should look like:

         1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \  / \
    4->5->6->7 -> NULL

#### Solution 1
- 将一个节点的左孩子链接到右孩子比较简单
- 根不同的节点无法直接连接在一起，这时需要借用上一层的信息，如果不同根节点的孩子需要连在一起，那么他们的根节点一定是连接起来的
- 所以只要有上一层的连接关系，就可以将下一层连接完成


    设置pre和cur两个指针，指示父层
    pre从跟开始，每次经过最左边的节点，cur从pre开始向右移动
    每到一个新的cur，先设置cur.left.next = cur.right
    如果cur有next节点，则需要设置cur.right.next = cur.next.left
    一层循环完成，pre = pre.left，直到树叶

```java
void connect(TreeLinkNode *root) {
    if (root == NULL) return;
    TreeLinkNode *pre = root;
    TreeLinkNode *cur = NULL;
    while(pre->left) {
        cur = pre;
        while(cur) {
            cur->left->next = cur->right;
            if(cur->next) cur->right->next = cur->next->left;
            cur = cur->next;
        }
        pre = pre->left;
    }
}
```

#### Problem 2
把第一题中的perfect binary tree变成一般的二叉树，要求O(1)空间复杂度
比如：

         1
       /  \
      2    3
     / \    \
    4   5    7
操作完成后：

         1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \    \
    4-> 5 -> 7 -> NULL
#### Solution 2
还是要利用父层的节点关系来帮助子层之间的连接，把父层和子层当成两个相关的list来处理
在二叉树为一般二叉树时，我们就需要考虑节点是否有左孩子，右孩子
我们引入三个指针now指示当前层最左节点。head和tail，分别表示子层上最左边的节点和当前最右的节点

	1 从根节点开始，设置head = tail = null
    2 如果now.left为空，跳过，否则：
        如果tail为空：head = tail = now.left. 表示当找到这一层的头
        否则：tail = tail.next = now.left. 把now.left接到tail上，tail移一位
    3 对now.right的处理和now.left一样
    4 处理完now的子树，将now向右移，now = now.left
    5 如果now = null，那么此时这一层已经结束，now下移一层到下一层最左边，即now = head，此时要把head和tail都设置为null
    6 否则，进入下一循环


```java
void connect(TreeLinkNode *root) {
    TreeLinkNode *now, *tail, *head;

    now = root;
    head = tail = NULL;
    while(now)
    {
        if (now->left)
            if (tail) tail = tail->next =now->left;
            else head = tail = now->left;
        if (now->right)
            if (tail) tail = tail->next =now->right;
            else head = tail = now->right;
        if(!(now = now->next)) // now没有后继，跳到下一行最左边的节点
        {
            now = head;
            head = tail=NULL;  // head和tail设置为null
        }
    }
}
```