---
title: Cpp Rule Fragment2
date: 2017-03-06 15:28:49
tags: [Cpp]
categories:
---

##### 左右的概念
###### 左值、右值
C++中左值与右值这两概念是从 c 中传承而来的，在 c 中，**左值指的是既能够出现在等号左边也能出现在等号右边的变量(或表达式)，右值指的则是只能出现在等号右边的变量(或表达式)**

**在 C语言中，通常来说有名字的变量就是左值**(如 a, b)，**而由运算操作(加减乘除，函数调用返回值等)所产生的中间结果(没有名字)就是右值**，如 3 + 4， a + b 等。

在 C++ 中，每一个表达式都会产生一个左值，或者右值，相应的，该表达式也就被称作“左值表达式"， "右值表达式"。对于内置的基本数据类型来说，左值右值的概念和 c 没有太多不同，不同的地方在于自定义的类型，具体如下：
- 对于内置的类型，右值是不可被修改的(non-modifiable)，也不可被 const, volatile 所修饰（volatile关键字的作用是防止优化编译器把变量从内存装入CPU寄存器中，保证每次取的值都是内存中值）
- 对于自定义的类型(user-defined types)，右值却允许通过它的成员函数进行修改
2
###### 左值引用、右值引用
- 左值引用，`Type & 左值引用名 = 左值表达式;`
- 声明时必须初始化，初始化之后无法在改变；对别名的一切操作都等价于对原来变量的操作。
- 右值不能赋值给左值引用，加上const限定符即可
- c++中临时变量默认const属性，所以只能传给const引用(延长生命周期)

---

- 右值引用，`Type && 右值引用名 = 右值表达式;`
- 可以直接把左值或者右值转换成右值引用，但转换后原对象就不能使用了

```java
int val = 10;
int & a1 = val+1;  // 错误，此时val+1（中间结果用const型的临时变量保存）等价于右值，右值不能赋值给左值引用
const int& a2 = val+1; // 正确
const int& a3 = 10;  //  正确

int && a4 = std::move(val+1); // 正确
```

#### 动态内存与智能指针
- 智能指针负责自动释放所指向的对象，定义在`memory`头文件中
- 智能指针也是模板，创建智能指针时需要提供类型信息
- 智能指针的使用与普通指针类似
- 包括shared_ptr（允许多个指针指向同一个对象）、unique_ptr（独占所指向的对象）、weak_ptr（指向shared_ptr所指向的对象）

注意事项
- 不用相同的内置指针初始化多个智能指针
- 不delete get函数返回的值
- 不用get返回值初始化/reset另一个智能指针
- 如果智能指针管理的资源不是new分配的资源，需要传给他一个删除器


##### shared_ptr
```java
shared_ptr<T> sp; // 空指针
if (p)   //  如果p指向一个对象则为true
*p
p->mem
p.get()   // 返回p中保存的指针
swap(p, q)  // 交换p和q中的指针
```
**不要将get函数得到的内置指针用于初始化其他智能指针**，可能会导致两个智能指针指向同一个对象，且他们的计数器都为1
以上操作也适用于unique_ptr，下面的操作则是shared_ptr独占：
```java
make_shared<T> (args)  // 返回一个shared_ptr, 指向类型T的动态内存对象，使用args初始化
shared_ptr<T>p(q)   // p是q的拷贝；q中的计数器加一，要求q中的指针必须能转化位T*
p = q    // p,q都是shared_ptr，保存的指针必须能相互转换。p的引用计数器递减，q的递增。若p的引用计数器变为0，则将其管理的资源释放
p.unique()   //  若p.use_count()为1，返回true；否则返回false
p.use_count  // 返回与p共享对象的智能指针个数；一般用于调试
```

```java
auto p1 = new auto(obj); // p指向一个与obj类类型相同的对象，该对象用obj初始化

auto p2 = new auto{a,b,c}; // 错误，括号中只能有单个初始化器

// 内存耗尽时new操作会抛出bad_alloc异常，下面的方法可以避免抛出异常
int *p = new (notthrow) int;   // 内存耗尽时返回空指针

```
- delete空指针没有问题
- delete之后应该重置指针

###### shared_ptr和new
- 可以使用new返回的指针初始化智能指针
- **接受指针参数的智能指针构造函数为explicit**（不准指针隐式转换），必须使用直接初始化形式

```java
shared_ptr<int> p(new int(42));
shared_ptr<int> p1 = new int(42); // 错误，可以使用reset


shared_ptr<T> p(u);  // p从unique_ptr接管对象所有权，将u置空
shared_ptr<T> p(q, d)  // p接管内置指针q所指向的对象，q必须能转换为T*，p使用可调用对象d代替delete
p.reset()   // 若p是唯一指向其对象的shared_ptr，reset释放该对象
p.reset(q)  // 若传递了参数内置指针q，令p指向q，否则将p置空
p.reset(q, d);  // 有d则使用可调用对象代替delete
```

