---
title: Word Search
date: 2016-09-11 10:23:58
tags: [DFS, LeetCode]
categories: OJ
---

#### Word Search
Given a 2D board and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. <b>The same letter cell may not be used more than once.</b>

    For example,
    Given board =

    [
      ['A','B','C','E'],
      ['S','F','C','S'],
      ['A','D','E','E']
    ]
    word = "ABCCED", -> returns true,
    word = "SEE", -> returns true,
    word = "ABCB", -> returns false.


解题思路
- 典型的DFS题
- 每到一个点，将其做标记（可以通过异或操作减少空间浪费），然后继续递归，递归完成后，把这个点的值还原


#### Word Search
在上一题的基础上，给定一个单词集合words，找到words中的能由board构建的全部单词。对每个单词，假设board的每个格子只能用1次。

    For example,
    Given words = ["oath","pea","eat","rain"] and board =

    [
      ['o','a','a','n'],
      ['e','t','a','e'],
      ['i','h','k','r'],
      ['i','f','l','v']
    ]
    Return ["eat","oath"].

解题思路
- 还是要用dfs的思想
- 关于words的形式，trie树显然是最natural的
- trie树节点包含26个指针，指向其可能存在的子节点，还包含一个string属性，此属性只在根节点上有用，表示以这个根结点结尾的word
- 对board的每一个节点，调用dfs算法，dfs算法根据trie树经行搜索。遇到根结点的话，将对应的结果存储
- 结果对重复的word并不计算，所以要考虑去重

```java
public List<String> findWords(char[][] board, String[] words) {
    List<String> res = new ArrayList<>();
    TrieNode root = buildTrie(words);
    for(int i = 0; i < board.length; i++) {
        for(int j = 0; j < board[0].length; j++) {
            dfs(board, i, j, root, res);
        }
    }
    return res;
}

public void dfs(char[][] board, int i, int j, TrieNode p, List<String> res) {
    char c = board[i][j];
    if(c == '#' || p.next[c - 'a'] == null) return;
    p = p.next[c - 'a'];
    if (p.word != null) {   // 叶节点
        res.add(p.word);
        p.word = null;     // 记录这个单词一次就够了，以后不需要记录它
    }

    board[i][j] = '#';
    if(i > 0) dfs(board, i - 1, j ,p, res);
    if(j > 0) dfs(board, i, j - 1, p, res);
    if(i < board.length - 1) dfs(board, i + 1, j, p, res);
    if(j < board[0].length - 1) dfs(board, i, j + 1, p, res); 
    board[i][j] = c;
}

public TrieNode buildTrie(String[] words) {
    TrieNode root = new TrieNode();
    for(String w : words) {
        TrieNode p = root;
        for(char c : w.toCharArray()) {
            int i = c - 'a';
            if(p.next[i] == null) p.next[i] = new TrieNode();
            p = p.next[i];
       }
       p.word = w; // 叶节点的word属性值为这个单词
    }
    return root;
}

// trie树的定义
class TrieNode {
    TrieNode[] next = new TrieNode[26];
    String word;
}
```




