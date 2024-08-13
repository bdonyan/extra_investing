import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
import threading

# Initialize undetected ChromeDriver with custom options
def _get_custom_page_load_strategy(driver, url: str) -> None:
    driver.get(url)
    start_time = time.time()
    while time.time() - start_time < 30:
        if driver.execute_script(
            "return document.readyState == 'complete' || document.readyState == 'interactive'"
        ):
            return
        time.sleep(1)
    raise TimeoutError()

# Setup Chrome options to avoid issues with page loading
def setup_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.page_load_strategy = 'none'  # disable page load strategy
    driver = uc.Chrome(options=chrome_options, use_subprocess=True)
    return driver

driver = setup_driver()

def press_escape_key_periodically():
    while True:
        try:
            print("Pressing Escape...")
            actions = ActionChains(driver)  # Create an ActionChains instance
            actions.send_keys(Keys.ESCAPE).perform()  # Perform the escape key action
        except Exception as e:
            print(f"Failed to send Escape key: {e}")
        time.sleep(2)  # Adjust the interval as needed

# Start the thread to press the Escape key periodically
escape_thread = threading.Thread(target=press_escape_key_periodically)
escape_thread.daemon = True
escape_thread.start()

def extract_additional_info(url, symbol, name):
    print(f"Navigating to URL: {url}")
    actions = ActionChains(driver)
    try:
        _get_custom_page_load_strategy(driver, url)  # Custom page load strategy
        print("URL loaded successfully")
    except Exception as e:
        print(f"Failed to load URL: {e}")
        return None

    info = {"URL": url, "Symbol": symbol, "Name": name}
    print(info)

    try:
        print("Waiting for page to load")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[class*="text-left"]'))
        )
        print("Progress Made")

        actions.send_keys(Keys.ESCAPE).perform()
        # Extract 52-week range
        try:
            week_range_elements = driver.find_elements(By.CSS_SELECTOR, 'dd[data-test="weekRange"] span.key-info_dd-numeric__ZQFIs')
            if len(week_range_elements) >= 2:
                info['52 wk range start'] = week_range_elements[0].text.strip()
                info['52 wk range end'] = week_range_elements[1].text.strip()
                print(f"52 wk range: {info['52 wk range start']} - {info['52 wk range end']}")
            else:
                info['52 wk range start'] = None
                info['52 wk range end'] = None
        except Exception as e:
            print(f"Failed to extract 52 wk range: {e}")
            info['52 wk range start'] = None
            info['52 wk range end'] = None

        actions.send_keys(Keys.ESCAPE).perform()
        try:
            # First attempt: Common detailed view
            try:
                # Locate the element containing the Technical Analysis header
                tech_analysis_header = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Technical Analysis"]'))
                )
                # Locate the following element that contains the result
                tech_analysis_result = tech_analysis_header.find_element(By.XPATH, '../following-sibling::div[contains(@class, "text-")]')
                info['Technical Analysis'] = tech_analysis_result.text.strip()

            except Exception:
                # Second attempt: Summary view with broader search
                tech_analysis_result = driver.find_element(By.XPATH, '//div[contains(@class, "rounded-full") and contains(@class, "px-4") and contains(@class, "py-1.5")]')
                info['Technical Analysis'] = tech_analysis_result.text.strip()

            print(f"Technical Analysis: {info['Technical Analysis']}")
            
        except Exception as e:
            print(f"Failed to extract Technical Analysis: {e}")
            info['Technical Analysis'] = None
        
        # Attempt to extract Analysts Sentiment, but handle cases where it might not exist
        try:
            analysts_sentiment_header = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Analysts Sentiment"]'))
            )
            analysts_sentiment_result = analysts_sentiment_header.find_element(By.XPATH, '../following-sibling::div[contains(@class, "text-") and contains(@class, "font-bold")]')
            info['Analysts Sentiment'] = analysts_sentiment_result.text.strip()
            print(f"Analysts Sentiment: {info['Analysts Sentiment']}")
        except Exception as e:
            print(f"Analysts Sentiment not available")
            info['Analysts Sentiment'] = None

        # Extract the Upside value
        try:
            # Locate the Upside label first
            upside_label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Upside")]'))
            )
            
            # Find the following sibling element that contains the upside value
            # Here, we assume that the upside value is always located within a span or div following the Upside label
            upside_value = upside_label.find_element(By.XPATH, './following::span[contains(text(), "%")]')

            # Store the extracted Upside value in info
            info['Upside'] = upside_value.text.strip()
            print(f"Upside: {info['Upside']}")
            
        except Exception as e:
            print(f"Failed to extract Upside: {e}")
            info['Upside'] = None

        try:
            # Locate the ProTips label
            protips_label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "ProTips")]'))
            )
            
            # Find the container that follows the ProTips label
            protips_text_container = protips_label.find_element(By.XPATH, '../../../following::div[1]')
            
            # Extract the text from the identified container
            protips_text = protips_text_container.text.strip()
            print(f"ProTips: {protips_text}")
            
            info['ProTips'] = protips_text

        except Exception as e:
            print(f"Failed to extract ProTips: {e}")
            info['ProTips'] = None

        # Extract 1-Year Change
        try:
            # Locate the "1-Year Change" label
            one_year_change_label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "1-Year Change")]'))
            )
            
            # Find the value following the "1-Year Change" label
            one_year_change_value = one_year_change_label.find_element(By.XPATH, '../following-sibling::dd//span[@class="key-info_dd-numeric__ZQFIs"]').text.strip()
            
            # Print and store the value
            print(f"1-Year Change: {one_year_change_value}")
            info['1-Year Change'] = one_year_change_value

        except Exception as e:
            print(f"Failed to extract 1-Year Change: {e}")
            info['1-Year Change'] = None

        # Extract Market Cap
        try:
            # Locate the "Market Cap" label
            market_cap_label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Market Cap")]'))
            )
            
            # Find the value following the "Market Cap" label
            market_cap_value = market_cap_label.find_element(By.XPATH, '../following-sibling::dd//span[@class="key-info_dd-numeric__ZQFIs"]').text.strip()
            
            # Print and store the value
            print(f"Market Cap: {market_cap_value}")
            info['Market Cap'] = market_cap_value

        except Exception as e:
            print(f"Failed to extract Market Cap: {e}")
            info['Market Cap'] = None

    except Exception as e:
        print(f"Failed to extract additional info from {url}: {e}")

    return info

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('company_links.csv')
    detailed_data = []
    time.sleep(2)

    for _, row in df.iterrows():
        company_info = extract_additional_info(row['URL'], row['Symbol Name'], row['Company Name'])
        if company_info:
            detailed_data.append(company_info)

    detailed_df = pd.DataFrame(detailed_data)
    detailed_df.to_csv('detailed_company_data.csv', index=False)
    print("Detailed company data saved to detailed_company_data.csv")

    driver.quit()
