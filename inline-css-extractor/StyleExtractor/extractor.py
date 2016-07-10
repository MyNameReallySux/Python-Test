from bs4 import BeautifulSoup

import requests
import collections 
import os

numeric_attrs = {
    'height':       'height',
    'width':        'width',
    'border':       'border',
}

url_attrs = {
    'background': 'background-image'
}

color_attrs = {
    'bgcolor':   'background-color',
}

alternate_attrs = {
    'align':     'margin'
}

table_attrs = {
    'valign':       'vertical-align',
}

table_border_attrs = {
    'cellspacing':  'border-spacing',
    'cellpadding':  'padding'
}

singleton_tags = [
#    'area','base','br','col','command','embed','hr',
#    'img', 'input','link','meta', 'object', 'param',
#    'source'
    'br', 'hr', 'param'
]

ignore_tags = [
    'embed'
]

def extract_style(page):
    text = page.text
    text = text.replace('<br>', '<br/>')
    text = text.replace('<br />', '<br/>')
    text = fix_singleton_tags(text)
    
    soup = BeautifulSoup(text, 'html.parser')
    tree = soup.findAll()
    
    soup.head.append(soup.new_tag('style', id = 'sux-generated', type = 'text/css'))
    new_style_tag = soup.head.findAll('style')
    pulled_style = new_style_tag[-1]
    
    for tag in tree:
        tag.name = tag.name.lower()
        if tag.name not in ignore_tags:
            should_print = False
            #####################################
            #   Numeric Attributes
            #####################################
            for attr in numeric_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    replace_attr(tag, attr)
            #####################################
            #   Alternate Attributes
            #####################################
            for attr in alternate_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    replace_attr(tag, attr, '0 auto')
            #####################################
            #   Color Attributes
            #####################################
            for attr in color_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    replace_attr_with_color(tag, attr)
            #####################################
            #   Table Attributes
            #####################################
            for attr in table_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    replace_style(tag, 'display', 'table-cell')
                    replace_attr(tag, attr)
            #####################################
            #   Table-Border Attributes
            #####################################
            for attr in table_border_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    if tag.has_attr('cellpadding'):
                        if int(tag['cellpadding']) > 0: replace_style(tag, 'border-collapse', 'separate')
                        else:                      replace_style(tag, 'border-collapse', 'collapse') 
                    replace_attr(tag, attr)
            #####################################
            #   Url Attributes
            #####################################
            for attr in url_attrs:
                if tag.has_attr(attr):
                    should_print = True
                    replace_attr_with_url(tag, attr)

            # if should_print: print(tag)

        tag_count = {}

        def increment_tag_count(tag):
            if tag.name not in tag_count: tag_count[tag.name] = 0
            tag_count[tag.name] = tag_count[tag.name] + 1

        def get_classname(tag):
            increment_tag_count(tag)
            return '.' + tag.name + "-" + str(tag_count[tag.name])

        def format_style(tag):
            style = tag['style']
            style = "\t" + style
            style = style.replace('; ', ';')
            style = style.replace(';', ';\n\t')
            return style

        def append_class(tag, classname):
            if not tag.has_attr('class'): tag['class'] = []
            tag['class'].append(classname[1:])

        def extract_inline_style(tag):
            style = format_style(tag)
            classname = get_classname(tag)     
            append_class(tag, classname)

            if style[-1] == '\t': style = style[:-2]

            pulled_style.append(classname+' {\n'+style+'}');
            del tag['style']
    
    for tag in tree:
        if tag.has_attr('style'):
            extract_inline_style(tag)
    
    print(soup.prettify())
    html = soup.prettify('utf-8')
    
    output_to_file(html)
    return html
    
def fix_singleton_tags(html):
    for tag in singleton_tags:
        start = html.find('<'+tag)
        while start != -1:
            end = html.find('>', start)
            if html[end - 1] != "/":
                separator = '/'                
                html = html[:end] + separator + html[end:]
                end += len(separator)
            start = html.find('<'+tag, end)          
    return html
            

def add_style(tag, attr, value = False):
    if value == False: value = tag[attr]      
    unit = get_unit(attr, value)
    if not tag.has_attr('style'): tag['style'] = ""   
    style_attr = get_style_attr(attr)
    tag['style'] += style_attr + ": " + value + unit + "; "
    
def replace_style(tag, attr, value):
    if not tag.has_attr('style'): tag['style'] = ""
    if isinstance(value, str):
        if attr not in tag['style'] and value not in tag['style']: 
            add_style(tag, attr, value)
    else:
        print('Nothing replaced')
    
def get_unit(attr, value):
    unit = ''
    if attr in numeric_attrs:
        if '%' in value: unit = ''
        else:            unit = 'px'
    return unit

def replace_text(text, to_replace, replace_with):
    return text.replace(to_replace, replace_with)

def replace_attr(tag, attr, value = False):
    add_style(tag, attr, value)
    del tag[attr]

def replace_attr_with_color(tag, attr):
    value = "#" + tag[attr]
    add_style(tag, attr, value)
    del tag[attr]
    
def replace_attr_with_url(tag, attr):
    value = "url('" + tag[attr] + "')"
    add_style(tag, attr, value)
    del tag[attr]
    
def get_style_attr(attr):
    if attr in numeric_attrs:
        return numeric_attrs[attr]
    elif attr in alternate_attrs:
        return alternate_attrs[attr]
    elif attr in color_attrs:
        return color_attrs[attr]
    elif attr in table_attrs:
        return table_attrs[attr]
    elif attr in table_border_attrs:
        return table_border_attrs[attr]
    elif attr in url_attrs:
        return url_attrs[attr]
    else:
        return attr
    
def output_to_file(data, path = 'output', name = 'output', ext = 'html'):
    if not os.path.exists(path): os.makedirs(path)
    with open(os.path.join(path, name+"."+ext), "wb") as file:
        file.write(data)