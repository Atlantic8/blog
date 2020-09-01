---
title: Java Future
date: 2017-01-18 10:25:54
tags: [Java]
categories: Dev
---

###### Callable与Runnable
Java中的多线程实现可以通过继承`Thread`或者实现`Runnable`接口来实现，但是这两种方法都不能将执行结果取回。`Runnable`接口定义如下：
```java
public interface Runnable {
    public abstract void run();
}
```
由于`run()`方法返回值为void类型，所以在执行完任务之后无法返回任何结果。

`Callable`位于java.util.concurrent包下，它也是一个泛型接口，在它里面也只声明了一个方法`call()`，返回的类型就是传递进来的`V`类型：
```java
public interface Callable<V> {
    /**
     * Computes a result, or throws an exception if unable to do so.
     *
     * @return computed result
     * @throws Exception if unable to compute a result
     */
    V call() throws Exception;
}
```
`Callable`一般情况下是配合`ExecutorService`来使用的，在`ExecutorService`接口中声明了若干个`submit`方法的重载版本：
```java
<T> Future<T> submit(Callable<T> task);

<T> Future<T> submit(Runnable task, T result);

Future<?> submit(Runnable task);
```
这三个方法中，常用的是第一个和第三个。

---

###### Future
`Future`是一个接口，位于`java.util.concurrent`包下，定义如下
```java
public interface Future<V> {
    boolean cancel(boolean mayInterruptIfRunning);
    boolean isCancelled();
    boolean isDone();
    V get() throws InterruptedException, ExecutionException;
    V get(long timeout, TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException;
}
```
`Future`就是对于具体的`Runnable`或者`Callable`任务的执行结果进行取消、查询是否完成、获取结果。必要时可以通过`get`方法获取执行结果，此方法会阻塞直到任务返回结果。上述方法中：

---

1 `cancel`方法用来取消任务，如果取消任务成功则返回true，如果取消任务失败则返回false。参数`mayInterruptIfRunning`表示是否允许取消正在执行却没有执行完毕的任务，如果设置true，则表示可以取消正在执行过程中的任务。如果任务已经完成，则无论`mayInterruptIfRunning`为true还是false，此方法肯定返回false，即如果取消已经完成的任务会返回false；如果任务正在执行，若`mayInterruptIfRunning`设置为true，则返回true，若`mayInterruptIfRunning`设置为false，则返回false；如果任务还没有执行，则无论`mayInterruptIfRunning`为true还是false，肯定返回true

2 `isCancelled`方法表示任务是否被取消成功，如果在任务正常完成前被取消成功，则返回 true

3 `isDone`方法表示任务是否已经完成，若任务完成，则返回true

4 `get()`方法用来获取执行结果，这个方法会产生阻塞，会一直等到任务执行完毕才返回

5 `get(long timeout, TimeUnit unit)`用来获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null

---

###### FutureTask
由于`Future`是个接口，所以其不能实例化，`FutureTask`应运而生，也是`Future`接口的唯一实现类。

FutureTask类实现了RunnableFuture接口
```java
public class FutureTask<V> implements RunnableFuture<V> {}

public interface RunnableFuture<V> extends Runnable, Future<V> {
    void run();
}
```
`RunnableFuture`继承了`Runnable`接口和`Future`接口，而`FutureTask`实现了`RunnableFuture`接口，关系如图所示。所以它既可以作为`Runnable`被线程执行，又可以作为`Future`得到`Callable`的返回值。

<center>![关系图](http://wx1.sinaimg.cn/mw690/9bcfe727ly1fbumuzrzbaj20hz0dhq31.jpg)</center>

FutureTask提供了2个构造器
```java
public FutureTask(Callable<V> callable) {
}

public FutureTask(Runnable runnable, V result) {
}
```

---

###### 使用方法
使用`Callable + Future`获取执行结果
```java
ExecutorService executor = Executors.newCachedThreadPool();
Task task = new Task();
Future<Integer> result = executor.submit(task);
executor.shutdown();

try {
    System.out.println("task运行结果"+result.get());
} catch (InterruptedException e) {
    e.printStackTrace();
} catch (ExecutionException e) {
    e.printStackTrace();
}

class Task implements Callable<Integer>{
    @Override
    public Integer call() throws Exception {
        System.out.println("子线程在进行计算");
        Thread.sleep(3000);
        int sum = 0;
        for(int i=0;i<100;i++)
            sum += i;
        return sum;
    }
}
```

---

使用`Callable + FutureTask`获取执行结果
```java
ExecutorService executor = Executors.newCachedThreadPool();
Task task = new Task();
FutureTask<Integer> futureTask = new FutureTask<Integer>(task);

executor.submit(futureTask);
executor.shutdown();

try {
    System.out.println("task运行结果"+futureTask.get());
} catch (InterruptedException e) {
    e.printStackTrace();
} catch (ExecutionException e) {
    e.printStackTrace();
}

class Task implements Callable<Integer>{
    @Override
    public Integer call() throws Exception {
        System.out.println("子线程在进行计算");
        Thread.sleep(3000);
        int sum = 0;
        for(int i=0;i<100;i++)
            sum += i;
        return sum;
    }
}
```
