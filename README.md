BJTU抢课脚本


[项目地址](https://github.com/aosiweixin/BJTU-CC)||[博客地址](http://www.auswitz.top/2021/11/27/BJTU%E9%80%89%E8%AF%BE%E5%86%B2%E5%86%B2%E5%86%B2/)

## 依赖

主要单独需要下载一个selenium用于模拟浏览器，安装起来稍微有一点麻烦，要注意对应版本，网上搜教程就好啦~~

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
import base64
import json
import requests
```

## 使用

第一部分需要修改这些参数

```
type = 1  # 1为本方案课程 2为其他方案课程
type2 = 1  # 1为搜索 0为不搜索
user_id_str = '1928****'  # 学号
password_str = '********'  # 密码
xpath_str = ''
delta = 0.9
course_number = 'A121006B'
```

自动读取验证码需要使用[图鉴](http://www.ttshitu.com/)的api

进入图鉴之后，注册账号

[![](https://pic.imgdb.cn/item/61a2456d2ab3f51d9138e3dd.jpg)](https://pic.imgdb.cn/item/61a2456d2ab3f51d9138e3dd.jpg)

非常便宜，充值1元可以用四年。

[图鉴使用文档](http://www.ttshitu.com/docs/python.html#pageTitle)

```python
import base64
import json
import requests
# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


if __name__ == "__main__":
    img_path = "C:/Users/Administrator/Desktop/file.jpg"
    result = base64_api(uname='你的账号', pwd='你的密码', img=img_path, typeid=3)
    print(result)
```

也可以选择不使用自动识别（自动识别稍微有一点慢，需要看运气）

如果可以抽空盯着，看到验证码弹出来手输也还可以。

但最近选课平台没开就没法贴使用截图了，但在上学期期末，已经测试好了，可用！

