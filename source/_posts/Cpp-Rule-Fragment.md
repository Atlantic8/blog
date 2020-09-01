---
title: Cpp Rule Fragment
date: 2017-02-23 08:50:23
tags: [Cpp]
categories: Dev
---

#### 变量和基本类型
##### 初始化
###### 列表初始化
C++11中，一下初始化方法都是成立的
```java
int x = 0;
int x = {0};
int x{0};
int x(0);
```
使用花括号初始化变量在C++11中得到全面应用，但是用于内置类型的变量时，使用花括号初始化形式有个重要的特点：

    使用列表初始化且初始化存在丢失信息的风险，编译器将报错

比如

```java
double db = 3.141592653;
int x{db};              // 错误，转换存在丢失信息的风险
int y(db);              // 正确，转换执行，丢失部分信息
```

###### 默认初始化
如果内置类型的变量未被显示初始化，它的值由定义的位置决定。**定义与任何函数体之外的变量初始化为0，定义于函数体内部的内置类型将不会被初始化**。

##### 定义与声明
- 声明使得名字为程序所知，定义负责创建与名字关联的实体
- 只声明一个变量而非定义它，使用`extern`关键字，不要显示初始化
- 任何包含了显示初始化的声明即成了定义
- 变量只能定义一次，但是可以声明多次

```java
extern int i;     // 声明
int j;            // 声明且定义
extern int k = 2; // 定义
```

##### 复合类型
###### 引用
- 引用必须被初始化，因为引用是要和初始值绑定到一起的
- 引用不能被重新绑定到另一个对象
- 引用不能被绑定到字面值、表达式计算结果
- 引用类型要与绑定对象类型严格匹配，只在极少数情况下有例外
- 因为引用不是对象，所以不能创建引用的引用

```java
int x=10, &y = x, z=20;
&y = z;         // 错误，不能重新绑定
y = z;          // 正确，相当于赋值

int &i = 10;   // 错误
double j = 2.55;
int &k = j;    // 错误，类型不匹配
```

###### 指针
- 指针是一个对象，可以有指针的指针，且无需定义时赋初值
- 指针类型要与其指向对象类型严格匹配，只在极少数情况下有例外

```java
// 生成空指针的方法
int *p1 = nullptr;
int *p2 = 0;
int *p3 = NULL;
```
void*指针
- 可以存放任意对象的地址
- 不能直接操作void*指针指向的对象，因为不知道其类型

##### const
- const对象必须初始化，一旦创建，不能修改
- 利用一个对象去初始化另一个对象，无论他们是不是const都无关紧要，因为拷贝不会改变什么
- 默认情况下，const变量尽在文件内有效
- 多个文件共享的方法：声明、定义都添加extern关键字

```java
// file 1，定义、初始化
extern const int x = getSize();

// file 2，再次声明一下，与file 1中的是同一个
extern const int x;
```

###### const引用
- 不能通过引用改变常量的值
- 初始化常量引用时允许用任意表达式作为初始值，只要表达式结果能转换成引用类型即可
- **允许为一个常量引用绑定非常量对象、字面值，甚至表达式**，非常量不行

```java
int i = 42;
const int &r1 = i; // correct
const int &r2 = 42; // correct
const int &r3 = r1*2; // correct
int &r4 = r1*2;     // 错误，r4是非常量引用
```

###### 指针和const
**指向常量的指针**
- **允许指向常量的指针指向非常量对象**
- 常量对象的地址只能存在指向常量的指针里

**常量指针**
- 常量指针是常量，必须初始化，且一旦初始化就不能改变，但其指向的对象可以被改变

**顶层const**
顶层const表示指针本身是个常量，顶层const表示指针指向一个常量
左为底，右为顶即可分辨
```java
const int k=0; // 这个也是顶层const
```

###### constexpr和常量表达式
- 常量表达式的值不会改变，且在编译时期就能得到结果
- C++11中将变量声明为constexpr类型，由编译器验证变量的值是否为常量表达式
- **声明为constexpr的变量一定是常量，且必须用常量表达式初始化**
- 一个constexpr指针的初始值必须是nullprt或者0，或是存储与某个固定地址（比如全局变量，局部变量不行）中的对象
- constexpr声明的指针，仅对指针有约束，不能约束指向的对象，顶层const

