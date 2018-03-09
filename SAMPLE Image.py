from PIL import Image
import requests
from io import BytesIO

url = input("url of image: ")
print("Retreving image . . .")

url = "https://rlv.zcache.com/happy_smiley_face_round_stickers-rbdcd90a58b8e40a9b895e7c2fd1e65ef_v9waf_8byvr_540.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
print("Image retrieved\n\tsource width  : {}px\n\tsource height : {}px\n".format(img.width, img.height))

targetWidth = int(input("Target width(32 for solo, 43 for team): "))
maxHeight = int(input("Max height(default is 73): "))
print("Processing . . .")
targetHeight = min(round(float(targetWidth*img.height)/img.width), maxHeight)
img.resize((targetWidth, targetHeight), Image.LANCZOS)
print("Image processed\n\tprint width  : {} blocks\n\tprint height : {} blocks\n".format(targetWidth, targetHeight))