##### unique_ptr
- 一个对象只能有一个unique_ptr，不支持拷贝（除非是返回即将要销毁或局部对象的拷贝）、赋值
- 必须采用直接初始化形式

```java
unique_ptr<T, D> u // D为可调用对象，用来释放内存
unique_ptr<T, D> u(d)   // 用d代替D

u = nullptr  // 释放u指向的对象，将u置空
u.release()  // u交出控制权，返回内置指针，将u置空

u.reset()     // 释放u指向的对象
u.reset(q)   // 提供内置指针q，则令u指向这个对象；否则将u置空
u.reset(nullptr)
```
###### unique_ptr和动态数组
```java
unique_ptr<T[]> u;  // u指向一个动态分配的数组
unique_ptr<T[]> u(p);  // u指向内置指针p指向的动态动态分配的数组，p类型必须能转换为T*
u[i];   // 访问数组
```
shared_ptr没有提供管理动态数组的功能，需要使用需要自己定义删除器。

##### weak_ptr
- 不能控制对象生存周期，指向由shared_ptr管理的对象，切不改变shared_ptr引用计数
- 需要用shared_ptr初始化
- 指向对象可能被释放掉，所以不能直接访问

```java
weak_ptr<T> w(sp);  // 初始化

w = p; // p可以是weak_ptr或shared_ptr，赋值后两者共享对象
w.reset()  // w置空
w.use_count()  // 与w共享对象的shared_ptr的数量
w.expired()     // w.use_count() == 0返回true
w.lock()   // w.expired() 为true返回一个空shared_ptr，否则返回一个与w共享对象的shared_ptr

// 访问
if (shared_ptr<int> np = w.lock()) {  // np不为空成立
    // 使用np访问对象
}
```

##### allocator类
- 定义在memory头文件中，是一个模板
- allocator分配的内存都是未构造的

```java
allocator<T> a;
a.allocate(n);  // 分配一段原始的、未构造的内存，保存n个类型为T的对象
a.deallocate(p, n);  // 释放从T*类型的指针p开始的内存，这块内存保存了n个T类型对象；p必须是由allocate函数返回的指针，n必须是p创建时要求的大小。调用之前，必须对这n个T对象调用destory

a.construct(p, args); // p必须是类型为T*的指针，指向一块原始内存，args被传递给类型为T的构造函数，用来在p指向的内存中构造一个对象
a.destory(p)  // 对p指向的对象指向析构函数
```

###### 构造、填充未初始化内存的算法
```java
uninitialized_copy(b, e, b2);  // 拷贝迭代器b、e指定范围元素到b2指定的未构造的原始内存中，b2指向的内存必须足够大
uninitialized_copy_n(b, n, b2); // 从b开始，n个元素

uninitialized_fill(b, e, t);  // 拷贝值均为t
uninitialized_fill_n(b, n, t);

// 这几个算法都返回下一个未初始化的内存位置
```

#### 拷贝控制
##### 拷贝、赋值与销毁
###### 拷贝构造函数
- 成员类型决定拷贝方式，内置类型直接拷贝，类类型需要拷贝构造函数来拷贝
- 不应该是explicit的
- 参数是自身类类型的引用
- 编译器会为我们定义一个（如果我们没有定义）

**拷贝初始化发生的时间不仅在用=定义变量时，也会发生在**：
1. 将对象作为实参传递给非引用类型的形参
2. 从返回非引用类型的函数返回一个对象
3. 用花括号列表初始化一个数组中的元素或一个聚合类中的成员

###### 拷贝赋值运算符
- 编译器会为我们定义一个（如果我们没有定义）

###### 析构函数
- 编译器会为我们定义一个（如果我们没有定义）
- 一般为空，成员是在析构函数体之后隐含的析构阶段被销毁的
- 某些类中，析构函数也被用来阻止该类型的对象被销毁
- 需要析构函数的类也需要拷贝、赋值操作

