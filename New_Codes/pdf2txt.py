# credits to akash karothiya: 
# https://stackoverflow.com/questions/39012739/need-to-extract-all-the-font-sizes-and-the-text-using-beautifulsoup/39015419#39015419

import re
import pandas as pd
from bs4 import BeautifulSoup

# open the html file
html = open(pathHTMLoutput, 'r')
soup = BeautifulSoup(html)

font_spans = [data for data in soup.select('span') if 'font-size' in str(data)]
output = []
for i in font_spans:
    # extract fonts-size
    fonts_size = re.search(r'(?is)(font-size:)(.*?)(px)', str(i.get('style'))).group(2)
    # extract into font-family and font-style
    fonts_family = re.search(r'(?is)(font-family:)(.*?)(;)', str(i.get('style'))).group(2)
    # split fonts-type and fonts-style
    try:
        fonts_type = fonts_family.strip().split(',')[0]
        fonts_style = fonts_family.strip().split(',')[1]
    except IndexError:
        fonts_type = fonts_family.strip()
        fonts_style = None
    output.append((str(i.text).strip(), fonts_size.strip(), fonts_type, fonts_style))

# create dataframe
df = pd.DataFrame(output, columns = ['text', 'fonts-size', 'fonts-type', 'fonts-style'])