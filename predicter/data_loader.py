"""
data loader
"""

import re

data_pattern = '\d+\d*[.]\d+\d*|\d+'

def get_data(text):
    for data in re.findall(data_pattern,text):
        if float(data) > 1:
            yield float(data)
            pass
        pass
    pass