---
title: Bounds in Binary Search
mathjax: true
date: 2020-09-01 23:12:12
tags: [Binary Search]
categories: OJ
---

二叉搜索的理念比较简单，不赘述，这里说的是在循环处理、边界条件上的内容。
- 循环条件：包含的是**有必要继续进行搜索的区间**，如果没有必要继续计算了，把循环条件放开
- 边界处理：初始的范围应该覆盖所有可能的取值
- 边界缩进：判断时，把可能找到最终结果的条件放在一起；缩进边界的时候要保证**可能的结果依旧在新的边界范围中**，也就是考虑要不要多移一位


#### naive
先从原始的二叉搜素开始;
- 边界范围：就是数组的序号边界
- 循环条件：算法需要精确到单个长度的区间（l=r），即l<=r，因为查询目标可能不存在
- 边界缩进：比较明显
```python
int binarySearch(int[] nums, int l, int r, int target) {
    while (l <= r) {//[l....r]闭区间查询，l > r 时候形成不了闭区间了，说明没有找到
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) {//找到
            return mid;
        } else if (nums[mid]target){
            //说明中间位置太大了，所以要在[l.....mid-1]中继续查找
            r = mid - 1;
        } else {
            //说明中间位置太小了，所以要在[mid+1 ....r]中继续查找
            l = mid + 1;
        }
    }
    return -1; //跳出循环了没有找到 返回-1
}
```

#### upper bound和lower bound
upper bound是要找有序序列中第一个大于target的值，而lower bound是要找有序序列中第一个不小于target的值。

在STL中，基本定义如下
```c++
Iterator lower_bound(Iterator first, ForwardIterator last, const T& val, Compare comp);
Iterator upper_bound(Iterator first, ForwardIterator last, const T& val, Compare comp);
```
其中，右边界是序列最后一个的下一个位置，因为target可能比最后一个元素还大

###### upper bound
- 边界范围：因为target可能比最后一个元素还大，所以合理的边界是[0, n]，假设n是序列长度
- 循环条件：并不要求元素一定要存在，不需要判断这个元素是否存在，就算是不存在，我们只需要知道“假设target存在，它应该在的位置",**当l=r时候(最终肯定有l=r)，[l,r]正好能够得到一个唯一的位置，就是我们需要的结果**，所以满足l<r让循环一直执行即可
- 边界缩进：当中间值大于target，则当前这个中间值可能就是结果，所以r变化时要保留mid；中间值小于等于target的情况则可以放在一起，因为都没可能是结果，l变化时不用保留mid值


```c++
int upperBound(int[] num, int l, int r,int target) {
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (num[mid] > target) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```


###### lower bound
- 边界范围：因为target可能比最后一个元素还大，所以合理的边界是[0, n]，假设n是序列长度
- 循环条件：同upper bound
- 边界缩进：当中间值大于等于target（大于等于都可能是最终结果），则当前这个中间值可能就是结果，所以r变化时要保留mid；中间值小于target的情况下，因为都没可能是结果，所以l变化时不用保留mid值

```c++
int lowerBound(int[] nums, int l, int r, int target) {
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] >= target) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```




