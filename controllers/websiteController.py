# controller.py
from services.websiteService import WebsiteService

class WebsiteController:

    def __init__(self):
        self.title = None
        self.text = None

    def extract_text(self, url):
        return WebsiteService.extract_content_from_url(url)