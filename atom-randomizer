#!/usr/bin/env python

import re
import requests
import json
import cson
import os
import sys
from random import randrange
from subprocess import call
from datetime import datetime

atom_configdir = atom = os.path.join(os.path.expanduser('~'), '.atom')
atom_config_uri = os.path.join(atom_configdir, 'config.cson')
theme_history_uri = os.path.join(atom_configdir, 'random_theme_history.json')


# Find the last page of the themes list
pagenum_regex = re.compile('(?<=page=)\d+')
themes_page = requests.get('https://atom.io/themes/list').content
pagenums = [int(x) for x in pagenum_regex.findall(themes_page)]
pagenums.sort()
maxpage = pagenums[-1]

# Randomize theme page
random_pagenum = randrange(1,maxpage)
random_pageurl = 'https://atom.io/themes/list?direction=desc&page={}&sort=downloads'.format(random_pagenum)
theme_page = requests.get(random_pageurl).content

# Find all themes on page
themes_on_page_regex = re.compile('(?<=/themes/)(?!search|list)([0-9a-zA-Z\-]+)')
theme_list = themes_on_page_regex.findall(theme_page)

# Random theme from list
random_theme = theme_list[randrange(0,len(theme_list))]

# Load theme history into dict
try:
    with open(theme_history_uri, 'rb') as f:
        theme_history = json.load(f)
except:
    theme_history = {}

# Exit if theme alrteady instaled
if random_theme in theme_history:
    print("{}? Already tried that flavor...".format(random_theme))
    sys.exit()
else:
    theme_history[random_theme] = datetime.now().isoformat()

# Write new theme to theme history
with open(theme_history_uri, 'wb') as f:
    f.write(json.dumps(theme_history, indent=4))

# Load atom config
with open(atom_config_uri, 'rb') as f:
    atom_config = cson.load(f)

# Put theme at index based on type
if '-ui' in random_theme:
    print("replacing {} with {}".format(atom_config['*']['core']['themes'][0], random_theme))
    atom_config['*']['core']['themes'][0] = random_theme
elif '-syntax' in random_theme:
    print("replacing {} with {}".format(atom_config['*']['core']['themes'][1], random_theme))
    atom_config['*']['core']['themes'][1] = random_theme

# Write atom config / Using string to prettify the output
with open(atom_config_uri, 'w') as f:
    f.write(cson.dumps(atom_config, indent=4))


install_cmd = 'apm install {}'.format(random_theme)
result = call(install_cmd.split())
