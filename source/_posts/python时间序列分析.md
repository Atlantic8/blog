---
title: python时间序列分析
date: 2016-08-15 19:06:30
tags: [python, time_series_data]
categories:
---

#### 基础工具
##### 基础工具类，datetime模块

|type|explanation|
|:--:|:---------:|
|date|以公历形式存储日历日期|
|time|以时、分、秒、毫秒形式存储时间|
|datetime|存储如期和时间|
|timedelta|两个datetime之间的差|

- datetime以毫秒形式存储日期和时间，datetime.timedelta表示两个datetime对象之间的时间差
- 可以给datetime加上、减去一个或者多个timedelta对象

```python
from datetime import datetime, timedelta
now = datetime.now()
now.year, now.month, now.day
$-> datetime.datetime(2016, 8, 4, 15, 14, 36, 899000)

# timedelta只有days和seconds这两个成员
delta = datetime(2011,7,2)-datetime(2011,7,1,9)
delta.days, delta.seconds
$-> (0, 54000)

delta = datetime(2011,7,2)-2*timedelta(10)

```
##### 字符串和datetime的相互转换
datetime -> string
- str方法
- strftime方法

```python
stamp = datetime(2011,8,1)
str(stamp)
$-> '2011-08-01 00:00:00'
stamp.strftime('%Y-%m-%d')
$-> '2011-08-01'
```

string -> datetime
- datetime.strptime
- dateutil的parser.parse方法，dateutil几乎可以理解所有人类能够理解的日期格式

```python
value = '2011-1-25'
# 返回一个datetime对象
datetime.strptime(value, '%Y-%m-%d')

from dateutil.parse import parse
parse('2011-03-12')
```

##### pandas中的时间数据处理
- pandas处理成组的时间数据
- 可以处理空值和非法值，用NaT表示
- 可能会把一些不是日期的字符串变成日期

```python
datestr = ['2011-04-12','2015-11-09']
pd.to_datetime(datestr)
```

#### 时间序列基础
```python
from datetime import datetime
dates = [datetime(2012,1,1), datetime(2012,1,2)]
# datetime对象放置在一个DatetimeIndex中，pandas会自动识别这个Series为时间序列数据
ts = Series(np.random.randn(2), index=dates)

# DatetimeIndex中的各个标量是pandas的TimeStamp对象
ts.index[0]
$-> Timestamp('2012-01-01 00:00:00')
```

##### 索引与子集
```python
# 可以传入被解释为日期的字符串来访问
ts['2012-01-01']

# 切片操作，可以传入‘年’或者‘年月’
# periods决定date_range的长度
longer_ts = Series(np.random.randn(1000), index=pd.date_range('1/1/2000',period=1000))

# 也可以像列表切片那样，可以传入字符串日期，datetime或TimeStamp对象
# 这样切片产生的是源数据的视图，与numpy数组的切片运算一致
ts[datetime(2011,1,7):] # 2011-1-7起的所有数据
ts['1/6/2011':'1/11/2011'] # 从[2011-1-6, 2011-1-11)的数据

ts.truncate(after='1/1/2011') # 也有类似的效果
```
在Series与DataFrame中均适用，只要设置index即可

##### 日期范围
###### date_range
- pandas.date_range(start=s, end=e, period=p, freq=f, normalize=True)
- [s, e)：决定了初始时间和结束时间
- p：周期值，决定日期长度
- f：决定频率，默认为'D',表示天。常用频率见下表，更详细的见书本314页
- normalize：True表示产生规范化到午夜的时间戳

|value|explanation|value|explanation|
|:---:|:---------:|:---:|:---------:|
|D|每日历日|B|每工作日|
|H|每小时|T or min|每分钟|
|S|每秒钟|L or ms|每毫秒|
|U|每微秒|M|每月最后一个日历日|
|BM|每月最后一个工作日|MS|每月第一个日历日|
|W-MON,W-TUE,..|从指定的星期几开始起的每一周|BMS|每月第一个工作日|
|Q-JAN,Q-FEB,..|从起始时间开始，每个季度最后一个月的最后一个工作日|WOM-1MON,WOM-2MON,..WOM-1FRI..|产生每月第x个星期几|

