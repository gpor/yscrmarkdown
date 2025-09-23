(el, allowed) => {
  const inline = new Set(["strong", "em", "b", "i", "span", "a"]);
  const allow = new Set(allowed);
  function walk(node, depth = 50) {
    const el = node.tagName ? node.tagName.toLowerCase() : null;
    const text = node.nodeType === Node.TEXT_NODE && node.nodeValue ? node.nodeValue.trim() : null;
    
    if (!text && !allow.has(el) && !inline.has(el)) {
      return null;
    }
      
    const props = {};
      
    if (el) {
      props.el = el;
    }
      
    const classes = node.classList ? [...node.classList] : [];
    if (classes.length) {
      props.cls = classes.join(' ');
    }
    
    if (text) {
      props.TEXT__ = text;
    }

    if (depth > 0) {
      const nodes = node.childNodes;
      if (typeof nodes[Symbol.iterator] === 'function') {
        let children = [];
        let textNodes = [];
        [...nodes].forEach(child => {
          const child_props = walk(child, depth - 1);
          if (child_props) {
            if (child_props.TEXT__ && !child_props.el) {
              textNodes.push(child_props.TEXT__);
            } else if (inline.has(child_props.el)) {
              const _nodes = child.childNodes;
              if (typeof _nodes[Symbol.iterator] === 'function') {
                let inline_texts = [];
                [..._nodes].filter(n => n.nodeType === Node.TEXT_NODE).forEach(n => {
                  const n_props = walk(n, depth - 1);
                  if (n_props && n_props.TEXT__) {
                    inline_texts.push(n_props.TEXT__);
                  }
                });
                if (inline_texts.length) {
                  textNodes.push(inline_texts.join(' '));
                }
              }
            } else if (child_props.el && (child_props.ch || child_props.TEXT__)) {
              children.push(child_props);
            }
          }
        })
        if (children.length) {
          props.ch = children;
        }
        if (textNodes.length) {
          props.TEXT__ = textNodes.join(' ');
        }
      }
    } else {
      props.isFullDepth = true;
    }
    return props;
  }
  return walk(el);
}