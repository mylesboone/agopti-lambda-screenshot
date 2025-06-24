from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import random
import time

def handler(event=None, context=None):
    url = event['url']
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={event['x_pixels']}x{event['y_pixels']}")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--hide-scrollbars')

    chrome = webdriver.Chrome(options=options, service=service)
    chrome.get(url)
    time.sleep(random.uniform(int(event['low_sleep']), int(event['high_sleep'])))

    encoded_image = chrome.get_screenshot_as_base64()

    chrome.quit()

    return { 'statusCode': 200, 'body': { 'encoded_image': encoded_image } }
