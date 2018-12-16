---
title: Java Thread Pool
date: 2017-01-17 14:43:08
tags: [Java]
categories:
---

##### ThreadPoolExecutor

---

###### 构造方法

`java.uitl.concurrent.ThreadPoolExecutor`类是线程池中最核心的一个类，继承自`AbstractExecutorService`，`AbstractExecutorService`是一个抽象类，它实现了ExecutorService接口。`ThreadPoolExecutor`的构造方法如下：
```java
public class ThreadPoolExecutor extends AbstractExecutorService {

    public ThreadPoolExecutor(int corePoolSize,int maximumPoolSize,long keepAliveTime,TimeUnit unit,
            BlockingQueue<Runnable> workQueue);
    public ThreadPoolExecutor(int corePoolSize,int maximumPoolSize,long keepAliveTime,TimeUnit unit,
            BlockingQueue<Runnable> workQueue,ThreadFactory threadFactory);

    public ThreadPoolExecutor(int corePoolSize,int maximumPoolSize,long keepAliveTime,TimeUnit unit,
            BlockingQueue<Runnable> workQueue,RejectedExecutionHandler handler);

    public ThreadPoolExecutor(int corePoolSize,int maximumPoolSize,long keepAliveTime,TimeUnit unit,
        BlockingQueue<Runnable> workQueue,ThreadFactory threadFactory,RejectedExecutionHandler handler);

}
```
前面三个构造器都是调用的第四个构造器进行的初始化工作，参数介绍如下：

---

1 `corePoolSize` : 核心池的大小。默认情况下，在创建了线程池后，线程池中的线程数为0，当有任务来之后，就会创建一个线程去执行任务，当线程池中的线程数目达到`corePoolSize`后，就会把到达的任务放到缓存队列当中。（正式工）
2 `maximumPoolSize` : 线程池最大线程数，表示在线程池中最多能创建多少个线程。最大线程数意味着当核心池不够用时可以额外开辟新线程，但这些新加入的线程在空闲时可以销毁（临时工）。
3 `keepAliveTime` : 线程没有任务执行时最多保持多久时间会终止。默认情况下，只有当线程池中的线程数大于`corePoolSize`时，`keepAliveTime`才会起作用，直到线程池中的线程数不大于`corePoolSize`，即当线程池中的线程数大于`corePoolSize`时，如果一个线程空闲的时间达到`keepAliveTime`，则会终止，直到线程池中的线程数不超过`corePoolSize`。但是如果调用了`allowCoreThreadTimeOut(boolean)`方法，在线程池中的线程数不大于`corePoolSize`时，`keepAliveTime`参数也会起作用，直到线程池中的线程数为0。
4 `unit` : `keepAliveTime`的时间单位. 包括

	TimeUnit.DAYS
    TimeUnit.HOURS
    TimeUnit.MINUTES
    TimeUnit.SECONDS
    TimeUnit.MILLISECONDS
    TimeUnit.MICROSECONDS
    TimeUnit.NANOSECONDS

5 `workQueue` : 一个阻塞队列，用来存储等待执行的任务。可以是如下三种，其中`ArrayBlockingQueue`和`PriorityBlockingQueue`使用较少，一般使用`LinkedBlockingQueue`和`Synchronous`。线程池的排队策略与BlockingQueue有关。

	ArrayBlockingQueue：基于数组的先进先出队列，此队列创建时必须指定大小
    LinkedBlockingQueue：基于链表的先进先出队列，如果创建时没有指定此队列大小，则默认为Integer.MAX_VALUE
    SynchronousQueue：不会保存提交的任务，而是将直接新建一个线程来执行新来的任务
    PriorityBlockingQueue

6 `threadFactory` ：线程工厂，主要用来创建线程
7 `handler` ：表示当拒绝处理任务时的策略，可以是

	ThreadPoolExecutor.AbortPolicy:丢弃任务并抛出RejectedExecutionException异常
	ThreadPoolExecutor.DiscardPolicy：也是丢弃任务，但是不抛出异常
	ThreadPoolExecutor.DiscardOldestPolicy：丢弃队列最前面的任务，然后重新尝试执行任务（重复此过程）
	ThreadPoolExecutor.CallerRunsPolicy：由调用线程处理该任务

---

###### 继承结构

