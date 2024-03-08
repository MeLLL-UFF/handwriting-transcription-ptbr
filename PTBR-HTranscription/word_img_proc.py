import numpy as np
import cv2
import os

## Calculate median height from coordinates list
# @param coords_list list of coordinates [y0,y1,x0,x1]
# @return int value with median height
def get_median_height(coords_list):
    print("Calculating median height for word regions...")
    median = []
    mid_height = 0
    for coord in coords_list:
        y0 = coord[0]
        y1 = coord[1]

        img_height = y1 - y0
        median.append(img_height)

    median.sort()
    factor = len(median)//2
    if len(median)%2 == 0:
        mid_height = (median[factor-1]+median[factor])/2
    else:
        mid_height = median[factor]
    return int(mid_height)

## Return list of coordinates from coordinates file
# @param coord_file path to coordinates file
# @return list of coordinates considering [y0,y1,x0,x1] points from a box region
def list_coords(coord_file):
    coord_data = open(coord_file, 'r').read().split("\n\n")[:-1]    #coordinates separated with "\n\n"
    coord_list = []
    for line in coord_data:
        line = line.split(',')
                                #height values              width values
        coord_list.append([int(line[1]),int(line[5]),int(line[0]),int(line[2])])
    return coord_list

## Crop words from image based on coordinates list
# @param image_path path to the image to be cropped
# @param image_file name for image file
# @param words_path path to save cropped words image
# @param coord_list list of words coordinates
# @param median_threshold value used to split word images with height greater than
# @return int value with the number of saved images
def crop_images(image_path, image_file, words_path, coord_list, median_threshold):
    # get image infos
    image_data = image_file.split('.')
    image_name = image_data[0]
    image_ext = "."+image_data[1]
    
    # set result folder to save cropped images
    result_folder = image_path+words_path
    if not os.path.isdir(result_folder):
        os.mkdir(result_folder)

    image = cv2.imread(image_path+"/"+image_file)

    # calculate median height from word images
    if(median_threshold > 0 and len(coord_list) > 0):
        mid_height = get_median_height(coord_list)

    #get coordinates and crop image
    i = 0       #'iterator for word images name'
    for coord in coord_list:
        if(median_threshold > 0):
            img_height = coord[1] - coord[0]

            # split word image in half if its height is greater than median threshold
            if(img_height > mid_height+mid_height*median_threshold):
                #first half
                word_img1 = image[coord[0]:coord[0]+mid_height, coord[2]:coord[3]]
                word_file1 = result_folder+"/"+image_name+"_crop_"+str(i)+"_half-1"+image_ext
                if(word_img1 is not None):
                    cv2.imwrite(word_file1, word_img1)
                    i += 1
                else:
                    print("Empty word image:", word_file1)

                #second half
                word_img2 = image[coord[0]+mid_height+1:coord[1], coord[2]:coord[3]]
                word_file2 = result_folder+"/"+image_name+"_crop_"+str(i)+"_half-2"+image_ext
                if(word_img2 is not None):
                    cv2.imwrite(word_file2, word_img2)
                    i += 1
                else:
                    print("Empty word image:", word_file2)
                
                continue

        # save word image without calculating median height
        # or if its height is less than median threshold
                        #height values         width values
        word_img = image[coord[0]:coord[1], coord[2]:coord[3]]
        word_file = result_folder+"/"+image_name+"_crop_"+str(i)+image_ext
        if(word_img is not None):
            cv2.imwrite(word_file, word_img)
            i += 1
        else:
            print("Empty word image:", word_file)

    return i

## Generate word images from image and coordinate files
# @param data_path path with sample and coordinate files
# @param words_path result folder to store word images
# @param median_threshold value used to split word images with height greater than
# @return int value with the number of saved images
def create_word_images(data_path, words_path, median_threshold):
    crops = 0                       #number of words cropped into images
    coord_file = ""
    image_file = ""
    
    if(os.path.isdir(data_path)):
        data_files = os.listdir(data_path)

        # set file path for coordinate file and original image file based on their extension and name
        for i in range(len(data_files)):
            if(os.path.isfile(data_path+data_files[i])):
                file_name, file_ext = os.path.splitext(data_files[i])
                if(file_ext == ".txt"):
                    coord_file = data_path+data_files[i]
                else:
                    if(file_name.split("_")[0] != "res"):
                        image_file = data_files[i]

        if(coord_file == ""):
            print("Missing coordinates text file (.txt) in "+str(data_path))
            return crops

        if(image_file == ""):
            print("Missing original image file in "+str(data_path))
            return crops

        # create a list with coordinates 
        coord_list = list_coords(coord_file)
        coords = len(coord_list)

        # crop word images based on coordinates list
        crops = crop_images(data_path, image_file, words_path, coord_list, median_threshold)
        print(crops, "word image files created.")

        if(coords != crops):
            print("Number of coordinates ("+str(coords)+") differ from number of cropped words ("+str(crops)+").")      
    else:
        print(data_path + " is not a valid path.")

    return crops