import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"
scraped_books = [] # List untuk menyimpan data buku

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')

    if books:
        for book in books:
            title_tag = book.find('h3').find('a')
            price_tag = book.find('p', class_='price_color') # Asumsi ada elemen harga
            rating_tag = book.find('p', class_='star-rating') # Asumsi ada elemen rating

            title = title_tag['title'] if title_tag else 'N/A'
            price = price_tag.text.strip() if price_tag else 'N/A'
            # Mengambil kelas rating (one, two, etc.) dan mengubahnya ke angka jika perlu
            rating = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else 'N/A'

            scraped_books.append({
                'Judul Buku': title,
                'Harga': price,
                'Rating': rating
            })
    else:
        print("Tidak ada buku ditemukan di halaman ini.")

    # --- Ini adalah bagian penting untuk membuat DataFrame ---
    if scraped_books: # Pastikan ada data sebelum membuat DataFrame
        df = pd.DataFrame(scraped_books)
        df.to_csv('buku.csv', index=False, encoding='utf-8')
        print("Data berhasil disimpan ke buku.csv")
    else:
        print("Tidak ada data untuk disimpan ke CSV.")

except requests.exceptions.RequestException as e:
    print(f"Error saat membuat permintaan: {e}")
except Exception as e:
    print(f"Terjadi kesalahan lain: {e}")
