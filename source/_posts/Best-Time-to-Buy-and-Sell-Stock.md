---
title: Best Time to Buy and Sell Stock
date: 2016-07-19 14:32:38
tags: [DP, LeetCode, Greedy, State Machine]
categories: OJ
---

### Problem : Time to Buy and Sell Stock II
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete <b>as many transactions as you like</b> (ie, buy one and sell one share of the stock multiple times). However, you may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

### Solution
<b>贪心算法</b>：条件是假设一天内卖完了可以再买，1-2-3可以拆分成1-2和2-3.
```java
public class Solution {
public int maxProfit(int[] prices) {
    int total = 0;
    for (int i=0; i< prices.length-1; i++) {
        if (prices[i+1]>prices[i]) total += prices[i+1]-prices[i];
    }
    return total;
}
```

如果不允许在一天内卖完了可以再买，贪心的算法是没有意义的，虽然答案是对的。
这时，每一次需要找到local最小值和local最大值，然后把差值加到返回值上。
```java
public int maxProfit(int[] prices) {
    int profit = 0, i = 0;
    while (i < prices.length) {
        // 找到local最小值
        while (i < prices.length-1 && prices[i+1] <= prices[i]) i++;
        int min = prices[i++]; // 因为price[i+1]>price[i]，所以将i++
        // 找到local最大值
        while (i < prices.length-1 && prices[i+1] >= prices[i]) i++;
        profit += i < prices.length ? prices[i++] - min : 0;
    }
    return profit;
}
```


### Problem : Time to Buy and Sell Stock III
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete at most two transactions.

Note:
You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

##### [Original Address](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

### Solution
依旧是DP问题，如果用a[i][j]表示从标号i到j单次最大的利润，代码如下：
```java
public int maxProfit(int[] prices) {
	int n = prices.length;
	if (n <= 1)
		return 0;
	int[][] minElement=new int[n][n], maxpay=new int[n][n];
	for (int i=0; i<n; i++) {
		minElement[i][i] = prices[i];
		maxpay[i][i] = 0;
	}
	for (int len=1; len<n; len++) {
		for (int i=0; i+len<n; i++) {
			int j = i+len;
			if (prices[i]-minElement[i][j-1] > maxpay[i][j-1])
				maxpay[i][j] = prices[i]-minElement[i][j-1];
			minElement[i][j] = Math.min(prices[j], minElement[i][j-1]);
		}
	}
	int div = 2, maxprofit = maxpay[0][n-1];
	if (n <= 3)
		return maxprofit;
	for (int i=div; i<n-2; i++) {
		int x1 = maxpay[0][i];
		int x2 = maxpay[i][n-1];
		if (x1+x2 > maxprofit)
			maxprofit = x1+x2;
	}
	return maxprofit;
}
```
但是，这样时间复杂度为O(n^2)。TLE！！！！！！！！！
然后参考了别人的思路：-----------------------------
<b>
以f[k][i]表示第k个transaction后从开始到标号i-1得到的最大利润
迭代方程要考虑两种情况：
1. p[i]不比前一个售出点的price高，所以f[k][i]=f[k][i-1]
2. p[i]  比前一个售出点的price高，所以f[k][i]=max{f[k-1][j]+p[i]-p[j]}=p[i]+max{f[k-1][j]-p[j]} (其中1<j<i-1)

所以，f[k][i] = max{f[k][i-1], max{f[k-1][j]+p[i]-p[j]} }
问题来了，如果这么实现，复杂度又会达到O(n^2).
注意到情况2中的“ max{f[k-1][j]-p[j]} ”，可以使用一个变量记录最大的f[k-1][j]-p[j]，然后每次更新它即可
对于每个transaction循环，它的初始值为：tmp = maxpay[k-1][0]-p[0], 每到一个新的i，更新tmp=max{tmp, f[k-1][i]-p[i])。
所以迭代方程就可以写成：f[k][i]=p[i]+tmp. 这样，时间复杂度就降到了O(n). </b>
本题也可以变形为至多执行k个transaction，只需要把代码中2,3改成k,k+1即可。
```java
public class Solution {
    public int maxProfit(int[] prices) {
		int n = prices.length;
		if (n <= 1)
			return 0;
        // maxpay[t][i] indicates the max profit in t-th transaction
		int[][] maxpay=new int[3][n];
		// initialize maxpay, when t=0, maxpay[t][i]=0
        for (int j=0; j<3; j++)
			for (int i=0; i<n; i++)
				maxpay[j][i] = 0;
		for (int t=1; t<3; t++) {
        	// for every t, initialize t
			int tmp = maxpay[t-1][0]-prices[0];
			for (int i=1; i<n; i++) {
				//iteration formula
				//maxpay[t][i] = Math.max{ maxpay[t][i-1] , prices[i]+max<j>{maxpay[t-1][j]-prices[j]} };
				maxpay[t][i] = Math.max(maxpay[t][i-1], prices[i]+tmp);
				// make sure that tmp = max(tmp , maxpay[t-1][i]-prices[i])
                tmp = Math.max(tmp, maxpay[t-1][i]-prices[i]);
			}
		}
		return maxpay[2][n-1];
    }
}
```

