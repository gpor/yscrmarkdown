
const allowed = new Set([
  "body", "div", "main", "ul", "li",
  "h1", "h2", "h3", "h4", "h5", "h6", "p",
  "section", "article", "header", "footer", "nav",
  "table", "thead", "tbody", "tr", "th", "td",
  "pre", "code", "blockquote"
]);

const inline = new Set(["strong", "em", "b", "i", "span", "a"]);

function w28(node, depth = 20) {
  const el = node.tagName ? node.tagName.toLowerCase() : null;
  const text = node.nodeValue ? node.nodeValue.trim() : null;
  
  if (!text && !allowed.has(el) && !inline.has(el)) {
    return null;
  }
  
  const props = {};
  
  if (el) {
    props.el = el;
  }
  
  const classes = node.classList ? [...node.classList] : [];
  if (classes.length) {
    props.class = classes[0];
  }
  
  if (text) {
    props.text = text;
  }

  if (depth > 0) {
    const nodes = node.childNodes;
    if (typeof nodes[Symbol.iterator] === 'function') {
      let children = [];
      let textNodes = [];
      [...nodes].forEach(child => {
        const child_props = w28(child, depth - 1);
        if (child_props) {
          if (child_props.text && !child_props.el) {
            textNodes.push(child_props.text);
          } else if (inline.has(child_props.el)) {
            const _nodes = child.childNodes;
            if (typeof _nodes[Symbol.iterator] === 'function') {
              let inline_texts = [];
              [..._nodes].filter(n => n.nodeType === Node.TEXT_NODE).forEach(n => {
                const n_props = w26(n, depth - 1);
                if (n_props && n_props.text) {
                  inline_texts.push(n_props.text);
                }
              });
              if (inline_texts.length) {
                textNodes.push(inline_texts.join(' '));
              }
            }
          } else if (child_props.el) {
            children.push(child_props);
          }
        }
      })
      if (children.length) {
        props.children = children;
      }
      if (textNodes.length) {
        props.text = textNodes.join(' ');
      }
    }
  } else {
    props.isFullDepth = true;
  }
  return props;
}

