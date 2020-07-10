from PIL import ImageGrab
import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.ocr.v20181119 import ocr_client, models 

path = 'D:\GitHub'
img_path = '%s/1.jpg'%(path)
txt_path = '%s/1.txt'%(path)

img = ImageGrab.grab(bbox=(0, 60, 200, 140))
img.save(img_path)

with open(img_path, 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    ImageBase64_value = 'data:image/jpeg;base64,%s'%s

try:
    cred = credential.Credential("AKIDB7nCLGEOaWIn1ONBCyUt50mKYWEgYqaA", "SgNo0YryyiDSQ8gy2xgBPSNgQw5xbzGW") 
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
    transjson = json.loads(result1)
    for item in transjson['TextDetections']:
        line1 = transjson['TextDetections'][0]['DetectedText']
        line2 = transjson['TextDetections'][1]['DetectedText']

    with open(txt_path,"w") as f:
        f.write("%s\n" %(line1))
        f.write("%s\n" %(line2))

except TencentCloudSDKException as err:
    print(err)