###### 使用`=default`
- 将拷贝控制成员定义为`=default`可以显式地要求编译器生成合成的版本
- 类内使用`=default'修饰的成员将隐式地声明为内联的
- 如果不希望内联，则只对类外的定义使用`=default`。

###### 阻止拷贝
- 在函数第一次声明后面写上`=delete`表示**删除的函数**，不希望定义这些成员
- 拷贝构造函数、拷贝赋值运算符定义为删除的函数可以阻止拷贝
- 析构函数不能是删除的成员，因为存在对象无法销毁的问题
- 但如果你真的这么干了：如果一个类有数据成员不能默认构造、拷贝、复制、销毁，则对应的成员函数将被定义为删除的

##### 动态内存管理类
- 在运行时分配可变大小内存的空间
- 以vector为例，添加元素的成员函数检查是否有更多空间，没有则申请新的空间，**将已有元素移到新空间**，释放旧空间，添加新元素

##### 移动构造函数和std::move
- 移动构造函数通常是将资源从给定对象“移动”而不是拷贝到正在创建的对象
- 调用标准库函数move（utility头文件）表示希望使用移动构造函数

###### 右值引用
- **右值引用是指必须绑定到右值的引用**，通过`&&`获得
- 右值引用只能绑定到将要销毁的对象，因此可以将一个将要销毁的资源移动到另一个对象中
- 左值引用不能绑定到要求转换的表达式、字面常量、返回右值的表达式（变量是左值）
- 右值引用有相反的要求；一般右值生命周期短（字面常量、临时对象等）
- 通过move函数显式地将左值转换为对应的右值引用类型，使用move不用using声明，直接用`std::move`
- 右值引用做形参时不能为const，因为需要窃取他的数据

```java
int &&r1 = 42; // correct
int &&r2 = r1;  // wrong, 变量表达式r1是左值
// 调用move后，意味着除了对r1赋值、销毁外，将不再使用它
int &&r3 = std::move(r1); // ok
```

##### 移动构造函数、移动赋值运算符
- 移动构造函数的**第一个参数是该类型的一个右值引用**
- 必须确保移动后，源对象处于销毁无害的状态，也就是说**源对象必须不再指向被移动的资源**（指针置为nullptr，因为源对象可以被销毁，如果它的指针还指向被移动的资源，执行析构函数时就会将被移动的资源释放）
- 移动操作**通常**不抛出异常。编写不抛出异常的移动操作，应该使用`noexcept`通知标准库，免去其为了处理可能存在的异常做的额外工作（可能出现异常的还是不要写比较好）
- `noexcept`出现在参数列表之后；如果是构造函数，其在初始化列表的`:`之前

```java
A::A(A &&a) noexcept : x(a.x), y(x.y) {
    a.x = a.y = nullptr;
}

A &A::operator=(A && a) noexcept {
    if (this == &a) return *this;  // 自赋值
    free();   // 释放现在对象的资源
    x = a.x;
    y = a.y;
    a.x = a.y = nullptr;  // 重置源对象的指针
    return *this;
}
```

- **只有当一个类没有定义任何自己版本的拷贝控制成员，且类的每个非`static`数据成员都可以移动时，编译器才会为它合成移动构造函数或移动赋值运算符。编译器可以移动内置类型的成员；也可以移动有对应移动操作的类成员**
- 移到构造函数永远不会隐式地定义为删除的函数（delete）
- 如果显式要求编译器生成`=default`的移动操作，但编译器不能移动所有成员，则编译器将移动操作定义为删除的
- 类本身的析构函数为删除的、不可访问的，则其移动构造函数为删除的
- 如果类成员是const的或者是引用，则类的移动赋值运算符定义为删除的

```java
struct X {
    int i;               // 内置成员可以移动
    std::string s;   //  string有自己的移动操作
};
struct Y {
    X mem;     // X有合成移动操作
};

X x1, x = std::move(x1);   // 合成移动构造函数
Y y1, y = std::move(y1);   // 使用合成移动构造函数
```

- 既有拷贝构造函数也有移动构造函数时，遵循**移动右值，拷贝左值**的方法
- 没有移动构造函数时，右值也被拷贝

```java
A  a1, a2;
a1 = a2;  // a2是左值，使用拷贝
A getA(istream& is);  // 函数getA返回一个右值
a2 = getA();      // 返回右值，使用移动赋值
```

###### 移动迭代器
- 一般的迭代器解引用操作返回一个指向元素的左值，**移动迭代器的解引用操作生成一个右值引用**
- 调用`make_move_iterator`将一个普通迭代器转化为一个移动迭代器，原迭代器的所有操作在移动迭代器中都正常工作

```java
auto first = alloc.allocate(new_capacity);
// 使用移动构造函数来构造每个元素
auto last = uninitialized_copy(make_move_iterator(begin()), make_move_iterator(end()), first);
```

###### 右值、左值引用成员函数、重载和引用函数
- 类成员函数的参数列表后可以放置`&`或`&&`，称为引用限定符
- 引用限定符指出`this`可以指向一个左值或右值
- 引用限定符只能用在非static成员函数中（类似const限定符），且必须在声明、定义中都出现
- **引用限定符就是限制调用成员函数的对象有引用限定**
- `&`限定的函数，只能将这个函数用于左值；`&&`则只能用于右值
- 同时有const限定符的函数，引用限定符应该在const限定符之后`const &`
- 引用限定符可以区分重载版本（const也可以），表示其对象是右值还是左值
- 定义两个及以上具有相同名字和参数列表的函数，就必须对所有函数加上引用限定符，或者所有都不加。（有的加，有的不加不行）

**右值执行排序，可以直接进行，因为右值没有其他用户，可以改变；但是，对const右值、左值进行排序时，不能改变对象，所以先拷贝再排序。**


#### 重载运算与类型转换
- 运算符作用域内置类型的运算对象时，运算符的含义无法改变（不能重载）
- 只能重载已有的运算符
- 不能被重载的运算符包括`::        .*        .        ?: `
- 下标运算符`[]`返回的是元素的引用

##### 输入输出运算符
- 输入、输出运算符必须是非成员函数
- 一般地，重载输出运算符`<<`函数的第一个参数是一个非常量`ostream`对象引用（非常量是因为向流写入内容会改变其状态，引用是因为ostream不能拷贝），第二个参数一般是要打印对象的常量引用；函数返回ostream的形参
- 重载输入运算符函数的第二个参数**非常量对象的引用**，返回istream的形参
- 重载输入运算符要处理可能失败的情况，输出则不需要

```java
ostream& operator<<(ostream& os, const A& a) {
    // ...
    return os;
}

