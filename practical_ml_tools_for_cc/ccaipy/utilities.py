'''
This function is meant to read text files
like the icecore data files. It expects
header rows (number of rows to skip)
and each data row to contain the same number
of values. 

The text file will be transformed into a 
dictionary. Each column from the text file
will become a list of values associated with the
keys of the dictionary. The input variable 
<keys> should be the name of each column
in the input file. 

Inputs:
fname - file to read, expected to be space delimited
skiprows - number of header rows
keys - list of strings, one for each column of the input file

Output:
<data> dictionary - keys are the same as the input
variable, values are each column from the text file. 

'''
import numpy as np

def read_text_file(fname, skiprows=1, keys=[]):
  data = {}
  values = np.loadtxt(fname, skiprows=skiprows,unpack=True)

  if len(keys) != len(values):
    print(f"Different number of keys({len(keys)}) in input args than "+\
          f"values({len(values)}) in file. Please correct.")
    return

  for idx, key in enumerate(keys):
    data[key] = values[idx]

  return data
  
  '''
This is a function to display a particular slide from the 
lesson's slide deck.
'''
import IPython

# This is the publication URL for the slide deck
deck_url = 'https://docs.google.com/presentation/d/e/2PACX-1vTkkbNHNhIC1REyvZU69wYew8DqPnuwpp2hsCui2UFJOCdH5Lma8fXyr31iXbtYaA/embed?start=false&loop=false&delayms=3000'

def display_slide(slide_number):
  src_url = f'{deck_url}&slide=id.p{slide_number}'
  html_str = f'<iframe src="{src_url}"'+ \
             ' frameborder="0" width="960" height="749"'+ \
             ' allowfullscreen="true"'+ \
             ' mozallowfullscreen="true"'+ \
             ' webkitallowfullscreen="true"></iframe>'
  return IPython.display.HTML(html_str)