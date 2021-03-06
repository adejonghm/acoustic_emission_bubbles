#!/usr/bin/env python3

"""
Dev: 	adejonghm
----------

Script to Manage the JSON file using jilib library.
"""


# Standard library imports
import os
import json
import argparse
from datetime import datetime, date

# Third party imports

# Local application imports
import dsip.jilib as jm


if __name__ == "__main__":

    #### VALIDATE THE ARGUMENT ####
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="path to the input JSON file")
    args = vars(ap.parse_args())
    input_path = ''

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)


    #### READ JSON FILE ####
    with open(input_path, encoding='utf-8') as file:
        json_loaded = json.load(file)


    #### MAKE A BACKUP ####
    date_time = str(date.today()) +"_"+ datetime.now().strftime("%H-%M-%S")
    name = input_path.split('.')[0]
    os.system("cp {} {}_{}.old".format(input_path, name, date_time))


    #### OPERATIONS ####
    new_node = {"test": 100}
    outFile = jm.add_node(json_loaded, new_node)


    #### WRITE NEW JSON FILE ####
    with open(input_path, 'w', encoding='utf-8') as file:
        json.dump(outFile, file, indent=2, separators=(',', ':'))

    print('JSON file saved.')