istream& operator>>(istream& is, A& a) {
    // .... 包括处理失败情况
    return is;
}
```

##### 递增递减运算符
- 区分前置、后置的办法是：**后置版本有一个不被使用的int类型形参**
- 后置版本需要先记录对象的状态，操作完成后返回之前记录的状态
- **后置运算符返回对象的原值**，不是引用
- 显式调用后置运算符需要多加一个参数: `a.operator++(0);`

```java
A& operator++();    // 前置
A operator++(int);  // 后置，有形参，返回原值

A A::operator++() {
    A ret = *this;
    ++*this;
    return ret; // 返回之前的记录
}
```

##### 成员访问运算符
- 包括解引用`*`和箭头运算符`->`两种
- `->`必须是类成员，解引用通常是类成员


```java
string& operator*() const {
    // 检查curr是否在有效范围内，如果是，返回curr所知元素的引用
    auto p = check(curr, "dereference past end");
    return (*p)[curr];          // *p是对象所指的vector
}

string * operator->() const{
    // 将工作委托给解引用运算符
    return & this->operator*();
}
```

##### 函数调用运算符
- 重载函数调用运算符就可以向调用函数一样使用类对象
- 由于可以像使用函数对象那样使用，重载调用运算符可以替代lambda表达式


```java
struct absInt() {
    int operator()(int val) const {   // 注意参数放在后面的括号里
        return val<0? -val:val;
    }
}
absInt ai;
ai(-10);  // 返回10


stable_sort(words.begin(), words.end(), [](const string& s1, const string& s2){return s1.size < s2.size()};);
// 类似于
class short_string {
public:
    bool operator()(const string& s1, const string& s2) const{
        return s1.size < s2.size();
    }
}
// short_string()构造一个对象，由于重载了调用运算符，就可以看作"可调用对象"使用
stable_sort(words.begin(), words.end(), short_string());
```

###### 标准库定义的函数对象
标准库定义了一组表示算术运算符、关系运算符和逻辑运算符的类，每个类分别定义了一个执行命名操作的调用运算符（所以其对象也可以被“调用”）。

| 算术 | 关系 |逻辑|
|--------|--------|
|   plus<T>     |    equal_to<T>    |    logical_and<T>     |
|  minus<T>   |     not_equal_to<T>    |   logical_or<T>     |
|    multiplies<T>    |   greater<T>     |    logical_not<T>     |
|    divides<T>    |    greater_equal<T>    |         |
|    modules<T>    |    less<T>    |         |
|    megate<T>    |    less_equal<T>    |         |

```java
plus<int> intadd;
intadd(10, 15);  // 25

negate<int> intnegate;
intnegate(10);  // -10
intnegate(intadd(10,15));  // -25

sort(vec.begin(), vec.end(), greater<string>());
// 如果vector里面是string*也照样可以
sort(vec.begin(), vec.end(), greater<string*>());
```

###### 可调用对象与function
C++中的可调用对象包括：**函数、函数指针、lambda表达式、bind创建的对象、重载了调用运算符的类**

- function类型定义在`functional`头文件中，是一个模板

```java
function<T> f;  // f是用来存储可调用对象的空的function，T限定函数类型（T就是`返回值 (各个参数)`）
function<T> f(nullptr);  //  显式构造一个空的function
function<T> f(obj);  // f中存储可调用对象obj的副本
f                               // f中有可调用对象为真，否则为假
f(args);                    // 调用f中的对象，args是参数

// 定义为function<T>的成员类型
result_type       // 可调用对象的返回类型
argument_type // T一个实参时，实参的类型
first_argument_type, second_argument_type
```
使用示例
```java
function<int(int, int)> f1 = add;    // 函数指针
function<int(int, int)> f2 = divide(); // 重载了调用运算符的类的对象
function<int(int, int)> f3 = [](int i, int j) {return i+j;};  // lambda表达式

