from webpage_to_image import get_image
from gpt_functions import encode_image, summarize_image
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

get_image('https://www.lovebonito.com/sg/abilene-square-neck-knit-dress.html')
summarize_image(encode_image('webpage_screenshot.png'), ['Product Type', 'Colour', 'Price'])