```java
constexpr int * p = nullptr; // p是指向整数的常量指针
```

##### 处理类型
###### 类型别名
**typedef**和**别名声明**
```java
typedef double wage, *p; // wage是double同义词，p相当于double*

using vi = vector;
```
###### auto
- auto定义的变量必须有初始值
- auto可以一次声明多个变量，但是这些变量的初始基本数据类型必须一样
- auto推断的类型与原始类型可能会不太一样，比如**auto会忽略掉顶层const**
- 引用类型也可以是auto，原来初始化规则适用

```java
const int i = 0;
auto a = i;       // a是一个整数，顶层const被忽略
const auto b = i; // b是一个const int

auto &c = i;
auto &d = 42; // 错误
const auto &e = 42; // 正确
```

###### decltype
- decltype的作用是**选择并返回操作数的严格基本类型**
- 如果decltype使用的表达式是一个变量，则decltype返回该变量的类型（包括const和引用）
- 如果表达式内容是解引用，decltype得到引用类型
- 如果**变量名加上了一层或多层括号，就会被当成表达式，会得到引用类型**

```java
const int ci=0, &cj=ci;
decltype(ci) x=0;  // x为const int
decltype(cj) y=x;  // y为const int&，y绑定到x
decltype(cj) z;    // 错误，z是引用，必须初始化

int i=42, *p=&i;
decltype(*p) c;    // 错误，c是int&，必须初始化

decltype(i) m;     // 正确，一个未初始化的int
decltype((i)) n;   // 错误，int& 必须初始化
```


#### 字符串，向量，数组
数组不允许直接拷贝、赋值
##### 字符数组
字符数组可以使用字符串字面值进行初始化，但字符串结尾处还有一个空字符`'\0'`，这个空字符也会被拷贝到数组中去

```java
char a1[] = {'c','+', '+'};         // 长度为3
char a2[] = {'c','+', '+', '\0'};  // 长度为4
char a3[] = "c++";              // 长度为4
char a4[3] = "c++";            // 错误，数组空间不足
```

##### 负载数组声明
```java
int * ptr[10];           // 含义10个整型指针的数组 
int &refs[10]=/*...*/  // 不存在引用的数组
int (*Parray)[10];     // 指向一个10个整型元素数组的指针
int (&arrRef)[10]     // 引用一个10个整型元素数组的指针
```

##### 显式类型转换
###### static_cast
**`static_cast`可以完成任何具有明确定义的类型转换(支持强制转换)，只要不包含底层const**
```java
int i=2,j=1;
double slope = static_cast<double>(j) / i;

void* p = &d;
double *dp = static_cast<double*>(p);
```

###### const_cast
**`const_cast`只能改变运算对象的底层const**，通常用于有函数重载的上下文中
```java
const char *pc;
char *p = const_cast<char*>(pc);

const char *cp;
char *q = static_cast<char*>(cp);  // 错误，static_cast不能转换掉const性质
static_cast<string>(cp);           // 正确，字符串字面值转换成string属性
const<string>(cp);                 // 错误，const_cast只改变常量属性
```

###### reinterpret_cast
**`reinterpret_cast`通常为运算对象的位模式提供较低层次上的重新解释**，容易引发错误
```java
int *ip;
char *cp = reinterpret_cast<char*>(ip); // 虽然转换，但pc所指对象依旧是int型
```


#### 函数
##### 参数传递
- **用实参初始化形参时会忽略掉顶层const，也就是说给形参传递常量对象或者非常量对象都可以**
- 由于顶层const被忽略，只有形参顶层const差异的函数会被当成同一个函数
- **可以使用一个非常量初始化一个底层const对象，但是反过来不行**
- **普通引用必须用同类型的对象初始化**

```java
int func(int i){...}        //
int func(const int i){...}  // 错误，重复定义func

//————————————————————————————————————————————————————————

void reset(int &i){i=0;}

int i=0;
const int ci = i;
string::size_type ctr = 0;
reset(&i);           // 调用形参类型是int*的reset函数
reset(i);            // 调用形参类型是int&的reset函数
reset(&ci);          // 错误，普通引用必须用同类型的对象初始化
reset(ci);           // 错误，普通引用必须用同类型的对象初始化
reset(42);           // 错误，普通引用必须用同类型的对象初始化
reset(ctr);          // 错误，普通引用必须用同类型的对象初始化
```

