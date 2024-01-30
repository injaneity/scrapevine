from app import celery  # Import Celery instance from your main app module

if __name__ == '__main__':
    celery.worker_main()

# get_image('https://www.lovebonito.com/sg/abilene-square-neck-knit-dress.html')
# summarize_image(encode_image('webpage_screenshot.png'), ['Product Type', 'Colour', 'Price'])