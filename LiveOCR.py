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
    img_path = '%s/screen.jpg'%(path) # 全屏截图文件名
    ocr_area = '%s/ocrarea.jpg'%(path) # 文字识别区域截图文件名
    traget_path = '%s/target.jpg'%(path) # 图像模板截图文件名
    txt_path = '%s/result.txt'%(path) # 输出文字结果文件名
fp = FilePath()

# 腾讯云Key
class KEY:
    SECRET_ID = "yourid"
    SECRET_KEY = "yourkey"
k = KEY()

# 隔多少秒全屏截图一次
second = 5

# OCR识别区域坐标
class Position:
    left = 820 # 识别区域的左侧坐标
    top = 900 # 识别区域的顶部坐标
    right = 1200 # 识别区域的右侧坐标
    bottom = 940 # 识别区域的底部坐标
p = Position()

# 保存OCR区域截图
def picocr():
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
        result1 = resp.to_json_string()
        
        with open(fp.txt_path,"w", encoding='utf-8') as f:
            transjson = json.loads(result1)
            for item in transjson['TextDetections']:
                line1 = item['DetectedText']
                f.write("%s\n" %(line1))
    
    except TencentCloudSDKException as err:
        print(err)

# 保存全屏截图，并输出相似度
while True:
    time.sleep(second)
    screen = ImageGrab.grab()
    screen.save(fp.img_path)
    
    cvscreen = cv2.imread(fp.img_path, 0)
    cvtarget = cv2.imread(fp.traget_path, 0)
    cvres = cv2.matchTemplate(cvscreen, cvtarget, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cvres)
    strmin_val = float(max_val)
    print(strmin_val)

    if strmin_val > 0.9:
        picocr()