##### 引用返回左值
- 一般函数的返回值均为右值，但也有返回左值的函数
- 由函数的返回值类型决定，具体来说，**调用一个返回引用的函数得到左值，其他类型为右值**
- **左值可以被赋值，右值不行**
- 如果返回值类型是常量引用，那么就不能赋值了（常量不能修改啊）

```java
char &get_val(string &s, string::size_type ix) { //返回的是引用
    return s[ix];
}
string s("hello world");
get_val(s,3) = 'A';       // 可以对左值进行赋值
```

##### 返回数组指针
普通的数组指针声明如下

    type (*name)[dimension]

返回数组指针的函数形式如下

    type ( *function(parameter_list) ) [dimension]

###### 类型别名
也可以考虑使用类型别名

    typedef int arrT[10];
    using arrT = int[10];
    arrt* func(int i);

###### 尾置返回类型
- 任何函数都可以使用尾置返回类型
- 这种返回方法对复杂的返回类型比较有效
- 尾置返回类型跟在形参列表后面，以`->`开头，在原本返回类型出现的地方加上`auto`

```java
auto func(int i) -> int(*) [10];
```

###### 使用decltype
```java
int odd[] = {1,3,5,7,9};
// decltype(odd) 返回的是数组，需要在加一个*变成指针
decltype(odd) * func(int i) {
    // ...........
    return &odd;
}
```

##### 函数重载
- 重载函数的名字肯定一样，需要形参类型或者数量上有差异
- 仅仅返回值不一样不是重载函数，而是重定义
- **仅有顶层const的差异不构成重载，底层const可以**

```java
int func(const int i);
int func(int i);      // 顶层const，重复定义

int func(const int * i);
int func(int *i);     // 底层const，重载函数，指针换引用也一样
```
###### 作用域
- **如果在内层作用域中声明名字，它将隐藏外层作用域中所有同名的实体**
- 声明在内部作用域的名字可能会是外部作用域中同名的所有重载函数失效（不声明名字就没事）
- 不同的作用域中无法承载函数名

##### 默认语言用途
###### 默认实参
- 默认实参填补函数调用缺少的尾部实参，所以默认形参都在尾部
- 尾部参数没省略时，中间参数不能省略
- 给定作用域中，一个形参只能被赋予一次默认实参
- **局部变量不能成为默认实参**

```java
int screen(sz, sz, char=' ');
int screen(sz, sz, char='*');  // 错误，重复声明
```

###### 函数匹配
- 优先选择精确匹配、最匹配，所谓最匹配要看实参与形参的接近程度
- 有且只有一个函数满足以下条件，则匹配成功
    - 该函数每个函数的匹配都不劣与其他函数需要的匹配
    - 至少有一个实参的匹配优于其他可行函数提供的匹配
- 上面两步检查后没有函数脱颖而出，那么判定为二义性，报错

```java
int f(int, int);
int f(double, double);

f(2,2.5);
```
上面的例子中，对于第一个实参，`f(int,int)`好；对于第二个实参，`f(double,double)`好。最终判断此调用具有二义性，拒绝请求。

实参到形参的类型转换分为几个等级，如下
1. 精确匹配
    - 实参、形参类型相同
    - 实参从数组或函数类型转化成对应的指针
    - 向实参添加顶层const、从实参中删除顶层const
2. 通过const转换实现的匹配（比如创建指向非常量的常量指针、引用）
3. 通过类型提升实现的匹配（short+int=int整型提升）
4. 通过算术类型转换（int转double，所有算术类型转换级别一样）或指针实现的匹配
5. 通过类类型转换实现的匹配

##### inline和constexpr
- inline函数编译时，一般适用于代码量很少的函数
- const是指用于常量表达式的函数，返回类型及所有形参都必须是字面值类型，并且要求有且只有一个return语句
- inline函数和constexpr函数可以多次定义，且通常定义在头文件内

