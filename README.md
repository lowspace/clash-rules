# Python 脚本重构 `config.yaml`

## 简介

本项目适用于使用 macOS 的 [**Clash Premium 内核**](https://github.com/Dreamacro/clash/releases/tag/premium) 用户。该脚本允许用户将机场提供的代理节点提取出来放到了由脚本定义的`config.yaml`中。

脚本的一些特性：

+ 采用了 [clash-rules](https://github.com/Loyalsoldier/clash-rules) 规则集，是目前最全面和最强大的 Clash 规则了；
+ 区分了白名单（WhiteList）和黑名单（BlackList）方便用户切换模式：
  + 白名单：规则集内的按规则走，规则外的地址全走代理；
  + 黑名单：规则集内的按规则走，规则外的地址全直连。
+ 设定的测试的 url 是 `http://www.google.com.hk/`；
+ 进行五次测试，找出最佳的国内 DNS 地址，选取效果最好的前三个作为主力，剩下的留作备用，DNS 地址是:

    ``` python
    '223.5.5.5',
    '223.6.6.6',
    '119.29.29.29',
    '119.28.28.28',
    '114.114.114.114',
    '114.114.115.115',
    ```

## 文件介绍

`parser.py`:

+ 调用 `dns_helper.sh` 进行 DNS 五次并行测速并提取结果；
+ 读取用户名，找到 clash 的设置文件夹位置并读取机场所提供的`jichang.yaml` 文件；
+ 设置 `config.yaml`:
  + 配置 DNS 相关参数；
  + 设置规则集；
  + 设置黑白名单
+ 将配置信息写入`config.yaml`中。

`dns.helper.sh`:

+ 对一系列的 DNS 地址进行测速，目标地址有：

  ``` python
  'www.google.com amazon.com',
  'facebook.com',
  'www.youtube.com',
  'www.reddit.com',
  'wikipedia.org', 
  'twitter.com', 
  'gmail.com', 
  'telegram.org', 
  'whatsapp.com'
  ```

+ 输出该 DNS 地址对各个目标节点的测速平均值。