`Executor`是一个顶层接口，在它里面只声明了一个方法`execute(Runnable)`，返回值为void，参数为`Runnable`类型，从字面意思可以理解，就是用来执行传进去的任务的。

`ExecutorService`接口继承了`Executor`接口，并声明了一些方法：`submit`、`invokeAll`、`invokeAny`以及`shutDown`等。

抽象类`AbstractExecutorService`实现了`ExecutorService`接口，基本实现了`ExecutorService`中声明的所有方法。

`ThreadPoolExecutor`继承了类`AbstractExecutorService`。在`ThreadPoolExecutor`类中有几个非常重要的方法：

---

1 `execute()` : `execute()`方法实际上是`Executor`中声明的方法，在`ThreadPoolExecutor`进行了具体的实现，这个方法是`ThreadPoolExecutor`的核心方法，通过这个方法可以向线程池提交一个任务，交由线程池去执行。

2 `submit()` : `submit()`方法是在`ExecutorService`中声明的方法，在`AbstractExecutorService`就已经有了具体的实现，在`ThreadPoolExecutor`中并没有对其进行重写，这个方法也是用来向线程池提交任务的，但是它和`execute()`方法不同，它能够返回任务执行的结果(`Future`)

3 `shutdown()` : 关闭线程池，不再接受新的任务，等到所有线程完成任务关闭线程池

4 `shutdownNow()` : 立即结束所有线程，关闭线程池

---

##### 线程池实现原理

---

###### 线程状态

`ThreadPoolExecutor`中定义了一个`volatile`变量`volatile int runState`表示当前线程池的状态，它是一个volatile变量用来保证线程之间的可见性。还有几个`static final`变量表示`runState`可能的几个取值：

	static final int RUNNING    = 0;
	static final int SHUTDOWN   = 1;
	static final int STOP       = 2;
	static final int TERMINATED = 3;

创建线程池后，初始时，线程池处于`RUNNING`状态。
调用了`shutdown()`方法，则线程池处于`SHUTDOWN`状态，此时线程池不能够接受新的任务，它会等待所有任务执行完毕。
调用了`shutdownNow()`方法，则线程池处于`STOP`状态，此时线程池不能接受新的任务，并且会去尝试终止正在执行的任务。
当线程池处于`SHUTDOWN`或`STOP`状态，并且所有工作线程已经销毁，任务缓存队列已经清空或执行结束后，线程池被设置为`TERMINATED`状态。

---

###### 任务执行
`ThreadPoolExecutor`类中其他的一些比较重要成员变量如下：
```java
private final BlockingQueue<Runnable> workQueue;  //任务缓存队列，用来存放等待执行的任务

private final ReentrantLock mainLock = new ReentrantLock(); //线程池的主要状态锁，对线程池状态（比如线程池大小、runState等）的改变都要使用这个锁

private final HashSet<Worker> workers = new HashSet<Worker>();  //用来存放工作集

private volatile long  keepAliveTime;    //线程存货时间

private volatile boolean allowCoreThreadTimeOut;   //是否允许为核心线程设置存活时间

private volatile int   corePoolSize;     //核心池的大小（即线程池中的线程数目大于这个参数时，提交的任务会被放进任务缓存队列）

private volatile int   maximumPoolSize;   //线程池最大能容忍的线程数

private volatile int   poolSize;       //线程池中当前的线程数

private volatile RejectedExecutionHandler handler; //任务拒绝策略

private volatile ThreadFactory threadFactory;   //线程工厂，用来创建线程

private int largestPoolSize;   //用来记录线程池中曾经出现过的最大线程数

private long completedTaskCount;   //用来记录已经执行完毕的任务个数

```

任务提交执行依靠`execute()`方法，`submit()`也是提交任务的方法，但是它也是调用了`execute()`方法。`execute()`方法处理方法的逻辑如下：

```java
public void execute(Runnable command) {
    if (command == null)
        throw new NullPointerException();
    if (poolSize >= corePoolSize || !addIfUnderCorePoolSize(command)) {
        if (runState == RUNNING && workQueue.offer(command)) {
            if (runState != RUNNING || poolSize == 0)
                ensureQueuedTaskHandled(command);
        } else if (!addIfUnderMaximumPoolSize(command))
            reject(command); // is shutdown or saturated
    }
}
```

