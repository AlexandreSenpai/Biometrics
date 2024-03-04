import cv2
from PIL import Image
import numpy as np

def process_image(img: bytes):
    nparr = np.frombuffer(img, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (256, 400))

    cv2.normalize(image, image, alpha=0, beta=200, norm_type=cv2.NORM_MINMAX)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return Image.fromarray(image)