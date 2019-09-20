---
title: Water and Jug Problem
date: 2016-09-22 14:58:18
tags:
categories:
---

##### Problem
You are given two jugs with capacities x and y litres. There is an infinite amount of water supply available. You need to determine whether it is possible to measure exactly z litres using these two jugs.

If z liters of water is measurable, you must have z liters of water contained within one or both buckets by the end.

Operations allowed:

- Fill any of the jugs completely with water.
- Empty any of the jugs.
- Pour water from one jug into another till the other jug is completely full or the first jug itself is empty.


    Example 1: (From the famous "Die Hard" example)

    Input: x = 3, y = 5, z = 4
    Output: True
    Example 2:

    Input: x = 2, y = 6, z = 5
    Output: False


##### Solution
贝祖等式（Bézout's identity / 定理）：
对任何整數 a、 b和它们的最大公约数 d，关于未知数 x 和 y 的线性方程（称为贝祖等式）：

    ax + by = m

有整数解时当且仅当m是d的倍数。

所以，只要x、y的最大公约数d能整除m，并且x+y<=m，那么存在a、b满足 ax + by = m

```java
public boolean canMeasureWater(int x, int y, int z) {
    if(x + y < z) return false;
    // 出现x=0或者y=0、x + y == z
    if( x == z || y == z || x + y == z ) return true;
    // 利用贝祖定理，求最大公约数
    return z%GCD(x, y) == 0;
}

public int GCD(int a, int b){
    while(b != 0 ){
        int temp = b;
        b = a%b;
        a = temp;
    }
    return a;
}
```