def indent_xml(root, level = 0):
  i = '\n' + level * '  '
  if len(root):
    if not root.text or not root.text.strip():
      root.text = i + '  '
    if not root.tail or not root.tail.strip():
      root.tail = i
    for root in root:
      indent_xml(root, level + 1)
    if not root.tail or not root.tail.strip():
      root.tail = i
  else:
    if level and (not root.tail or not root.tail.strip()):
      root.tail = i
