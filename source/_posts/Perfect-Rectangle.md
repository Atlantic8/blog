---
title: Perfect Rectangle
date: 2016-08-30 19:50:39
tags: [Geometry, LeetCode]
categories: OJ
---

#### Problem
Given N axis-aligned rectangles where N > 0, determine if they all together form an exact cover of a rectangular region.

Each rectangle is represented as a bottom-left point and a top-right point. For example, a unit square is represented as [1,1,2,2]. (coordinate of bottom-left point is (1, 1) and top-right point is (2, 2)).

Example
<center>![](https://leetcode.com/static/images/problemset/rectangle_perfect.gif)</center>

rectangles = [
  [1,1,3,3],
  [3,1,4,2],
  [3,2,4,4],
  [1,3,2,4],
  [2,3,3,4]
]
Return true. All 5 rectangles together form an exact cover of a rectangular region.

#### Solution
可以拼凑成矩形的情形应当满足一下条件：
- 大矩形面积 = sum(小矩形面积)
- 除了最外边的4个角(corner)，其他角都应该重复偶数次(2或者4次)
- 重复在同一个点的角(corner)应该方向不同(左下、左上、右下、右上)

解决思路：
- 使用哈希表维护边角()和其类型，类型分别取值1、2、4、8
- 这些类型其二进制都只有一个位是1。与运算结果不为0时表示出现重复(方块重叠发生)，否则做或运算并更新哈希表(保持这个值的存在)
- 单独考虑总体矩形的边角，最后哈希表里值为1、2、4、8的只能且必须有4个

```python
HashMap<String, Integer> mapp = new HashMap<>();
    public boolean isRectangleCover(int[][] rectangles) {
        if (rectangles.length==0 || rectangles[0].length==0) return false;
        int minx=Integer.MAX_VALUE,miny=Integer.MAX_VALUE,maxx=0,maxy=0,sum=0,count=0;
        for (int[] rect : rectangles) {
        	minx = Math.min(minx, rect[0]);
        	miny = Math.min(miny, rect[1]);
        	maxx = Math.max(maxx, rect[2]);
        	maxy = Math.max(maxy, rect[3]);
        	if (isRectangleCover_assist(rect[0]+" "+rect[1], 1)) return false;
        	if (isRectangleCover_assist(rect[0]+" "+rect[3], 2)) return false;
        	if (isRectangleCover_assist(rect[2]+" "+rect[1], 4)) return false;
        	if (isRectangleCover_assist(rect[2]+" "+rect[3], 8)) return false;
        	sum += (rect[2]-rect[0])*(rect[3]-rect[1]);
        }
        for (Integer tmp : mapp.values())
        	// 只有整体矩形的四个边角才是这些值
        	if (tmp==1 || tmp==2 || tmp==4 || tmp==8) count += 1;
        return count==4 && sum==(maxx-minx)*(maxy-miny);
    }
    // 确定mapp中是否已经存在两个一样的pair
    public boolean isRectangleCover_assist(String key, int value) {
    	if (mapp.containsKey(key) && (mapp.get(key)&value)!=0) return true;
    	mapp.put(key, mapp.containsKey(key)?mapp.get(key)|value:value);
    	return false;
    }
```