##### 调试帮助
###### assert
assert的用法是`assert(expr);`，如果表达式expr的值为true，assert什么也不做；否则，assert输出信息并终止程序执行。
###### NDEBUG
如果定义了NDEBUG，那么调试模式就关闭了，assert就不能起作用了。此外，NDEBUG也有助于开发者编写自己的调试代码。
```java
#define NDEBUG  // 表示关闭了调试模式

# ifndef NDEBUG  // 没有关闭调试模式
// 。。。。
# endif
```

##### 函数指针
- 函数指针也是指针，可以赋值为nullptr、0等
- 指向不同函数类型的函数指针不存在类型转换
- **定义重载函数指针时，指针类型必须与重载函数中的某一个精确匹配**

```java
bool func(int);
// 定义函数指针
bool (*pf)(int) = func;     // 定义指向函数func的函数指针
bool (*pf)(int) = &func   // 与上面等价
// 使用函数指针
pf(1);
(*pf)(2);

```

**C++中，形参和返回值都不能是函数，但可以是函数指针**，使用类型别名、decltype等可以使得函数指针的声明变得简单
```java
// 等价的两种定义方式，funcp可以使用在函数实参、返回值
typedef bool (*funcp) (int);
typedef decltype(func) *funcp;

// 使用using、尾置返回类型
using pf = bool(*) (int);  // pf是函数指针
pf f1(int);
using f  = bool (int);     // f类型是函数
f *f1(int);                    // 显示指定返回类型是指向函数的指针

auto f1(int) -> bool(*) (int); // 尾置返回类型指定返回类型
decltype(func) *f1(int);        // 知道返回的函数是哪一个更方便
```


#### 类
##### 定义抽象数据类型
###### const成员函数
- const成员函数不能改变调用它的对象的内容

```java
double const_func(int a, int b) const {}

// 返回this对象的函数
// 返回值是引用
New_Class& New_Class::hello () {
    //....
    attribute += 1;
    return *this;
}
New_Class nc;
nc.hello();  // nc的attribute属性已经改变了
```

###### 类相关的非成员函数
- 这里的相关非成员函数包括但不限于`read`、`print`等
- 如果非成员函数是类接口的组成部分，这些函数的声明应当与类在同一个头文件内

```java
// IO类型不能拷贝，所以只能以引用的形式加入形参
// 最后需要返回IO类型的引用
// ostream、print也类似，定义输出函数应该尽量减少对格式的控制
istream &read(istream &is, New_Class &item) {
    is >> item.a1 >> item.a2 >> item.a3;
    return is;
}
// 调用
istream &is;
read(is, *this)
```

###### 构造函数
- **构造函数不能为const**
- **const对象和引用都应该在初始值列表中初始化**
- 初始化列表：成员初始化的顺序与类定义中的顺序一致
- 构造const对象时，知道构造函数完成其初始化过程，对象才能取得其“常量”属性
- 默认构造函数的规则如下：
   - 如果有别的构造函数，编译器不会生成默认构造函数
   - **如果存在类内初始值，用它来初始化成员**
   - 否则，默认初始化（string为""，int块外为0，块内未定义）
- C++11中，如果需要默认行为可以在参数列表之后写上 `=default`要求编译器生成默认构造函数
- **当某个数据成员被构造函数初始值列表忽略时，它将以合成默认构造函数相同的方式隐式初始化**

```java
// 有其他构造函数的情况下，还想要默认构造函数可以这样
New_Class() = default;

// 通过默认参数也等与实现了默认构造函数
New_Class(string s = " "):name(s){}
```

**委托构造函数**就是利用其他构造函数执行自己的初始化过程，其在参数列表初始化位置调用其他构造函数
```java
New_Class() : New_Class("zhangsan"){}
```

###### 隐式类类型转换
- 通过一个实参调用的构造函数定义一条**从构造函数参数类型向类类型隐式转换**的规则
- 只允许一步类类型转换，隐式转换可能会出错
- 抑制隐式转换的方法是在构造函数前加上关键字`explicit`
- 使用`static_cast`这样的显式转换也能达到转换的效果
```java
string lisi = "lisi";
New_Class zhangsan("zhangsan");
// playWith函数的参数类型是New_Class
zhangsan.playWith(lisi);
```


##### 访问控制与封装
- class和struct定义类时的唯一区别就是默认访问权限
- struct默认为public，而class默认为private

