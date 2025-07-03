# website_extraction_service.py

from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class WebsiteService:

    def extract_article_links(self, url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]

            # crude filter to avoid ads, navigation etc.
            if any(x in href for x in ["/202", "/news", "/article", "/world"]) and not href.startswith("#"):
                full_url = href if href.startswith("http") else requests.compat.urljoin(url, href)
                links.add(full_url)

        return list(links)
    
    def extract_content_from_url(self, url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup.body(["script", "style", "img", "input"]):
            tag.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
        return text
    

    def extract_articles_from_homepage(self, url, maximum_news):
        article_links = self.extract_article_links(url)[:maximum_news]
        articles = []

        for link in article_links:
            try:
                text = self.extract_content_from_url(link)
                if len(text.split()) > 100:  # crude filter: avoid blank or nav pages
                    articles.append({
                        "url": link,
                        "content": text
                    })
            except Exception as e:
                continue  # skip failed ones

        return articles