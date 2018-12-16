---
title: Sunday
date: 2017-03-15 22:01:25
tags: String
categories: Algorithm
---

###### 算法描述
`Sunday`算法是用于字符串匹配的算法，平均复杂度为`O(n)`，平均效率高于`KMP`和`BM`。

示例如下：
匹配时，从左到右匹配，第一个字符不匹配，看模式串后一位`t`对应的字符，因为`t`位的字符也总是要匹配的。所以我们需要查找`t`位字符在模式串中最右侧的位置，然后移动模式串。如果`t`位的字符在模式串中不存在，那么移动模式串首到当前模式串尾部的下一个位置。

	suck kmy balls
	kmy

对齐字母`k`，如下

	suck kmy balls
	   kmy

还不匹配，继续

	suck kmy balls
	     kmy

匹配出现，记录下。然后再看下一个字符` `，其在模式串没出现，移动模式串到

	suck kmy balls
	         kmy

依此类推，直到结束。

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fdoevubjcbj216o0djgm5)

下面看一下具体移动的步长，设当前p和s的位置分别在pi和si，p结尾的最后一个位置对应于s中序号为`skey = si+p.length()-pi`的位置：

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fdof40xqgpj21e60dkwf1)

- 如果`skey`中的字符在模式串p中没有，则将`pi=0`，`si`移到`skey+1`位置

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fdoezdgengj21a10ea0ta)

![](http://ww1.sinaimg.cn/large/9bcfe727ly1fdof5yzhjkj219x0duzkt)

- 否则，要令`skey`与p中对应的最右相同元素对齐，设p中序号为`k`的元素满足条件，`si`需要移动变成`skey-k=si+p.length()-pi-k`，同样地`pi=0`

###### 代码
`sunday`算法需要维护一个数组，记录s串中下一个字符为x时模式串移动的距离。命其名为`next`
```java
void get_next(string p, vector<int> &next) {
    for (int i=0; i<p.length(); i++) {
	    next[p[i]] = p.length()-i;  // 模式串有的字符
	}
}

void sunday(string s, string p) {
    vector<int> next(255, p.length()+1);  // 默认不存在模式串中的字符对应的移动长度为p.length()+1
	get_next();
	int si=0, pi=0;
	while (si+p.length() < s.length()) {
	    pi = 0;
	    for (pi=0; pi<p.length(), s[si++] != p[pi]; pi++); // matching
		if (pi == p.length())  // match found
		    cout << "match found, index is " << si-p.length()+1 << endl;
		int skey = si + p.length() - pi;
		if (skey >= s.length) break;
		si += next(s[skey]) - pi;
	}
}
```