###### 友元
- 类中使用`friend`关键字可以使其他类或者函数成为它的友元
- 成为友元的类、函数可以访问当前类的非公有成员
- 友元不是类的成员，不受其所在区域访问控制级别的约束
- 类内友元函数的声明并非普通意义上的声明，所以在其他地方还得声明一次，即便定义在类内部也还要在外面声明
- 友元函数也可以定义在类内部，隐式inline
- **友元关系不存在传递性**

```java
class Class2 {
friend class Class1;
friend istream & read(istream &is, Class2 & c2);
}
```

###### 其他特性
- 定义在类内部的成员函数自动是`inline`类型的
- **`mutable`成员用于不会是const，即使在const成员函数内他也是可以被改变的**
- 返回`*this`的函数返回的是左值引用（返回类型是引用），返回的是对象本身而不是副本

###### 聚合类
- 所有成员都是public
- 没有定义任何构造函数
- **没有类内初始值**
- 没有基类、没有虚函数

```java
struct data {
    int x;
    char c;
    string s;
}
```

##### 类的静态成员
- 静态成员于类本身直接相关
- 静态成员函数不包含this指针、也不能显式、隐式地使用this指针（**不能操作非静态成员**）
- **静态成员函数不能声明成const**
- 在类的外部定义静态成员时，不能重复static关键字
- 静态成员变量应该在类的外部定义
- 静态数据成员可以是不完全类型（类在声明之后、定义之前称为不完全类型）
- 静态成员可以是默认实参，非静态的不可以

```java
class A {
private:
    static A a;  // 正确，静态成员可以使不完全类型
    A b;           // 错误，数据成员必须是完全类型，不过可以定义指针、引用
}
```


#### IO库与容器库
##### string流
`sstream`包含三个支持string读写的类型，分别是`istringstream`、`ostringstream`和`stringstream`。
sstream的使用可以如下
```java
sstream strm;
sstream strm(s); // strm是sstream的对象，保存string s的拷贝

strm.str()           // 返回strm所保存的string的拷贝
strm.str(s)         // copy string s to strm, return void
```
`istringstream`、`ostringstream`的用法也很简单，如下所示
```java
string line("suck my balls"), word;
istringstream is(line);
while (is >> word)
    cout << word << endl;
```
向`ostringstream`对象写入string其实就是将string添加字符。

###### array
- array容器的大小是一定的，其大小也是类型的一部分
- array容器与普通数组不同的是，array支持拷贝与赋值

```java
array<int> arr;  // 错误，缺少大小
array<int, 10> arr1 // 正确

array<int, 3> arr = {0, 1, 2};
array<int, 3> arr1 = arr;  //正确，类型一定要一致
```

###### 顺序容器的操作

    seq.assign(b,e); // 将seq中的元素替换成迭代器b、e所表示范围中的元素
    seq.assign(il);   // 将seq中的元素替换成初始化列表il中的元素，比如il={1,2,3,4}，为值列表
    seq.assign(n,t); // 将seq中的元素替换成n个元素t
    
    c.insert(p, t); // 在迭代器p之前添加元素t，返回添加元素的迭代器
    c.insert(p, n, t); // 在迭代器p之前添加n个元素t，返回第一个添加的元素的迭代器
    c.insert(p, b, e); // 在迭代器p之前添加迭代器b、e之间的元素
    c.insert(p, il);

**向一个vector、string、deque插入元素会使所有的指向容器的迭代器、引用和指针失效**

- `emplace_front, emplace_back, emplace`分别对应`push_front, push_back, insert`
- 这些函数可以构造元素

```java
class person{
public:
    string name;
    int age;
    person(string nm, int ag);
}
c.emplace_front("zhangsan", 10); // 插入10岁的zhangsan的元素
c.push_front("zhangsan", 10); // 错误，没有接受三个参数的push_front版本
c.push_front(person("zhangsan",10)); // 正确，先构造对象
```

顺序容器还支持关系运算符，从头向尾比较，比较直观。
###### swap

    c1.swap(c2);
    swap(c1, c2);

- swap交换元素很快，因为元素本身没有交换，swap只是交换了两个容器的内部数据结构
- array是个例外，swap真正交换元素，所以交换所需时间与元素数目成正比

###### 改变容器大小、容量
**改变size**：size是容器当前大小，采用多退少补的方法
- 函数resize可以改变改变容器大小`resize(n)`，也可以将新添加的元素设置为t `resize(n,t)`
- array不支持

