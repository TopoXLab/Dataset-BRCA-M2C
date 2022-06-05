import numpy as np
import glob
import os
import sys
import skimage.io as io
from scipy import ndimage

'''
Read labels files and generate a visualization overlaying colored dot labels on the images, similar to those in the folder 'images_with_labels'
'''
color_set = {1:(0,162,232),2:(255,0,0),3:(255,255,0)} 
# 1: lymphocytes: blue
# 2: tumor/epithelial: red
# 3: stromal/vessel: yellow

labels_dir = './labels'
images_dir = './images'
out_dir = './out_tmp'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

image_files = glob.glob(os.path.join(images_dir,'*.png'))

for image_filepath in image_files:    
    img_filename = os.path.split(image_filepath)[-1]
    print(img_filename)
    gt_filepath = os.path.join(labels_dir, img_filename.replace('.png', '_gt_class_coords.txt'))
    out_filepath = os.path.join(out_dir, img_filename.replace('.png', '_vis.jpg'))
    img = io.imread(image_filepath)
    label_coords = np.loadtxt(gt_filepath, dtype=int, delimiter =' ')
    for cid in color_set.keys():
        patch_label_arr = np.zeros((img.shape[0],img.shape[1]))
        cy = label_coords[np.where(label_coords[:,-1]==cid)][:,0]
        cx = label_coords[np.where(label_coords[:,-1]==cid)][:,1]
        patch_label_arr[(cy,cx)] = 1
        patch_label_arr = ndimage.convolve(patch_label_arr, np.ones((5,5)), mode='constant', cval=0.0)            
        img[patch_label_arr > 0] = color_set[cid]
    io.imsave(out_filepath,img)
