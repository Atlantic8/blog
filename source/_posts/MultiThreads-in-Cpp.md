---
title: MultiThreads in Cpp
date: 2017-06-12 09:41:32
tags: [Cpp]
categories: Dev
---



##### thread
```java
#include <thread>
```
###### 构造
| 用途 | 说明 |
|--------|--------|
|    创建一个空的 thread 执行对象    |   ` thread() noexcept; `   |
|   创建一个 thread对象，该 thread对象可被 joinable，新产生的线程会调用 fn 函数，该函数的参数由 args 给出   |    `template <class Fn, class... Args> explicit thread (Fn&& fn, Args&&... args);`    |
|   copy [deleted]      |    `thread (const thread&) = delete;`    |
|    调用成功之后 x 不代表任何 thread 执行对象    |    `thread (thread&& x) noexcept;`    |

###### 其他成员
- `get_id` : 获取线程 ID
- `joinable` : 检查线程是否可被 join
- `join` : 同步操作，线程所有的操作完成此函数才返回，阻塞调用此函数的线程。调用此函数后，对应thread对象变成`non-joinable`，并可以安全销毁
- `detach` : 将目标线程与调用线程分离开，调用此函数后，对应thread对象变成`non-joinable`，并可以安全销毁（这里很奇怪--!）
- `swap` : `void swap (thread& x) noexcept`，与x互换状态
- `native_handle` : 返回可以访问此线程详细实现信息的值
- `hardware_concurrency [static]` :  返回硬件线程上下文的数量

##### mutex
Mutex 又称互斥量，C++ 11中与 Mutex 相关的类（包括锁类型）和函数都声明在 <mutex> 头文件中.

###### std::mutex
std::mutex 对象提供了独占所有权的特性——即不支持递归地对 std::mutex 对象上锁(重复上锁)，其相关函数如下：
- 构造函数，std::mutex**不允许拷贝构造，也不允许 move 拷贝**，最初产生的 mutex 对象是处于 unlocked 状态的
- `lock()`，调用线程将锁住该互斥量。线程调用该函数会发生下面 3 种情况：(1). 如果该互斥量当前没有被锁住，则调用线程将该互斥量锁住，直到调用 unlock之前，该线程一直拥有该锁。(2). **如果当前互斥量被其他线程锁住，则当前的调用线程被阻塞住**。(3). **如果当前互斥量被当前调用线程锁住，则会产生死锁(deadlock)**
- `unlock()`， 解锁，释放对互斥量的所有权
- `try_lock()`，尝试锁住互斥量，如果互斥量被其他线程占有，则当前线程也不会被阻塞。线程调用该函数也会出现下面 3 种情况，(1). 如果当前互斥量没有被其他线程占有，则该线程锁住互斥量，直到该线程调用 unlock 释放互斥量。(2). **如果当前互斥量被其他线程锁住，则当前调用线程返回 false，而并不会被阻塞掉**。(3). 如果当前互斥量被当前调用线程锁住，则会产生死锁(deadlock)

```java
std::mutex mtx;
volatile int counter(0);
void func() {
    for (int i=0; i<10000; ++i) {
        if (mtx.try_lock()) {   // 没被上锁时才自增
            ++counter;
            mtx.unlock();
        }
    }
}
int main (int argc, const char* argv[]) {
    std::thread threads[10];
    for (int i=0; i<10; ++i)
        threads[i] = std::thread(func);
    for (auto& th : threads) th.join();
    std::cout << counter << " successful increases of the counter.\n";
    return 0;
}
```

###### std::recursive_mutex
recursive_mutex与mutex类似。但是和 std::mutex 不同的是，**std::recursive_mutex 允许同一个线程对互斥量多次上锁（即递归上锁），来获得对互斥量对象的多层所有权**，std::recursive_mutex 释放互斥量时需要调用与该锁层次深度相同次数的 unlock()，可理解为 lock() 次数和 unlock() 次数相同

###### std::time_mutex
定时Mutex类，有两个特殊函数：
- `try_lock_for` : 接受一个时间范围，表示在这一段时间范围之内线程如果没有获得锁则被阻塞住，超时则返回false
- `try_lock_until` : 接受一个时间点作为参数，在指定时间点未到来之前线程如果没有获得锁则被阻塞住，超时则返回false

```java
#include <chrono>

void fireworks() {
  // 等待获取锁，每200ms打印一个'-'
  while (!mtx.try_lock_for(std::chrono::milliseconds(200))) {
    std::cout << "-";
  }
  // 获取锁后休息1秒，然后打印'*'
  std::this_thread::sleep_for(std::chrono::milliseconds(1000));
  std::cout << "*\n";
  mtx.unlock();
}
```

