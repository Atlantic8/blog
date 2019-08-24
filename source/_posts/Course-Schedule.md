---
title: Course Schedule
date: 2017-06-28 13:24:03
tags: [LeetCode]
categories: OJ
---


课程调度这个题目一共有3个，以下分别描述其题目和解法。



###### Course Schedule 1

一共有标号从0到n-1的n个课程，有些课程需要在其他课程的基础上才能学，现在给定课程总数n和先决课程对（目标课程，先决课程）。输出这些课程能否学完



###### Solution 1

BFS拓扑排序可以做，DFS查找回路也可以。

```java

public class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        if (prerequisites.length==0 || prerequisites[0].length==0) return true;
        List<Set<Integer>> in = new ArrayList<>(), out = new ArrayList<>();
        for (int i=0; i<numCourses; i++) {
            in.add(new HashSet<>());
            out.add(new HashSet<>());
        }

        for (int i=0; i<prerequisites.length; i++) {
            in.get(prerequisites[i][0]).add(prerequisites[i][1]); // pre-course
            out.get(prerequisites[i][1]).add(prerequisites[i][0]); // later-course
        }

        List<Integer> ready = new ArrayList<>();
        for (int i=0; i<numCourses; i++)
            if (in.get(i).size() == 0) ready.add(i);

        while (ready.size() > 0) {
            int pos = ready.remove(0);
            Set<Integer> set = out.get(pos);
            for (Object it : set.toArray()) {
                in.get((int)it).remove(pos);
                if (in.get((int)it).size() == 0) ready.add((int)it);
            }

        }

        for (int i=0; i<numCourses; i++)
            if (in.get(i).size() > 0) return false;
        return true;

    }
}

```



###### Course Schedule 2

在上一题的基础上输出，如果可以学完，输出任意一个顺序即可，否则，输出一个空的顺序[]。



###### Solution 2

```java

public class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        int[] ret = new int[numCourses];
        List<Set<Integer>> in = new ArrayList<>(), out = new ArrayList<>();
        for (int i=0; i<numCourses; i++) {
            in.add(new HashSet<>());
            out.add(new HashSet<>());
        }

        for (int i=0; i<prerequisites.length; i++) {
            in.get(prerequisites[i][0]).add(prerequisites[i][1]); // pre-course
            out.get(prerequisites[i][1]).add(prerequisites[i][0]); // later-course
        }

        int k = 0;
        List<Integer> ready = new ArrayList<>();
        for (int i=0; i<numCourses; i++) {
            if (in.get(i).size()==0 && out.get(i).size()==0) ret[k++] = i;
            else if (in.get(i).size()==0 && out.get(i).size()>0) ready.add(i);
        }

        while (ready.size() > 0) {
            int pos = ready.remove(0);
            ret[k++] = pos;
            Set<Integer> set = out.get(pos);
            for (Object it : set.toArray()) {
                in.get((int)it).remove(pos);
                if (in.get((int)it).size() == 0) ready.add((int)it);
            }
        }

        for (int i=0; i<numCourses; i++)
            if (in.get(i).size() > 0) return new int[0];
        return ret;

    }
}

```



###### Course Schedule 3

一共有标号从0到n-1的n个课程，每个课程都有一个持续时间。给定每个课程的持续时间t和最晚结束时间d对（t,d），要求找到能够完成的课程的最大数量。其中，1 <= d, t, n <= 10,000，同一时刻不能同时学习两门课。



    [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]

    output: 3



###### Solution 3

先对每个课程按最晚结束时间从小到大排序。在前k-1个课程处理之后，对与第k个课程（tk,dk），前k个课程的最晚结束时间为dk，如果前k-1个课程中最优课程组合的总时长为x

- 如果此时`tk + x > dk`，那么这个课程就不能直接放进去，处理方法是将这个课程放进去，然后从已选课程中删除时长最大的课程（删除时长最大的肯定是最好的选择，最大堆）

- 否则，直接将当前课程放进去即可



```java

class Solution {

public:
    
    int scheduleCourse(vector<vector<int>>& courses) {
        int ret = 0, sum = 0, n = 0;
        priority_queue<int> pq;
        sort(courses.begin(), courses.end(), [](const vector<int>& a, const vector<int>& b){
            if (a[1] == b[1]) return a[0] < b[0];
            return a[1] < b[1];
        }); 

        for (int i=0; i<courses.size(); i++) {
            pq.push(courses[i][0]);
            sum += courses[i][0];
            if (sum > courses[i][1]) {
                sum -= pq.top();
                pq.pop();
            }
        }

        return pq.size();
    }
};

```