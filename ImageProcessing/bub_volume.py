#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""

# Standard library imports
import argparse
import json
import os

# Third party imports
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Local application imports
from dsip import improc as dip
from dsip.gfd import generic_fourier_descriptor


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE ####
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="path to the input JSON file")
    args = vars(ap.parse_args())

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)

    #### READ JSON FILE ####
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    #### LOADING JSON DATA ####
    # general data
    db_path = dataset[0]['path']
    backg_path = db_path + 'background.jpg'
    backg = cv.imread(backg_path, 0)

    # node data
    node = dataset[2]
    node_path = db_path + node['path']
    diameter = node['diameter']
    bw_frames_path = node_path + node['bwFramesPath']
    frames = sorted(os.listdir(bw_frames_path))
    # total_frames = ['1-00001.jpg', '2-00481.jpg', '3-00780.jpg', '4-01041.jpg', '5-01886.jpg']
    images_list = sorted(os.listdir(bw_frames_path))
    images = []
    volumes = []
    radii = []
    data = {}

    ### Looking for the first image of each sequence.
    for i in range(45):
        for k, name in enumerate(images_list):
            number, tex = name.split("-")
            if int(number) == i + 1:
                images.append(name)
                break

    for i, name in enumerate(images_list):
        short_name_frame = name.split('.')[0].split('-')[1]

        #### LOADING IMAGE ####
        frame = cv.imread(bw_frames_path + name, 0)
        _, bw_image = cv.threshold(frame, 200, 255, cv.THRESH_BINARY)

        #### VOLUME CALCULATION ####
        vol = dip.get_bubble_volume(bw_image, 0.3846)
        radius = pow((3 * vol) / (4 * np.pi), 1/3)

        volumes.append(round(vol, 2))
        radii.append(round(radius, 2))

        ### FOURIER DESCRIPTORS & CENTROID ####
        square_image = dip.center_bubble(bw_image)
        fd_bubble = generic_fourier_descriptor(square_image, 1, 10)
        cX, cY = dip.get_centroid(bw_image)

        fig, (a, b) = plt.subplots(1, 2)
        fig.set_size_inches(13, 4)
        fig.suptitle(f'Desc. de Fourier da imagen {short_name_frame}, bico {diameter}mm',
                     fontsize=15)
        a.imshow(bw_image)
        a.axis(False)

        b.set_yticks(np.arange(0, 1, 0.05))
        b.set_xticks(np.arange(0, 14, 1))
        b.stem(fd_bubble, use_line_collection=True)
        plt.show(block=False)
        plt.pause(2)
        plt.close()

    ### SAVE DATA
    volumes_file = node_path + 'volumes.txt'
    np.savetxt(volumes_file, volumes, delimiter=',', fmt='%.2f')

    volumes_radii_file = node_path + 'volumes_radii.json'
    data['volumes'] = volumes
    data['radii_from_images'] = radii
    with open(volumes_radii_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, separators=(',', ':'))
    print('*SAVED*')
