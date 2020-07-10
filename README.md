# LiveOCR
[![version](https://img.shields.io/badge/version-v0.2-orange)]()

使用Python3、OpenCV、腾讯云OCR实现识别屏幕内容，对屏幕特定区域的元素（文字、关卡名、死亡瞬间）进行识别，转化为文字，输出到OBS。

## 前言

灵感来自于超级小桀的[直播间](https://www.douyu.com/74751)，希望桀哥湖南常杀人手下留情。

之前听到桀哥在咬咬牙环节，说他直播间上的关卡名和死亡数是通过图像识别实现的，我一个没学过1分钟 python 的文科生想硬着头皮试着自己做一下，花了1天+1个网上写出来这个项目。

**目前实现了根据用户提供的特定图片（如关卡读取标志、死亡标志等），自动定时检测目前屏幕画面是否存在此元素，进一步对屏幕的某一固定区域进行OCR识别，输出到 .txt 文件。简而言之就是能智能识别出关卡名等信息，并提供给OBS使用。**

## 用法

- 到[腾讯云](https://cloud.tencent.com/product/generalocr)注册账号，获取账号的 SecretID 和 SecretKEY。

- 安装 pip，Pillow，OpenCV：

  ```
  python3 -m pip install --upgrade pip
  pip install Pillow
  pip install opencv-python
  ```

- 修改 LiveOCR.py 中的 `path` 为自己存放截图和识别结果的目录地址。

- 修改 LiveOCR.py 中的 `SECRET_ID` 和 `SECRET_KEY` 为自己在腾讯云申请到的。

- 使用截图工具（以微信为例），获取你需要进行文字识别的区域坐标，填入 `Position`。

  - 保存需要读取文字的画面截图，尽量保持之后识别的过程中电脑也是类似画面。

  - 光标定位到文字的左上一些位置，此时的坐标分别填入`left`，`top`。

    ![Inked无标题_LI](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/screenshot_left.jpg)

  - 光标定位到文字的右下一些位置，此时的坐标分别填入`right`，`bottom`。

    ![screenshot_right](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/screenshot_right.jpg)

- 截取触发OCR的区域图片，另存为 /Capture/target.jpg 。之后每次画面出现这个内容，会自动对上一步选定的区域进行OCR文字识别。

  - 以欧卡2为例，我发现每次单人任务开始会出现这个标志，截图保存为target.jpg：

    ![target](https://cdn.jsdelivr.net/gh/tonyleelyy/BlogImages/img/target.jpg)

- 可以按照适合自己的情况设置全屏截图的间隔。

- 运行即可开始检测，自动输出图像匹配值。

- 在obs中添加从 /Capture/result.txt 文件中读取的 `文本（GDI+）`，即可实时显示文字结果。



## 开源相关

Python: https://www.python.org/

tencentcloud-sdk-python: https://github.com/TencentCloud/tencentcloud-sdk-python

PyPI: https://pypi.org/

Pillow: https://pillow.readthedocs.io/en/stable/

OpenCV: https://opencv.org/