---
title: Substring with Concatenation of All Words
date: 2016-08-27 10:04:46
tags: [Sliding window, LeetCode, String]
categories: OJ
---

#### Problem
You are given a string, s, and a list of words, words, that are all of the same length. Find all starting indices of substring(s) in s that is a concatenation of each word in words exactly once and without any intervening characters.

For example, given:
s: "barfoothefoobarman"
words: ["foo", "bar"]

You should return the indices: [0,9].
(order does not matter).

#### Solution
每个单词的长度一致，考虑滑动窗口的思想
- 使用滑动窗口的思想，双层循环
- 第一层确定要寻找的单词组合的开头下标
- 第二层循环试图寻找一个可能的组合，如果成功则记录开头下标；否则，退出第二层循环
- 程序采用复制哈希表的方式会超时

```java
public static List<Integer> findSubstring(String S, String[] L) {
    List<Integer> res = new ArrayList<Integer>();
    if (S == null || L == null || L.length == 0) return res;
    int len = L[0].length(); // length of each word
    Map<String, Integer> map = new HashMap<String, Integer>(); // map for L
    for (String w : L) map.put(w, map.containsKey(w) ? map.get(w) + 1 : 1);

    for (int i = 0; i <= S.length() - len * L.length; i++) { // possible start index
        Map<String, Integer> copy = new HashMap<String, Integer>(map);
        for (int j = 0; j < L.length; j++) { // checkc if match
            String str = S.substring(i + j*len, i + j*len + len); // next word
            if (copy.containsKey(str)) { // is in remaining words
                int count = copy.get(str);
                if (count == 1) copy.remove(str);
                else copy.put(str, count - 1);
                if (copy.isEmpty()) { // matches
                    res.add(i);
                    break;
                }
            } else break; // not in L
        }
    }
    return res;
}
```

这样的代码还有一种写法，也是使用双层循环。第一层循环为单个单词的长度，第二层以固定的步长进行匹配，不推荐这么写。

```java
public List<Integer> findSubstring(String s, String[] words) {
        List<Integer> ret = new LinkedList<>();
        if (s.length() == 0 || words.length == 0)
            return ret;
        Map<String, Integer> map = new HashMap<>();
        for (String word : words) map.put(word, map.containsKey(word)?map.get(word)+1:1);
        int len = words[0].length(), start = 0, end = 0, count;
        Map<String, Integer> tmp_map = new HashMap<>();
        for (int i = 0; i < len; i++) {
            tmp_map.clear();
            start = i;
            end = i;
            count = 0;
            while (end + len <= s.length()) {
                String tmp_str = s.substring(end, end + len), tmp = null;
                if (map.containsKey(tmp_str)) { // a word
                    if (tmp_map.containsKey(tmp_str)) tmp_map.put(tmp_str, tmp_map.get(tmp_str)+1);
                    else tmp_map.put(tmp_str, 1);
                    count++;
                    if (tmp_map.get(tmp_str) > map.get(tmp_str)) {
                        while (start <= end && tmp_map.get(tmp_str) > map.get(tmp_str)) {
                            tmp = s.substring(start, start + len);
                            tmp_map.put(tmp, tmp_map.get(tmp) - 1);
                            start += len;
                            count--;
                        }
                    }
                    if (count == words.length) {
                        --count;
                        tmp = s.substring(start, start+len);
                        tmp_map.put(tmp, map.get(tmp)-1);
                        ret.add(start);
                        start += len;
                    }
                    end += len;
                } else { // not a word
                    end += len;
                    start = end;
                    tmp_map.clear();
                    count = 0;
                }
            }
        }
        return ret;
    }
```