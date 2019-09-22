---
title: CherryPy Torturial
mathjax: true
date: 2019-09-21 23:51:48
tags: [python, web]
categories: Other
---

python有多种工具包，其中就包括一些可以提供网页服务的package，比如Django、CherryPy等。在不同的情况下一般有不同的选择，比如如果只想是通过浏览器下载服务器上的文件，那么通过SimpleHTTPServer即可
```python
python -m SimpleHTTPServer 8000
```

今天介绍的是一种上手极快的工具，CherryPy，下面会通过一些例子展示如何快速搭建自己需要的简单网页。

#### 安装
pip安装即可

#### 返回静态网页
一般的使用方法都是封装一个app类，然后在这个类中定义函数，将函数设置为cherrypy.expose则表示可以通过url访问这个函数。生效的时候通过`quickstart(Test(), '/', conf)`函数生效，这个函数有三个参数，后两个是应用的根位置和配置词典，为可选参数
```python
import cherrypy

class Test(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, param='bingo'): #给定param参数
        return 'calling generate %s' % param 


if __name__ == '__main__':
    cherrypy.quickstart(Test())
```
上面这个例子，我们可以通过`http://localhost:8080/generate?param=success`返回`calling generate success`. 

#### 提交form
如果我们希望在网页端采集用户的输入，那么我们就需要通过form获取了。网页端用户操作的组件由html中的name属性指示
```python
import cherrypy


class Test(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              <input type="text" value="bingo" name="param" />
              <button type="submit">generate</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, param='bingo'):
        return 'calling generate %s' % param


if __name__ == '__main__':
    cherrypy.quickstart(Test())
```
如果想返回一个网页，那么直接return这个网页的内容即可。这里是通过get方式发送form数据，也可以使用post，推荐使用post


#### 配置
默认配置一般在Lib/site-packages/cherrypy/scaffold/site.conf中，内容如下
```python
[global]
# Uncomment this when you're done developing
#environment: "production"

server.socket_host: "0.0.0.0"
server.socket_port: 8088

# Uncomment the following lines to run on HTTPS at the same time
#server.2.socket_host: "0.0.0.0"
#server.2.socket_port: 8433
#server.2.ssl_certificate: '../test/test.pem'
#server.2.ssl_private_key: '../test/test.pem'

tree.myapp: cherrypy.Application(scaffold.root, "/", "example.conf")
```
###### 全局配置
这里主要是全局【global】配置，在代码中可以通过
```
cherrypy.config.update({'server.socket_host': '64.72.221.48',
                        'server.socket_port': 80})
```
进行更改

> 如果修改端口后浏览器上打不开网页，其他都ok的话，需要看一下这个端口是不是系统默认端口，比如9090

###### 局部配置
局部配置仅在单个app内部生效，由`/`符号开头，形式如下
```python
[/]
tools.trailing_slash.on = False

[/app1]
tools.trailing_slash.on = True
```
代码中这样用
```python
config = {'/':
    {
        'tools.trailing_slash.on': False,
    }
}
cherrypy.tree.mount(Root(), config=config)
```

###### 其他配置
也可以加其他配置，与上面所述配置区分开即可
```pyhton
[Databases]
driver: "postgres"
host: "localhost"
port: 5432
```
当然这些配置自己准备配置文件也可以

#### 用户session
session的使用就是要记住用户的一些设置或历史数据，主要是通过`cherrypy.session`这个字典完成
```python
import cherrypy

class Test(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, param='bingo'): #给定param参数
        ret = 'calling generate %s' % param
        cherrypy.session['buf'] = ret
        return ret

    @cherrypy.expose
    def display(self):
        return cherrypy.session['buf']


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    cherrypy.quickstart(Test(), '/', conf)
```

#### 多应用
单个应用的时候，我们通过
```python
cherrypy.quickstart(Blog())
```
启动应用，但是多个应用的时候这个函数的capacity不够，这时候用`cherrypy.tree.mount`函数，如下
```python
cherrypy.tree.mount(Blog(), '/blog', blog_conf)
cherrypy.tree.mount(Forum(), '/forum', forum_conf)

cherrypy.engine.start()
cherrypy.engine.block()
```
实现上，mount函数是把quickstart函数的返回结果当作一个参数使用，所以mount与quickstart并不互斥
