import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_dynamic_quotes():
    """
    Scrapes quotes from a JS-rendered page with infinite scroll.
    Demonstrates handling dynamic content similar to modern e-commerce sites.
    """
    # Configure Chrome for headless scraping (faster, no GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    data = []
    
    try:
        url = "http://quotes.toscrape.com/js/"  # Safe test site with JS rendering
        driver.get(url)
        
        # Handle Infinite Scroll
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for AJAX load
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Extract structured data
        quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
        for quote in quotes:
            text = quote.find_element(By.CSS_SELECTOR, "span.text").text
            author = quote.find_element(By.CSS_SELECTOR, "small.author").text
            tags = [tag.text for tag in quote.find_elements(By.CSS_SELECTOR, "a.tag")]
            
            data.append({
                "Quote": text.replace('"', '').replace('...', ''),
                "Author": author,
                "Tags": ", ".join(tags)
            })
            
    except Exception as e:
        print(f"Scraping Error: {e}")
    finally:
        driver.quit()
    
    # Save to CSV (Standard deliverable format)
    df = pd.DataFrame(data)
    df.to_csv("scraped_quotes.csv", index=False)
    print(f"Successfully scraped {len(data)} records.")
    return df

if __name__ == "__main__":
    scrape_dynamic_quotes()