f1(3,4);
f2(3,4);
f3(3,4);
```

##### 重载、类型转换与运算符
- 可以通过定义类类型转换运算符达到类类型转换的效果
- 转换构造函数和类型转换运算符共同定义了类类型转换

###### 类型转换运算符
- **类型转换运算符是类成员函数**
- 可以面向除了`void*`之外的任意类型进行定义，只要该类型能作为函数的返回类型（数组、函数类型就不行）
- 一般形式`operator type() const`
- 类型转换运算符是**隐式执行**的，没有形参，不能传递实参，不能指定返回类型
- 可能产生意外结果

```java
class smallInt {
public:
    smallInt(int i=0) : val(i) {
        if (i<0 || i>255) throw std::out_of_range("Invalid value");
    }
    operator int() const {return val;}
    int operator int() const; // wrong，不能有返回类型
    operator int(int = 0) const; // wrong，不能有形式参数

private:
    std::size_t val;
}
smallInt si;
si = 4;  // 先将4隐式转换为smallInt，再调用赋值运算符
si+3;    // 先将si隐式转换为int，再执行整数加法

smallInt s = 3.14;  // 内置类型转换double->int，再调用smallInt(int)构造
s+3.14                // smallInt先转成int，内置类型再将int转换成double

```
由于隐式转换可能会带来意想不到的结果，所以有时候需要使用**显式的类型转换运算符**。定义显式类型转换运算符只需要加上`explicit`即可，但转换时就行必须使用显式的强制转换方式。
**有一个例外：当表达式被用作条件判断（`if, while, do, for, &&, ||, !, ?:`），编译器会将显式的类型转换自动用于它，也就是会隐式执行**
```java
explicit operator int() const {return val;}  // 改变的类型转换运算符

smallInt si = 3; // ok
si+3                 // wrong，此处需要隐式转换，但转换函数是显式的
static_cast<int>(si) + 3  // 显示请求转换
```

IO类型可以向void*转换，C++11下支持将IO类型向bool显式类型转换，IO类型向bool的转换一般定义成显式（explicit），因为通常用在条件判断部分，所以也可以隐式执行。

###### 二义性问题
二义性类型转换的途径
- 两个类提供了相同的类型转换（分别通过构造函数和类型转换运算符）
- 定义了多个转换规则，这些转换**涉及的类型本身可以通过其他类型转换联系在一起**

```java
struct A {
    A(int = 0); // 最好不要创建两个转换源都是算术类型的类型转换
    A(double);
    operator int() const;  // 最好不要创建两个转换对象都是算术类型的类型转换
    operator double() const;
    // other member
}
void f2(long double);

A a;
f2(a);  // 二义性错误，两个类型转换函数都可以

long lg;
A a2(lg);  // 二义性，编译器无法区分long转int和double的好坏

short s = 42;
A a3(s);  //ok, 使用A::A(int)
```
但是short转int确实比short转double好

**重载函数于转换构造函数**
- 如果两个或多个类型的转换都提供了同一种可行的匹配，则这些类型转换一样好
- **即使其中一个能精确匹配，另一个需要额外的标准类型转换，编译器也会将其表示为二义性错误**

```java
struct C {
    C(int);
    ...
}
struct D {
    D(ing);
    ...
}

void f(const C&);
void f(const D&)
f(10);  //二义性

// ---------------------------------分割线----------------------------------

struct E {
    E(double);
    ...
}
void f(const C&);
void f(const E&);
f(10);  // 依旧二义性错误，即使其中一个能精确匹配，另一个需要额外的标准类型转换，编译器也会将其表示为二义性错误
```

函数匹配与重载运算符
- 表达式中运算符的候选函数集包括成员函数和非成员函数
- **如果对同一个类既提供了转换目标是算术类型的类型转换，也提供了重载的运算符，则将会遇到重载运算符与内置运算符的二义性**

```java
class A {
friend A operator+(const A& a, const A& b);
public:
    A(int = 0);
    operator int() const {return val};
private:
    size_t val;
}

