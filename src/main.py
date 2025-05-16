import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# Setup Selenium options
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(), options=options)   

urls = [
    "https://www.amazon.in/Rockerz-450-Wireless-Bluetooth-Headphone/dp/B07PR1CL3S/ref=sr_1_3?dib=eyJ2IjoiMSJ9.dgKDtT8X6ZGiRIleF-lFoEvg2JqIJtMzMT2LSZUi6sB3PJhA_PkuQ27YUoBZebn8pnq-7ARSUsamZ7igFXseNmaw29JtMg-NBeDzipqQkfc-9mILgXbuw5vXujSrAcxbxOX5IuJ-y9nRU0VEqh_nfIzamLIRPHVL5f2XxwiEOgEgNAmY1GTY4tcEVnoiarlkaB8X9L98k2FUWQ4Oukt3D2B76tcKRAWi3tIBVO2a_bc.T2ARiAB6KAgDH_jRiIFp9iKkmGxBkMH2z5pfOjauD2U&dib_tag=se&keywords=wireless%2Bheadphones&qid=1747354850&sr=8-3&th=1",
   "https://www.flipkart.com/boat-rockerz-450-w-40mm-drivers-15-hrs-playback-soft-padded-earcups-bluetooth/p/itm077a566bd128b?pid=ACCFEHZ8GSGWMMSD&lid=LSTACCFEHZ8GSGWMMSDXS5YX5&marketplace=FLIPKART&q=boAt+Rockerz+450&store=0pm%2Ffcn&spotlightTagId=default_BestsellerId_0pm%2Ffcn&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=32ab5d28-b521-4b1a-8f51-5cc2e6645cbb.ACCFEHZ8GSGWMMSD.SEARCH&ppt=sp&ppn=sp&ssid=8n1apwino00000001747355452853&qH=19f48aed180493f3",
   
]

products_data = []
try:
    for url in urls:
        driver.get(url)
        time.sleep(3) 
        if "amazon" in url:
            title = driver.find_element(By.ID,"productTitle").text
            price = driver.find_element(By.CLASS_NAME,"a-price-whole").text
            rating = driver.find_element(By.CLASS_NAME,"a-color-base").text
            reviews = driver.find_element(By.ID,"acrCustomerReviewText").text
            products_data.append({
                "site": "Amazon",
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
            
                
            })
        
        if "flipkart" in url:
                title = driver.find_element(By.CLASS_NAME,"VU-ZEz").text
                price = driver.find_element(By.CLASS_NAME,"CxhGGd").text
                rating = driver.find_element(By.CLASS_NAME,"XQDdHH").text
                reviews =  40,644 
                products_data.append({
                    "site": "Flipkart",
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                })
    print(products_data)
except Exception as e:
    print(f"An error occurred: {e}")

driver.quit()

# Create DataFrame
df = pd.DataFrame(products_data)
# Save to CSV
df.to_csv("aggregated_products.csv", index=False)
print("Data saved to aggregated_products.csv")
df['price'] = df['price'].replace('[₹,]', '', regex=True).astype(float)

# Create bar chart
plt.figure(figsize=(6, 4))
plt.bar(df['site'], df['price'], color='skyblue')
plt.title('Price Comparison by Site')
plt.xlabel('Site')
plt.ylabel('Price (INR)')
plt.tight_layout()
plt.savefig("price_comparison.png")
print("Chart saved as price_comparison.png")
   