首先，判断提交的任务`command`是否为`null`，若是`null`，则抛出空指针异常。接着还是一个判断语句，如果线程池中当前线程数不小于核心池大小，直接执行判断语句中的代码；否则执行`addIfUnderCorePoolSize(command)`，如果返回false，则继续执行判断语句中的代码，否则整个方法就直接执行完毕了。

第二层判断语句中，如果当前线程池处于RUNNING状态，则将任务放入任务缓存队列(`workQueue.offer(command)`就是将任务放入缓存队列)；如果当前线程池不处于RUNNING状态或者任务放入缓存队列失败，则执行`addIfUnderMaximumPoolSize(command)`，如果执行`addIfUnderMaximumPoolSize`方法失败，则执行`reject()`方法进行任务拒绝处理。

如果说当前线程池处于RUNNING状态且将任务放入任务缓存队列成功，则继续执行第三层判断语句`if (runState != RUNNING || poolSize == 0)`，这句判断是为了防止在将此任务添加进任务缓存队列的同时其他线程突然调用`shutdown`或者`shutdownNow`方法关闭了线程池的一种应急措施，如果是这样就需要应急处理`ensureQueuedTaskHandled(command)`。

```java
private boolean addIfUnderCorePoolSize(Runnable firstTask) {
    Thread t = null;
    final ReentrantLock mainLock = this.mainLock;
    mainLock.lock();
    try {
        if (poolSize < corePoolSize && runState == RUNNING)
            t = addThread(firstTask);        //创建线程去执行firstTask任务
        } finally {
        	mainLock.unlock();
    }
    if (t == null)
        return false;
    t.start();
    return true;
}
```

上面提到的`addIfUnderCorePoolSize`方法，由字面意思是当低于核心池大小时执行的方法，因为涉及线程池的变化，所以需要加锁。if语句判断当前线程池中的线程数目是否小于核心池大小，虽然前面在`execute()`方法中已经判断过了，但是没有加锁。因此可能在`execute`方法判断的时候`poolSize`小于`corePoolSize`，而判断完之后，在其他线程中又向线程池提交了任务，就可能导致`poolSize`不小于`corePoolSize`了。

```java
private Thread addThread(Runnable firstTask) {
    Worker w = new Worker(firstTask);
    Thread t = threadFactory.newThread(w);  //创建一个线程，执行任务
    if (t != null) {
        w.thread = t;            //将创建的线程的引用赋值为w的成员变量
        workers.add(w);
        int nt = ++poolSize;     //当前线程数加1
        if (nt > largestPoolSize)
            largestPoolSize = nt;
    }
    return t;
}
```

对于`runState`的判断也是类似的。满足条件的话，通过`addThread`方法创建线程，创建成功则启动线程。在`addThread`方法中，首先用提交的任务创建了一个`Worker`对象，然后调用线程工厂`threadFactory`创建了一个新的线程`t`，然后将线程`t`的引用赋值给了`Worker`对象的成员变量`thread`，接着通过`workers.add(w)`将`Worker`对象添加到工作集当中。

```java
public void run() {
    try {
        Runnable task = firstTask;
        firstTask = null;
        while (task != null || (task = getTask()) != null) {
            runTask(task);
            task = null;
        }
    } finally {
        workerDone(this);
    }
}
```
`Worker`类实现了`Runnable`接口，在其`run`函数中首先执行的是通过构造器传进来的任务`firstTask`，在调用`runTask()`执行完`firstTask`之后，在`while`循环里面不断通过`getTask()`去取新的任务来执行，`getTask`是`ThreadPoolExecutor`类中的方法，从任务缓存队列中取。

任务提交后，线程池的处理策略总结如下：
- 如果当前线程池中的线程数目小于`corePoolSize`，则每来一个任务，就会创建一个线程去执行这个任务；
- 如果当前线程池中的线程数目>=`corePoolSize`，则每来一个任务，会尝试将其添加到任务缓存队列当中，若添加成功，则该任务会等待空闲线程将其取出去执行；若添加失败（一般来说是任务缓存队列已满），则会尝试创建新的线程去执行这个任务；
- 如果当前线程池中的线程数目达到`maximumPoolSize`，则会采取任务拒绝策略进行处理；
- 如果线程池中的线程数量大于`corePoolSize`时，如果某线程空闲时间超过`keepAliveTime`，线程将被终止，直至线程池中的线程数目不大于`corePoolSize`；如果允许为核心池中的线程设置存活时间，那么核心池中的线程空闲时间超过`keepAliveTime`，线程也会被终止。