A a1, a2;
A a3 = s1 + s2;  // 使用重载的operator+
int i = s3 + 1;    //  二义性错误
```

#### 面向对象程序设计 OOP
- OOP的核心思想是**数据抽象、继承和动态绑定**

##### 基类与派生类（父类与子类）
- 子类经常覆盖父类中的虚函数，如果不覆盖，子类将直接继承父类的版本
- 能把子类对象当成父类对象来用，也能把父类的指针或引用绑定到子类对象的父类部分上
- 子类构造函数先初始化父类部分，然后按照声明顺序依次初始化子类成员
- **派生类可以访问基类的公有和受保护成员**

---

- 基类中的静态成员在整个继承体系中都只存在该成员的唯一定义，如果是private的，派生类就不能访问
- **声明派生类时不能加上派生列表**
- 派生类一定要有定义，类不能派生自己
- 使用final关键字可以禁止类被继承

```java
class father {};
class A final : public father {};  // ok, 但A不能被继承
class B : public A{};  // 错误，A是final的
```

- 派生类向基类的自动类型转换只对指针、引用类型有效
- 用派生类对象为基类对象初始化或者赋值时，其派生类独有的部分会被忽略

##### 虚函数
- 运行时动态绑定
- 所有虚函数都必须有定义
- 派生类中的虚函数可以不加`virtual`关键字，因为一旦某个函数被声明为虚函数，他在所有派生类中都是虚函数
- 覆盖基类虚函数的派生类函数必须在形参上与派生类完全一致
- `override`关键字用来说明派生类中的虚函数
- `final`关键字阻止函数派生类覆盖此函数
- 如果虚函数使用默认实参，实参由本次调用的静态类型决定（使用基类的指针就用基类的虚函数默认实参），所以最好定义派生类、基类虚函数的默认实参一致
- 回避虚函数机制，可使用作用域运算符机制

```java
class A {
virtual void f1() const;
};
class B : A {
virtual void f1() const final;  // 不允许后续的其他类覆盖f1
};

A * a = new B();
a->f1();  // 调用B类中的虚函数f1
a->A::f1();  // 无论a类型是什么，都是用A中的虚函数f1
```

##### 抽象基类
- 抽象基类负责定义接口，不能直接创建其对象

###### 纯虚函数
- 在函数声明加上`=0`就可以将函数声明为纯虚函数
- 纯虚函数无需定义，非要定义的话必须在类的外部

##### 访问控制与继承
###### 受保护的成员 protected
- 类的用户不能访问受保护的成员，私有的更不行
- 派生类的成员、友元可访问继承来的protected、public成员，private不行
- **派生类的成员、友元只能通过派生类对象访问基类的受保护成员。派生类无法访问基类对象中的受保护成员**

```class
class base {
protected:
    int mem;
};
class sneak : base {
    friend void get(sneak&);  // 可以通过自身对象访问基类的受保护部分
    friend void get(base&);   // 不能访问基类对象中的受保护成员
    int j; // private
};
void get(sneaky& s){s.j = s.mem = 0;}
void get(base &b) {b.mem = 0;}  // 错误，不能访问
```

- 派生类对其继承而来的成员的访问权限收到两个因素影响：
  - 基类中该成员的访问说明符
  - 派生类的派生列表中的访问说明符
- **派生访问说明符对于派生类的成员及其友元能否访问直接基类的成员没什么影响**，**其对基类成员的访问权限只与基类中的访问说明符有关**
- **派生访问说明符的目的是控制派生类用户（包括派生类的派生类）对于基类成员的访问权限**
  - 如果继承是公有的，成员遵循原有的访问说明符
  - 如果继承是私有的，则所有对象都是私有的
  - 如果继承是protected的，原本public的称为protected的

---

**派生类向基类转换的可访问性**（假定D继承自B）
- 只有继承方式是public，用户代码才能使用派生类向基类的转换
- 无论以什么方式继承，D的成员和友元都能使用派生类向基类的转换
- 如果D以public或protected方式继承B，则D的派生类的成员和友元可以使用D向B的转换
- 要改变个别成员的可访问性，可使用`using`关键字

```java
class base {
protected:
    int mem, n;
};
class derived : private base{
public:
    using base::mem;
protect:
    using base::n;
};
```

---

友元与继承
- 友元关系不能继承

##### 继承中的类作用域
- 先名字查找再类型检查（p->mem(), obj.mem()）
  1. 确定p的静态类型，因为调用的是成员，该类型必然是类类型
  2. 在p的静态类型对应的类中查找mem，找不到则直接基类中查找直到继承链最顶端。还是找不到就报错
  3. 一旦找到mem，就进行常规的类型检查以确认本次调用是否合法
  4. 如果调用合法，则编译器将根据调用的是否是虚函数产生不同的代码
- 内层作用域的函数不会重载声明在外层作用域的函数
- 名字查找过程中，**派生类会隐藏基类的同名成员（即使形参列表不一样）**

```java
class base {
int f();
};
class derived : private base{
int f(int);  // 隐藏了基类的f()
};

