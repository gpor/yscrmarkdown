from playwright.async_api import async_playwright
import json
from pathlib import Path

async def node_to_dict(element):
    allowed_tags = ["body", "div", "main", "ul", "li",
                    "h1", "h2", "h3", "h4", "h5", "h6", "p",
                    "section", "article", "header", "footer", "nav",
                    "table", "thead", "tbody", "tr", "th", "td",
                    "pre", "code", "blockquote",
                    # "hr", "br",
                    ]
    js_file = Path("js/dom_walker2.js")
    js_code = js_file.read_text()
    dom = await element.evaluate(
        js_code,
        allowed_tags
    )
    return dom

async def walk_dom(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        response = await page.goto(url)
        status = response.status if response else None
        if status != 200:
            await browser.close()
            return {"status": status}
        body = await page.query_selector("body")
        dom = await node_to_dict(body)
        await browser.close()
        return dom

class Url_iterator_pw:
    def __init__(self, urls, output_format):
        self.urls = urls
        self.output_format = output_format

    async def crawl(self):
        for url in self.urls:
            dom = await walk_dom(url)
            if isinstance(dom, dict) and "status" in dom:
                output_text = f"HTTP status: {dom['status']}"
            elif self.output_format == 'yaml':
                import yaml
                output_text = yaml.dump(dom, sort_keys=False)
            else:
                output_text = json.dumps(dom, indent=2)
            yield url, output_text