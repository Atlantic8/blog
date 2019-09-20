---
title: STL Heap
date: 2016-09-19 21:50:49
tags: [Cpp, STL]
categories: Algorithm
---



##### 堆

###### make_heap

```java

void make_heap (RandomAccessIterator first, RandomAccessIterator last, Compare comp );



make_heap (v.begin(),v.end());

```

重新组织[first, last)，使之成为一个堆（默认为大顶堆）。





###### is_heap

```java

bool is_heap (RandomAccessIterator first, RandomAccessIterator last, Compare comp);



is_heap(foo.begin(), foo.end());

```

检查[first, last)范围内的元素是否满足堆的定义





###### is_heap_until

```java

RandomAccessIterator is_heap_until (RandomAccessIterator first, RandomAccessIterator last, Compare comp);



auto last = std::is_heap_until (foo.begin(),foo.end());

```

返回[first, last)范围内第一个不满足heap定义的迭代器。





###### pop_heap & push_heap

```java

void pop_heap (RandomAccessIterator first, RandomAccessIterator last, Compare comp);



pop_heap (v.begin(), v.end());

v.pop_back();

```

pop, push完了之后，重新调整，pop默认最大值。





###### sort_heap

```java

void sort_heap (RandomAccessIterator first, RandomAccessIterator last, Compare comp);

```

排序，heap的属性可能会丢失



---









##### 排序



```java

#include <algorithm>

```



|function|explanation|function|explanation|

|:------:|:---------:|:------:|:---------:|

|sort|对给定区间所有元素进行排序|stable_sort|对给定区间所有元素进行稳定排序|

|partial_sort|对给定区间所有元素部分排序|partial_sort_copy|对给定区间复制并排序|

|nth_element|找出给定区间的某个位置对应的元素|is_sorted|判断一个区间是否已经排好序|

|partition|使得符合某个条件的元素放在前面|stable_partition|相对稳定的使得符合某个条件的元素放在前面|



###### sort

```java

void sort (RandomAccessIterator first, RandomAccessIterator last, Compare comp);

sort (myvector.begin(), myvector.end());

```

将[first, last)范围内元素排序，排序方式由comp决定，**comp是自定义函数，可以使用lambda表达式替代**。

```java

/* lambda表达式形式如下

capture：指定了在可见域范围内 lambda 表达式的代码内可见得外部变量的列表，可能取值如下：

    []             不截取任何变量

    [&]         截取外部作用域中所有变量，并作为引用在函数体中使用

    [=]         截取外部作用域中所有变量，并拷贝一份在函数体中使用

    [=, &foo]     截取外部作用域中所有变量，并拷贝一份在函数体中使用，但是对foo变量使用引用

    [bar]         截取bar变量并且拷贝一份在函数体重使用，同时不截取其他变量

    [x, &y]     x按值传递，y按引用传递

    [this]         截取当前类中的this指针。如果已经使用了&或者=就默认添加此选项

params：  指定 lambda 表达式的参数

ret:  返回类型

body: 函数体

*/



[ capture ] ( params ) -> ret { body }

sort (envelopes.begin(), envelopes.end(), [](const pair<int, int> &a, const pair<int, int> &b){

    if (a.first == b.first) return a.second > b.second;

    return a.first < b.first;

});

```



###### stable_sort

```java

void stable_sort ( RandomAccessIterator first, RandomAccessIterator last, Compare comp );

```

函数用法与sort一致，它的排序结果是稳定的。



###### partial_sort

```java

void partial_sort (RandomAccessIterator first, RandomAccessIterator middle, RandomAccessIterator last, Compare comp);

```

对[first, middle)范围的元素进行排序。



###### partial_sort_copy

```java

void partial_sort_copy (InputIterator first,InputIterator last,RandomAccessIterator result_first,RandomAccessIterator result_last, Compare comp);

```

对[first, last)范围的元素进行排序，并将排序结果复制到[result_first, result_last)



###### is_sorted

```java

bool is_sorted (ForwardIterator first, ForwardIterator last, Compare comp);

```

判断[first, last)范围的元素是否有序。



###### nth_element

```java

void nth_element (RandomAccessIterator first, RandomAccessIterator nth, RandomAccessIterator last, Compare comp);

```

重新组织[first, last)范围的元素，使第n大元素处于第n位置，并且比这个元素小的元素都排在这个元素之前，比这个元素大的元素都排在这个元素之后，但不能保证他们是有序的



###### partition

```java

BidirectionalIterator partition (BidirectionalIterator first, BidirectionalIterator last, UnaryPredicate pred);

```

将区间[first,last)中的元素重新排列，满足判断条件pred的元素会被放在区间的前段，不满足pred的元素会被放在区间的后段。该算法不能保证元素的初始相对位置，**返回指向第二类第一个元素的迭代器**。

用法：

```java

bool IsOdd (int i) { //用语判断奇数

    return (i%2) == 1; //奇数返回true，偶数返回0

}



int main(void)

{

    std::vector<int> ivec;

    for (int i=1; i<10; ++i)

        ivec.push_back(i); // 1 2 3 4 5 6 7 8 9

    auto bound = partition (ivec.begin(), ivec.end(), IsOdd);

    std::cout << "odd elements:";

    for (auto it=ivec.begin(); it!=bound; ++it)

        std::cout << ' ' << *it;       //输出1,9,3,7,5

    std::cout << "even elements:";

    for (auto it=bound; it!=ivec.end(); ++it)

        std::cout << ' ' << *it;     //输出6,4,8,2

    return 0;

}

```



