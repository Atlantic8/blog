---
title: Trapping Rain Water
date: 2016-10-02 16:25:51
tags: [LeetCode]
categories: OJ
---

##### 一维情况
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.


	For example
	Given [0,1,0,2,1,0,1,3,2,1,2,1], return 6.

![](http://ww3.sinaimg.cn/mw690/9bcfe727jw1f8e0cp2n0rj20bg04h3yf.jpg)
The above elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped. Thanks Marcos for contributing this image!

##### 解决方案
- 双指针，分别指向数组两端，主要是由两边到中间的思想
- 维护左边最高、右边最高的值
- 如果: a[left] < a[right]，先处理left-side [ 否则，right-side。这样保证未被处理的一边总有大于另一边最大值的元素。]
	- 假如a[left] >= maxleft, 那么: maxleft = a[left]
	- 否则：ret += maxleft-a[left]. 因为右边总有比maxleft大的，否则，不可能处理left这边的数。

```java
class Solution {
public:
    int trap(int A[], int n) {
        int left=0; int right=n-1;
        int res=0;
        int maxleft=0, maxright=0;
        while(left<=right){
        	// 先处理小的一方，保证对面方总有更大的数
            if(A[left]<=A[right]){
            	// 更新最大值
                if(A[left]>=maxleft) maxleft=A[left];
                // 因为另一边总有大于maxleft的值，所以，此时可盛水maxleft-A[left]
                else res+=maxleft-A[left];
                left++;
            } else { // 同左边
                if(A[right]>=maxright) maxright= A[right];
                else res+=maxright-A[right];
                right--;
            }
        }
        return res;
    }
};
```

##### 二维状况
Given an m x n matrix of positive integers representing the height of each unit cell in a 2D elevation map, compute the volume of water it is able to trap after raining.

Note:
Both m and n are less than 110. The height of each unit cell is greater than 0 and is less than 20,000.

	Example:

	Given the following 3x6 height map:
	[
  		[1,4,3,1,3,2],
  		[3,2,1,3,2,4],
  		[2,3,3,2,3,1]
	]

	Return 4.

![](http://ww1.sinaimg.cn/mw690/9bcfe727jw1f8e0cossfsj20dw08cjrl.jpg)
The above image represents the elevation map [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]

##### 解决方案
###### 从四周开始，由外向内的方法
- 从边界开始，挑选最矮的已经访问过的cell，检查它的邻居(没有被访问过的)
- 如果邻居比当前的矮，收集邻居能手机的水量（邻居不必当前矮则无法收集），并填充能收集水的邻居（更新其高度）
- 把所有的邻居加入到队列

```java
public class Solution {

    public class Cell {
        int row;
        int col;
        int height;
        public Cell(int row, int col, int height) {
            this.row = row;
            this.col = col;
            this.height = height;
        }
    }

    public int trapRainWater(int[][] heights) {
        if (heights == null || heights.length == 0 || heights[0].length == 0)
            return 0;

        PriorityQueue<Cell> queue = new PriorityQueue<>(1, new Comparator<Cell>(){
            public int compare(Cell a, Cell b) {
                return a.height - b.height;
            }
        });

        int m = heights.length;
        int n = heights[0].length;
        boolean[][] visited = new boolean[m][n];

        // Initially, add all the Cells which are on borders to the queue.
        for (int i = 0; i < m; i++) {
            visited[i][0] = true;
            visited[i][n - 1] = true;
            queue.offer(new Cell(i, 0, heights[i][0]));
            queue.offer(new Cell(i, n - 1, heights[i][n - 1]));
        }

        for (int i = 0; i < n; i++) {
            visited[0][i] = true;
            visited[m - 1][i] = true;
            queue.offer(new Cell(0, i, heights[0][i]));
            queue.offer(new Cell(m - 1, i, heights[m - 1][i]));
        }

        // from the borders, pick the shortest cell visited and check its neighbors:
        // if the neighbor is shorter, collect the water it can trap and update its height as its height plus the water trapped
       // add all its neighbors to the queue.
        int[][] dirs = new int[][]{{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int res = 0;
        while (!queue.isEmpty()) {
            Cell cell = queue.poll();
            for (int[] dir : dirs) {
                int row = cell.row + dir[0];
                int col = cell.col + dir[1];
                if (row >= 0 && row < m && col >= 0 && col < n && !visited[row][col]) {
                    visited[row][col] = true;
                    res += Math.max(0, cell.height - heights[row][col]);
                    queue.offer(new Cell(row, col, Math.max(heights[row][col], cell.height)));
                }
            }
        }

        return res;
    }
}
```



###### Dijkstra
构建一个图，每个cell都是一个节点，再加上一个dummy节点表示外部区域。
如果cell(i, j)与cell(i', j')相邻，那么，创建一个由cell(i, j)到cell(i', j')的有向边，边的权值为height(i, j)
边上cell与dummy节点有一条权值为0的边。
设定每条路径的权值为：该路径上最大的权值。所以对每一个cell(i,j)，它能盛的水就是cell(i, j)到dummy节点的最短路径的权值dist(i, j)
如果：dist(i, j) <= height(i, j)，那么cell(i, j)不能盛水。

我们可能需要计算dist(i, j) 对于每个(i, j)对，即多个cell，只有一个终点dummy节点。所以将每条边的方向逆转，那么只需要使用一次Dijkstra算法就可以计算dummy节点到每个cell的最短路径，继而计算出每个cell能盛水的量（最短路径的权值）。

假设cell由r行、c列，那么时间复杂度：O(rc*log(rc)) = O(rc*max(log r, log c))，空间复杂度为：O(rc).

```java
public class Solution {

    int[] dx = {0, 0, 1, -1};
    int[] dy = {1, -1, 0, 0};

    List<int[]>[] g;
    int start;

    private int[] dijkstra() {
        int[] dist = new int[g.length];
        Arrays.fill(dist, Integer.MAX_VALUE / 2);
        dist[start] = 0;
        TreeSet<int[]> tree = new TreeSet<>((u, v) -> u[1] == v[1] ? u[0] - v[0] : u[1] - v[1]);
        tree.add(new int[]{start, 0});
        while (!tree.isEmpty()) {
            int u = tree.first()[0], d = tree.pollFirst()[1];
            for (int[] e : g[u]) {
                int v = e[0], w = e[1];
                if (Math.max(d, w) < dist[v]) {
                    tree.remove(new int[]{v, dist[v]});
                    dist[v] = Math.max(d, w);
                    tree.add(new int[]{v, dist[v]});
                }
            }
        }
        return dist;
    }

    public int trapRainWater(int[][] a) {
        if (a == null || a.length == 0 || a[0].length == 0) return 0;
        int r = a.length, c = a[0].length;

        start = r * c;
        g = new List[r * c + 1];
        for (int i = 0; i < g.length; i++) g[i] = new ArrayList<>();
        for (int i = 0; i < r; i++)
            for (int j = 0; j < c; j++) {
                if (i == 0 || i == r - 1 || j == 0 || j == c - 1) g[start].add(new int[]{i * c + j, 0});
                for (int k = 0; k < 4; k++) {
                    int x = i + dx[k], y = j + dy[k];
                    if (x >= 0 && x < r && y >= 0 && y < c) g[i * c + j].add(new int[]{x * c + y, a[i][j]});
                }
            }

        int ans = 0;
        int[] dist = dijkstra();
        for (int i = 0; i < r; i++)
            for (int j = 0; j < c; j++) {
                int cb = dist[i * c + j];
                if (cb > a[i][j]) ans += cb - a[i][j];
            }

        return ans;
    }
}
```
