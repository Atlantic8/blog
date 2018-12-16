---
title: Word Break
date: 2016-09-11 10:00:56
tags: [LeetCode, DP, Backtracking]
categories: OJ
---

#### Word Break
给定一些单词集合dic，问给定字符串s是否可以拆分成这些单词。
思路如下：
- 使用DP思想，f[i]表示s.substring(0,i)是否可以拆分
- f[i] |= (f[k] && s.substring(k,i) in dic)对于所有的k in [0,i]

#### Word Break II
在上题的基础上，要求给出所有可能的拆分，单词之间用空格隔开

	For example, given
	s = "catsanddog",
	dict = ["cat", "cats", "and", "sand", "dog"].

	A solution is ["cats and dog", "cat sand dog"].

解题思路：
- 由于需要给出所有的结果，上面的DP就不行了
- 解法是使用递归求解，<b>对于已经处理过的子串，要用哈希表保存其结果，再次遇到可以直接使用</b>
代码如下：

```java
public class Solution {
	HashMap<String, List<String> >map = new HashMap<String, List<String> >();
	public List<String> wordBreak(String s, Set<String> dict) {
		if (map.containsKey(s) == true) // 已经处理过的子串
			return map.get(s);
		List<String> ret = new ArrayList<String>();
		for (int i=1; i<=s.length(); i++) {
			String tmp1 = s.substring(0, i), tmp2 = s.substring(i);
			if (dict.contains(tmp1) == true) { // 第一段是word的话
				if (tmp2.length() == 0)
					ret.add(tmp1);
				else {
					List<String> l = wordBreak(tmp2, dict); // 获取第二段的组成方式
					for (String str:l)
						ret.add(tmp1+" "+str); //拼接
				}
			} // 否则进入下一次循环
		}
		map.put(s, ret);
		return ret;
    }
}
```