###### std::recursive_timed_mutex
std::recursive_timed_mutex之于std::timed_mutex如同std:recursive_mutex之于std::mutex，就是允许重复上锁。

###### std::lock_guard
方便线程对互斥量上锁，不用考虑销毁、异常时的解锁问题。
```java
#include <stdexcept>

void print_even (int x) {
    if (x%2 == 0) std::cout << x << " is even\n";
    else throw (std::logic_error("not even"));
}

void print_thread_id (int id) {
    try {
        // 实用局部的lock_guard锁定mtx保证在销毁、异常中的解锁
        std::lock_guard<std::mutex> lck (mtx);
        print_even(id);
    }
    catch (std::logic_error&) {
        std::cout << "[exception caught]\n";
    }
}
```

###### std::unique_lock
方便线程对互斥量上锁，但提供了更好的上锁和解锁控制。
```java
void print_block (int n, char c) {
    // 临界区 (lck生存周期内对std::cout的互斥访问权)
    std::unique_lock<std::mutex> lck (mtx);
    for (int i=0; i<n; ++i) {
        std::cout << c;
    }
    std::cout << '\n';
}
```

##### future
```java
#include <future>
```

###### std::future
从异步任务中获取结果，通过查询future的状态（future_status）可获取异步操作的结果。future_status有三种状态：
- deferred：异步操作还没开始
- ready：异步操作已经完成
- timeout：异步操作超时

```java
std::future_status status;
    do {
        status = future.wait_for(std::chrono::seconds(1));
        if (status == std::future_status::deferred) {
            std::cout << "deferred\n";
        } else if (status == std::future_status::timeout) {
            std::cout << "timeout\n";
        } else if (status == std::future_status::ready) {
            std::cout << "ready!\n";
        }
    } while (status != std::future_status::ready);
```
获取future结果有三种方式：get、wait、wait_for
- get等待异步操作结束并返回结果
- wait只是等待异步操作完成，没有返回值
- wait_for是超时等待返回结果。


<future> 头文件中包含了以下几个类和函数：
- Providers 类：std::promise, std::package_task
- Futures 类：std::future, shared_future
- Providers 函数：std::async()
- 其他类型：std::future_error, std::future_errc, std::future_status, std::launch

###### std::promise
`std::promise`为获取线程函数中的某个值提供便利，在**线程函数中给外面传进来的promise赋值，当线程函数执行完成之后就可以通过promis获取该值**了，值得注意的是取值是间接的通过promise内部提供的future来获取的.
```java
std::promise<int> pr;
    std::thread t (
        [] (std::promise<int>& p) { p.set_value_at_thread_exit(9); } ,
        std::ref(pr)
    );
    std::future<int> f = pr.get_future();
    auto r = f.get();
```

| 函数 | 说明 |
|--------|--------|
|    promise();    |    默认构造函数，初始化一个空的共享状态    |
|    template <class Alloc> promise (allocator_arg_t aa, const Alloc& alloc);    |    带自定义内存分配器的构造函数，与默认构造函数类似，但是使用自定义分配器来分配共享状态    |
|    promise (const promise&) = delete;    |   删除的拷贝构造函数     |
|    promise (promise&& x) noexcept;    |    移动构造函数    |

- promise 对象可以保存某一类型 T 的值，该值可被 future 对象读取（可能在另外一个线程中），因此 promise 也提供了一种线程同步的手段
- 在 promise 对象构造时可以和一个共享状态（通常是std::future）相关联，并可以在相关联的共享状态(std::future)上保存一个类型为 T 的值。
- 可以通过 `get_future` 来获取与该 promise 对象相关联的 future 对象，调用该函数之后，两个对象共享相同的共享状态
    - promise 对象是异步 Provider，它可以在某一时刻设置共享状态的值
    - future 对象可以异步返回共享状态的值，或者在必要的情况下阻塞调用者并等待共享状态标志变为 ready，然后才能获取共享状态的值
- promise对象可以通过`set_value`函数设置共享状态的值
- `std::promise::set_value_at_thread_exit` : 设置共享状态的值，但是不将共享状态的标志设置为 ready，当线程退出时该 promise 对象会自动设置为 ready

```java
void print_int(std::future<int>& fut) {
    int x = fut.get(); // 获取共享状态的值.
    std::cout << "value: " << x << '\n'; // 打印 value: 10.
}

int main () {
    std::promise<int> prom; // 生成一个 std::promise<int> 对象.
    std::future<int> fut = prom.get_future(); // 和 future 关联.
    std::thread t(print_int, std::ref(fut)); // 将 future 交给另外一个线程t.
    prom.set_value(10); // 设置共享状态的值, 此处和线程t保持同步.
    t.join();
    return 0;
}
```

