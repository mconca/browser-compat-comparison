import json
import os

# List of browsers for which we want to output compat data
browser_list = ['firefox', 'chrome', 'safari']

# List of status fields to extract for each item
status_list = ['deprecated', 'standard_track', 'experimental']

# Location of the MDN browser compatibility data
# Github repo: /mdn/browser-compat-data
bcdlocation = 'c:/Users/Mike Conca/Documents/GitHub/browser-compat-data'

# JSON files we want to skip
skip_files = ['browsers.schema.json', 'compat-data.schema.json']

# Default separator to use for CSV file
sep_char = ','

def get_browser_support(support_obj):
    global browser_list
    compat_str = ''
    for b in browser_list:
        bspt = support_obj[b]
        if isinstance(bspt, list):
            bspt = bspt[0]
        val = bspt['version_added']
        if isinstance(val, bool) and val is False:
            compat_str += 'False' + sep_char
        else:
            # Getting conservative and assuming all non-false means true
            compat_str += 'True' + sep_char
    return(compat_str)
           
def get_status_info(status_obj):
    global status_list
    status_str = ''
    for s in status_list:
        sts = status_obj[s]
        status_str += str(sts) + sep_char
    return(status_str)

def print_compat_data(json_input, prefix):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == '__compat':
                print(prefix[:-1], sep_char, get_browser_support(v['support']), get_status_info(v['status'])[:-1], sep='')
            print_compat_data(v, prefix + k + '.')


if __name__=='__main__':

    print('Name', end=''),
    for x in browser_list:
        print(sep_char, x, sep='', end='')
    for x in status_list:
        print(sep_char, x, sep='', end='')
    print()

    for (root,dirs,files) in os.walk(bcdlocation):
        # Skip WebExtensions. They are not standardized yet and are missing information
        # to properly parse (specifically, the 'status' section of the compat data).
        if 'webextensions' in root:
            continue

        print(root, dirs, files)
        for filename in files:
            if not filename.endswith('.json'):
                continue
            if filename in skip_files:
                continue

            try:
                jsonfile = json.loads(open(os.path.join(root, filename)).read())
            except:
                print('Could not parse', os.path.join(root, filename))
                continue

            print_compat_data(jsonfile, '')

