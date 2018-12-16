---
title: Repeated DNA Sequences
date: 2016-09-10 16:03:17
tags: [LeetCode, Sliding window]
categories: OJ
---

#### Problem
All DNA is composed of a series of nucleotides abbreviated as A, C, G, and T, for example: "ACGAATTCCG". When studying DNA, it is sometimes useful to identify repeated sequences within the DNA.

Write a function to find all the <b>10-letter-long sequences</b> (substrings) that occur more than once in a DNA molecule.

For example,

	Given s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",

	Return:
	["AAAAACCCCC", "CCCCCAAAAA"].

#### Solution
滑动窗口和哈希表的思想很明显，不过直接将子串作为key放入哈希表中会超出内存限制
所以，关键是要减少内存使用量，一个可行的办法如下：
- 由于A,C,G,T这四个字母的二进制值的最后三位是不一样的，所以他们&111的值也是不同的，也就是说三位二进制就能区分出这四个字母
- 因为window的长度是10，所以表示长度为10的子串需要30位的长度，int型长度是32位(前两位需要设置为0，可以&3fffffff达到效果)，满足条件
- 随着窗口移动，左边的退出，右边的加入，我们使用的int数可以每次向左移动三位

```java
public class Solution {
	public List<String> findRepeatedDnaSequences(String s) {
		List<String> ret = new ArrayList<String>();
		int res=0;
		HashMap<Integer,Integer> map = new HashMap<Integer,Integer>();
		for (int i=0; i<s.length(); i++) {
			// 3 bits can indicates one letter. so we total need 30 bits to represent a 10-letter string
			// while int is 32 bits long, so, &0x3FFFFFFF helps set the first 2 bits to 0.
			// res<<3 : move the header.
			// s.charAt(i)&7 : add a new letter.
			res = res << 3 & 0x3FFFFFFF | (s.charAt(i) & 7);   //get rid of the header and add the tailer.
			if (map.containsKey(res)==true) {
				if (map.get(res) == 1)
					ret.add(s.substring(i-9, i+1));
                map.put(res, map.get(res)+1);
        	} else
				map.put(res, 1);
		}
		return ret;
	}
}
```

更加节省空间的方法也有，<b>区分四个数其实只需要2bit</b>。先看下ACGT的二进制后三位

	A : 001
	C : 011
	G : 111
	T : 100
所以，对于一个字母先&100，再&010即可区分这四个数。（区分较难也没关系，可以写个函数搞定）