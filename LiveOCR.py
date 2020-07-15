from PIL import ImageGrab
import base64
import json
import time
import cv2
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.ocr.v20181119 import ocr_client, models 

# 文件保存地址
class FilePath:
    path = 'D:\GitHub\LiveOCR\Capture' # 存储文件的文件夹
    img_path = '%s/screen.jpg'%(path)
    ocr_area = '%s/ocrarea.jpg'%(path)
    traget_ocr_path = '%s/target_ocr.jpg'%(path)
    traget_death_path = '%s/target_death.jpg'%(path)
    txt_ocr_path = '%s/result_ocr.txt'%(path)
    txt_death_path = '%s/result_death.txt'%(path)
fp = FilePath()

# 腾讯云Key
class KEY:
    SECRET_ID = "yourid"
    SECRET_KEY = "yourkey"
k = KEY()

# 检测频率，单位：秒，默认值5
second = 5

# 检测延迟，在输出结果后停止检测一定时间，单位：秒
delay_ocr = 10 # OCR输出后的延迟，默认值10
delay_death = 10 # 死亡数输出后的延迟，默认值10

# 模式选择，"1"只进行OCR；"2"只进行死亡数统计，"3"同时输出OCR结果和死亡数
mode = 1

# 运行时重置文本内容，"1"清除所有内容；"2"不清除旧内容
reset = 1

# OCR识别区域坐标
class Position:
    left = 820 # 识别区域的左侧坐标
    top = 900 # 识别区域的顶部坐标
    right = 1200 # 识别区域的右侧坐标
    bottom = 940 # 识别区域的底部坐标
p = Position()

# 识别匹配度，默认0.9，匹配度大于这个值则进行后续操作
match = 0.9

# 清除所有文本内容
def resetall():
    with open(fp.txt_ocr_path, 'w') as file:
        file.truncate(0)
    with open(fp.txt_death_path, 'w') as file:
        file.truncate(0)

if reset == 1:
    resetall()

# OCR流程
class Orecognition():
    ocrresult = 0
    def picocr(self):
        ocrarea = ImageGrab.grab(bbox=(p.left, p.top, p.right, p.bottom))
        ocrarea.save(fp.ocr_area)
        with open(fp.ocr_area, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            ImageBase64_value = 'data:image/jpeg;base64,%s'%s

        try:
            cred = credential.Credential(k.SECRET_ID, k.SECRET_KEY) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.ap-guangzhou.tencentcloudapi.com"
        
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile) 
        
            req = models.GeneralBasicOCRRequest()
            params = '{"ImageBase64":"' + ImageBase64_value + '"}'
            req.from_json_string(params)

            resp = client.GeneralBasicOCR(req) 
            Orecognition.ocrresult = resp.to_json_string()

            with open(fp.txt_ocr_path,"w", encoding='utf-8') as f:
                transjson = json.loads(ocrresult)
                for item in transjson['TextDetections']:
                    line = item['DetectedText']
                    f.write("%s\n" %(line))
    
        except TencentCloudSDKException as err:
            print(err)

# 死亡数统计流程
class Drecognition():
    deathcount = 0
    def death(self):
        Drecognition.deathcount += 1

    def deathsave(self):
        with open(fp.txt_death_path,"w", encoding='utf-8') as f:
            f.write("死亡数：%s" %(Drecognition.deathcount))

# 保存全屏截图，输出相似度，判断
while True:
    time.sleep(second)
    screen = ImageGrab.grab()
    screen.save(fp.img_path)
    strmaxocr_val = 0
    strmaxdeath_val = 0

    def cvocr():
        cvscreen = cv2.imread(fp.img_path, 0)
        cvtargetocr = cv2.imread(fp.traget_ocr_path, 0)
        cvresocr = cv2.matchTemplate(cvscreen, cvtargetocr, cv2.TM_CCOEFF_NORMED)
        min_val, maxocr_val, min_loc, max_loc = cv2.minMaxLoc(cvresocr)
        global strmaxocr_val
        strmaxocr_val = float(maxocr_val)

    def cvdeath():
        cvscreen = cv2.imread(fp.img_path, 0)
        cvtargetdeath = cv2.imread(fp.traget_death_path, 0)
        cvresdeath = cv2.matchTemplate(cvscreen, cvtargetdeath, cv2.TM_CCOEFF_NORMED)
        min_val, maxdeath_val, min_loc, max_loc = cv2.minMaxLoc(cvresdeath)
        global strmaxdeath_val
        strmaxdeath_val = float(maxdeath_val)
    
    if mode == 1:
        cvocr()
        print("\nOCR触发匹配度：%s" %(strmaxocr_val))
        if strmaxocr_val > match:
            print("OCR目标识别成功！")
            oc = Orecognition()
            oc.picocr()
            time.sleep(delay_ocr)
    
    if mode == 2:
        cvdeath()
        print("\n死亡触发匹配度：%s" %(strmaxdeath_val))
        if strmaxdeath_val > match:
            print("死亡信息识别成功！")
            dr = Drecognition()
            dr.death()
            dr.deathsave()
            time.sleep(delay_death)
    
    if mode == 3:
        cvocr()
        print("\nOCR触发匹配度：%s" %(strmaxocr_val,))
        if strmaxocr_val > match:
            print("OCR目标识别成功！")
            oc = Orecognition()
            oc.picocr()
            time.sleep(delay_ocr)
        
        cvdeath()
        print("死亡触发匹配度：%a" %(strmaxdeath_val))
        if strmaxdeath_val > match:
            print("死亡信息识别成功！")
            dr = Drecognition()
            dr.death()
            dr.deathsave()
            time.sleep(delay_death)