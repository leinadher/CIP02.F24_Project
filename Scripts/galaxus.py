import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

#create dataframe
df = pd.DataFrame(columns=["brand", "model", "price", "memory", "screen", "camera", "network", "color", "date"])

# Number of elements to load
num_phones = 15
url = f"https://www.galaxus.ch/en/s1/producttype/smartphones-24"
driver.get(url)

# Give website time to load

phones = driver.find_elements(By.CLASS_NAME, 'sc-c228a714-1 elDjrO')
print(len(phones))

