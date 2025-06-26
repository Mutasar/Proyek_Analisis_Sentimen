from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_tokopedia_reviews(product_url, max_pages=3):
    options = Options()
    options.headless = True  # Jalankan tanpa tampilan GUI
    driver = webdriver.Firefox(options=options)

    driver.get(product_url)
    time.sleep(5)  # Tunggu halaman dan JS load

    wait = WebDriverWait(driver, 15)
    reviews = []

    for _ in range(max_pages):
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='review-item']")))
        except:
            print("Timeout: Elemen ulasan tidak ditemukan.")
            break

        soup = BeautifulSoup(driver.page_source, "html.parser")
        review_items = soup.select("div[data-testid='review-item']")

        for item in review_items:
            user = item.select_one("div[data-testid='review-author-name']")
            user = user.text.strip() if user else None

            rating_svg = item.select_one("div[data-testid='review-rating'] svg")
            rating = int(rating_svg['aria-label'][0]) if rating_svg and rating_svg.has_attr('aria-label') else None

            content = item.select_one("div[data-testid='review-content']")
            content = content.text.strip() if content else None

            date = item.select_one("time")
            date = date.text.strip() if date else None

            reviews.append({
                "user": user,
                "rating": rating,
                "content": content,
                "date": date
            })

        # Klik tombol Load More jika ada
        try:
            load_more = driver.find_element(By.CSS_SELECTOR, "button[data-testid='btn-load-more']")
            load_more.click()
            time.sleep(3)
        except:
            print("Tidak ada tombol Load More atau sudah halaman terakhir.")
            break

    driver.quit()
    return pd.DataFrame(reviews)

# Ganti dengan URL produk Tokopedia yang ingin Anda scrape ulasannya
url_produk = "https://gql.tokopedia.com/graphql/ShopReviewList"
df_ulasan = scrape_tokopedia_reviews(url_produk, max_pages=3)
print(df_ulasan.head())
df_ulasan.to_csv("ulasan_tokopedia.csv", index=False)
