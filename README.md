# Stock Data Scraper

## Project Overview

This project is a web scraping tool designed to extract stock data from financial websites like Investing.com using Selenium and Python. It dynamically retrieves key financial metrics such as the following:

- **Price Range**
- **Technical Analysis**
- **Analyst Sentiment**
- **Upside/Downside Percentage**
- **ProTips**
- **1-Year Change**
- **Market Cap**
- **P/E Ratio**
- **EPS**
- **Dividend Yield**
- **Beta**
- **Next Earnings Date**

The project is built to handle dynamic and JavaScript-heavy pages, ensuring that the data is extracted only when the page is fully loaded and ready for interaction. It also includes robust error handling to account for edge cases where data might not be available in the expected format.

## Features

- **Custom Page Load Strategy:** Utilizes a custom page load strategy to wait for the page to be in an `interactive` or `complete` state before attempting to scrape data, ensuring higher reliability when dealing with dynamic content.
- **Dynamic Data Extraction:** Efficiently extracts stock data from web pages by identifying HTML elements based on their XPath and class names.
- **Edge Case Handling:** The scraper is designed to account for variations in data presentation, such as different formats of the Dividend Yield, ensuring accurate data collection across multiple cases.
- **Timeout Management:** Implements a timeout mechanism to avoid the script hanging on slow or unresponsive pages.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/stock-data-scraper.git
   ```
   
2. **Install the Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver:**
   Ensure that you have [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and that it's compatible with your version of Google Chrome.

4. **Run the Script:**
   ```bash
   python stock_scraper.py
   ```

## Usage

1. **Customize the URLs:** 
   Update the script with the specific stock URLs you wish to scrape data from.

2. **Run the Script:**
   Execute the script to start scraping data. The extracted data will be displayed in the console and can also be stored in a file for further analysis.

3. **Handling Edge Cases:**
   The script includes logic to handle different formats of financial data presentation, such as handling cases where `Dividend Yield` is displayed without parentheses.

## Dependencies

- **Python 3.7+**
- **Selenium**
- **ChromeDriver**

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to reach out to me at [your.email@example.com](mailto:your.email@example.com).
