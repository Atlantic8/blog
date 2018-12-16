---
title: Combination Sum
date: 2016-07-19 15:20:12
tags: [Backtracking, LeetCode]
categories: OJ
---

### Problem 1 : Combination Sum

Given a set of candidate numbers (C) and a target number (T), find all unique combinations in C where the candidate numbers sums to T.
<b>The same repeated number may be chosen from C unlimited number of times.</b>

Note:
- All numbers (including target) will be positive integers.
- The solution set must not contain duplicate combinations.

For example, given candidate set [2, 3, 6, 7] and target 7, 
A solution set is:
[ [7], [2, 2, 3] ]

### Solution

the solution is: use recursive way , the function in the code following:
- recursive(vector<vector<int> > &results,vector<int> &candidates, int target, int index, vector<int> res);
- results indicates the final results we want, index indicates the position where we start from, where res is a temp vector containing one solution of all.

```java
class Solution {
public:
    vector<vector<int> > combinationSum(vector<int> &candidates, int target) {
        vector<vector<int> > results;
        sort(candidates.begin(),candidates.end());  //sort to fit the requirement of non-descending orde.
        vector<int> res;
        recursive(results,candidates,target,0,res); //we start from index 0
        return results;
    }
    void recursive(vector<vector<int> > &results,vector<int> &candidates, int target, int index, vector<int> res) {
    	if (target == 0) {   //a valid solution is achieved
	    	results.push_back(res);
	    	return;
	    }
	    for (int i=index; i<candidates.size(); i++) {
    		if (target-candidates.at(i) >= 0) {
		    	vector<int> temp = res;
		    	temp.push_back(candidates.at(i));
		    	////new target, new temp vector,index is i because same candidate is allowed to be used in unlimitde times.
		    	recursive(results,candidates,target-candidates.at(i),i,temp); 
		    } else     //if current sum is bigger than target, then adding bigger candidates is useless
				return;
    	}
    }
};
```

### Problem 2 : Combination Sum II

Given a collection of candidate numbers (C) and a target number (T), find all unique combinations in C where the candidate numbers sums to T.
<b>Each number in C may only be used once in the combination.</b>

Note:
All numbers (including target) will be positive integers.
The solution set must not contain duplicate combinations.
For example, given candidate set [10, 1, 2, 7, 6, 1, 5] and target 8, 
A solution set is:
[ [1, 7], [1, 2, 5], [2, 6], [1, 1, 6] ]

### Solution

- difference between Combination Sum and Combination Sum II is "Each number in C may only be used once in the combination"
- so we recursively use the function: recursive(vector<vector<int> > &results,vector<int> &candidates, int target, int index, vector<int> res);
- i should start from index+1 to avoid duplication, the others are all the same.

```java
class Solution {
public List<List<Integer>> combinationSum2(int[] cand, int target) {
    Arrays.sort(cand);
    List<List<Integer>> res = new ArrayList<List<Integer>>();
    List<Integer> path = new ArrayList<Integer>();
    dfs_com(cand, 0, target, path, res);
    return res;
}
void dfs_com(int[] cand, int cur, int target, List<Integer> path, List<List<Integer>> res) {
    if (target == 0) {
        res.add(new ArrayList(path));
        return ;
    }
    if (target < 0) return;
    for (int i = cur; i < cand.length; i++){
        if (i > cur && cand[i] == cand[i-1]) continue;
        path.add(path.size(), cand[i]);
        dfs_com(cand, i+1, target - cand[i], path, res);
        path.remove(path.size()-1);
    }
}
};
```

### Problem 3 : Combination Sum III

Find all possible <b>combinations of k numbers</b> that add up to a number n, given that only numbers from 1 to 9 can be used and each combination should be a unique set of numbers.

Example 1:
Input: k = 3, n = 7
Output:
[[1,2,4]]

Example 2:
Input: k = 3, n = 9
Output:
[[1,2,6], [1,3,5], [2,3,4]]

### Solution
control the number of integers used.

```python
class Solution:
    # @param {integer} k
    # @param {integer} n
    # @return {integer[][]}
    def __init__(self):
        self.ret=[]

    def combinationSum3(self, k, n):
        self.findTuple(k, n, [], 1)
        return self.ret

    def findTuple(self, k, n, tmp, start):
        if k<0 or n<0:
            return
        if k==0 and n==0:
            if sorted(tmp) not in self.ret:
                self.ret.append(sorted(tmp))
            return
        for cand in range(start, 10):
            if cand>n:
                break
            if cand not in tmp and cand<=n:
                temp = copy.deepcopy(tmp)
                temp.append(cand)
                self.findTuple(k-1, n-cand, temp, cand+1)
```

### Problem 4 : Combination Sum IV
Given an integer array with all **positive numbers and no duplicates**, find the number of possible combinations that add up to a positive integer target.

	nums = [1, 2, 3]
	target = 4

	The possible combination ways are:
    (1, 1, 1, 1)
	(1, 1, 2)
	(1, 2, 1)
	(1, 3)
	(2, 1, 1)
	(2, 2)
	(3, 1)

Note that different sequences are counted as different combinations.

Therefore the output is 7.

#### Solution
这是一个DP题，如果简单使用统计的方法可能会超时。

	comb[target] = sum(comb[target - nums[i]]), where 0 <= i < nums.length, and target >= nums[i]

代码为
```java
public int combinationSum4(int[] nums, int target) {
    int[] comb = new int[target + 1];
    comb[0] = 1;
    for (int i = 1; i < comb.length; i++) {
        for (int j = 0; j < nums.length; j++) {
            if (i - nums[j] >= 0) {
                comb[i] += comb[i - nums[j]];
            }
        }
    }
    return comb[target];
}
```
