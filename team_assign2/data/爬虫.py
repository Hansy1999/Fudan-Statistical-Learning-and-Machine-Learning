import requests
from lxml import etree
import numpy as np
import pandas as pd

def tail_num2aircraft_type(tailnum):
    url = 'https://zh.flightaware.com/live/flight/' + tailnum
    data = requests.get(url).text
    s = etree.HTML(data)
    aircrafttype = s.xpath('/html/head/title/text()')[0]
    ## It is a sentence like "N832UA … History (A319 owned by …",
    ## therefore, we split the string to get the aircraft type.
    ## Sometimes the sentence may be not in that form, just try again.
    if '(' in aircrafttype:
        aircrafttype = aircrafttype.split('(')[1].split()[0]
    return aircrafttype

## There will be an error if the file name contains Chinese,
## so I have to rename the original file as American2018.csv,
## however, without changing the content of the original file.
data = pd.DataFrame(pd.read_csv("American2018.csv"))
tail_nums = data['TAIL_NUM'].unique()  # take the TAIL_NUM column
aircraft_types = []                    # initialize the output list

## For each tail_num, use the defined function to get its aircraft_type.
for index, tail_num in enumerate(tail_nums):
    aircraft_type = tail_num2aircraft_type(tail_num)
    aircraft_types.append(aircraft_type)  # add to output list
    print(index + 1, aircraft_type)       # print for examine

## Create output DataFrame and then output as a csv file.
output = {"TAIL_NUM": tail_nums, "AIRCRAFT_TYPE": aircraft_types}
output = pd.DataFrame(output)
output.to_csv('L_AIRCRAFT_TYPE.csv', encoding = "utf-8", index = False)
