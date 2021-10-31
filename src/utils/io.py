import os


def create_directory_if_not_exists(directory):
  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError:
    raise OSError('It was not possible to create the directory.')
