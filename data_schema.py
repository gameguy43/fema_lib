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

#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker, mapper

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import json
import os.path
from django.template import Template, Context

table_name = 'fema_metadata'


resolutions = {
    'hires' : {
        'status_column_name' : 'hires_status',
        'url_column_name'    : 'url_to_hires_img',
        'subdir'             : 'hires/',
        'extension'          : '.tif',
        },
    'lores' : {
        'status_column_name' : 'lores_status',
        'url_column_name'    : 'url_to_lores_img',
        'subdir'             : 'lores/',
        'extension'          : '.jpg',
        },
    'thumb' : {
        'status_column_name' : 'thumb_status',
        'url_column_name'    : 'url_to_thumb_img',
        'subdir'             : 'thumb/',
        'extension'          : '.jpg',
        },
    }

their_fields = {
    'photo_date' : {
        'column' : Column(String),
        },
    'desc' : {
        'column' : Column(String),
        },
    'location' : {
        'column' : Column(String),
        },
    'original_filename' : {
        'column' : Column(String),
        },
    'size' : {
        'column' : Column(String),
        },
    'photographer' : {
        'column' : Column(String),
        },
    'dimensions' : {
        'column' : Column(String),
        },
    'categories' : {
        'column' : Column(String),
        },
    'disasters' : {
        'column' : Column(String),
        },
    }

our_fields = {
    'url_to_lores_img': {
        'column' : Column(String),
        },
    'url_to_hires_img': {
        'column' : Column(String),
        },
    'url_to_thumb_img': {
        'column' : Column(String),
        },
    'hires_status' : {
        'column': Column(Boolean, default=False),
        },
    'lores_status' : {
        'column': Column(Boolean, default=False),
        },
    'thumb_status' : {
        'column': Column(Boolean, default=False),
        },
    'page_permalink' : {
        'column': Column(String),
        },
    'access_time' : {
        'column': Column(Integer),
        },
    'doesnt_exist' : {
        'column': Column(Boolean),
        },
    'we_couldnt_parse_it' : {
        'column': Column(Boolean),
        },
#   'is_color = Column(Boolean)
    }

def prep_data_for_insertion(data_dict):
    if 'disasters' in data_dict:
        data_dict['disasters'] = json.dumps(data_dict['disasters'])
    if 'categories' in data_dict:
        data_dict['categories'] = json.dumps(data_dict['categories'])
    return data_dict

def re_objectify_data(data_dict):
    if 'disasters' in data_dict:
        data_dict['disasters'] = json.loads(data_dict['disasters'])
        print data_dict['disasters']
    if 'categories' in data_dict:
        data_dict['categories'] = json.loads(data_dict['categories'])
    return data_dict


def links_to_html(json_str):
    parsed = json.loads(json_str)
    retval = "<ul>"
    for string, url in parsed:
        retval += '<li><a href="' + url + '">' + string + "</a></li>\n";
    retval += "</ul>"
    return retval

def categories_to_html(categories_dict):
    retval = "<ul>"
    for category in categories_dict:
        retval += '<li><a href="' + category[1] + '">' + category[0] + '</a></li>\n'
    retval += "</ul>"
    return retval

template_file = 'django_template.html'

def floorify(id):
    ## mod 100 the image id numbers to make smarter folders
    floor = id - id % 100
    floored = str(floor).zfill(5)[0:3]+"XX"
    return floored

def repr_as_html(image_as_dict, image_resolution_to_local_file_location_fxn):
    floorified = floorify(image_as_dict['id'])
    id_zfilled = str(image_as_dict['id']).zfill(5)
    image_urls = {}
    for resolution in resolutions:
        image_urls[resolution] = image_resolution_to_local_file_location_fxn(resolution)

    # add link rel=license
    #image_as_dict['copyright'] = image_as_dict['copyright'].strip("'").replace('None', '<a href="http://creativecommons.org/licenses/publicdomain/" rel="license">None</a>')

    '''
    if image_as_dict['links']:
        image_as_dict['links'] = links_to_html(image_as_dict['links'])
    '''
    if image_as_dict['categories']:
        image_as_dict['categories'] = categories_to_html(image_as_dict['categories'])

    image_as_dict['next_id'] = int(image_as_dict['id']) + 1
    image_as_dict['prev_id'] = int(image_as_dict['id']) - 1
    template_str = get_template_str()
    template = Template(template_str)
    context = Context({'image': image_as_dict, 'image_urls': image_urls})
    html = template.render(context)
    return html



# the stuff below here should stand on its own

def get_template_str():
    path = os.path.dirname(__file__)
    relpath = os.path.relpath(path)
    template_relpath = relpath + '/' + template_file
    fp = open(template_relpath, 'r')
    template_as_str = fp.read()
    return template_as_str

Base = declarative_base()

class OurMetadata(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)

all_fields = dict(their_fields.items() + our_fields.items())

for fieldname, fieldinfo in all_fields.items():
    setattr(OurMetadata, fieldname, fieldinfo['column'])
