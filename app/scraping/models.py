# app/scraping/models.py
from pydantic import BaseModel, validator

class ProductData:
    """
    Model ProductData
    """
    def __init__(self, product_id, product_name, product_description, price_range,
                 total_quantity, category_path, url, variants, rating, seller):
        self.id = product_id
        self.name = product_name
        self.description = product_description
        self.price = {
            "range": {
                "min": price_range[0],
                "max": price_range[1]
            },
            "currency": "THB"
        }
        self.totalQuantity = total_quantity
        self.categoryPath = category_path
        self.url = url
        self.variants = variants
        self.rating = rating
        self.seller = seller


class ScrapeParams(BaseModel):
    username: str
    password: str
    keyword: str
    numpage: int
    itemperpage: int

    @validator("numpage")
    def numpage_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("numpage must be greater than 0")
        return v

    @validator("itemperpage")
    def itemperpage_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("itemperpage must be greater than 0")
        return v