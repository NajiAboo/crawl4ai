import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

url = "https://medium.com/about"

async def main():

    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.8, threshold_type="fixed")
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        markdown_generator=md_generator
    )

    browswer_config = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browswer_config) as crawler:

        restult = await crawler.arun(
            url=url, 
            config=run_config
        )

        print("Row markdown length: ", len(restult.markdown))
        print("Fit markdwon: ", len(restult.markdown_v2.fit_markdown))
        print(restult.markdown_v2.fit_markdown)


if __name__=="__main__":
    asyncio.run(main())