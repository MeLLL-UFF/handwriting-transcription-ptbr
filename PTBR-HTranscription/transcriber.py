import os
import sys
sys.path.insert(1, "./CRAFT-pytorch-master")
from file_utils import get_files
from words_finder import run_craft
from word_img_proc import create_word_images
from text_infer import load_model, infer_text
from dict_proc import find_similarities, dict_indexing, dict_pt_words

#default paths
samples_path = "./data/"
ptdict_file = "dicionario_port.txt"
words_path = "word_images/"

## Save info in file
# @param file_name path for file to be written
# @param text text to be written
def save_text(file_name, text):
    f = open(file_name, 'w')
    f.write(text)
    f.close()

## Call methods for handwriting text automatic transcription
# @param data_paths text images path
# @param decoder decoder used to turn infos into word
# @param token_unity text information unity for inference
# @param find_sims distance value to find nearest word neighboors from dictionary
# @param median_threshold value used to split word images with height greater than
# @param craft_args tool arguments to find words in image
# @param inferred_file path for inferred text file to refine text with simhash
def process_folder(data_paths, decoder, token_unity, find_sims, median_threshold, craft_args, inferred_file):
    # load infer model
    if(decoder != ""):
        model = load_model(decoder, token_unity)

    # create pt-br dictionary
    if(find_sims > -1):
        pt_dict = dict_pt_words(ptdict_file)
        index = dict_indexing(pt_dict, find_sims)

    # each path has 1 text image
    for path in data_paths:
        image_path = samples_path+path+'/'
        print("-------------------------------------------------")
        print("Processing path", image_path, ":")

        # find words in image
        if(craft_args["text_threshold"] > -1):
            print("\nSearching for words in the image files...")
            image_list, _, _ = get_files(image_path)
            boxes = run_craft(image_list, image_path, craft_args)
            print("Found", boxes, "words in image path", image_path, "\n")

        # crop words from image
        cropped = create_word_images(image_path, words_path, median_threshold)
        print()
        
        
        # infer text from word images
        inferred_text = ""
        if(decoder != ""):
            if(craft_args["text_threshold"] > -1 and cropped == 0):
                '''TODO: verificar se programa deve seguir p proxima pasta ou parar a execucao nesse caso'''
                print("Issue from CRAFT procedure. Please check the log in terminal e rerun the application.")
                print("If you don't want to execute CRAFT procedure, please set 'text_threshold' value as -1.\n")
            else:
                if(os.path.isdir(image_path+words_path)):
                    inferred_text = infer_text(model, image_path+words_path)
                    text_file = image_path+"text_"+path+'.txt'
                    save_text(text_file, inferred_text)
                    print("Inferred text saved as file at ", text_file)
                else:
                    print("Path for word images is not valid: ", image_path+words_path)

        # replace misinferred words with dict words
        if(find_sims > -1):
            if(inferred_text == "" and inferred_file == ""):
                '''TODO: verificar se programa deve seguir p proxima pasta ou parar a execucao nesse caso'''
                print("Inferred text not found. Please check the log in terminal e rerun the application.")
                print("If you want to generate inferred text, please set a 'decoder' value from default options: ['bestpath', 'beamsearch', 'wordbeamsearch'].\n")
                continue

            if(inferred_file != ""):
                print("\nReading inferred text from file...")
                if(not os.path.isfile(inferred_file)):
                    '''TODO: verificar se programa deve seguir p proxima pasta ou parar a execucao nesse caso'''
                    print("Inferred text file not found: ", inferred_file)
                    continue
                inferred_text = open(inferred_file, 'r').read()
                print("Inferred text from file " + inferred_file + " :")
                print(inferred_text)

            print("\nRefining inferred text with dictionary words...")
            refined_text = find_similarities(index, pt_dict, inferred_text)
            text_file = image_path+"text-refined_"+path+".txt"
            save_text(text_file, refined_text)
            print("Refined text saved as file at ", text_file)
        print("-------------------------------------------------")


if __name__ == '__main__':
    if os.path.isdir(samples_path):
        data_paths = os.listdir(samples_path)
        if(data_paths):
            
            #--------CRAFT--------------[set text_threshold = -1 to not execute this process]
            text_threshold = 0.7                    #default value to enable or not (-1) craft process
            
            craft_args = {
                'cuda': False,                      #'use cuda for inference'   (default = True)
                'poly': False,                      #'enable polygon type'      (default = False)
                'refine': False,                    #'enable link refiner'      (default = False)
                'text_threshold': text_threshold,   #'text confidence threshold'(default = 0.7)
                'low_text': 0.4,                    #'text low-bound score'     (default = 0.4)
                'link_threshold': 0.4               #'link confidence threshold'(default = 0.4)
            }

            #--------CROP-IMAGE---------[set median_threshold = -1 to not execute this process]
            median_threshold = 0.8                   #'split images with height greater than median * median_threshold' (default = 0.8)

            #--------SIMPLEHTR----------[set decoder = "" to not execute this process]
            decoder = 'bestpath'                    #'method used for decoding info into words' (default = 'bestpath)
            token_unity = 'word'                    #'granularity level for inference processing' (default = 'word')
            
            #--------SIMHASH------------[set find_sims = -1 to not execute this process]
            find_sims = 2                           #'distance value to find nearest word neighboors from dictionary' (default = 2)
            inferred_file = ""                      #'inferred file to read text and refine with dictionary'
            
            process_folder(data_paths, decoder, token_unity, find_sims, median_threshold, craft_args, inferred_file)

        else:
            print("Empty folder: ", samples_path)

    else:
        print("Folder not found: "+samples_path)
    
    