###### stable_partition

partition的稳定版本。



###### sort_heap

```java

void sort_heap (RandomAccessIterator first, RandomAccessIterator last, Compare comp);

```

用法和上面的函数一致。







###### lower_bound & upper_bound

```java

ForwardIter lower_bound(ForwardIter first, ForwardIter last, const _Tp& val);

ForwardIter upper_bound(ForwardIter first, ForwardIter last, const _Tp& val);

```

**lower_bound返回一个非递减序列[first, last)中的第一个大于等于值val的位置.**

**upper_bound返回一个非递减序列[first, last)中第一个大于val的位置**

这两个函数都是用**二分查找**方法实现的，复杂度为O(logn)





---





##### 集合set

set作为一个容器也是用来存储同一数据类型的数据类型，并且能从一个数据集合中取出数据，在set中每个元素的值都唯一，而且元素的值是有序的。**set中数元素的值不能直接被改变**。C++ STL中标准关联容器`set, multiset, map, multimap`内部采用RB树(插入元素迭代器不会失效，删除元素时除了被删除的那个以外的迭代器不会失效)。



其包含的方法包括

- `begin(), end(), rbegin(), rend()`

- `clear(), empty(), find(), insert(key_value)`

- `inset(first,second)`;将迭代器`first`到`second`之间的元素插入到`set`中，返回值是`void`

- `size(), max_size()`

- `equal_range() `，返回一对**迭代器**，分别表示第一个大于或等于给定关键值的元素迭代器 以及 第一个大于给定关键值的元素的迭代器，这个返回值是一个pair类型，如果这一对定位器中哪个返回失败，就会等于`end()`的值。

- `erase(iterator)`  ，删除迭代器`iterator`指向的值

- `erase(first,second)`，删除迭代器`first`和`second`之间的值

- `erase(key_value)`，删除键值`key_value`的值

- `lower_bound(key)`:返回第一个**大于等于**`key`的迭代器指针

- `upper_bound(key)`:返回第一个**大于**`key`的迭代器指针



---





##### 链表list

c++中的list容器是双向链表。

```java

#include < list > 

list<int> new_list;



assign(iter1, iter2) 将两个迭代器之间的元素赋值给当前list

back() 返回最后一个元素

begin() 返回指向第一个元素的迭代器

clear() 删除所有元素

empty() 如果list是空的则返回true

end() 返回末尾的迭代器

erase() 删除一个元素 

front() 返回第一个元素 

get_allocator() 返回list的配置器 

insert(const_iterator position, const value_type& val) 插入一个元素到list中 

max_size() 返回list能容纳的最大元素数量 

merge(list& x, Compare comp) 合并当前list和x

pop_back() 删除最后一个元素 

pop_front() 删除第一个元素 

push_back() 在list的末尾添加一个元素 

push_front() 在list的头部添加一个元素 

rbegin() 返回指向第一个元素的逆向迭代器 

remove(const value_type& val) 从list删除元素元素val

remove_if(Predicate pred) 按指定条件删除所有满足条件的元素 

rend() 指向list末尾的逆向迭代器 

resize(size_type n, const value_type& val) 改变list的大小，val是增加空间用的填充值

reverse() 把list的元素倒转 

size() 返回list中的元素个数 

sort(Compare comp) 给list排序，复杂度大约是NlogN，可以用归并

splice() 合并两个list 

swap(list& x) 交换当前list和x

unique() 删除list中重复的元素

```

遍历使用迭代器



---



##### forward_list

forward_list是单向链表



---



##### deque

`deque`容器类与`vector`类似，支持随机访问和快速插入删除，它在容器中某一位置上的操作所花费的是线性时间。与`vector`不同的是，`deque`还支持从开始端插入数据：`push_front()`。其余类似`vector`操作方法的使用。



- 随机访问方便，即支持[ ] 操作符和`vector.at()` ，但性能没有`vector` 好；

- 可以在内部进行插入和删除操作，但性能不及list ；

- 可以在两端进行push 、pop ；

- 相对于verctor 占用更多的内存。



---





##### priority_queue

将任意类型的序列容器转换为一个优先级队列，一般使用vector作为底层存储方式。

只能访问第一个元素，**不能遍历整个`priority_queue`**。



模板声明带有三个参数，`priority_queue<Type, Container, Functional>`

其中`Type` 为数据类型， `Container` 为保存数据的容器，`Functional` 为元素比较方式。

`Container` 必须是用数组实现的容器，比如 `vector, deque` 但不能用`list`.

STL里面容器默认用的是 `vector`. 比较方式默认用 `operator < `

缺省时优先队列就是大顶堆，队头元素优先级最大。



```java

#include <queue>



priority_queue <Elem> c;    // 创建一个空的queue

c.top();     // 返回队列头部数据

c.push(elem);     // 在队列尾部增加elem数据

c.pop();     // 队列头部数据出队

c.empty();

c.size();

```



























