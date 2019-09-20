---
title: Copy List with Random Pointer
date: 2016-09-12 23:40:24
tags: [LeetCode]
categories: OJ
---

##### Copy List with Random Pointer
A linked list is given such that each node contains an additional random pointer which could point to any node in the list or null.

Return a deep copy of the list.
节点的数据结构如下：

    class RandomListNode {
        int label;
        RandomListNode next, random;
        RandomListNode(int x) { this.label = x;}
    };

##### Solution
本题的naive思想如下：
1. 在原来list上，每个节点后面插入一个拷贝这个节点的节点
2. 从第一个节点开始，若：nodei->random = nodek, 那么设置nodei->next.random = nodek->next即可
3. 还原原来的list，提取复制的list

```java
public RandomListNode copyRandomList(RandomListNode head) {
    RandomListNode iter = head, next;

    // 在原链表上每个节点后一位创建copy
    while (iter != null) {
        next = iter.next;

        RandomListNode copy = new RandomListNode(iter.label);
        iter.next = copy;
        copy.next = next;

        iter = next;
    }

    // random指针设置
    iter = head;
    while (iter != null) {
        if (iter.random != null) {
            iter.next.random = iter.random.next;
        }
        iter = iter.next.next;
    }

    // 还原原来的list，提取复制的list
    iter = head;
    RandomListNode pseudoHead = new RandomListNode(0);
    RandomListNode copy, copyIter = pseudoHead;

    while (iter != null) {

        // extract the copy
        copy = iter.next;
        copyIter.next = copy;
        copyIter = copy;

        // restore the original list
        next = iter.next.next;
        iter.next = next;

        iter = next;
    }

    return pseudoHead.next;
}
```