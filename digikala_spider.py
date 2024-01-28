import scrapy
from scrapy.http import Request, Response
from pathlib import path

class DigikalaSpider(scrapy.Spider):
    name = 'product_digikala2'
    
    def parse_vendors(self, response: Response) -> None:
        vendors = json.loads(response.text)
        vendors = vendors["data"]["widgets"][5]["data"]["categories"]
        vendor_codes = [vendor["code"] for vendor in vendors]
        
        for code in vendor_codes:
            if code == "laptop":
                laptop_url = f"https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno=1&sortby=4"
                yield scrapy.Request(url=laptop_url, callback=self.parse_brands)
                # Save the webpage HTML to a file
                self.save_page(response, 'vendor_laptops.html')

    def save_page(self, response: Response, filename: str) -> None:
        path = Path('saved_pages')
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / filename
        with open(file_path, 'wb') as file:
            file.write(response.body)

    def parse_product_detail(self, response: Response) -> None:
        data = json.loads(response.text)
        # Process data as needed...
        # For example, let's say you extract the product details into a dictionary:
        product_details = {
            'name': data['data']['name'],
            'price': data['data']['price'],
            'description': data['data']['description'],
            # Add more fields as needed...
        }
        self.save_json(product_details, f"laptop_{product_details['name']}.json")

    def save_json(self, data: dict, filename: str) -> None:
        path = Path('saved_data')
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / filename
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)