###### 日期偏移量
```python
from pandas.tseries.offsets import Hour,Minute
hour = Hour(4)
# 也可以更加简洁地使用freq参数
# freq = '1h30min'
pd.date_range('1/1/2011', '1/2/2011', freq='4h')
$-> DatetimeIndex(['2011-01-01 00:00:00', '2011-01-01 04:00:00',
                   '2011-01-01 08:00:00', '2011-01-01 12:00:00',
                      '2011-01-01 16:00:00', '2011-01-01 20:00:00',
                      '2011-01-02 00:00:00'],
                  dtype='datetime64[ns]', freq='4H')
```

###### 移动数据
- Series和DataFrame都有一个shift方法用于移动数据
- shift移动步长参数：正值后移，负值前移
- shift也可以带有参数 freq，这种情况下，数据不变，索引移动(正值前移)

```python
# 计算变化率
ts / ts.shift(1) - 1

ts.shift(2,freq='D')
```

- 日期偏移量可以做用在datetime或TimeStamp对象上
- 如果加的是锚点偏移量(如MonthEnd)，第一次会偏移到符合频率规则的下一日期
- 通过锚点偏移量的rollforward和rollback方法

```python
from pandas.tseries.offsets import Day, MonthEnd

now = datetime(2011,2,15)
now + MonthEnd()
$-> Timestamp('2011-02-28 00:00:00')
now + MonthEnd(2)
$-> Timestamp('2011-03-31 00:00:00')'

offset = MonthEnd()
offset.rollforward(now)
$-> Timestamp('2011-02-28 00:00:00')
offset.rollback(now)
$-> Timestamp('2011-01-31 00:00:00')
```

##### 时区处理
时间序列、日期范围和时间戳都可以从naive型转化为本地化时区意识型，也可以从一个时区转化为另一个时区
```python
import pytz
# 常用时区列表
pytz.common_timezones
# 获取时区对象
tz = pytz.timezone('UTC')
```
默认情况下，pandas中的时区是naive的，其索引的<b>tz字段</b>为None
所以在生成日期范围的时候可以加上一个时区信息,设置tz参数。也可以直接使用tz_localize方法
```python
pd.date_range('1/1/2001',period=10,tz='UTC')
# 完成本地化操作
ts_utc = ts.tz_localize('UTC')

# 时区转化
ts_utc.tz_convert('US/Eastern')

# 时间戳转换
stamp = pd.TimeStamp('2011-03-12 04:00')
stamp_utc = stamp.tz_localize('UTC')
stamp_eu = stamp.tz_convert('Europe/Moscow')

stamp_moscow = pd.TimeStamp('2011-03-12 04:00', tz='Europe/Moscow')
```

合并两个时间序列数据，时区不同时，结果自动转化为UTC时间。

##### 时期Period及其算术运算
- 时期Period表示的是时间区间，如数日、数月、数季、数年等，包含在pandas中
- 构造函数需要一个字符串或者整数，以及freq参数
- pandas.period_range函数，pandas.PeriodIndex函数

```python
# 这个Period表示的是从2007-1-1到2007-12-31日之间的整段时间
# 可以被看成一个被划分成多个月度时期的时间段中的游标
p = pd.Period(2007,freq='A-DEC')
# 与整数直接进行加、减法运算
p + 5
$-> Period('2012', 'A-DEC')

# Period对象之间的加、减法运算
# freq不同时会抛出异常
pd.Period('2014', freq='A-DEC') - p
$-> 7L

# 创建时期范围
pd.period_range('1/1/2000', '6/30/2000', freq='M')

values = ['2001Q3', '2002Q2', '2003Q1']
index = pd.PeriodIndex(values, freq='Q-DEC')
index $-> PeriodIndex(['2001Q3', '2002Q2', '2003Q1'], dtype='int64', freq='Q-DEC')
```

