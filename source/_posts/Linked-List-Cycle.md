---
title: Linked List Cycle
date: 2016-09-04 15:41:13
tags: [LeetCode]
categories: OJ
---

#### Problem 1
Description

Given a linked list, determine if it has a cycle in it.

Note: Solve it using O(1) space

#### Solution 1
决定一个list是否有环的方法是：

- 使用一个慢指针slow每次移动1步
- 使用一个快指针fast每次移动2步
- 如果快指针和慢指针在迭代一定次数后相遇，则存在回路
- 否则，如果fast.next=null或者slow.next=null，说明不存在回路

```java
public boolean hasCycle(ListNode head) {
    if(head==null) return false;
    ListNode walker = head;
    ListNode runner = head;
    while(runner.next!=null && runner.next.next!=null) {
        walker = walker.next;
        runner = runner.next.next;
        if (walker==runner) return true;
    }
    return false;
}
```

#### Problem 2
Description

Given a linked list, return the node where the cycle begins. If there is no cycle, return null.

Note: Do not modify the linked list.
      Solve it using O(1) space

#### Solution 2
确认一个list是否有回路的方法如上。确定回路入口的方法如下：
- 不妨假设list头到loop入口的距离是 l1
- loop入口到两个指针相遇点的距离是 l2
- loop的长度位 c，n表示fast指针绕loop的圈数
- 指针相遇时，slow指针走过的距离是：l1 + l2 + m x c，fast指针走过的距离是：l1 + l2 + n x c
- 因为fast指针的路程是slow指针的两倍， 所以：l1 + l2 + n x c = 2 x (l1 + l2 + m x c)
- l1 = (c-l2) + (n-2 x m-1)c，而c-l2是相遇点到loop入口的距离
- 所以分别从list头和指针相遇点出发、每次移动步长均为1的两个指针会在loop入口回合

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        while (fast!=null && fast.next!=null){
            fast = fast.next.next;
            slow = slow.next;
            // 找到快指针和慢指针的汇合点，说明loop存在
            if (fast == slow){
                ListNode slow2 = head;
                // 分别从链表头和汇合点出发的指针，在loop入口处相遇
                while (slow2 != slow){
                    slow = slow.next;
                    slow2 = slow2.next;
                }
                return slow;
            }
        }
        return null;
    }
}
```

相似问题：[Find the Duplicate Number](http://atlantic8.github.io/2016/09/04/Find-the-Duplicate-Number/)
