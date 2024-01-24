from webpage_to_image import get_image
from image_summary import encode_image, summarize_image
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print(summarize_image(encode_image('webpage_screenshot.png'), ['Product Name', 'Price']))

