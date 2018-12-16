---
title: Maximum XOR of Two Numbers in an Array
date: 2017-05-02 20:05:02
tags: [LeetCode, ]
categories: OJ
---


###### 题目描述
给定一个非空数组$a_0,a_1,...,a_{n-1}$满足$0\le a_i \le 2^{31}$，找到两个元素异或的最大值。
要求时间复杂度为`O(n)`。

	Input: [3, 10, 5, 25, 2, 8]

	Output: 28

	Explanation: The maximum result is 5 ^ 25 = 28.

###### 解题思路
思路是**`Trie Tree`**，第一步将每一个元素按二进制位存储在树中，第二步对于每一个元素$a_i$，尝试找到树中能和$a_i$构成最大异或值的元素，记录这个最大值。

```java
struct TrieNode {
	TrieNode *son[2]; // 0
	int val;
	TrieNode(int v) :val(v) {
		son[0] = NULL;
		son[1] = NULL;
	}
};
class Solution {
public:
int findMaximumXOR(vector<int>& nums) {
	TrieNode *root = new TrieNode(-1), *p;
	for (int i=0; i<nums.size(); i++) {  // 建树
		int cur = nums[i];
		TrieNode *father=root;
		for (int k=31; k>=0; k--) {
			int x = (cur>>k) & 1;
			if (father->son[x] == NULL) {
				p = new TrieNode(x);
				father->son[x] = p;
			} else p = father->son[x];
			father = p;
		}
	}
	int ret = 0;
	vector<int> res;
	for (int j=0; j<nums.size(); j++) { // 找最值
		int cur = nums[j], tmp=0;
		p = root;
		for (int i=31; i>=0; i--) {     // 按位找
			int x = (cur>>i) & 1;
			if (p->son[1^x] != NULL) {
				tmp += 1<<i;
				p = p->son[1^x];
			} else p = p->son[0^x];
		}
		ret = max(ret, tmp);
	}
	return ret;
}
};
```

再来看看解题报告上别人写的[NB解法](https://discuss.leetcode.com/topic/63213/java-o-n-solution-using-bit-manipulation-and-hashmap/7)，大致思想是从高到低确定最终结果的每一位上究竟是0还是1，通过迭代剔除不可能的元素
```java
public int findMaximumXOR(int[] nums) {
    int max = 0, mask = 0;
    for (int i = 31; i >= 0; i--) {
        mask |= (1 << i); // 掩码每轮多一个1
        HashSet<Integer> set = new HashSet<Integer>();
        for (int num : nums)
            set.add(num & mask); // 计算通过掩码能得到的最大值

        /* Use 0 to keep the bit, 1 to find XOR
         * 0 ^ 0 = 0
         * 0 ^ 1 = 1
         * 1 ^ 0 = 1
         * 1 ^ 1 = 0
         */
        int tmp = max | (1 << i); // in each iteration, there are pair(s) whoes Left bits can XOR to max
        for (int prefix : set) {
            if (set.contains(tmp ^ prefix))
                max = tmp;
        }
    }
    return max;
}
```


