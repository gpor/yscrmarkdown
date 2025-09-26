
(el, allowed) => {
  const inline = new Set(["strong", "em", "b", "i", "span", "a"])
  const allow = new Set(allowed)
  
  function walk(node) {
    const element = {}
    const textParts = []
    const childrenElements = []
    if (node.nodeType === Node.TEXT_NODE) {
      return node.nodeValue || null
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      element.el = node.tagName.toLowerCase();
      if (!allow.has(element.el) && !inline.has(element.el)) {
        return null
      }
      [...node.childNodes].forEach(n => {
        const elementOrText = walk(n)
        if (typeof elementOrText === 'string') {
          textParts.push(elementOrText)
        } else if (elementOrText !== null) {
          childrenElements.push(elementOrText)
        }
      })
    }
    if (textParts.length) {
      element.TEXT_ = textParts.join(' ')
    }
    if (childrenElements.length) {
      element.ch = childrenElements
    }
    const classes = node.classList ? [...node.classList] : [];
    if (classes.length) {
      element.cls = classes.join(' ');
    }
    return element
  }
  return walk(el)
}