base b; derived d;
d.f(10);  // ok
d.f();      // wrong，参数列表为空的f函数被隐藏了
```

##### 拷贝函数与拷贝控制
###### 虚析构函数
- 派生类会继承基类析构函数的虚属性
- 基类虚析构函数能保证delete基类指针时使用正确的析构函数版本
- 定义了虚析构函数的类，编译器就不会为其合成移动操作

###### 派生类中删除的拷贝控制与基类的关系
- 基类中的默认构造函数、拷贝构造函数、拷贝赋值运算符或析构函数是被删除的或不可访问的，则派生类中对应的成员将是删除的
- 基类中的析构函数是不可访问或删除的，那么派生类中的合成的默认和拷贝构造函数都是删除的
- 基类中对应操作是删除的，派生类中的也会是删除的（比如说移动构造函数）

###### 移动操作与继承
- 带有虚析构函数的类，编译器不会为其合成移动操作，所以其子类也没有
- 确实需要移动操作时，可以显式地定义（可以使用合成版本）

```java
class A {
public:
    A() = default;   // 默认构造
    A(const A&) = default;   // 拷贝构造
    A(A&&) = default;        // 移动构造
    A& operator=(const A&) = default;   // 拷贝赋值
    A& operator=(A&&) = default;        // 移动赋值
    virtual ~A();
    // ......
}
```

###### 派生类的拷贝控制
- 派生类在拷贝、移动的同时要拷贝、移动基类部分(显式地)
- 派生类赋值运算符的处理方法也类似
- 派生类的析构函数只负责销毁派生类自己分配的资源

```java
class base {};
class D : private base{
    D(const D& d) : base(d), /*D的成员初始值*/ {...} // d作为参数将被绑定到类型为base&的实参上
    D(D&& d) : base(std::move(d)), /*D的成员初始值*/ {...}
};

D& D::operator= (const D& d) {
    base::operator=(d);  // 为基类部分赋值
    // 酌情处理自赋值、释放已有资源
    return *this;
}
```

###### 在构造函数和虚构函数中调用虚函数
- **如果构造函数或析构函数调用了某个虚函数，则程序会执行与调用构造函数或析构函数所属类型相对应的虚函数版本**
- 这个例子：创建派生类对象时，先调用基类的构造函数，此时对象的派生类部分是未被初始化的，调用派生类的虚函数存在风险，所以应该调用基类的虚函数。

###### 继承的构造函数
- 一个类可以继承其直接基类的构造函数
- 类不能继承默认、移动、拷贝构造函数
- 继承方式是使用`using base::base;`就可以继承base的构造函数，对于基类的构造函数，编译器将会为派生类与之对应的派生类版本`derived(params) : base(args) {}`
- 构造函数的using声明不会改变该构造函数的访问级别（私有还是私有，公有还是共有）
- 当基类构造函数有默认实参，派生类将获得多个构造函数，每个构造函数省略掉一个含有默认实参的形参
- 派生类不继承某些构造函数的原因可能是：
  - 派生类自己定义了有相同参数列表的构造函数
  - 默认、移动、拷贝构造函数按照正常规则被合成

###### 容器与继承
- 不能把具有继承关系的对象放在一个容器中
- 在容器中放置（智能）指针而非对象
- 派生类的（智能）指针可以隐式转换为基类的（智能）指针

```java
vector<shared_ptr<quote>> basket;
basket.push_back(make_shared<quote>("00001", 50));
basket.push_back(make_shared<derived_quote>("972719", 35, 21, 7));
```

##### 多重继承与虚继承
###### 多重继承
- 每个基类包含一个可选的访问说明符
- 关键字`class`的默认访问说明符是`private`，`struct`的默认访问说明符是`public`
- 派生类的对象包含每个基类的子对象，派生类的构造函数初始值只能初始化它的直接基类
- **基类的构造顺序与派生列表中的基类出现的顺序一致**
- 多重构造在析构时，顺序与构造时相反，派生类的析构函数只负责销毁自己的部分
- 派生列表中，同一个基类只能出现一次

**多重继承构造函数的继承**
- C++11中允许派生类从他的基类中继承构造函数
- 如果继承的多个构造函数相同（形参列表完全相同），程序产生错误
- 如果不想上述错误出现，这个类必须为该构造函数定义它自己的版本

```java
struct base1 {
    base1() = default;
    base1(const string&);
};
struct base2 {
base2() = default;
base2(const string&);
};
// D1尝试继承两个基类中的参数为 const string& 的构造函数
struct D1 : public base1, public base2 {
    using base1::base1;  // 继承base1
    using base2::base2;  // 继承base2
};

