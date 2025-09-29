from playwright.async_api import async_playwright
import json
from pathlib import Path

async def node_to_dict(element, js_walker=None):
    # allowed_tags = ["body", "div", "main", "ul", "li",
    #                 "h1", "h2", "h3", "h4", "h5", "h6", "p",
    #                 "section", "article", "header", "footer",
    #                 "table", "thead", "tbody", "tr", "th", "td",
    #                 "pre", "code", "blockquote",
    #                 # "hr", "br", "nav",
    #                 ]
    js_file = Path(f"js/walker/{js_walker or 'default'}.js")
    js_code = js_file.read_text()
    dom = await element.evaluate(
        js_code,
    )
    return dom

async def walk_dom(url, auth=None, js_walker=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        if auth:
            username, password = auth
            context = await browser.new_context(
                http_credentials={'username': username, 'password': password}
            )
        else:
            context = await browser.new_context()
        page = await context.new_page()
        response = await page.goto(url)
        status = response.status if response else None
        if status != 200:
            await context.close()
            await browser.close()
            return {"status": status}
        body = await page.query_selector("body")
        dom = await node_to_dict(body, js_walker)
        await context.close()
        await browser.close()
        return dom

class Url_iterator_pw:
    def __init__(self, urls, output_format, auth=None, js_walker=None):
        self.urls = urls
        self.output_format = output_format
        self.auth = auth
        self.js_walker = js_walker

    async def crawl(self):
        for url in self.urls:
            dom = await walk_dom(url, self.auth, self.js_walker)
            if isinstance(dom, dict) and "status" in dom:
                output_text = f"HTTP status: {dom['status']}"
            elif self.output_format == 'yaml':
                import yaml
                output_text = yaml.dump(dom, sort_keys=False)
            else:
                output_text = json.dumps(dom, indent=2)
            yield url, output_text