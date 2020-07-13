# LiveOCR
[![version](https://img.shields.io/badge/version-v0.3-orange)]()

使用Python3、OpenCV、腾讯云OCR实现识别屏幕内容，对屏幕特定区域的元素（文字、关卡名、死亡瞬间）进行识别，转化为文字，输出到OBS。

## 前言

灵感来自于超级小桀的[直播间](https://www.douyu.com/74751)，希望桀哥湖南常杀人手下留情。

之前听到桀哥在咬咬牙环节，说他直播间上的关卡名和死亡数是通过图像识别实现的，我一个没学过1分钟 python 的文科生想硬着头皮试着自己做一下，花了一天一夜写出来这个项目。

**目前实现自动识别画面中的读盘画面、死亡信息，可分别实时输出为 .txt 文本，供OBS使用**

## 更新日志

2020-07-13：增加了死亡数统计功能，并添加了更多可供用户调节的参数。修正README。（感谢 [Jackie1123](https://github.com/Jackie1123)）

## 参数说明
- `path = '*'` 存储文件的文件夹
- `second = 5` 全屏截图检测的频率，单位：秒，默认值5
- `mode = 1` 模式选择，"1"只进行OCR；"2"只进行死亡数统计，"3"分别输出OCR结果和死亡数
- `reset = 1` 重置选项，"1"运行时清除所有内容；"2"运行时不清除旧内容，默认值1
- `Position` OCR识别区域坐标，`left` `top` `right` `bottom` 分别为`左`、`上`、`右`、`下`的像素坐标
- `match = 0.9` 识别匹配度判断值，默认值0.9，若提供的 target 图片在屏幕中的匹配度大于这个值，则进行后续OCR、死亡统计等操作


## 用法

- 到[腾讯云](https://cloud.tencent.com/product/generalocr)注册账号，获取账号的 SecretID 和 SecretKEY，分别填入`SECRET_ID` 和 `SECRET_KEY` 。

- 为 Python 安装 pip，Pillow，OpenCV：

  ```
  python3 -m pip install --upgrade pip
  pip install Pillow
  pip install opencv-python
  ```

- 使用截图工具（以微信为例），在全屏画面中定位你需要进行文字识别的区域坐标，填入`Position`

  - 光标定位到文字的左上一些位置，此时的坐标分别填入`left`，`top`。

      ![Inked无标题_LI](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/screenshot_left.jpg)

  - 光标定位到文字的右下一些位置，此时的坐标分别填入`right`，`bottom`。

      ![screenshot_right](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/screenshot_right.jpg)

- 截取读盘、死亡画面的关键元素，分别保存为 `target_ocr.jpg`、`target_death.jpg`，放入 path 参数所填的文件夹中。之后每次画面出现这些内容，会自动对上一步选定的区域进行OCR文字识别，或累计死亡数。

  - 以欧卡2为例，我发现每次单人任务读盘会出现这个标志，截图保存为target_ocr.jpg：

    ![target](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/target.jpg)
    
  - 死亡画面同理，截图游戏中的死亡提示，保存为target_death.jpg

- 运行即可开始检测，自动输出图像匹配值。

- 在obs中添加从 /Capture目录下的 .txt 文件中读取的 `文本（GDI+）`，即可实时显示文字结果。

## 开源相关

Python: https://www.python.org/

tencentcloud-sdk-python: https://github.com/TencentCloud/tencentcloud-sdk-python

PyPI: https://pypi.org/

Pillow: https://pillow.readthedocs.io/en/stable/

OpenCV: https://opencv.org/