---

###### 线程初始化
默认情况下，创建线程池之后，线程池中是没有线程的，需要提交任务之后才会创建线程。如果需要线程池创建之后立即创建线程，可以通过以下两个方法办到：
```java
// 初始化一个核心线程
public boolean prestartCoreThread() {
    return addIfUnderCorePoolSize(null); //注意传进去的参数是null
}

// 初始化所有核心线程
public int prestartAllCoreThreads() {
    int n = 0;
    while (addIfUnderCorePoolSize(null))//注意传进去的参数是null
        ++n;
    return n;
}
```
上面传入参数为null，最后执行线程会阻塞在`getTask`方法中的`workQueue.take()`，等待直到任务队列中有任务。

---

###### 容量的动态调整

	setCorePoolSize：设置核心池大小
	setMaximumPoolSize：设置线程池最大能创建的线程数目大小

---

##### 线程池应用

---

###### ThreadPoolExecutor
```java
// 缓存任务队列大小为8，核心池大小为5
ThreadPoolExecutor executor = new ThreadPoolExecutor(5, 10, 200, TimeUnit.MILLISECONDS, new ArrayBlockingQueue<Runnable>(8));
executor.execute(myTask);
// myTask 应该是显示了Runnable的类的对象
executor.shutdown();
```

---

###### 推荐实现
Java官方不推荐直接使用`ThreadPoolExecutor`，而是使用`Executors`类中提供的几个静态方法来创建线程池。分别是
```java
Executors.newCachedThreadPool();        //创建一个缓冲池，缓冲池容量大小为Integer.MAX_VALUE
Executors.newSingleThreadExecutor();   //创建容量为1的缓冲池
Executors.newFixedThreadPool(int);    //创建固定容量大小的缓冲池
Executors.newScheduledThreadPool(int); //创建固定容量的延迟连接池
```
这三种方法也都是调用了`ThreadPoolExecutor`，支持参数设定不同而已。

```java
public static ExecutorService newFixedThreadPool(int nThreads) {
    return new ThreadPoolExecutor(nThreads, nThreads,
                                  0L, TimeUnit.MILLISECONDS,
                                  new LinkedBlockingQueue<Runnable>());
}

ExecutorService pool = Executors.newFixedThreadPool(2);
Thread t1 = new MyThread();
Thread t2 = new MyThread();
pool.execute(t1);
pool.execute(t2);
pool.shutdown();


public static ExecutorService newSingleThreadExecutor() {
    return new FinalizableDelegatedExecutorService
        (new ThreadPoolExecutor(1, 1,
                                0L, TimeUnit.MILLISECONDS,
                                new LinkedBlockingQueue<Runnable>()));
}
ExecutorService pool = Executors.newSingleThreadExecutor();
Thread t1 = new MyThread();
pool.execute(t1);
pool.shutdown();


public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                                  60L, TimeUnit.SECONDS,
                                  new SynchronousQueue<Runnable>());
}
ExecutorService pool = Executors.newCachedThreadPool();
Thread t1 = new MyThread();
Thread t2 = new MyThread();
pool.execute(t1);
pool.execute(t2);
pool.shutdown();



ScheduledExecutorService pool = Executors.newScheduledThreadPool(2);
Thread t1 = new MyThread();
Thread t2 = new MyThread();
Thread t3 = new MyThread();

pool.execute(t1);

pool.schedule(t2, 1000, TimeUnit.MILLISECONDS);
pool.schedule(t3, 10, TimeUnit.MILLISECONDS);

pool.shutdown();
```

`newFixedThreadPool`创建的线程池`corePoolSize`和`maximumPoolSize`值是相等的，它使用的`LinkedBlockingQueue`；

`newSingleThreadExecutor`将`corePoolSize`和`maximumPoolSize`都设置为1，也使用的`LinkedBlockingQueue`；

`newCachedThreadPool`将`corePoolSize`设置为0，将`maximumPoolSize`设置为`Integer.MAX_VALUE`，使用的`SynchronousQueue`，也就是说来了任务就创建线程运行，当线程空闲超过60秒，就销毁线程。

---

感谢[原文](http://www.cnblogs.com/dolphin0520/p/3932921.html)




