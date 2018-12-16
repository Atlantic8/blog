---
title: Cpp Rule Fragment3
date: 2017-03-16 10:05:38
tags: Cpp
categories:
---

#### 模板与泛型编程
##### 定义模板
- 函数模板可以定义为inline、constexpr，关键字位置应该在模板参数列表之后，返回类型之前
- 编译器遇到模板时不生成代码，只有在实例化特定版本（使用）时，编译器才会生成代码
- 使用普通类对象时，类定义必须可用但成员函数的定义不必已经出现，因此类定义和函数声明放在头文件，函数、类成员函数定义在源文件。但**实例化模板时，编译器需要知道模板定义**，所以**函数模板、类模板的定义通常放在头文件中**
- 大多数编译错误在实例化时期报告

```java
template <typename T>   // typename有的也写做class，意义相同
.....

template <typename T>
inline T sort(const T&, const T&); // ok

inline template <typename T> T sort(const T&, const T&); // wrong
```
**非类型模板参数**
- 非类型模板参数表示值，而非类型
- 非类型模板参数被用户提供的或者编译器推断的值替代，这些实参值必须是常量表达式
- 非类型参数可以是整型（实参必须是常量表达式），指向对象或函数类型的指针、左值引用（实参必须具有静态生存期（局外变量、静态变量、栈））

##### 类模板
- 类的作用域包括：类定义中，源文件类成员函数的函数体内(`{}`之内)
- 类的作用域中，编译器处理模板自身引用时可以不带类型名

```java
template <typename T>
void Blob<T>::check (const T& t1, const T& t2) {
    // ......
}

// 类作用域中
Blob<T>& func();  // ok
Blob& func(); // ok
// 之外
Blob& func {   // wrong
    Blob ret = *this; // ok, in scope
	...
	return ret;
}
```
###### 类模板和友元
1. **如果类模板包含非模板友元，则该友元可以访问所有模板实例**
2. **如果类模板包含模板友元，类可以授权给所有模板实例，也可以只授权给特定实例**

```java
template <typename T>
class A {
friend B<T>;  // 授权给特定实例，要求类型相同
friend C<F>;  // 授权给所有模板实例
}
```

**模板类型别名**
```java
typedef Blob<string> strBlob;
// 为类模板定义一个类型别名
template<typename T> using twin = pair<T, T>;
twin<int> p;  // 定义类型为<int, int>类型

// 可以固定一个、多个模板参数
template<typename T> using partNo = pair<T, unsigned>;
```
**静态成员**
- 模板的`static`成员也定义成模板，每个模板的实例都可以有一个自己的静态成员
- `template<typename T> size_t Foo<T>::ctr = 0;`
- 通过引用特定实例、作用域运算符访问成员`Foo<int>::ctr;`

###### 模板参数
- 模板内不能重用模板参数名
- 模板声明必须包含模板参数
- 使用模板类型参数的类型成员，必须通过关键字typename(class不行)显式地告诉编译器该名字是一个类型

```java
T::size_type *p; // 可以是定义指向size_type类型的指针，也可以是T的静态成员乘以p的结果

typename T::size_type *p; // 定义指向size_type类型的指针
```

###### 成员模板
- 成员模板不能是虚函数
- 实例化类模板的成员模板，必须同时提供类和函数模板的实参`Blob<int> a1(vi.begin(), vi.end());`

```java
class Blob {
template<typename T> void func(const T&);
}
string s = "hello";
Blob b;
b.func(s);
```

---

```java
template<typename T> class Blob {
template<typename F> Blob(const F&);
}
string s = "hello";
Blob<int> b(s);
```
###### 控制实例化
- 模板在使用时才会实例化，多个文件中的模板实例化可能会造成严重额外开销
- 通过显示实例化避免开销，**编译器遇到`extern`模板声明时就不会在本文件中生成实例化代码**
- 类模板的实例化会实例化所有成员（包括内联）（和普通类不同）

```java
extern template declaration; // 实例化声明
template declaration;  // 实例化定义
```

##### 模板实参推断
###### 模板转换
- 如果函数形参使用了模板类型参数，其采用特殊的初始化规则
- 编译器通常不是对实参进行类型转换，而是生成一个新的模板实例，例外在下面
  - const转换，忽略顶层const
  - 数组、函数指针转换（函数形参不能为引用类型）

###### 显式模板实参、`remove_reference`
- 显式模板参数在`<>`中给出，函数名后，参数列表之前
- 显式模板实参按从左向右的顺序与对应的模板参数匹配，尾部的可以忽略

```java
template<typename T1, typename T2, typename T3>
T1 func(T2, T3);  // bad
T1 func<int>(T2, T3); // T1 is int
T1 func<int, string>(T2, T3); // T1 is int, T2 is string

template<typename T1, typename T2, typename T3>
T3 func(T2, T1); // wrong
T3 func<int>(T2, T1); // wrong, T3是int，但不能推断T1、T2
T3 func<int, int, int>(T2, T1); // ok

// 尾后类型的使用
template<typename T>
auto func(T beg, T end) -> decltype(*beg) {
    return *beg;
}

// 上面迭代器返回的是引用，如果希望返回原来类型，如下
template<typename T>
auto func(T beg, T end) -> typename remove_reference<delctype(*beg)>::type {
    return *beg;  // 返回元素的拷贝
}
```
其中，`remove_reference<T&>`将得到原本的T类型，类型由其类型成员`type`表示