struct D2 : public base1, public base2 {
    using base1::base1;  // 继承base1
    using base2::base2;  // 继承base2
    // 定义自己的 参数为 const string& 的构造函数
    D2(const string& s) : base1(s), base2(s);
    D2() = default;  // 一旦D2定义了自己的构造函数，就必须出现这个
};
```
###### 类型转换与多个基类
- 可以使某个可访问的基类的指针、引用直接指向一个派生类的对象
- 编译器认为基类们向派生类的转换不分优劣，因此可能会产生二义性错误

###### 虚继承
- 派生类可能通过直接基类间接继承自同一个间接基类，所以派生类对象会包含两份间接基类的对象
- 虚继承可以解决上述问题，**其目的是令某个类作出声明，承诺愿意共享它的基类**
- 共享的基类称为虚基类
- **含有虚基类的对象构造顺序：虚基类总是先于非虚基类构造**
- 先虚：虚子对象按照他们在派生列表中出现的顺序从左向右出现，然后才是非虚对象从左向右

```java
// base是D1、D2的虚基类
class D1 : public virtual base {};
class D2 : virtual public base {};
```

    class Character {};
    class BookCharacter : public Character{};
    class ZooAnimal {};
    class Bear : public ZooAnimal{};
    class ToyAnimal{};
    class TeddyBear : public BookCharacter, public Bear, public virtual ToyAnimal{};
    // 构造TeddyBear时，构造顺序如下：
    ZooAnimal();
    ToyAnimal();
    Character();
    BookCharacter();
    Bear();
    TeddyBear();


#### 标准库特殊设施
##### bitset类
`#include <bitset>`

###### 定义与初始化

| 函数 | 解释 |
|--------|--------|
|    `bitset<n> b`    |   ` b有n位，每一位均是0。此构造函数为constexpr`    |
| `bitset<n> b(u)` |  `b是unsigned long long值u的低n位的拷贝，如果u没有n位，则补0。此构造函数为constexpr`   |
| `bitset<n> b(s, pos, m, zero, one)` |  `explicit型。从string s的pos（默认为0）位置开始的m（默认为string::npos）个字符，s中只能包含zero（默认'0'）和one（默认'1'）`   |
| `bitset<n> b(cp, pos, m, zero, one)` |  `explicit型。从字符数组cp的pos（默认为0）位置开始的m（默认为string::npos）个字符，cp中只能包含zero（默认'0'）和one（默认'1'）`   |

###### 操作
| 函数 | 解释 | 函数 | 解释 |
|--------|--------|--------|--------|
|  `b.any()`  |  `b中是否有为1的二进制位`   |  `b.all()`  |   `是否所有的位置都为1`  |
|  `b.none()`  |  `b中是否所有的位置都为0`   |  `b.count()`  |  `b中1的个数`   |
|  `b.size()`  |  `b中位数总和，constexpr型`   |  `b.test(pos)`  |  `pos位位1：true，否则false`   |
|  `b.set(pos, v)`  |  `将pos位置为v(默认true是1)，不带参数pos则设置所有位`   |  `b.reset(pos)`  | ` 将pos复位，没有pos则全部复位`   |
|  `b.flip(pos)`  |  `反转pos位或者全部反转`   |  `b[pos]`  |  `访问pos位置，如果b是const的，返回true/false布尔值`   |
|  `b.to_ulong()`  |  `返回b对应的unsigned long值，放不下则抛出异常`   |  `b.to_ullong()`  |   `返回b对应的unsigned long long值，放不下则抛出异常`  |
|  `b.to_string(zero, one)`  |  `将b转换成'0','1'组成的string类型`   |  `os<<b`  |  `打印b中的01流`   |
|  `is>>b`  |  `从is读入字符存入b，当下一个字符不是'0','1'或是已经到达b.size()时停止`   |   |     |

##### 随机数
`#include <random.h>`
###### 随机数引擎类和随机数分布
随机数引擎是函数对象类，定义了调用运算符，该运算符不接收参数并返回一个随机unsigned整数
```java
default_random_engine e;
e();
```
随机数引擎操作如下：

| 操作 | 解释 |
|--------|--------|
|    `Engine e`    |    `默认构造函数，使用默认种子`    |
|    `Engine e(s)`    |    `使用整型值s作为种子`    |
|    `e.seed(s)`    |    `使用种子s重置e的状态`    |
|    `e.min()`    |    `此引擎可生成的最小值`    |
|    `e.max()`    |    `最大值`    |
|    `Engine::result_type`    |    `此引擎生成的unsigned整型类型`    |
|    `e.discard(u)`    |    `将引擎推进u步，u的类型位uul`    |

为了得到一个指定范围内的数，使用一个分布类型的对象
```java
// 0-9之间的均匀分布
// u是一个调用运算符，接受一个随机数引擎作为参数
unifrom_int_distribution<unsigned> u(0, 9);
default_random_engine e;
cout << u(e) << endl;
```

###### 其他随机数分布
- 使用`uniform_real_distribution<double>`类型的对象生成随机浮点数，用法类似上面
- `uniform_real_distribution<>`默认为`double`类型
- 高斯分布：`normal_distribution<> n(u, sigma);` // 均值为`u`，标准差为`sigma`
- `lround(a)`函数对`a`进行四舍五入转化为整数，来自头文件`cmath`
- `bernoulli_distribution b(p)`一次成功概率为`p`。它不是模板类（没有`<>`）



