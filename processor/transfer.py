import requests
import json
import base64

# path to image needs adjustment maybe direct camera output or something similar 
image_file = "MockImages\IR_7128.jpg"

with open(image_file, "rb") as f:
    image_data = f.read()

b64_image = base64.b64encode(image_data).decode("utf-8")

# payload with image data
payload = {
    "image": b64_image
}

# send POST req to /img endpoint
response = requests.post("http://localhost:8000/img", json=payload)

# check request
if response.status_code == 200:
    print("Image sent successfully")
else:
    print("Error sending image:", response.text)