**改变capacity**：capacity是容器的最大容量
- `capacity()`获取容量
- `reserve(n)`分布至少能容纳n个元素的内存空间
- `shrink_to_fit()`将`capacity`减少为`size`大小

###### string的搜索操作
| 函数 | 解释 |
|--------|--------|
|   s.find(args)     |    s中args第一次出现的位置    |
|    s.rfind(args)   |      s中args最后一次出现的位置      |
|    s.find_first_of(args)   |      s中查找args中任何一个字符第一次出现的位置      |
|    s.find_last_of(args)   |      s中查找args中任何一个字符最后一次出现的位置      |
|    s.find_first_not_of(args)   |      s中查找第一个不在args中的字符      |
|    s.find_last_not_of(args)   |      s中查找最后一个不在args中的字符       |

其中`args`的形式为包括（pos默认为0）

    c, pos ：    pos为开始查找的位置，c是一个字符
    s2, pos：    s2是字符串
    cp, pos：    cp是指向c风格的字符串的指针（以'\0'结尾）
    cp, pos, n： n表示只看前n个字符

搜索失败则返回一个名为`string::npos`的static成员，其值初始化为-1.

###### string数制转换
| 函数 | 解释 |
|--------|--------|
|    to_string(val)    |    任何算术类型向string转换    |
|      stoi(s, p, b)       |       string转int，s是字符串               |
|       stol(s, p, b)       |         string转long，b是转换基数（默认为10，十进制）             |
|        stoul(s, p, b)      |        string转unsigned long，p是起始位置             |
|        stoll(s, p, b)      |         string转long long             |
|      stoull(s, p, b)        |         string转unsigned long long             |
|      stof(s, p)       |          string转float，p是起始位置            |
|        stod(s, p)      |           string转double           |
|        stold(s, p)      |          string转long double            |

##### 容器适配器
**适配器是一种机制，能使某种事物的行为看起来像另外一种事物**
标准库中有三个顺序容器适配器，`stack、queue、priority_queue`


#### 泛型算法
- 泛型算法定义在头文件`numeric`中

##### 几个基本的泛型算法
- `find(iter1, iter2, val);` // 元素查找，iter1、iter2迭代器至少查找的范围，val是查找的元素。查找失败返回iter2，否则返回对应的迭代器
- `accumulate(iter1, iter2, sum);`  // 元素累加，执行+运算，sum是和的初值，返回最终的和
- `equal(iter1, iter2, another_iter);`  //  比较两个序列元素是否完全一致，一致返回true。another_iter表示第二个序列的起始迭代器
- `fill(iter1, iter2, val);`  // 将迭代器范围中的每个值置为val
- `fill_n(iter, n, val);`  // 将从iter起的n个元素置为val（必须保证有n个元素）
- `copy(iter1, iter2, another_iter);`  // 将iter1-iter2范围内的元素拷贝到以another_iter起始的位置上，要求another_iter对应的容器大小不能比iter1对应的容器小，返回another_iter的位置迭代器位置
- `replace(iter1, iter2, val, new_val);`  // 迭代器范围内，将所有的val换成 new_val
- `replace_copy(iter1, iter2, new_iter, val, new_val);`  // 保持iter1对应的容器不变，将替换后的结果写入new_iter对应的容器中
- `unique(iter1, iter2);`  // 去重，返回指向不重复区域之后一个位置的迭代器

##### 定制操作
###### lambda表达式

    [捕获列表] (参数列表) -> 返回类型 {函数体};

- lambda可以理解成未命名的inline函数
- 捕获列表：表达式所在函数的局部变量列表，局部变量间以`,`分隔，通常为空。`&`引用捕获，`=`
- 参数列表、返回类型、函数体和普通函数一个意思
- **参数列表和返回类型可以忽略，但捕获列表和函数体必须存在**
- lambda表达式的返回值是一个可调用对象，不接收参数，直接带括号调用。可调用对象包括函数、函数指针、lambda表达式等

```java
auto f = []{return 0;} // f是可调用对象
cout << f() << endl;
```