###### 时期的频率转换
Period和PeriodIndex对象都可以通过其asfreq方法被转换到其他频率
```python
p = pd.Period('2007', freq='A-DEC')
p.asfreq('M',how='start')
$-> Period('2007-01','M')
p.asfreq('M',how='end')
$-> Period('2007-12','M')
P.asfreq('B',how='start')
$-> Period('2007-01-01', 'B')

# 高频率转化为低频率
p = pd.Period('2007-08', 'M')
p.asfreq('A-JUN')
# 在频率A-JUN中，2007-08实际上是属于2008年
$-> Period('2008','A-JUN')

# 按季度计算的时期频率
# 频率为 Q-JAN,Q-FEB,Q-MAR,....Q-DEC, JAN starts from feb
p = pd.Period('2012Q4', freq='Q-JAN')
# 2012年Q4是从2011-11-01到2012-01-31
p.asfreq('D', 'start')
$-> Period('2011-11-01', 'D')
p.asfreq('D','e')
$-> Period('2012-01-31', 'D')

# TimeStamp和Period的相互转换
# to_timestamp()和to_period('freq')方法
ts = Series(np.random.randn(3), index=pd.date_range('1/1/2000',periods=3,freq='M'))
ts  $->
2000-01-31    2.375484
2000-02-29    0.726024
2000-03-31   -0.328938
Freq: M, dtype: float64

pts = ts.to_period()
pts $->
2000-01    2.375484
2000-02    0.726024
2000-03   -0.328938
Freq: M, dtype: float64

pts.to_timestamp(how='end')
$->
2000-01-31    2.375484
2000-02-29    0.726024
2000-03-31   -0.328938
Freq: M, dtype: float64
```

通过数组创建PeriodIndex
固定频率的数据集通常会将时间信息分开存放在多个列中，将这些数据以及频率传入PeriodIndex中就可以将它们合并成一个DataFrame索引
```python
# quarter表示季度
pd.PeriodIndex(year=data.year, quarter=data.quarter, freq='Q-DEC')
```

##### 重采样及频率转换
- 重采样指的是将时间序列从一个频率转换到另一个频率的处理过程
- 低频到高频称为升采样，反之为降采样
- pandas对象都有一个resample方法

|param|explanation|param|explanation|
|:---:|:---------:|:---:|:---------:|
|freq|表示重采样频率的字符串或DataOffset,'M','5min',Second(15)|how='mean'|产生聚合的函数名或数组函数，默认为mean，还有'first','last','ohlc','min'|
|axis=0|采样轴，默认为axis=0|fill_method=None|升采样时的插值方式，可取'ffill'或'bfill'|
|closed='right'|降采样中，时间段哪一端是闭合的|label='right'|降采样中聚合值的标签|
|loffset=None|面元标签的时间校正值，-1s(Second(-1))将时间调早1s|limit=None|向前、向后填充时，允许填充的最大时期数|
|kind=None|聚合到时期或时间戳，默认聚合到时间序列的索引类型|convention=None|重采样时期，低频到高频所采用的约定('start'/'end')，默认为'end'|

###### 降采样
```python
# 聚合到5min范围，聚合函数为'sum'求和
ts.resample('5min', how='sum')

ts.resample('5min', how='sum', closed='left', label='left', loffset='-1s')
```
OHLC重采样
- 经常应用于金融数据的采样方法，计算各面元的四个值，分别是第一个值（open/开盘）、最后一个值（close/收盘）、最大值（high/最高）、最小值（low/最低）
- 传入how='ohlc'即可得到含有这四种聚合值的DataFrame
- ts.resample('5min', how='ohlc')
- 也可以通过groupby进行重采样
- ts.groupby(lambda x: x.month).mean()
- ts.groupby(lambda x: x.weekday).mean()

