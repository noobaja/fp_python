import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_page(self, path=""):
        """Mengambil halaman web dari URL."""
        url = f"{self.base_url}{path}"
        try:
            print(f"Mengambil halaman: {url}")
            response = self.session.get(url)
            response.raise_for_status()  # Raise error jika status bukan 200
            return response.text
        except requests.RequestException as e:
            print(f"Error saat mengambil halaman: {e}")
            return None

    def parse_html(self, html_content, tag, class_name=None):
        """Mem-parse HTML dan mengembalikan elemen berdasarkan tag dan kelas."""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            if class_name:
                elements = soup.find_all(tag, class_=class_name)
            else:
                elements = soup.find_all(tag)
            return elements
        except Exception as e:
            print(f"Error saat mem-parse HTML: {e}")
            return []

    def extract_links(self, html_content):
        """Mengambil semua tautan (link) dari halaman."""
        soup = BeautifulSoup(html_content, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def scrape_data(self, path, tag, class_name=None):
        """Menggabungkan semua langkah untuk scraping data tertentu."""
        html_content = self.fetch_page(path)
        if html_content:
            return self.parse_html(html_content, tag, class_name)
        return []

if __name__ == "__main__":
    base_url = input("Masukkan URL: ")

    scraper = WebScraper(base_url)

    page_content = scraper.fetch_page()
    if page_content:
        quotes = scraper.parse_html(page_content, "span", "text")
        for idx, quote in enumerate(quotes, start=1):
            print(f"Kutipan {idx}: {quote.text}")

    links = scraper.extract_links(page_content)
    print("\nTautan yang ditemukan:")
    for link in links:
        print(link)
