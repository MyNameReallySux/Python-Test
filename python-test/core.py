import requests
import collections 
import os

from StyleExtractor.extractor import extract_style

def main():
    page = requests.get('http://www.robinwallack.com/' + input('Get Site, http://www.robinwallack.com/'))
    page = extract_style(page)
    page = combine_classes()
    
main();
