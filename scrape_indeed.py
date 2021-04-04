import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

def parse(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    df = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
    return df

url = "https://www.indeed.co.uk/jobs?q=computer+science&start=10"
print(parse(url))