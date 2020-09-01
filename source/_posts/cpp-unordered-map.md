---
title: cpp-unordered_map
date: 2016-05-04 22:42:11
tags: Cpp
categories: Dev
---

`unordered_map`的基本用法如下：
```c++
unordered_map<string, int> map ;
map["zhangsan"]=3;
map["lisi"]=9;
int x = map["lisi"]; //9
unordered_map<string, int>::iterator it;
for (it=map.begin(); it!=map.end(); it++)
    cout<<it->first<<" "<<it->second<<endl;
```
关于支持复杂类型key，`unordered_map`支持`string`类型，但是自定义类型不行。下面给出通过重载使得`unordered_map`支持自定义类型的例子：
```c++
struct ReadingPair //作为key的类型
{
    double real, modified;
    ReadingPair() {
        this->real = 0;
        this->modified = 0;
    }
    // 判断两个示例是否相等的函数
    bool operator== (const struct ReadingPair& other) const {
        if (real != other.real || modified != other.modified)
            return false;
        return true;
    }
};
另外还需要一个hash函数，重载操作符(),计算key的哈希值。
一个比较直观的方法是特化（specialize）std::hash模板。
namespace std {
    template <>
    struct hash<ReadingPair> {
        std::size_t operator()(const ReadingPair& k) const {
            // Compute individual hash values for first,
            // second and third and combine them using XOR
            // and bit shifting:
            using std::hash; //重要
            return ((hash<double>()(k.real)
                ^ (hash<double>()(k.modified) << 1)) >> 1);
        }
    };
}
由于unordered_map不需要排序，所以不需要重载<符号。
```