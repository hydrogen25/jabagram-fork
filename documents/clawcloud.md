# Jabagram桥接机器人免费部署教程

## 准备工作

- 一个可以访问墙外网站的设备
- 一个Github账户，要求注册超过180天（否则只能使用一个月）

## 准备机器人账户

### 准备Telegram机器人

按照以下教程注册机器人，之后复制好机器人Token令牌

<https://www.telegrambcn.com/jiaocheng/288.html>

### 准备XMPP账户

注册一个XMPP账户，建议使用下面列表中A分级的服务器

<https://providers.xmpp.net/>

**⚠️请注意 桥接机器人不能在Conversations服务器上被注册，并且需要桥接的群也不能在Conversation服务器上**

记下**机器人的JID（形如[example@foo.bar](mailto:example@foo.bar)）和密码**

## 注册ClawCloud账户

在  <https://run.claw.cloud/> 主页选择Get Started，登陆方式**选择Github**，并用一个注册**超过180天的Github账户**登录

## 配置ClawCloud容器

进入ClawCloud面板后，推荐选择新加坡区，之后选择App Launchpad，之后点击右上角的Create App，按照以下要求填写表单

- Application Name填入jabagram
- Image选择Public，ImageName填入 `hydrogenx/jabagram:latest`
- Usagea选择Fixed，Replicas选择1，CPU选择0.5，Memory选择1G
- Network保持默认
- Advanced中的Commands输入 `python jabagram.py --token=上面Telegram机器人的Token --jid=上面XMPP机器人的JID --password=上面XMPP机器人的密码`，其余保持默认

![681f176caf8d5.png](https://cdn-fusion.imgcdn.store/i/2025/3cd0925ace7cbdc8.png)

当你完成表单后，**右上角点击Apply Applications**即可部署

## 建立桥接桥

如果你看到此处，你已经完成了以上步骤，但此时桥接机器人仍没有运行，因为我们还需要告诉机器人要桥接那两个群，请按照以下步骤建立桥接桥

在这些步骤开始前，你需要记下需要桥接的XMPP房间的JID，一般这些JID长这样

> [exampleroom@muc.5222.de](mailto:exampleroom@muc.5222.de) 或者  [exampleroom@conference.macaw.me](mailto:exampleroom@conference.macaw.me)

### Telegram群组

将你创建的Telegram机器人拉入群组，保证机器人可以正常发言

输入 `/jabagram 你的XMPP房间JID` 来完成桥接

此时Telegram机器人会返回一条消息

### XMPP群组

你必须使用gajim客户端作为所有者进入你的群组页面

执行 `/invite 机器人JID SUxvdmVYTVBQ`完成桥接

此时你的群成员列表会多出一个叫Telegram Bridge 的参与者，赋予成员权限来允许机器人发言，完成此步后即可完成部署
