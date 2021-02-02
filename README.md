# simpleTranslate
简单的翻译工具，使用pyqt和百度翻译api，仅支持翻译成中文

#### 使用
0. 支持选择百度api或有道api:
    - 百度：需要创建config文件，写入接口需要的百度开发者相关信息，第一行是appid，第二行是密钥
    - 有道：有道api的apikey是网上搜的，不需要另外配置。
1. 取词方式：
    - 剪贴板：勾选“剪贴板”选框，复制文本即为选词并翻译。
    - 快捷键：勾选“Alt+T”选框，选中文本后按Alt+T组合键。目前仅支持x11的linux(ubuntu)。需要pip安装pyqtkeybind。

#### 截图
![image](https://github.com/xing2387/simpleTranslate/blob/main/Screenshot.png)

#### 相关
百度翻译api文档：https://api.fanyi.baidu.com/doc/21