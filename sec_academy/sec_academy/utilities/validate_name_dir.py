def validate_name_dir(name):
  """
  I found a problem when admin upload any content if name for this content contains (\/:*?<>"|)
  I found Error NotADirectoryError
  """
  pattern = """\/:*?<>"|"""
  new_name = ""
  for sym in name:
      if not sym in pattern:
          new_name += sym
  return new_name