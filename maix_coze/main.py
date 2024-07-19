import requests, json, time, os,re
from maix import camera, display, image

print(os.getcwd())
print(os.path.abspath(os.path.dirname(__file__)))
print(os.listdir('.'))

start_time = time.time()
token = 'pat_YLqsHDMrl4P46OoQOjMgwFYKdo7h5S6tcSz9TEXgbiIw4OvJ4g8vNM1q5La0UHDy'

cam = camera.Camera(480, 320)
print("=============================== -- camera init ok")

disp = display.Display(640, 480)
print("=============================== -- display init ok")

img = cam.read()
for i in range(3):
    img = cam.read()
    disp.show(img, fit=image.Fit.FIT_CONTAIN)

img.save("/tmp/captured_image.jpg")
file_path = "/tmp/captured_image.jpg"

upload_url = "https://api.coze.cn/v1/files/upload"

upload_headers = {
    'Authorization': f'Bearer {token}',
}
files = {
    'file': ('captured_image.jpg', open(file_path, 'rb'), 'image/jpeg')
}

upload_response = requests.post(upload_url, headers=upload_headers, files=files)
upload_response_data = upload_response.json()
file_id = upload_response_data.get('data', {}).get('id')

if not file_id:
    print("文件上传失败")
else:
    api_url = 'https://api.coze.cn/v3/chat'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "bot_id": "7388444168786018367",
        "user_id": "Ljj_926",
        "stream": True,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": json.dumps([{"type": "image", "file_id": file_id}, {"type": "text", "text": "简单描述这张图"}]),
                "content_type": "object_string"
            }
        ]
    }

response = requests.post(api_url, headers=headers, data=json.dumps(payload))

response.encoding = 'utf-8'

response_text = response.text
match = re.search(r'response_for_model\\":\\"(.*?)\\"', response_text)
if match:
    response_for_model = match.group(1)
    print(response_for_model)
else:
    print(response_text)

end_time = time.time()
run_time = end_time - start_time
print(f"运行时间: {run_time:.2f} 秒")

while 1:
    img = cam.read()
    disp.show(img)
