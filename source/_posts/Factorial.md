---
title: Factorial
date: 2016-09-27 23:19:41
tags: [Math]
categories: OJ
---

##### 问题 POJ 1401
给一个数n，  求出n！ 有多少个后导零

##### 解决方案
因为n!中的5因子比2多，所以只需要找5的个数就好。

	令f(x)表示正整数x末尾所含有的“0”的个数，则有：
      	当0 < n < 5时，f(n!) = 0;
      	当n >= 5时，f(n!) = k + f(k!), 其中 k = n / 5（取整）


```java
int countZero(int N) {
  	int ret = 0;
  	while (N) {
    	ret += N/5;
   		N /= 5;
  	}
  	return ret;
}
```

如果是要求n!中k因子的个数，那么有：

	f(n) = x + f(x), where x = n / k.