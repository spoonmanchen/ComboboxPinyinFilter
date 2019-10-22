from pypinyin import pinyin, lazy_pinyin, Style

def getPinyinStr(string):
  str_list = lazy_pinyin(string)
  string_joined = ''.join(str_list)
  string_joined = string_joined.replace(' ', '')
  return string_joined

def vagueOrderedSearch(search, string):
  """
  string: search; the string to be searched
  string: string
  """
  # assert they are all english strings
  # loop througt the search string
  index = 0
  for letter in search:
    # compared with the previous index, the new index should be bigger, if not, return False
  
    index = string.find(letter, index)
    if index == -1:
      return False
  return True
    