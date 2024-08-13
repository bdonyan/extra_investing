from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import threading 

service = Service('chromedriver.exe')  # Ensure the path to your ChromeDriver is correct
driver = webdriver.Chrome(service=service)
driver.maximize_window()

def press_escape_key_periodically():
    while True:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(5)  # Adjust the interval as needed

# Start the thread to press Escape key periodically
escape_thread = threading.Thread(target=press_escape_key_periodically)
escape_thread.daemon = True
escape_thread.start()

# def press_escape_key():
#     webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# def handle_popups():
#     while True:
#         popups_detected = False
#         try:
#             sign_up_popup = WebDriverWait(driver, 0.5).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="signup"]'))
#             )
#             press_escape_key()
#             popups_detected = True
#             print("Pressed escape for sign-up pop-up.")
#         except Exception as e:
#             print("No sign-up pop-up found or failed to close it.")

#         try:
#             general_popup = WebDriverWait(driver, 0.5).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'button2'))
#             )
#             press_escape_key()
#             popups_detected = True
#             print("Pressed escape for general pop-up.")
#         except Exception as e:
#             print("No general pop-up found or failed to close it.")

#         try:
#             sidebar_overlay_lightbox = WebDriverWait(driver, 0.5).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='sidebar-overlay-lightbox']"))
#             )
#             press_escape_key()
#             popups_detected = True
#             print("Pressed escape for sidebar overlay lightbox.")
#         except Exception as e:
#             print("No sidebar overlay lightbox found or failed to close it.")
        
#         if not popups_detected:
#             break

def click_next_page():
    skip_button = True
    while skip_button:
        try:
            # Check and click the Skip button if it appears
            skip_button = WebDriverWait(driver, 0.5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-73lxnr'))
            )
            skip_button.click()
            print("Clicked Skip button.")
        except Exception as e:
            skip_button = False
            print("No Skip button found or failed to click it.")

    try:
        # Check and click the Close button if it appears
        close_button = WebDriverWait(driver, 0.5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-us0nsg'))
        )
        close_button.click()
        print("Clicked Close button.")
    except Exception as e:
        print("No Close button found or failed to click it.")

    try:
        next_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Next']]"))
        )
        next_button.click()
        print("Clicked next page button.")
        return True
    except Exception as e:
        print(f"Failed to click next page button: {e}")
        return False

def extract_company_links():
    company_data = []
    print("Extracting company links from current page")
    # handle_popups()
    
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr')
    for row in rows:
        try:
            symbol_name = row.find_element(By.CSS_SELECTOR, 'a[class*="leading-3.5"]').text
            company_name =  row.find_elements(By.CSS_SELECTOR, 'td')[0].text.strip()
            base_url = row.find_element(By.CSS_SELECTOR, 'a[class*="leading-3.5"]').get_attribute('href')

            industry_element = row.find_elements(By.CSS_SELECTOR, 'td')[3]
            industry = industry_element.text.strip()
            
            company_data.append({"Symbol Name": symbol_name, "Company Name": company_name, "URL": base_url, "Industry": industry})
            print(f"Extracted: {symbol_name}, {company_name}, {base_url}, {industry}")
        except Exception as e:
            print(f"Failed to extract company data for a row: {e}")
            continue

    return company_data

def scraping():
    page_counter = 1
    all_data = []
    while True:
        print(f"Scraping page {page_counter}")
        # handle_popups()

        try:
            first_company = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class*="leading-3.5"]'))
            ).text
            if first_company == 'AAPL' and page_counter != 1:
                print("AAPL detected on a non-first page, stopping scraping.")
                break
        except Exception as e:
            print(f"Failed to detect first company name: {e}")

        data = extract_company_links()
        all_data.extend(data)

        if not click_next_page():
            pass # handle_popups()
        else:
            page_counter += 1
        time.sleep(1)
    return all_data

if __name__ == "__main__":
    driver.get("https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1")
    time.sleep(2)
    all_data = scraping()
    print(all_data)
    
    df = pd.DataFrame(all_data)
    df.to_csv('company_links.csv', index=False)
    print("Company links saved to company_links.csv")

    driver.quit()