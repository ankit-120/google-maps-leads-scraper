from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape_maps(query):

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 15)

    driver.get(f"https://www.google.com/maps/search/{query}")

    # Wait for listings to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))

    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

    print("Scrolling results...")

    # Scroll multiple times to load more businesses
    for _ in range(10):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            scrollable_div
        )
        time.sleep(2)

    listings = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")

    print("Total listings found:", len(listings))

    results = []

    for i in range(len(listings)):

        listings = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")

        try:
            listings[i].click()
        except:
            continue

        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
            )
        except:
            continue

        time.sleep(1)

        # NAME
        try:
            name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
        except:
            name = ""

        # RATING
        try:
            rating = driver.find_element(By.CSS_SELECTOR, "div.F7nice span").text
        except:
            rating = ""

        # REVIEWS
        try:
            reviews = driver.find_element(By.CSS_SELECTOR, "div.F7nice span:nth-child(2)").text
        except:
            reviews = ""

        # ADDRESS
        try:
            address = driver.find_element(
                By.XPATH,
                '//button[@data-item-id="address"]//div[contains(@class,"fontBodyMedium")]'
            ).text
        except:
            address = ""

        # PHONE
        try:
            phone = driver.find_element(
                By.XPATH,
                '//button[contains(@data-item-id,"phone")]//div[contains(@class,"fontBodyMedium")]'
            ).text
        except:
            phone = ""

        # WEBSITE
        try:
            website = driver.find_element(
                By.XPATH,
                '//a[@data-item-id="authority"]'
            ).get_attribute("href")
        except:
            website = ""

        results.append({
            "Name": name,
            "Rating": rating,
            "Reviews": reviews,
            "Phone": phone,
            "Website": website,
            "Address": address
        })

        print(f"{i+1}. {name}")

    driver.quit()

    df = pd.DataFrame(results)
    df.to_excel("leads.xlsx", index=False)

    print("Saved leads.xlsx")


scrape_maps("dentists in chennai")