###### bind函数
- 头文件为`functional`
- 接受一个可调用对象，生成一个新的可调用对象来适应原对象的参数列表
- 可以看成一个通用的函数适配器
- bind在绑定过程中都是采用参数拷贝的方式，所以对于需要引用的类型，可以使用`ref`、`cref`函数表示引用（常量c）

    `auto newCallable = bind(callable, arg_list);`

`arg_list`中可能包含`_n`这样的名字（n是整数），这些是占位符，表示newCallable的参数。`_n`表示第n个参数。
```java
// f是有5个参数的可调用对象
auto g = bind(f, a, b, _2, c, _1);
// 传递给g的参数会被分别绑定到_1、_2位置上
// g(X, Y) 等价于 f(a, b, Y, c, X)

ostream &print(ostream &os, string &s, char c) {
    return os << s << c;
}
for_each(words.begin(), words.end(), bind(print, os, _1, ' '));  // 错误，os不能拷贝
for_each(words.begin(), words.end(), bind(print, ref(os), _1, ' '));  //正确
```

##### 特殊迭代器
###### 插入迭代器
包括`back_inserter, front_inserter, inserter`三种，分别创建使用`push_back, push_front, insert`的迭代器。
使用 `inserter(c, iter)`时，插入元素位置在iter位置之前，并且插入前后，iter指向的元素不变；但是`front_inserter(c)`就一直在容器头部插入。
```java
list<int> lst = {1,2,3,4};
list<int> lst2, lst3;
// 插入后lst2为 4 3 2 1
copy(lst.begin(), lst.end(), front_inserter(lst2));
// 插入后lst3为 1 2 3 4
copy(lst.begin(), lst.end(), inserter(lst3, lst3.begin()));
```
###### iostream迭代器
- 使用流迭代器，必须指定读写对象的类型
- istream_iterator迭代器要读取的内容必须定义了`>>`运算符，ostream_iterator迭代器要读取的内容必须定义了`<<`运算符
- 默认初始化istream_iterator迭代器，创建一个当作尾后值使用的迭代器
- 流迭代器不支持递减`--`操作
- istream_iterator迭代器支持`++, *, ->, ==,  !=`运算符
- ostream_iterator迭代器支持`++, =,  *`运算符

```java
istream_iterator<T> in(is);  // 迭代器对象in从输入流is中读取类型为T的值
istream_iterator<T> eof;     // 尾后迭代器
vector<T> vec(in, eof);  // 从迭代器范围构造vector对象
accumulate(in, eof, 0);   // 求和

ostream_iterator<T> out(os);  // out将类型为T的输出值写入到输出流os中
ostream_iterator<T> out(os, d);  // out将类型为T的输出值写入到输出流os中，每个值后面都额外输出一个d（d是C风格的字符串）
for (anto e : vec)
    *out++ = e;  // 直接写out=e;也可以，不过不推荐这么写
cout << endl;
copy(vec.begin(), vec.end(), out);
cout << endl;
```
###### 反向迭代器
- 在容器中从尾元素向首元素反向移动的迭代器
- 其递增、递减的操作是反过来的，即`++`会向前移动，前也是相对移动方向的
- 除了`forward_list`外都支持，使用`rbegin(),crbegin()`等

###### 链表类容器的特殊方法
`list、forward_list`

| 方法 | 说明 |
|--------|--------|
|   lst.merge(lst2)     |    将lst2中的元素合并入lst，要求lst、lst2都必须有序    |
| lst.merge(lst2, comp)|comp为特定的比较函数 |
|lst.remove(val)|调用erase删除lst内与val相等的元素|
|lst.remove(pred)|调用erase删除lst内使得一元谓词pred成立的元素|
|lst.reverse()|反转lst中元素的顺序|
|lst.sort()|排序，可以使用comp|
|lst.unique()|调用erase去重|
|lst.unique(pred)|调用erase去重，重复指的是满足二元谓词pred的元素|

**谓词是返回可以转换为bool类型值的函数。元对应参数个数**


#### 关联容器
- 关联容器支持高效的关键字查询和访问，可以分为有序集合和无序集合两种
- map和set的迭代器都不允许修改关键字
##### 分类
| 有序类型 | 说明 |
|--------|--------|
|    map    |     关联数组，保存（key, value）对   |
|    set      |       只保存关键字      |
|multimap|       关键字可重复出现的map|
|multiset|      关键字可重复出现的set    |

