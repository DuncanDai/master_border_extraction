import json
import os.path
import sys

PATH = r'D:\D\Masterarbeit\_Tools'

with open(PATH + '\labels_reduced.json', 'r') as f:
	labels = json.load(f)

print(labels.keys())

