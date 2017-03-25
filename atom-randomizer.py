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
theme_historydir = os.path.join(atom_configdir, 'random_theme_history')
theme_history_uri = os.path.join(theme_historydir, 'random_theme_history.json')

if not os.path.exists(theme_historydir):
    os.makedirs(theme_historydir)

def get_random_theme():
    # Return random theme from atom.io
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
    return random_theme

def load_history():
    # Load theme history return dict
    try:
        with open(theme_history_uri, 'rb') as f:
            return json.load(f)
    except:
        theme_history = {}
        return theme_history


def save_history(theme_history):
    # Saves theme_history
    try:
        with open(theme_history_uri, 'wb') as f:
            f.write(json.dumps(theme_history, indent=4))
    except:
        print("Unable to write theme history, exiting.")
        sys.exit()

def load_atom_config():
    # Load atom config returns atom_config dict
    try:
        with open(atom_config_uri, 'rb') as f:
            atom_config = cson.load(f)
        # Lets back up the config file just in case
        config_backup = os.path.join(theme_historydir, 'config.cson.bak')
        with open(config_backup, 'w') as f:
            f.write(cson.dumps(atom_config, indent=4))
        return atom_config
    except Exception as e:
        print("Unable to read atom config file, exiting.")
        print('{}'.format(e))
        sys.exit()

def add_theme_to_atom_config(atom_config, random_theme):
    # Adds theme to atom_config dict based on type
    if '-ui' in random_theme:
        atom_config['*']['core']['themes'][0] = random_theme
    elif '-syntax' in random_theme:
        atom_config['*']['core']['themes'][1] = random_theme
    return atom_config

def save_atom_config(atom_config):
    # Write atom config
    try:
        with open(atom_config_uri, 'w') as f:
            f.write(cson.dumps(atom_config, indent=4))
    except:
        print("Unable to write atom config, exiting.")
        sys.exit()


if __name__ == '__main__':
        # Get new theme
        random_theme = get_random_theme()
        theme_history = load_history()
        while random_theme in theme_history:
            random_theme = get_random_theme()
            theme_history = load_history()
        theme_history[random_theme] = datetime.now().isoformat()
        save_history(theme_history)
        # Run install
        install_cmd = 'apm install {}'.format(random_theme)
        result = call(install_cmd.split())
        # Set theme active
        atom_config = load_atom_config()
        atom_config = add_theme_to_atom_config(atom_config, random_theme)
        save_atom_config(atom_config)
        sys.exit(0)
