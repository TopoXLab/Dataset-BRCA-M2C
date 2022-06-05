import numpy as np
import glob
import os
import sys


labels_dir = './labels'

split_files = ['brca_ds_train.txt', 'brca_ds_val.txt', 'brca_ds_test.txt' ]

class_count_dict = {1:0 ,2:0 ,3:0} 
# 1: lymphocytes
# 2: tumor/epithelial
# 3: stromal/vessel

for split_file in split_files:
    print(split_file)
    file_arr = np.loadtxt(split_file, dtype=str)
    class_count_dict = {1:0 ,2:0 ,3:0} 
    for img_filename in file_arr:
        gt_filepath = os.path.join(labels_dir, img_filename.replace('.png', '_gt_class_coords.txt'))
        label_coords = np.loadtxt(gt_filepath, dtype=int, delimiter =' ')
        for cid in class_count_dict.keys():
            class_count_dict[cid] += (label_coords[:,-1]==cid).sum()
    print(class_count_dict)
