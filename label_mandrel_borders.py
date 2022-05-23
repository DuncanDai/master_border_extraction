import json
import os.path
import sys
import time
from datetime import datetime

import cv2
import numpy as np
from matplotlib import pyplot as plt

PATH_LABELS_FILE = 'labels.json'
PATH_IMAGES = 'Y:\\Data\\2022-04-28\\Data\\Images'  # TODO


def _get_labels():
    with open(PATH_LABELS_FILE, 'r') as f:
        labels = json.load(f)
    return labels


def _get_num_entries(labels):
    return sum([
        len(list(labels[folder].keys())) for folder in labels.keys()
    ])


def _load_image(folder, image):
    loaded = False
    while not loaded:
        try:
            image = cv2.imread(os.path.join(
                PATH_IMAGES, folder, image + '.png'))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            loaded = True
        except:
            loaded = False
            print('{}: Error loading image - retrying..'.format(datetime.now()))
            time.sleep(1)
    return image


def save_dict(labels):
    saved = False
    while not saved:
        try:
            with open(PATH_LABELS_FILE, 'w') as f:
                json.dump(labels, f)
            saved = True
        except:
            saved = False
            time.sleep(1)


def update_labels(labels, control_dict):
    labels[control_dict['folder']][control_dict['image']] = {
        'height': control_dict['height'],
        'width': control_dict['width'],
        'coords': [
            control_dict['x1'], control_dict['x2']
        ]
    }
    return labels


labels = None
image_counter = 0
starting = None


def label_borders():
    global starting
    starting = datetime.now()
    global image_counter
    global labels
    labels = _get_labels()
    num_labels = _get_num_entries(labels)

    index = 0
    control_dict = dict()
    for folder in labels.keys():
        for image_nr in labels[folder].keys():
            index += 1
            if labels[folder][image_nr] is not None:
                continue
            image_counter += 1
            image = _load_image(folder, image_nr)
            control_dict['finished'] = False
            control_dict['skip'] = False
            control_dict['x1'] = None
            control_dict['x2'] = None
            control_dict['height'] = None
            control_dict['width'] = None
            control_dict['folder'] = folder
            control_dict['image'] = image_nr

            t = datetime.now()
            sec_per_img = (t - starting).seconds / image_counter
            remaining = ((num_labels - index) * sec_per_img) / 3600

            while not control_dict['finished']:
                plt.close()
                fig = plt.figure()
                plt.title(
                    '{}/{}/{} - img/pers={}, remaining={}h, r=skip, e=exit, t=save&next, f=reset last'.format(
                        index, num_labels,
                        round((index / num_labels) * 100, 2),
                        round(sec_per_img, 2),
                        round(remaining, 2)
                    ))
                height, width, channels = image.shape
                control_dict['height'] = height
                control_dict['width'] = width
                plt.imshow(image, interpolation='none')

                if control_dict['x1'] is not None:
                    plt.axvline(control_dict['x1'])
                if control_dict['x2'] is not None:
                    plt.axvline(control_dict['x2'])

                def onKey(event):
                    global labels
                    if event.key == 'e':
                        plt.close()
                        print('Exiting..')
                        save_dict(labels)
                        sys.exit(0)
                    elif event.key == 'r':
                        plt.close()
                        control_dict['finished'] = True
                        control_dict['skip'] = True
                        control_dict['x1'] = None
                        control_dict['x2'] = None
                        labels = update_labels(labels, control_dict)
                    elif event.key == 't':
                        if (control_dict['x1'] is None) or (
                                control_dict['x2'] is None):
                            pass
                        else:
                            plt.close()
                            labels = update_labels(labels, control_dict)
                            control_dict['finished'] = True
                            control_dict['x1'] = None
                            control_dict['x2'] = None
                    elif event.key == 'f':
                        plt.close()
                        if control_dict['x2'] is not None:
                            control_dict['x2'] = None
                        elif control_dict['x1'] is not None:
                            control_dict['x1'] = None

                def onClick(event):
                    if event.dblclick:
                        if control_dict['x1'] is None:
                            control_dict['x1'] = int(event.xdata)
                        else:
                            tmp = control_dict['x1']
                            tmp2 = int(event.xdata)
                            if tmp > tmp2:
                                control_dict['x1'] = tmp2
                                control_dict['x2'] = tmp
                            else:
                                control_dict['x1'] = tmp
                                control_dict['x2'] = tmp2
                        plt.close()

                fig.canvas.mpl_connect('button_press_event', onClick)
                fig.canvas.mpl_connect('key_press_event', onKey)
                fig.canvas.mpl_connect('key_event', onKey)
                plt.grid()
                wm = plt.get_current_fig_manager()
                wm.window.showMaximized()
                plt.show()


if __name__ == '__main__':
    label_borders()
