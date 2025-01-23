url = "https://www.amazon.com/s?k=iphone"

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json


async def extract_amazon_products():
    browswer_config = BrowserConfig(
        browser_type="chromium",
        headless=True
    )

    crawler_config = CrawlerRunConfig(
        extraction_strategy= JsonCssExtractionStrategy(
            schema={
                "name": "Amazon product search result",
                "baseSelector": "[data-component-type='s-search-result']",
                "fields": [

                    {
                        "name": "title",
                        "selector":"h2 span",
                        "type": "text"

                    },
                    {
                        "name": "image",
                        "selector": ".s-image",
                        "type": "attribute",
                        "attribute": "src"
                    },
                    {
                        "name": "rating",
                        "selector": ".a-icon-star-small .a-icon-alt",
                        "type": "text"
                    },
                    {
                        "name": "reviews_count",
                        "selector": "[data-csa-c-func-deps=aui-da-a-popover]",
                        "type": "text"
                    },
                    {
                        "name": "price",
                        "selector": ".a-price .a-offscreen",
                        "type": "text"
                    }
                ]
            }
        )
    )

    async with AsyncWebCrawler(config=browswer_config) as crawler:
        result = await crawler.arun(url=url, config=crawler_config, cache_mode=CacheMode.BYPASS)

        if result and result.extracted_content:
            products = json.loads(result.extracted_content)
            print(len(products))
            for product in products:
                print("\n Product Details:")
                print(f"Title:  {product.get('title')}")
                print(f"Price: {product.get('price')}")
                print(f"Rating: {product.get('rating')}")
                print(f"Image: {product.get('image')}")
                print(f"Review Count: {product.get('reviews_count')}")
                print("-" * 80)

if __name__== "__main__":
    import asyncio
    asyncio.run(extract_amazon_products())