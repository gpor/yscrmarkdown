from playwright.async_api import async_playwright
import pprint
import json

async def node_to_dict(element):
    allowed_tags = ["body", "div", "main", "ul", "li",
                    "h1", "h2", "h3", "h4", "h5", "h6", "p",
                    "section", "article", "header", "footer", "nav",
                    "table", "thead", "tbody", "tr", "th", "td",
                    "pre", "code", "blockquote",
                    # "hr", "br",
                    ]

    dom = await element.evaluate(
        """(el, allowed) => {
            const inline = ["strong", "em", "b", "i", "span", "a"];
            function walk(node) {
                if (node.nodeType === 3) { // text node
                    return null;
                }

                if (node.nodeType === 1) { // element node
                    let tag = node.tagName.toLowerCase();

                    // Skip disallowed tags entirely
                    if (!allowed.includes(tag) && !inline.includes(tag)) {
                        return null;
                    }

                    // If it's an inline tag, flatten it: return its children directly
                    if (inline.includes(tag)) {
                        let children = [];
                        node.childNodes.forEach(child => {
                            let c = walk(child);
                            if (c) {
                                // Inline child might be array (flatten)
                                if (Array.isArray(c)) {
                                    children.push(...c);
                                } else {
                                    children.push(c);
                                }
                            }
                        });
                        return children.length ? children : null;
                    }

                    // Normal allowed block-level element
                    let obj = { el: tag };

                    // direct text children only
                    const directText = Array.from(node.childNodes)
                        .filter(c => c.nodeType === 3 && c.nodeValue.trim())
                        .map(c => c.nodeValue.trim())
                        .join(" ");
                    if (directText) obj.text = directText;

                    let children = [];
                    node.childNodes.forEach(child => {
                        let c = walk(child);
                        if (c) {
                            if (Array.isArray(c)) {
                                children.push(...c);
                            } else {
                                children.push(c);
                            }
                        }
                    });

                    if (children.length) obj.children = children;
                    return obj;
                }
                return null;
            }
            return walk(el);
        }""",
        allowed_tags
    )
    return dom

async def walk_dom(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        body = await page.query_selector("body")
        dom = await node_to_dict(body)
        await browser.close()
        return dom

class Url_iterator_pw:
    def __init__(self, urls):
        self.urls = urls

    async def crawl(self):
        for url in self.urls:
            dom = await walk_dom(url)
            text_json = json.dumps(dom, indent=2)
            yield url, text_json
            



# async def scrape_dom_walk_pw(urls):
#     results = {}
#     for url in urls:
#         print(f"Scraping {url}...")
#         dom = await walk_dom(url)
#         results[url] = dom
#         print(f"Done scraping {url}.")
#     print('results:')
#     pprint.pprint(results)
#     return results