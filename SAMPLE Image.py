from PIL import Image
import requests
from io import BytesIO
url = "https://rlv.zcache.com/happy_smiley_face_round_stickers-rbdcd90a58b8e40a9b895e7c2fd1e65ef_v9waf_8byvr_540.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
