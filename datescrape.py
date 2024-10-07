import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the chromedriver
path_to_chromedriver = r'C:\Users\samra\OneDrive\Desktop\drivers\chromedriver.exe'
s = Service(path_to_chromedriver)
driver = webdriver.Chrome(service=s)

# Target URL
url = 'https://in.investing.com/commodities/iron-ore-62-cfr-futures-historical-data'
driver.get(url)

# Wait for the date picker to be clickable using CSS selector
date_picker = WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flex.flex-1.flex-col.justify-center.text-sm.leading-5.text-[#333]"))
)
date_picker.click()

# Wait for the "1 Year" option to be clickable using CSS selector
# Note: Replace the class name with the actual class that contains the "1 Year" option.
one_year_option = WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-value='1 Year']"))  # Adjust based on actual attribute
)
one_year_option.click()

# Wait for the table to reload with updated data
WebDriverWait(driver, 40).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.freeze-column-w-1.w-full.overflow-x-auto.text-xs.leading-4"))
)

# Find the table with historical price data
table = driver.find_element(By.CSS_SELECTOR, "table.freeze-column-w-1.w-full.overflow-x-auto.text-xs.leading-4")
headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]
headers = [header.replace("Price", "Iron Ore Price") for header in headers]

# Get all table rows except header
rows = table.find_elements(By.TAG_NAME, "tr")[1:]

# Open CSV to write data
with open("iron_ore_data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text.strip() for cell in cells]
        writer.writerow(data)

# Get the absolute path of the CSV file
relative_path = "iron_ore_data.csv"
absolute_path = os.path.abspath(relative_path)
print("CSV saved at: " + absolute_path)

# Close the browser
driver.quit()
