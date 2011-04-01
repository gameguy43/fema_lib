################################################################################
################################################################################
#####################                                  #########################
#####################         Release Our Data         #########################
#####################                                  #########################
#####################       a HelloSilo Project        #########################
#####################       <ROD@hellosilo.com>        #########################
################################################################################
##                                                                            ##  
##     Copyright 2010                                                         ##
##                                                                            ##  
##         Parker Phinney   @gameguy43   <parker@madebyparker.com>            ##
##         Seth Woodworth   @sethish     <seth@sethish.com>                   ##
##                                                                            ##
##                                                                            ##
##     Licensed under the GPLv3 or later,                                     ##
##     see PERMISSION for copying permission                                  ##
##     and COPYING for the GPL License                                        ##
##                                                                            ##
################################################################################
################################################################################

import re
import time
from datetime import datetime
from html5lib import HTMLParser, treebuilders
import traceback
import json
import yaml

def init_dict():
    metadict = {
        'id': '',
        'location': '',
        'photographer': '',
        'photo_date': '',
        'original_filename': '',
        'size': '',
        'dimensions': '',
        'categories':  None,
        'url_to_lores_img':  '',
        'url_to_hires_img':  '',
        'url_to_thumb_img':  '',
    }
    return metadict


def get_first_result_index_from_quick_search_results(html):
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    block = soup.find(border="0", bgcolor="white") # isolate the table of data on the first result
    id_str = block.find('font').contents[0] #contents of first <font>
    # this should looke like: 'ID#:11901'
    # parse out the actual id and cast as int
    id = int(id_str.partition(':')[2])
    print id
    return id


def parse_quick_search(html):
    return html

def remove_surrounding_td_tags(str):
    # get the first one
    str = str.split("<td>")[1]
    split = str.split("</td>")
    str = split[len(split)-2]
    return str

def encode_all_nice(fieldvalue):
#    return unicode(remove_surrounding_td_tags(repr(str(fieldValue))))
    #return str(fieldvalue.encode("utf-8"))
    return unicode(fieldvalue)

def find_by_tag_and_contents(soup, tag, contents):
    for obj in soup.findAll(tag):
        if obj.contents and obj.contents[0] == contents:
            return obj
    return None

def parse_img(html):
    metadict = init_dict()
    # soupify the html
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    # the lores image url
    metadict['url_to_lores_img'] = soup.find("",{"class": "tophoto"}).find("img")["src"]
    # the description/caption
    metadict['desc'] = encode_all_nice(soup.find("", {"class": "caption"}).contents[0].strip())

    # html table with the rest of the data
    data_table = soup.find("", {"class": "photoinfo2"}).find("tbody")

    metadict['url_to_hires_img'] = find_by_tag_and_contents(data_table, "a", u"\u00BB Download original photo")['href']
    
    for data_label_cell in data_table.findAll("th"):
        try:
            label = data_label_cell.contents[0]
        except:
            continue
        if label == u"Location:":
            metadict['location'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Photographer:':
            metadict['photographer'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Photo Date:':
            metadict['photo_date'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'ID:':
            metadict['id'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Original filename:':
            metadict['original_filename'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Size:':
            metadict['size'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Dimensions:':
            metadict['dimensions'] = data_label_cell.findNextSibling("td").contents[0].strip()
        elif label == u'Categories:':
            categories_td = data_label_cell.findNextSibling("td")
            #TODO
    return metadict
    
def test_parse():
    f = open('./samples/46326.html')
    raw_html = f.read()
    import pprint
    pprint.pprint(parse_img(raw_html))
    f.close()

if __name__ == '__main__':
	test_parse()
