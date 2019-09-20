---
title: Design Twitter
date: 2016-09-01 19:10:24
tags:
categories: OJ
---

#### Problem
Design a simplified version of Twitter where users can post tweets, follow/unfollow another user and is able to see the 10 most recent tweets in the user's news feed. Your design should support the following methods:

- postTweet(userId, tweetId): Compose a new tweet.
- getNewsFeed(userId): Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.
- follow(followerId, followeeId): Follower follows a followee.
- unfollow(followerId, followeeId): Follower unfollows a followee.

<b>Example</b>
```java
Twitter twitter = new Twitter();

// User 1 posts a new tweet (id = 5).
twitter.postTweet(1, 5);

// User 1's news feed should return a list with 1 tweet id -> [5].
twitter.getNewsFeed(1);

// User 1 follows user 2.
twitter.follow(1, 2);

// User 2 posts a new tweet (id = 6).
twitter.postTweet(2, 6);

// User 1's news feed should return a list with 2 tweet ids -> [6, 5].
// Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
twitter.getNewsFeed(1);

// User 1 unfollows user 2.
twitter.unfollow(1, 2);

// User 1's news feed should return a list with 1 tweet id -> [5],
// since user 1 is no longer following user 2.
twitter.getNewsFeed(1);
```

#### Solution
解题思路：如果将所有用户的tweet放在一个队列里，在getNewsFeed时遍历查找会超时
- 每个用户维护一个follow集合，集合中元素时该用户关注的用户ID
- 每个用户维护一个自己的tweet列表，列表元素包含时间和tweet ID，列表按时间排好序
- getNewsFeed时，采用merge k sorted array的思想，将用户自己和关注的用户的tweet列表放入一个堆中
- 每次弹出第一个元素对应时间最近的列表，取出第一个元素，然后再将其加入进堆中（如果该列表还有元素）
- 取出的元素达到要求或者堆为空时退出

```java
public class Twitter {
    HashMap<Integer, Set<Integer>> cmap;
    HashMap<Integer, List<int[]>> tw;
    int count;
    /** Initialize your data structure here. */
    public Twitter() {
        cmap = new HashMap<>();
        tw = new HashMap<>();
        count = 0;
    }

    /** Compose a new tweet. */
    public void postTweet(int userId, int tweetId) {
        int[] tmp = {count++, tweetId};
        tw.computeIfAbsent(userId, k->new LinkedList<>()).add(0,tmp);
        System.out.println(count);
    }

    /** Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent. */
    public List<Integer> getNewsFeed(int userId) {
        int n = 0;
        Set<Integer> tmp = cmap.containsKey(userId)?cmap.get(userId):new HashSet<Integer>();
        List<Integer> ret = new LinkedList<>();

        PriorityQueue<List<int[]> > pq = new PriorityQueue<>(new Comparator<List<int[]>>(){

            @Override
            public int compare(List<int[]> o1, List<int[]> o2) {
                // TODO Auto-generated method stub
                return o2.get(0)[0] - o1.get(0)[0];
            }});
        if (tw.containsKey(userId) && tw.get(userId).size()>0) pq.offer(tw.get(userId));
        for (Integer it : tmp) {
            if (!tw.containsKey(it) || tw.get(it).size()==0) continue;
            pq.offer(tw.get(it));
        }
        while (pq.size()>0 && n++<10) {
            List<int[]> list = pq.poll();
            ret.add(list.get(0)[1]);
            if (list.size()>1) pq.offer(list.subList(1, list.size()));
        }
        return ret;
    }

    /** Follower follows a followee. If the operation is invalid, it should be a no-op. */
    public void follow(int followerId, int followeeId) {
        if (followerId == followeeId) return;
        cmap.computeIfAbsent(followerId, k -> new HashSet<Integer>()).add(followeeId);
    }

    /** Follower unfollows a followee. If the operation is invalid, it should be a no-op. */
    public void unfollow(int followerId, int followeeId) {
        if (followerId==followeeId || !cmap.containsKey(followerId)) return;
        Set<Integer> tmp = cmap.get(followerId);
        if (!tmp.contains(followeeId)) return;
        tmp.remove(followeeId);
    }
}
```
<b>实现过程中，tweet集合不使用java自带的List，改用自定义类和索引标识可以进一步加速程序。</b>

