from bs4 import BeautifulSoup
import requests
from PIL import Image
from pytesseract import pytesseract
headers = {'User-Agent': 'Mozilla/5.0'}

# GET request
url = 'https://sandbox.dereuromark.de/sandbox/captchas/math'
response = requests.get(url, headers= headers)

# Getting image from Captcha
soup = BeautifulSoup(response.text, "html.parser")
image_url = soup.find('label', {'for': 'captcha-result'}).img['src']
print(image_url)
with open('image.svg', "wb") as f:
    f.write(requests.get(image_url).content)

# Improving quality of image to extract text with more accuracy
black = (0,0,0)
white = (255,255,255)
threshold = (160,160,160)

# Open input image in grayscale mode and get its pixels.
img = Image.open("image.svg").convert("LA")
pixels = img.getdata()
newPixels = []
# Compare each pixel
for pixel in pixels:
    if pixel < threshold:
        newPixels.append(black)
    else:
        newPixels.append(white)

# Create and save new image with improved quality.
newImg = Image.new("RGB",img.size)
newImg.putdata(newPixels)
newImg.save("newImage.jpg")

# Image.open('newImage.png').convert('RGB').save('image1.jpg', quality=95)

# Extract text from image
text = pytesseract.image_to_string(Image.open('newImage.jpg'))
print(text)