### Problem : Time to Buy and Sell Stock IV

Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete at most k transactions.

Note:
You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

##### [Original Address](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

### Solution
we are allowed to perform at most k transactions
we can apply the algorithm above, but there is one thing to notice,
    when k is very large: k>=n/2, that's to say, we perform one transaction on each day.
    so, the problem becomes Best Time to Buy and Sell Stock II,
    greedy algorithm is ok, otherwise we get TLE.

```java
public class Solution {
	public int maxProfit(int k, int[] prices) {
        int len = prices.length;
        if (k >= len / 2) return quickSolve(prices);
        
        int[][] t = new int[k + 1][len];
        for (int i = 1; i <= k; i++) {
            int tmpMax =  -prices[0];
            for (int j = 1; j < len; j++) {
                t[i][j] = Math.max(t[i][j - 1], prices[j] + tmpMax);
                tmpMax =  Math.max(tmpMax, t[i - 1][j - 1] - prices[j]);
            }
        }
        return t[k][len - 1];
    }
    

    private int quickSolve(int[] prices) {
        int len = prices.length, profit = 0;
        for (int i = 1; i < len; i++)
            // as long as there is a price gap, we gain a profit.
            if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
        return profit;
    }
}
```

### Problem : Best Time to Buy and Sell Stock with Cooldown
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times) with the following restrictions:

You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
<b>After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1 day)</b>

	Example:

	prices = [1, 2, 3, 0, 2]
	maxProfit = 3
	transactions = [buy, sell, cooldown, buy, sell]

### Solution
本题中，可能的操作有buy、sell、rest(啥也不干)。可以使用状态机来解题：
由题可以绘制如下状态机：
![](http://ww4.sinaimg.cn/mw690/9bcfe727jw1f7xj05lgqrj20e20710t1.jpg)
转移方程表示如下：

	s0[i] = max(s0[i - 1], s2[i - 1]);
	s1[i] = max(s1[i - 1], s0[i - 1] - prices[i]);
	s2[i] = s1[i - 1] + prices[i];

由于s1状态是买完以后的状态，所以最值最大值肯定不在s1上出现，只要找到最大的s0和s2.
关于初值设置：
- s0=0，因为如果以s0为开始，你没有任何股票
- 如果以s1为开始，通过buy第一天的股票获得，可以设置s1的初值为-price[0]
- 设置s2的初值为INT_MIN，当然设置为0也完全没有问题(没有股票卖也卖不到钱)


```java
class Solution {
public:
	int maxProfit(vector<int>& prices){
		if (prices.size() <= 1) return 0;
		vector<int> s0(prices.size(), 0);
		vector<int> s1(prices.size(), 0);
		vector<int> s2(prices.size(), 0);
		s1[0] = -prices[0];
		s0[0] = 0;
		s2[0] = INT_MIN;
		for (int i = 1; i < prices.size(); i++) {
			s0[i] = max(s0[i - 1], s2[i - 1]);
			s1[i] = max(s1[i - 1], s0[i - 1] - prices[i]);
			s2[i] = s1[i - 1] + prices[i];
		}
		return max(s0[prices.size() - 1], s2[prices.size() - 1]);
	}
};
```

空间复杂度为O(n)，可以降低到O(1).

```java
class Solution {
	int maxProfit(vector<int>& prices) {
        if (prices.size() < 2) return 0;
        int s0 = 0, s1 = -prices[0], s2 = 0;
        for (int i = 1; i < prices.size(); ++i) {
            int last_s2 = s2;
            s2 = s1 + prices[i];
            s1 = max(s0 - prices[i], s1);
            s0 = max(s0, last_s2);
        }
        return max(s0, s2);
    }
}
```