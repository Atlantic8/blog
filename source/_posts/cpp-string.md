---
title: cpp-string
date: 2016-05-05 14:54:06
tags: Cpp
---
## toupper, tolower
地球人都知道 C++ 的 string 没有 toupper ，好在这不是个大问题，因为我们有 STL 算法：
```c++
string s("heLLo");
transform(s.begin(), s.end(), s.begin(), toupper);
cout << s << endl;
transform(s.begin(), s.end(), s.begin(), tolower);
cout << s << endl;
```
当然，我知道很多人希望的是 s.to_upper() ，但是对于一个这么通用的 basic_string 来说，的确没办法把这些专有的方法放进来。如果你用 boost stringalgo ，那当然不在话下，你也就不需要读这篇文章了。

## trim
我们还知道 string 没有 trim ，不过自力更生也不困难，比 toupper 来的还要简单：
```c++
string s("   hello   ");
s.erase(0, s.find_first_not_of(" /n"));
cout << s << endl;
s.erase(s.find_last_not_of(' ') + 1);
cout << s << endl;
```
注意由于 find_first_not_of 和 find_last_not_of 都可以接受字符串，这个时候它们寻找该字符串中所有字符的 absence ，所以你可以一次 trim 掉多种字符。

## erase
string 本身的 erase 还是不错的，但是只能 erase 连续字符，如果要拿掉一个字符串里面所有的某个字符呢？用 STL 的 erase + remove_if 就可以了，注意光 remove_if 是不行的。
```c++
string s("   hello, world. say bye   ");
s.erase(remove_if(s.begin(),s.end(), bind2nd(equal_to<char>(), ' ')), s.end());
```
上面的这段会拿掉所有的空格，于是得到 hello,world.saybye。

## replace
string 本身提供了 replace ，不过并不是面向字符串的，譬如我们最常用的把一个 substr 换成另一个 substr 的操作，就要做一点小组合：
```c++
string s("hello, world");
string sub("ello, ");
s.replace(s.find(sub), sub.size(), "appy ");
cout << s << endl;
```
输出为 happy world。注意原来的那个 substr 和替换的 substr 并不一定要一样长。

## startwith, endwith
这两个可真常用，不过如果你仔细看看 string 的接口，就会发现其实没必要专门提供这两个方法，已经有的接口可以干得很好：
```c++
string s("hello, world");
string head("hello");
string tail("ld");
bool startwith = s.compare(0, head.size(), head) == 0;
cout << boolalpha << startwith << endl;
bool endwith = s.compare(s.size() - tail.size(), tail.size(), tail) == 0;
cout << boolalpha << endwith << endl;
```
当然了，没有
```c++ 
s.startwith("hello") 
```
这样方便。

## toint, todouble, tobool...
这也是老生常谈了，无论是 C 的方法还是 C++ 的方法都可以，各有特色：
```c++
string s("123");
int i = atoi(s.c_str());
cout << i << endl;
    
int ii;
stringstream(s) >> ii;
cout << ii << endl;
    
string sd("12.3");
double d = atof(sd.c_str());
cout << d << endl;
    
double dd;
stringstream(sd) >> dd;
cout << dd << endl;
    
string sb("true");
bool b;
stringstream(sb) >> boolalpha >> b;
cout << boolalpha << b << endl;
```
C 的方法很简洁，而且赋值与转换在一句里面完成，而 C++ 的方法很通用。

## split
这可是件麻烦事，我们最希望的是这样一个接口： '''s.split(vect, ',')''' 。用 STL 算法来做有一定难度，我们可以从简单的开始，如果分隔符是空格、tab 和回车之类，那么这样就够了：
```c++
string s("hello world, bye.");
vector<string> vect;
vect.assign(
    istream_iterator<string>(stringstream(s)),
    istream_iterator<string>()
);
```

不过要注意，如果 s 很大，那么会有效率上的隐忧，因为 stringstream 会 copy 一份 string 给自己用。

## concat
把一个装有 string 的容器里面所有的 string 连接起来，怎么做？希望你不要说是 hand code 循环，这样做不是更好？

```c++
vector<string> vect;
vect.push_back("hello");
vect.push_back(", ");
vect.push_back("world");
    
cout << accumulate(vect.begin(), vect.end(), string(""));
```
不过在效率上比较有优化余地。

## reverse
其实我比较怀疑有什么人需要真的去 reverse 一个 string ，不过做这件事情的确是很容易：
```c++
std::reverse(s.begin(), s.end());
```
上面是原地反转的方法，如果需要反转到别的 string 里面，一样简单：
```c++
 s1.assign(s.rbegin(), s.rend());
```
效率也相当理想。


## 解析文件扩展名
字数多点的写法：
```c++
std::string filename("hello.exe");
std::string::size_type pos = filename.rfind('.');
std::string ext = filename.substr(pos == std::string::npos ? filename.length() : pos + 1);
```
不过两行，合并成一行呢？也不是不可以：
```c++
std::string ext = filename.substr(filename.rfind('.') == std::string::npos ? filename.length() : filename.rfind('.') + 1);
```
我们知道，rfind 执行了两次。不过第一，你可以希望编译器把它优化掉，其次，扩展名一般都很短，即便多执行一次，区别应该是相当微小。