`std::promise::set_exception`为 promise 设置异常，此后 promise 的共享状态变标志变为 ready。下面程序的意义是：线程1从终端接收一个整数，线程2将该整数打印出来，如果线程1接收一个非整数，则为 promise 设置一个异常(failbit) ，线程2 在std::future::get 是抛出该异常。

```java
void get_int(std::promise<int>& prom) {
    int x;
    std::cout << "Please, enter an integer value: ";
    std::cin.exceptions (std::ios::failbit);   // throw on failbit
    try {
        std::cin >> x;                         // sets failbit if input is not int
        prom.set_value(x);
    } catch (std::exception&) {
        prom.set_exception(std::current_exception());
    }
}

void print_int(std::future<int>& fut) {
    try {
        int x = fut.get();
        std::cout << "value: " << x << '\n';
    } catch (std::exception& e) {
        std::cout << "[exception caught: " << e.what() << "]\n";
    }
}

int main ()
{
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();

    std::thread th1(get_int, std::ref(prom));
    std::thread th2(print_int, std::ref(fut));

    th1.join();
    th2.join();
    return 0;
}
```

###### std::packaged_task
`std::packaged_task`**包装了一个可调用的目标**（如function, lambda expression, bind expression, or another function object）,以便异步调用，它和promise在某种程度上有点像，promise保存了一个共享状态的值，而packaged_task保存的是一个函数。
```java
std::packaged_task<int()> task([](){ return 7; });
std::thread t1(std::ref(task));
std::future<int> f1 = task.get_future();
auto r1 = f1.get();
```

###### std::async
`std::async`先将异步操作用`std::packaged_task`包装起来，然后将异步操作的结果放到`std::promise`中，这个过程就是创造未来的过程。外面再通过`future.get/wait`来获取这个未来的结果，`std::async`的原型`async(std::launch::async | std::launch::deferred, f, args...)`，**第一个参数是线程的创建策略**，有两种策略，默认的策略是立即创建线程：
- `std::launch::async`：在调用`async`就开始创建线程
- `std::launch::deferred`：延迟加载方式创建线程。调用async时不创建线程，直到调用了future的get或者wait时才创建线程

**第二个参数是线程函数，第三个参数是线程函数的参数.**
```java
std::future<int> f1 = std::async(
    std::launch::async,
    []() {return 8;}
);
std::future<int> f2 = std::async(
    std::launch::async,
    [](int x) {return 8+x;},
    100
);
```

##### std::condition_variable
```java
#include <condition_variable>
```
std::condition_variable 是条件变量，其构造方法如下：

| 方法 | 说明 |
|--------|--------|
|    condition_variable();    |    默认构造函数    |
|condition_variable (const condition_variable&) = delete;| 删除的拷贝函数 |

**当 `std::condition_variable` 对象的某个 wait 函数被调用的时候，它使用 `std::unique_lock`(通过 std::mutex) 来锁住当前线程。当前线程会一直被阻塞，直到另外一个线程在相同的 `std::condition_variable` 对象上调用了 `notify_one`或者'notify_all' 函数来唤醒当前线程**。

`wait`函数有两种形式：
- `void wait( std::unique_lock<std::mutex>& lock )` : 一直阻塞直到`notify_one`或者'notify_all' 函数被调用。
- `template< class Predicate > void wait( std::unique_lock<std::mutex>& lock, Predicate pred )` : **只有当谓词`pred()`不为真的时候才等待，否则直接跳过`wait`**

```java
std::mutex mtx; // 全局互斥锁.
std::condition_variable cv; // 全局条件变量.
bool ready = false; // 全局标志位.

void do_print_id(int id)
{
    std::unique_lock <std::mutex> lck(mtx);
    while (!ready) // 如果标志位不为 true, 则等待...
        cv.wait(lck); // 当前线程被阻塞, 当全局标志位变为 true 之后,
    // 线程被唤醒, 继续往下执行打印线程编号id.
    std::cout << "thread " << id << '\n';
}

void go()
{
    std::unique_lock <std::mutex> lck(mtx);
    ready = true; // 设置全局标志位为 true.
    cv.notify_all(); // 唤醒所有线程.
}

int main()
{
    std::thread threads[10];
    // spawn 10 threads:
    for (int i = 0; i < 10; ++i)
        threads[i] = std::thread(do_print_id, i);

    std::cout << "10 threads ready to race...\n";
    go(); // go!

  for (auto & th:threads)
        th.join();

    return 0;
}
```



**引用**
[1]. [C++11 并发指南二](http://www.cnblogs.com/haippy/p/3236136.html)
[2]. [C++11 并发指南三](http://www.cnblogs.com/haippy/p/3237213.html)
[3]. [C++11 并发指南](http://www.cnblogs.com/haippy/p/3239248.html)
[4]. [ C++11 并发指南五](http://blog.csdn.net/watson2016/article/details/52861094)