| 无序类型 | 说明 |
|--------|--------|
|    unordered_map    |    用哈希函数组织的map    |
|unordered_set|     用哈希函数组织的set    |
|unordered_multimap|     ....       |
|unordered_multiset|       ....      |

```java
vector<int> vec;
for (int i=0; i<10; i++) {
    vec.push_back(i);
    vec.push_back(i);
}

set<int> iset(vec.cbegin(), vec.cend());  // 10个元素
multiset<int> imset(vec.cbegin(), vec.cend());  // 20个元素
```
##### 关键字类型要求
- 有序元素的关键字类型必须定义元素比较的方法
- 不支持比较的复杂类型需要自定义比较函数

```java
// compareClass1是进行Class1对象比较的函数，定义时需要添加比较函数的函数指针
// 直接使用compareClass1也行，因为函数名会转化为函数指针
// 构造函数也使用比较函数的函数指针
set<Class1, decltype(compareClass1)*> cls(compareClass1);
```
###### 关联容器额外的类型别名

    key_type : 容器的关键字类型
    value_type : 对于set，与key_type相同；map则是pair<key, value>
    mapped_type : 关键字关联的类型

##### 添加元素

    c.insert(v);
    c.emplace(args);
    c.insert(iter1, iter2);
    c.insert(il);  // 花括号列表，返回void
    c.insert(iter, v); // 迭代器指示搜索新元素存储应该存储的位置。返回一个迭代器，指向具有给定关键字的元素
    c.emplace(iter, args);

**对于不包含重复关键字的容器，添加单一元素的inert和emplace返回一个pair，指示插入操作是否成功。pair的首元素（first）是一个迭代器，指向具有指定关键字的元素；second是一个bool值，指示元素成功插入还是已经存在于容器中，成功插入为true，否则为false**。
```java
auto ret = word_count.insert({"hello", 1}); 尝试插入
if (!ret.second) // 元素已经存在map中
    ++ret.first->second;  //  ret.first是指向“hello”关键字的迭代器，迭代器指向的second元素是原本"hello"对应的数目，加一即可
```

##### 访问元素

    c.find(k);  // 返回指向第一个key为k的迭代器
    c.count(k);  // 返回关键字k的个数
    c.lower_bound(k); // 返回一个迭代器，指向第一个关键字不小于k的元素
    c.upper_bound(k);  // 返回一个迭代器，指向第一个关键字大于k的元素
    c.equal_range(k);   //  返回一个迭代器pair，表示关键字等于k的元素的范围。如不存在，则pair的两个成员均为c.end()

`lower_bound`和`upper_bound`只适用于有序容器
通过下标访问元素返回左值，既可以读，也可以写回

##### 无序容器
- 无序容器在存储上组织为一组桶，每个桶保存0个或多个元素
- 无序容器的性能依赖于哈希函数的质量和桶的大小

    c.bucket_count();  // 正在使用的桶数目
    c.max_bucket_count();  // 容器能容纳的最多的桶的数量
    c.bucket_size(n);  // 第n个桶中有多少个元素
    c.bucket(k);  //  关键字为k的元素在哪个桶中
    
    local_iterator       // 访问桶中元素的迭代器
    const_local_iterator   //  const版本
    c.begin(n), c.end(n)   //  桶n元素的首、尾迭代器
    c.cbegin(n), c.cend(n)
    
    c.load_factor();   //  每个桶的平均元素数量，float类型
    c.max_load_factor();  // 最大平均桶元素数量，每个桶的平均元素数量大于这个值就需要添加新的桶
    c.rehash(n);    //  重组存储，使得bucket_count >= n且bucket_count>size/max_load_factor
    c.reserve(n);   //  重组存储，使得c可以保存n个元素且不必rehash

###### 无序容器对关键字的要求
- 无序容器使用`==`运算符比较元素
- 使用`hash<key_type>`类型的对象生成每个元素的哈希值

```java
size_t hasher(const Class1 & cls) {
    return hash<string>()(cls.name);
}
bool eqop(const Class1 & cls1, const Class1 & cls2) {
    return cls1.name == cls2.name;
}
using clsset = unordered_set<Class1, hasher, eqop>;
// 42是桶大小
clsset s(42, hasher, eqop);
```





























