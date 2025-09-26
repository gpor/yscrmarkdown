(el, allowed) => {
  const inline = new Set(["strong", "em", "b", "i", "span", "a"]);
  const allow = new Set(allowed);
  
  function _inlineElTextParts(inlineElChildrenNodes, depth) {
    let inlineElTextParts = [];
    [...inlineElChildrenNodes].filter(n => n.nodeType === Node.TEXT_NODE).forEach(n => {
      const inlineElChildProps = walk(n, depth - 1);
      if (inlineElChildProps && inlineElChildProps.TEXT__) {
        inlineElTextParts.push(inlineElChildProps.TEXT__);
      }
    });
    return inlineElTextParts;
  }

  function textAndChildren(nodes, depth) {
    let textParts = [];
    let children = [];
    [...nodes].forEach(child => {
      const child_props = walk(child, depth - 1);
      if (child_props) {
        if (child_props.TEXT__ && !child_props.el) {
          textParts.push(child_props.TEXT__);
        } else if (inline.has(child_props.el)) {
          const inlineElChildrenNodes = child.childNodes;
          if (typeof inlineElChildrenNodes[Symbol.iterator] === 'function') {
            let inlineElTextParts = _inlineElTextParts(inlineElChildrenNodes, depth);
            if (inlineElTextParts.length) {
              // if (child_props.el === 'a') {
              //   textParts.push('<a>'+inlineElTextParts.join(' ')+'</a>');
              // } else {
                textParts.push(inlineElTextParts.join(' '));
              // }
            }
          }
        } else if (child_props.el && (child_props.ch || child_props.TEXT__)) {
          children.push(child_props);
        }
      }
    })
    return {textParts, children};
  }

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
        const {textParts, children} = textAndChildren(nodes, depth);
        if (textParts.length) {
          props.TEXT__ = textParts.join(' ');
        }
        if (children.length) {
          props.ch = children;
        }
      }
    } else {
      props.isFullDepth = true;
    }
    return props;
  }
  return walk(el);
}