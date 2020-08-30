---
title: Binary Tree Traverse
date: 2016-09-07 20:27:27
tags: [Binary Tree]
categories: Algorithm
---
updated

---

##### 前序遍历
根据前序遍历访问的顺序，<b>优先访问根结点，然后再分别访问左孩子和右孩子<b>。即对于任一结点，其可看做是根结点，因此可以直接访问，访问完之后，若其左孩子不为空，按相同规则访问它的左子树；当访问其左子树时，再访问它的右子树。因此其处理过程如下：
**首先将根节点入栈**，然后对于任一结点P：
1. 弹出节点P，访问P
2. 分别将节点P的右、左孩子入栈（如果有的话）

```java
void preOrder(TreeNode *root) {    //非递归前序遍历
    stack<TreeNode*> s;
    TreeNode *p=root;
    while (p || !s.empty()) {
        if (p != NULL) { // 使劲向左
            visit(p);
            s.push(p);
            p = p->left;
        } else {
            p = s.top();
            s.pop();
            p = p->right;
        }
    }
}
```

##### 中序遍历
顺序：左、中、右

对于任一结点P，
1. 不断找当前结点的左边的子孙，将不是NULL的节点入栈
2. 否则，弹出一个节点，并访问它，将其右子树入栈
3. 直到P为NULL并且栈为空则遍历结束

```java
void inOrder(TreeNode *root) {  //非递归中序遍历
    stack<TreeNode*> s;
    TreeNode *p = root;
    while (p != NULL || !s.empty()) {
        if (p != NULL) { // 使劲向左
            s.push(p);
            p = p->left;
        } else {
            p = s.top();
            s.pop();
            visit(p);
            p = p->right;
        }
    }
}
```

##### 后序遍历
顺序：左、右、中

```java
void postOrder(TreeNode* root) {
    stack<TreeNode*> s;
    TreeNode *p = root;
    TreeNode *pre = NULL; // last visited
    while (p != NULL || !s.empty()) {
        if (p != NULL) { // 使劲向左
            s.push(p);
            p = p->left;
        } else {
            p = s.top();
            // 右孩子为空或者刚刚访问过了，可以访问当前节点了
            if (p->right == NULL || pre == p->right) {
                s.pop();
                visit(p);
                pre = p;
                p = NULL; // 不置空就重复访问了
            } else { // 否则访问右孩子
                p = p->right;
            }
        }
    }
}
```

另一个方法
intuition：**先遍历到的点总是后访问的**

```java
void postOrder(TreeNode *root) {  //非递归后序遍历
    stack<TreeNode*> sTraverse, sVisit;
    sTraverse.push(root);
    while(!s.empty()) {
        TreeNode * p = sTraverse.top();
        sTraverse.pop();
        sVisit.push(p);
        if (p->left) sTraverse.push(p->left);
        if (p->right) sTraverse.push(p->right);
    }
    while (!sVisit.empty()) {
        visit(sVisit.top());
        sVisit.pop();
    }
}
```



