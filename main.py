import argparse
from app.scraping.shopee_scraper import ShopeeScraper
from app.scraping.models import ScrapeParams

def main():
    parser = argparse.ArgumentParser(description="Shopee Scraper")
    parser.add_argument("--username", type=str, required=True, help="Shopee username")
    parser.add_argument("--password", type=str, required=True, help="Shopee password")
    parser.add_argument("--keyword", type=str, required=True, help="Search keyword")
    parser.add_argument("--numpage", type=int, default=None, help="Number of page")
    parser.add_argument("--itemperpage", type=int, default=None, help="Items per page")
    
    args = parser.parse_args()
    
    params = ScrapeParams(
        username=args.username,
        password=args.password,
        keyword=args.keyword,
        numpage=args.numpage,
        itemperpage=args.itemperpage
    )
    
    scraper = ShopeeScraper(
        username=params.username,
        password=params.password,
        keyword=params.keyword,
        numpage=params.numpage,
        itemperpage=params.itemperpage

    )

    scraper.scrape()

if __name__ == "__main__":
    main()
