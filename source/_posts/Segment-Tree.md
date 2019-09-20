---
title: Segment Tree
date: 2016-09-24 09:15:15
tags: [Binary Tree, LeetCode]
categories: Algorithm
---

##### 线段树
![](http://ww1.sinaimg.cn/mw690/9bcfe727jw1f768k0nw59j20ql0cmt9m.jpg)
线段树（英语：Segment Tree）是一种二叉搜索树，它将一个区间划分成一些单元区间，每个单元区间对应线段树中的一个叶结点。

对于线段树中的每一个非叶子节点[a,b]，它的左子树表示的区间为[a,(a+b)/2]，右子树表示的区间为[(a+b)/2+1,b]。因此线段树是平衡二叉树。叶节点数目为N，即整个线段区间的长度。

给定整个线段区间，建立一棵线段树的时间复杂度是O(N)。单点修改的时间复杂度是O(logN) 。单点查询的时间复杂度是O(1)。如果允许惰性赋值而加上延迟标记的话，许多的区间修改的时间复杂度也会是 O(log N)，但是单点查询的时间复杂度会变成O(log N)。

线段树的每个节点上往往都增加了一些其他的域。在这些域中保存了某种动态维护的信息，视不同情况而定。这些域使得线段树具有极大的灵活性，可以适应不同的需求。

###### 动态结构

    struct node{
         node* left;
         node* right;
        ……
    }

动态结构的方法在Range Sum Query中。

静态数组型结构：maxn是最大区间数，而节点数要开4倍多

    struct node{
          int left;
          int right;
        ……
    }Tree[maxn*4+5]

使用静态数组结构（从1开始计数），left、right表示其左右孩子在数组中对应的位置，如果当前节点的位置时i，那么左孩子2*i，右孩子2*i+1。

构造方法：主要思想是递归构造，如果当前节点记录的区间只有一个值，则直接赋值，否则递归构造左右子树，最后回溯的时候给当前节点赋值
```java
/*
node： 当前节点在静态数组segTree中的位置
begin：题目给定数组的下标起始位置
end：  题目给定数组的下标终止位置
*/
void build(int node, int begin, int end) {
    if (begin == end)
        segTree[node] = array[begin]; /* 只有一个元素,节点记录该单元素 */
    else {
        /* 递归构造左右子树 */
        build(2*node, begin, (begin+end)/2);
        build(2*node+1, (begin+end)/2+1, end);

        /* 回溯时得到当前node节点的线段信息 */
        if (segTree[2 * node] <= segTree[2 * node + 1])
            segTree[node] = segTree[2 * node];
        else
            segTree[node] = segTree[2 * node + 1];
    }
}
```

区间查询：
```java
/*
node：当前查询节点
begin,end：当前节点存储的区间，即当前结点的范围
left,right：此次query所要查询的区间
*/
int query(int node, int begin, int end, int left, int right) {
    int p1, p2;

    /*  查询区间和要求的区间没有交集  */
    if (left > end || right < begin)
        return -1;

    // 查询范围和当前结点的范围重合
    if (begin == left && end == right)
        return segTree[node];

    // 分别查询当前结点的左右孩子
    p1 = query(2 * node, begin, (begin + end) / 2, left, right);
    p2 = query(2 * node + 1, (begin + end) / 2 + 1, end, left, right);

    /*  return the expect value  */
    if (p1 == -1)
        return p2;
    if (p2 == -1)
        return p1;
    return  p1 + p2;
}
```

单节点更新：
```java
/*
node：当前节点的下标
left,right：当前节点的表示范围
ind,add：将原数组中ind位置元素增加add
*/
void Updata(int node, int left, int right, int ind, int add) {
    // 当前是叶节点了，直接更新
    if( begin == end ) {
        segTree[node] += add;
        return ;
    }
    int m = ( left + right ) >> 1;
    if(ind <= m)
        Updata(node * 2,left, m, ind, add);
    else
        Updata(node * 2 + 1, m + 1, right, ind, add);
    /*回溯更新父节点*/
    segTree[node] = segTree[node * 2] + segTree[node * 2 + 1];

}
```



##### Range Sum Query - Mutable
Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

The update(i, val) function modifies nums by updating the element at index i to val.
Example:
Given nums = [1, 3, 5]

sumRange(0, 2) -> 9
update(1, 2)
sumRange(0, 2) -> 8
Note:
- The array is only modifiable by the update function.
- You may assume the number of calls to update and sumRange function is distributed evenly.

使用直接的方法处理，在有大量的查询(O(N)复杂度)和更新时时间复杂度过高。使用线段树处理的话，查询和修改的复杂度均为O(logN). 本题中，每个节点包含左右孩子节点指示自己的范围，还包含一个表示以该节点为根的子树的所有元素的和。

```java
public class NumArray {
    SegmentTreeNode root = null;
    // 线段树的节点，包含左右孩子，和其全部孩子值的和
    class SegmentTreeNode {
        int sum;
        int start, end;
        public SegmentTreeNode left, right;

        public SegmentTreeNode(int start, int end) {
            this.start = start;
            this.end = end;
            this.left = null;
            this.right = null;
            this.sum = 0;
        }
    }
    // 将数据index位置的值转换成value，树中只需要更改sum值就好
    public void Update(SegmentTreeNode root, int index, int value) {
        // 到叶节点时，直接修改sum值
        if (root.start == root.end)
            root.sum = value;
        else { // 非叶节点，要考虑修改树的中间结点
            int mid = root.start + (root.end - root.start) / 2;
            if (index <= mid) // 如果需要修改的节点在左子树，右子树不需要修改
                Update(root.left, index, value);
            else // 只修改右子树
                Update(root.right, index, value);
            // 修改根节点的sum值
            root.sum = root.left.sum + root.right.sum;
        }
    }
    // 返回从索引start到end的值的和
    public int SumRange(SegmentTreeNode root, int start, int end) {
        // root对应的范围正好是查询的范围
        if (root.start == start && root.end == end)
            return root.sum;
        int mid = root.start + (root.end - root.start) / 2;
        // 查询范围在左子树上
        if (end <= mid)
            return SumRange(root.left, start, end);
        // 查询范围在右子树上
        else if (start > mid)
            return SumRange(root.right, start, end);
        // 查询范围在左、右子树上
        return SumRange(root.left, start, mid) + SumRange(root.right, mid + 1, end);
    }

    public SegmentTreeNode ConstructSegmentTree(int[] nums, int start, int end) {
        if (start > end)
            return null;
        SegmentTreeNode ret = new SegmentTreeNode(start, end);
        if (start == end) {
            ret.sum = nums[start];
        } else {
            int mid = start + (end - start) / 2;
            ret.left = ConstructSegmentTree(nums, start, mid);
            ret.right = ConstructSegmentTree(nums, mid + 1, end);
            ret.sum = ret.left.sum + ret.right.sum;
        }
        return ret;
    }

    public NumArray(int[] nums) {
        root = ConstructSegmentTree(nums, 0, nums.length - 1);
    }

    void update(int i, int val) {
        Update(root, i, val);
    }

    public int sumRange(int i, int j) {
        return SumRange(root, i, j);
    }
}
```

##### 线段(可能重合)的总长度
思路是在线段可能出现的范围内建立线段树，节点上设置一个表示此节点是否被覆盖的属性cover，cover=1表示该结点所对应的区间被完全覆盖，cover=0表示该结点所对应的区间未被完全覆盖。如下图的线段树，添加线段[1,2][3,5][4,6]
![](http://ww3.sinaimg.cn/mw690/9bcfe727jw1f751urtcoej20iq07v74p.jpg)

