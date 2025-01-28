from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/')
def home():
    youtube_data = scrape_youtube()
    amazon_data = scrape_amazon()
    return render_template('home.html', youtube_data=youtube_data, amazon_data=amazon_data)

def get_driver():
    """Initialize Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_youtube():
    url = 'https://www.youtube.com/results?search_query=lofi'
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load
        video_elements = driver.find_elements(By.CSS_SELECTOR, '#video-title')
        video_titles = [video.text for video in video_elements if video.text]
        return video_titles if video_titles else ["No data found (YouTube content is dynamic)"]
    except Exception as e:
        return [f"Error fetching data from YouTube: {e}"]
    finally:
        driver.quit()

def scrape_amazon():
    url = 'https://www.amazon.in/s?rh=n%3A976419031%2Cn%3A1458204031&dc&qid=1738081651&rnid=976419031&ref=sr_nr_n_4'
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.a-size-base-plus')
        product_names = [product.text for product in product_elements if product.text]
        return product_names if product_names else ["No data found (Amazon content is dynamic)"]
    except Exception as e:
        return [f"Error fetching data from Amazon: {e}"]
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
