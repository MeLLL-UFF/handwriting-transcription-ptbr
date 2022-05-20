import os
import sys
import cv2
sys.path.insert(1, './SimpleHTR-master/src')
sys.path.insert(1, './SimpleHTR-master/model')
from dataloader_iam import Batch
from model import Model, DecoderType
from main import infer, get_img_size
from preprocessor import Preprocessor

# map decoder input name to its object
decoder_mapping = {'bestpath': DecoderType.BestPath,
                        'beamsearch': DecoderType.BeamSearch,
                        'wordbeamsearch': DecoderType.WordBeamSearch}

# map token unity to its label file
token_unity_mapping = {'word': './model/charList.txt',
                        'line': './model/wordCharList.txt'}

## Load pretrained model
# @param decoder name of decode method used for inference
# @param token_unity text information unity for inference
# @return Model object
def load_model(decoder, token_unity):
    decoder_type = decoder_mapping[decoder]
    label_file = token_unity_mapping[token_unity]
    return Model(list(open(label_file).read()), decoder_type, must_restore=True, dump='')

## Get number of cropped word using its file name
# @param name file name
# @return int value that represents the cropped word position
def get_crop_number(name):
    basename = name.split('.')[0]
    alpha = basename.split('_')
    last_elem = alpha[len(alpha)-1]
    if(last_elem.split("-")[0] == "half"):  #half cropped images have "half-1" or "half-2" label at the end of their names
        return int(alpha[len(alpha)-2])     #get crop number before "half" label 
    else:
        return int(last_elem)               #crop number is the last information in file name

## Infer word from image
# @param model pretrained model
# @param img_file input file used to infer word
# @return word inferred and its probability
def infer_word(model, img_file):
    img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    #preprocess image before inference
    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    #infer word from image
    batch = Batch([img], None, 1)
    recognized, probability = model.infer_batch(batch, True)
    return recognized[0], probability[0]

## Infer a set of word images and concatenate them into a text
# @param model pretrained model
# @param words_path path for word images set
# @return text inferred from words concatenation
def infer_text(model, words_path):
    data_paths = os.listdir(words_path)
    if(data_paths):
        print("Infering text from word images...")
        
        if(len(data_paths) > 1):
            # sort path names based on its number at the end (0, 1, 2,... != 0, 1, 10, ..., 2)
            data_paths.sort(key=get_crop_number)
        
        inferred_text = ""   #result text from words inference

        # process each path for word image
        for path in data_paths:
            try:         
                recognized, probability = infer_word(model, words_path+path)
            except ValueError: #catch error when input image doesn't fit as model input
                recognized = '<UNK-infer>'
                print("Image from \'", path, "\' file couldn't be used as model input image.\nInference replaced with <UNK-infer> in final inferred text.\n")
            #print(path, ":", recognized)
            inferred_text += recognized + " "

        #print("Inferred text:")
        #print(inferred_text)
        return inferred_text
        
    else:
        print("Empty path: ", words_path)        