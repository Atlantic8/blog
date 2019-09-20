---
title: Subsets
date: 2016-09-10 16:28:50
tags: [LeetCode, bit]
categories: OJ
---

#### Problem
Given a set of distinct integers, nums, return all possible subsets.

Note: The solution set must not contain duplicate subsets. <无重复假设>

For example,
If nums = [1,2,3], a solution is:

    [
      [3],
      [1],
      [2],
      [1,2,3],
      [1,3],
      [2,3],
      [1,2],
      []
    ]

#### Solution
递归的做法很明显，不赘述了。
这里介绍使用bit思想的方法
- 一个长度为n的无重复数组，其子集的个数为2^n个，每一个元素可能出现或者不出现。
- 所以我们从0到2^n-1，逐个递增。对每个数，按位位移然后&1就可以得到每一位的值，然后根据每一位是0还是1确定对应的数组元素是否加入。这种方法的优势在于不用递归调用栈。代码略！

下面的代码是这样的思想
- 先生成2^n个空的集合
- 每一个元素都会在2^(n-1)个子集中出现
- 第一个元素每隔一个集合出现一次，第二个元素每4个元素出现连续2次，第三个元素每8个元素出现连续4次
- 所以第j个集合中，第i个元素是否出现可以由 j >> i & 1 决定

下面是例子[1,2,3]
    [], [], [], [], [], [], [], []

    [], [1], [], [1], [], [1], [], [1]

    [], [1], [2], [1, 2], [], [1], [2], [1, 2]

    [], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]

```java
class Solution {
public:
    vector<vector<int> > subsets(vector<int> &S) {
        sort (S.begin(), S.end());
        int elem_num = S.size();
        int subset_num = pow (2, elem_num);
        vector<vector<int> > subset_set (subset_num, vector<int>());
        for (int i = 0; i < elem_num; i++)
            for (int j = 0; j < subset_num; j++)
                if ((j >> i) & 1)
                    subset_set[j].push_back (S[i]);
        return subset_set;
    }
}
```

###### 数组允许重复的情况
在数组允许重复时，使用递归做的话，可以先排序，然后在遇到num[i] == num[i-1]时，直接跳过去就好

```java
public class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> each = new ArrayList<>();
        helper(res, each, 0, nums);
        return res;
    }
    public void helper(List<List<Integer>> res, List<Integer> each, int pos, int[] n) {
        if (pos <= n.length) {
            res.add(each);
        }
        int i = pos;
        while (i < n.length) {
            each.add(n[i]);
            helper(res, new ArrayList<>(each), i + 1, n);
            each.remove(each.size() - 1);
            while (i+1 < n.length && n[i] == n[i + 1]) i++;
        }
        return;
    }
}
```

迭代算法
- 采用逐个插入元素的思想，对每一个新元素，将其插入到每个已存在的子集中
- 如果当前元素是重复元素，那么只能把它插入到上一次插入位置的后面
- 比如说1,2,3,3，在插入最后一个3时，不能在[1],[2],[]这些集合中插入，因为第一个3插入时已经找到了这些子集，只能在第一个包含3的集合开始，所以需要插入第二个3的集合有[3],[1,3],[2,3],[1,2,3]。如果有3个3也是一样，第三个3只能插进包含2个3的子集。


```java
vector<vector<int> > subsetsWithDup(vector<int> &S) {
    sort(S.begin(), S.end());
    // 包含空集的集合
    vector<vector<int>> ret = {{}};
    int size = 0, startIndex = 0;
    for (int i = 0; i < S.size(); i++) {
        // startIndex从上一次开始插入的地方开始，不是重复元素则从0开始
        startIndex = i >= 1 && S[i] == S[i - 1] ? size : 0;
        size = ret.size();
        for (int j = startIndex; j < size; j++) {
            vector<int> temp = ret[j];
            temp.push_back(S[i]);
            ret.push_back(temp);
        }
    }
    return ret;
}
```