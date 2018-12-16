---
title: Permutation
date: 2016-09-10 14:01:06
tags: [LeetCode, Permutation]
categories: OJ
---

##### 生成全排列
举例来说，要生成[1,2,3,4,5]的全排列可以按如下方式继续：
1,x,x,x,x
  2,x,x,x
  3,x,x,x
  4,x,x,x
  5,x,x,x
2,x,x,x,x
3,x,x,x,x
4,x,x,x,x
5,x,x,x,x

所以可以使用递归的方式进行，设置一个pos表示当前递归到达数组的深度
然后:
for i=pos; i<n; i++
	交换pos和i处的值
    递归到pos+1层
    交换pos和i处的值
每次递归，如果pos>=n，则将一个排列结果存储，return

```java
public class Solution {
	public List<List<Integer>> permute(int[] num) {
 		List<List<Integer>> result = new ArrayList<List<Integer>>(); 
 		permute(num,0,result);
 		return result;
    }

	public void permute(int[] num, int begin, List<List<Integer>> result){
    	if(begin>=num.length){
        	List<Integer> list = new ArrayList<Integer>();
        	for(int i=0;i<num.length;i++){
            	list.add(num[i]);
        	}
        	result.add(list);
        	return;
    	}
    	for(int i=begin;i<num.length;i++){
        	swap(begin,i,num);
        	permute(num,begin+1,result);
        	swap(begin,i,num);
    	}
	}

	public void swap (int x, int y,int[] num){
    	int temp = num[x];
    	num[x]=num[y];
    	num[y]=temp;
	}
}
```

##### 下一个排列
寻找下一排列的方法如下：
- 从后向前搜索，找到第一个num[i]<num[i+1]，此时，[i+1, n-1]序号的元素非递增
  - 如果i+1=n-1的话，直接将num逆序即可
- 从[i+1, n-1]前向遍历，找到第一个小于num[i]的数num[k]，将num[i]与num[k]互换，注意此时[i+1, n-1]序号的元素还是非递增
- 将[i+1, n-1]序号的元素逆序


##### 第k个排列
还拿[1,2,3,4,5]的全排列举例：
以1开头的排列有4!个，以2开头的排列有4!个
所以思路很明显

```java
public class Solution {
	public String getPermutation(int n, int k) {
    	int pos = 0;
    	List<Integer> numbers = new ArrayList<>();
    	int[] factorial = new int[n+1];
    	StringBuilder sb = new StringBuilder();

    	// create an array of factorial lookup
    	int sum = 1;
    	factorial[0] = 1;
    	for(int i=1; i<=n; i++){
        	sum *= i;
        	factorial[i] = sum;
    	}
    	// factorial[] = {1, 1, 2, 6, 24, ... n!}
    	// create a list of numbers to get indices
    	for(int i=1; i<=n; i++){
        	numbers.add(i);
    	}
    	// numbers = {1, 2, 3, 4}

    	k--;
    	for(int i = 1; i <= n; i++){
        	int index = k/factorial[n-i];
        	sb.append(String.valueOf(numbers.get(index)));
        	numbers.remove(index);
        	k-=index*factorial[n-i];
    	}
    	return String.valueOf(sb);
	}
}
```