from webpage_to_image import get_image
from image_summary import encode_image, summarize_image
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

get_image('https://www.nike.com/sg/t/air-jordan-1-low-shoes-6Q1tFM/553558-161')

print(summarize_image(encode_image('webpage_screenshot.png')))