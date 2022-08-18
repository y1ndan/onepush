# onepush

A Python library to send notifications to your iPhone, Discord, Telegram, WeChat, QQ and DingTalk.

## Supported providers

[Bark](https://apps.apple.com/us/app/bark-customed-notifications/id1403753865), [Discord](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks), [Telegram](https://core.telegram.org/bots), [ServerChan](https://sc.ftqq.com/3.version), [ServerChanTurbo](https://sct.ftqq.com), [WechatWorkApp](https://work.weixin.qq.com/api/doc/90000/90135/90236), [WechatWorkBot](https://work.weixin.qq.com/api/doc/90000/90136/91770), [pushplus](https://www.pushplus.plus/doc), [go-cqhttp](https://docs.go-cqhttp.org), [Qmsg](https://qmsg.zendee.cn/api.html), [DingTalk](https://developers.dingtalk.com/document/app/custom-robot-access), [Lark](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN), [SMTP](https://docs.python.org/3/library/smtplib.html), Customised providers

## Installation

Via pip:

```
pip install onepush
```

Or via source code:

```
git clone https://github.com/y1ndan/onepush.git
cd onepush
python setup.py install
```

## Basic Usage

```python
from onepush import get_notifier

n = get_notifier('bark')
print(n.params)

response = n.notify(key='YOUR_BARK_KEY', title='OnePush', content='Hello World!')
print(response.text)

# {'required': ['key'], 'optional': ['title', 'content', 'sound', 'isarchive', 'icon', 'group', 'url', 'copy', 'autocopy']}
# {"code":200,"message":"success","timestamp":1633528319}
```

Or:

```python
from onepush import notify

notify('bark', key='YOUR_BARK_KEY', title='OnePush', content='Hello World!')
```

