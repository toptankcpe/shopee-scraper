# app/scraping/abstract_scraper.py

class AbstractScraper:
    """
    Template Method for Scrape
    """
    def scrape(self):
        self.before_scrape()
        self.do_scrape()
        self.after_scrape()

    def before_scrape(self):
        pass

    def do_scrape(self):
        raise NotImplementedError("Please implement do_scrape() in subclass")

    def after_scrape(self):
        pass
