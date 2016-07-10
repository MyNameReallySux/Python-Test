from bs4 import BeautifulSoup
import tinycss
import pprint

rule_map = {}

def combine_classes(text):
    parser = tinycss.make_parser('page3')
    soup = BeautifulSoup(text, 'html.parser')
    pp = pprint.PrettyPrinter(depth=6)
    
    style = soup.findAll('style')
    style = " ".join(style[-1].contents)
    
    stylesheet = parser.parse_stylesheet(style)
    rule_set = stylesheet.rules
    
    for rule in rule_set:
        add_to_rule_map(rule)
       
    for classname in rule_map:
        attr_map = {}
        declarations = get_declarations(classname) 
        attr_list = get_attr_list(declarations)
        print(classname)

        for declaration in declarations:
            for attr in declaration:    
                if get_attr_name(attr) in attr_map:
                    if(attr_map[get_attr_name(attr)] == get_attr_value(attr)):
                        # print('SAME: ', attr_map[get_attr_name(attr)], get_attr_value(attr))
                        test = 0
                    else:
                        # print('DIFFERNT: ', attr_map[get_attr_name(attr)], get_attr_value(attr))
                        test = 0

                else:
                     attr_map[get_attr_name(attr)] = get_attr_value(attr)
                        
            # pp.pprint(attr_map)
    
def get_attr_list(declarations):
    for declaration in declarations:
        for attr in declaration:
            print("\t", get_attr_name(attr), ":", get_attr_value(attr))
        print('')
        
def get_tag(rule):
    return split_classname(rule)[0]

def get_id(rule):
    return split_classname(rule)[1]

def split_classname(rule):
    return rule.selector.as_css().split('-')\

def get_declarations(classname):
    return rule_map[classname]['rules']

def get_attr_name(attr):
    return attr.name

def get_attr_value(attr):
    return attr.value.as_css()

def add_to_rule_map(rule):
    tag = get_tag(rule)
    class_id = get_id(rule)
    if tag not in rule_map: 
        rule_map[tag] = {
            'ids': [class_id], 
            'rules': [rule.declarations]
        }
    elif len(rule_map[tag]['rules']) > 0 or len(rule_map[tag]['ids']) > 0:  
        rule_map[tag]['ids'].append(class_id)
        rule_map[tag]['rules'].append(rule.declarations)
        
    
