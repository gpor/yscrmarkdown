
async def node_to_dict(element):
    allowed_tags = ["body", "div", "main", "ul", "li",
                    "h1", "h2", "h3", "h4", "h5", "h6", "p", "a",
                    # "strong", "em", "b", "i", "span",
                    "section", "article", "header", "footer", "nav",
                    "table", "thead", "tbody", "tr", "th", "td",
                    "pre", "code", "blockquote",
                    "hr", "br",
                    ]

    dom = await element.evaluate(
        """(el, allowed) => {
            const inline = ["strong", "em", "b", "i", "span", "a"];
            function walk(node) {
                if (node.nodeType === 3) { // text node
                    const text = node.nodeValue.trim();
                    if (text) {
                        return { el: "#text", text: text };
                    }
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

