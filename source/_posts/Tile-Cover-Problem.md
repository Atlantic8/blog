---
title: Tile Cover Problem
date: 2016-11-25 09:42:46
tags: [DP, POJ]
categories: OJ
---

##### 题目描述
POJ 2411
编程之美
用 1 x 2 的瓷砖覆盖 n x m 的地板，问共有多少种覆盖方式？

##### 解题思路
这是个<b>状态压缩DP问题</b>，意思就是把状态用比特位的形式表示出来，然后使用DP求解

	每个位置，有砖为1，无砖为0
	由于转是1x2规格的，规定：
	横着铺是连续两个都设成1
	竖着铺时上面的设为0，下面的为1（因为上面的砖头对第二行有影响，如果上面的为0，那么下面的必须为1）
	把每一行看作是一个二进制整数，这个整数就表示状态(有多少种01序列就有多少种状态)
	因此每行都有很多状态，状态即为这一行01序列对应的值

- <b>DP[i][j]表示第i行状态为j时有多少种方法</b>。
- <b>如果上一行的某个状态DP(i-1,k) 可以达到 DP(i, j) 那么两个状态是兼容的</b>。
- <b>如果DP(i-1,k)和DP(i, j)兼容并且 DP(i-1, k)有S种铺设方案，那么DP(i, j)就可以从DP(i-1, k)这条路径中获得S个方案</b>。

<b>兼容性：</b>
兼容性指的是上一行和下一行的关系。Concretely，<b>x和y兼容指的是x、y对应的二进制串对应的状态是兼容的</b>。
检测兼容性的方法是从左到右依次检测每一列是否兼容，具体检查内容包括：(假如现在铺设第i行x列)

	     x  x+1
	i-1
	  i  0

如果第i行x列上的值(i,x)是0， 那么第 i-1行x列上一定是1

	     x  x+1
	i-1
	  i  1

如果(i,x)为1，那么
- (i-1,x)为0，竖着铺的，下一步检测(i, x+1)
- (i-1,x)为1，下一步检测(i, x+2).因为(i,x)是横着铺，跨越两个格子。

第一行得兼容性
- 如果 (0,x) 是1，那么 (0,x+1) 也一定是1，然后测试到 (0,x+2)
- 如果(0,x)是0， 那么直接测试下一个(0,x+1)
- 因为是第一行，所以兼容只能获得一个方案

所以具体思路就是：

	对每一行，遍历其所有可能得状态
	检查其与上一行所有状态得兼容性，兼容则获取上一行状态所对应的方案数
	第一行单独处理
	最后一行结束后，返回DP[n-1][2^m-1]，因为最后一行必须全部为1

```java

#include <stdio.h>
#include <memory.h>
#include <math.h>
#include <algorithm>
using namespace std;


#define MAX_ROW 11
#define MAX_STATUS 2048
long long DP[MAX_ROW][MAX_STATUS];
int g_Width, g_Height;

// test the first line
bool TestFirstLine(int nStatus) {
	int i = 0;
	// 状态的每一个位
	while( i < g_Width) {
		if(nStatus & (0x1 << i)) {
			if( i == g_Width -1 || (nStatus & (0x1 << (i+1))) == 0)
				return false;
			i += 2;
		} else {
			i++;
		}
	}
	return true;
}

// test if status (i, nStatusA) and (i-1, nStatusB) is compatable.
bool CompatablityTest(int nStatusA, int nStatusB) {
	int i = 0;

	while( i < g_Width) {

		if( (nStatusA & (0x1 << i))  == 0) {
			if((nStatusB & (0x1 << i)) == 0)
				return false;
			i++;
		} else {
			if((nStatusB & (0x1 << i)) == 0 )
				i++;
			else if( (i == g_Width - 1) || ! ( (nStatusA & (0x1 << (i+1))) && (nStatusB & (0x1 << (i + 1)))) )
				return false;
			else
				i += 2;
		}
	}
	return true;
}
int main() {
	int i,j;
	int k;
	while(scanf("%d%d", &g_Height, &g_Width) != EOF ) {

		if(g_Width == 0 && g_Height == 0)
			break;

		if(g_Width > g_Height)
			swap(g_Width, g_Height);

		int nAllStatus = 1 << g_Width;
		memset(DP, 0, sizeof(DP));
		for( j = 0; j < nAllStatus; j++) {
			if(TestFirstLine(j))
				DP[0][j] = 1;
		}

		for( i = 1; i < g_Height; i++) { 
			// iterate all status for line i
			for( j = 0; j < nAllStatus; j++) {
				// iterate all status for line i-1
				for( k = 0; k < nAllStatus; k++) {
					if(CompatablityTest(j, k))
						DP[i][j] += DP[i-1][k];
				}
			}
		}
		printf("%lld\n", DP[g_Height-1][nAllStatus - 1]);
	}
	return 0;
}
```
