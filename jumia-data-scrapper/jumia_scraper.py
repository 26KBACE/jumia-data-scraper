# 1. Import all necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# 2. Setup ChromeDriver
options = Options()
options.add_argument("--headless")  # Browser runs in background
service = Service("chromedriver.exe")  # Make sure this file is in your folder
driver = webdriver.Chrome(service=service, options=options)

# 3. Define list to hold data
products = []

# 4. Loop through multiple pages (pagination)
for page in range(1, 4):  # Change range to scrape more or fewer pages
    url = f"https://www.jumia.co.ke/catalog/?q=laptop&page={page}"
    driver.get(url)
    time.sleep(5)  # Wait for page to load completely

    # 5. Extract product data
    items = driver.find_elements(By.CSS_SELECTOR, "article.prd")
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "h3.name").text
            price = item.find_element(By.CSS_SELECTOR, "div.prc").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

            products.append({
                "Product Name": name,
                "Price": price,
                "URL": link
            })
        except Exception as e:
            print("Skipping item due to error:", e)

# 6. Close the browser
driver.quit()

# 7. Convert list to DataFrame
df = pd.DataFrame(products)

# 8. Clean the data
df.drop_duplicates(inplace=True)
df['Price'] = df['Price'].str.replace("KSh", "").str.replace(",", "").str.strip()

# 9. Export to CSV
df.to_csv("jumia_laptops.csv", index=False)

# 10. Export to Excel (optional)
df.to_excel("jumia_laptops.xlsx", index=False)

# 11. Print confirmation
print("✅ Scraping complete. Files saved: jumia_laptops.csv and jumia_laptops.xlsx")
# Basic insights
print("\n--- Basic Analysis ---")
print("Total products scraped:", len(df))
print("Top 5 most expensive products:")
print(df.sort_values(by="Price", ascending=False).head(5))

print("\nTop 5 cheapest products:")
print(df.sort_values(by="Price", ascending=True).head(5))
driver.save_screenshot("jumia_screenshot.png")