###### 升采样
- 升采样过程中，不需要聚合，需要插值
- 既不是降采样也不是升采样的采样，需要传入新的频率 frame.resample('W-MON',fill_method='ffill')

```python
frame = DataFrame(np.random.randn(2,4),index=pd.date_range('1/1/2000',periods=2,freq='W-WED'),columns=['a','b','c','d'])
frame
$->               a         b         c         d
2000-01-05 -0.550387 -1.294863  0.274911  0.330741
2000-01-12  2.512896 -1.719330  0.090617  0.329635

# 设置fill_method为ffill或者bfill，不设置时，引入缺失值
# 如果设置limit值，则只填充limit行
frame.resample('D', fill_method='ffill', limit=4)
$->                a         b         c         d
2000-01-05 -0.550387 -1.294863  0.274911  0.330741
2000-01-06 -0.550387 -1.294863  0.274911  0.330741
2000-01-07 -0.550387 -1.294863  0.274911  0.330741
2000-01-08 -0.550387 -1.294863  0.274911  0.330741
2000-01-09 -0.550387 -1.294863  0.274911  0.330741
2000-01-10       NaN       NaN       NaN       NaN
2000-01-11       NaN       NaN       NaN       NaN
2000-01-12  2.512896 -1.719330  0.090617  0.329635
```

##### 绘图中的移动窗口函数
- 移动窗口上计算的各种函数也是一类常见于时间序列的数组变换，称之为移动窗口函数
- 它们接受TimeSeries或DataFrame对象，以及一个窗口长度。它们是pandas的函数

<center>移动窗口和指数加权函数</center>

|function|explanation|function|explanation|
|:------:|:---------:|:------:|:---------:|
|rolling_count|各窗口非NA观测值的数量|rolling_sum|窗口和|
|rolling_mean|窗口均值|rolling_median|窗口中位数|
|rolling_var,rolling_std|窗口无偏方差、标准差(n-1)|rolling_skew,rolling_kurt|窗口三阶矩(偏度)、四阶矩(峰度)|
|rolling_min,rolling_max|窗口的最值|rolling_quantile|窗口制定百分数、分位数位置的值|
|rolling_corr,rolling_cov|窗口的相关系数和协方差|rolling_apply|对窗口应用普通数组函数|
|ewma|指数加权移动平均|ewmvar,ewmstd|指数加权移动方差和标准差|
|ewmcorr,ewmcov|指数加权移动相关系数和协方差|||

这些函数均不考虑NA值，bottlenect则是NA友好的窗口移动函数集。
```python
# 窗口长度为250
pd.rooling_mean(data['col1'], 250, min_periods=10).plot()

# 将rolling_mean()函应用到所有列上,画出所有列对应的数据
expanding = lambda x : rolling_mean(x, len(x), min_periods=1)
pd.rolling_mean(data, 60).plot(logy=True)
```

###### 指数加权函数
- 通过定义一个衰减因子，decay factor，使得近期的观测值拥有更大的权重
- 衰减因子定义可以使用：时间间隔span，兼容于窗口大小等于时间间隔的简单移动窗口函数
- 具有较强的适应性

```python
pd.ewma(data['col1'], span=60).plot()
# ewmvar, ewmstd的使用同理
```

###### 二元移动窗口函数
- 作用在两个个序列上的函数，比如相关性计算和协方差计算

```python
pd.rolling_corr(series1, series2, 100, min_periods=100).plot()
# 计算一个序列与DataFrame的各个列的相关关系时
data = DataFrame(...)
pd.rolling_corr(data, series, 100, min_periods=100).plot()
```

###### 用户定义的移动窗口函数
- 使用rolling_apply()函数，需要自定义函数作为参数输入
- 自定义函数要求：能从数组的各个片段中产生单个值

```python
# percentileofscore(x,y)可用于计算样本x中特定值y的百分等级
from scipy.stats import percentileofscore
score_at_2percent = lambda x: percentileofscore(x, 0.02)
pd.rolling_apply(data['col'], 200, score_at_2percent)
```