import cv2
from PIL import Image
import numpy as np

def process_image(img: bytes):
    nparr = np.frombuffer(img, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 400))

    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.equalizeHist(image)

    return Image.fromarray(image)