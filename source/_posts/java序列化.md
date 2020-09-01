---
title: java序列化
date: 2016-05-05 15:10:53
tags: [Java]
categories: Dev
---
### 一. 描述
- 在网络通信和数据存储方面很有用
- 对于需要序列化的类，应该在其实现时在类头部加上implements Serializable

### 二. 示例
- 序列化
```java
public byte[] functionName (ClassType sample) {
    try {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(sample);
        byte[] bytes = baos.toByteArray();
        System.out.println("...serialization complete."); 
        return bytes;
    } catch (Exception e) {
        System.out.println("...serialization failed.");
    }
    return null;
}    
```
- 反序列化
```java
public ClassType deserializeCFC(byte[] bytes) {
    try {
        ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
        ObjectInputStream ois = new ObjectInputStream(bais);
        return (ClassType) ois.readObject();
    } catch (Exception e) {
        System.out.println("...deserialization failed.");
    }
    return null;
}
```