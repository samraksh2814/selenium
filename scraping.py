import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


# Path to the chromedriver
path_to_chromedriver = r'C:\Users\samra\OneDrive\Desktop\drivers\chromedriver.exe'
s = Service(path_to_chromedriver)

# Initialize webdriver
driver = webdriver.Chrome(service=s, options=Options())

# Target URL
url = 'https://in.investing.com/commodities/iron-ore-62-cfr-futures-historical-data'
driver.get(url)

# Wait until the table with prices is available
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.freeze-column-w-1.w-full.overflow-x-auto.text-xs.leading-4"))
)

table = driver.find_element(By.CSS_SELECTOR, "table.freeze-column-w-1.w-full.overflow-x-auto.text-xs.leading-4")

headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]

headers = [header.replace("Price", "Iron Ore Price") for header in headers]

rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row

# Open CSV to write data
with open("iron_ore_data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    # Write headers
    writer.writerow(headers)
    
    # Write row data
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
