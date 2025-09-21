from playwright.sync_api import sync_playwright

def node_to_dict(element):
    return element.evaluate("""(el) => {
        function walk(node) {
            let obj = { el: node.tagName.toLowerCase() };
            let children = [];
            node.childNodes.forEach(child => {
                if (child.nodeType === 1) { // element
                    children.push(walk(child));
                }
            });
            if (children.length) obj.children = children;
            return obj;
        }
        return walk(el);
    }""")

def walk_dom(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        dom = node_to_dict(page.query_selector("body"))
        browser.close()
        return dom