import requests
import collections 
import os

import StyleExtractor.extractor as StyleExtractor
import ClassReducer.reducer as ClassReducer

def main():
    page = requests.get('http://www.robinwallack.com/' + input('Get Site, http://www.robinwallack.com/'))
    page = StyleExtractor.extract_style(page) # Moves all inline styles to top of page in style tag
    page = ClassReducer.combine_classes(page) # Combines like styles of css
    
main();
