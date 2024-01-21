import os
print(os.environ.get('HEROKU_APP_DEFAULT_DOMAIN_NAME'))

from webpage_to_image import get_image
from image_summary import encode_image, summarize_image
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

get_image('https://www.lovebonito.com/sg/mira-knit-midi-dress.html')

print(summarize_image(encode_image('webpage_screenshot.png')))

