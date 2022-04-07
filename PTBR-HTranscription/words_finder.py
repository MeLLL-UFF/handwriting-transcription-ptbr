import os
import time
import cv2
import torch
import torch.backends.cudnn as cudnn
import sys
sys.path.insert(1, './CRAFT-pytorch-master')
from craft import CRAFT
from test import copyStateDict, test_net
from file_utils import get_files, saveResult
from imgproc import loadImage

#default paths
model_folder = "./weights/craft_mlt_25k.pth"
refiner_model = ""

## Crop found words in image
# @param image_list list of images to find words
# @param result_folder folder to store word images  
# @param craft_args tool arguments
# @param model_folder pretrained model folder
# @param refiner_model pretrained refiner model
def run_craft(image_list, result_folder, craft_args, model_folder=model_folder,  refiner_model=refiner_model):
    # load CRAFT net
    net = CRAFT()
    print('Loading weights from checkpoint (' + model_folder + ')')

    # load CUDA procedures
    if craft_args['cuda']:
        net.load_state_dict(copyStateDict(torch.load(model_folder)))
    else:
        net.load_state_dict(copyStateDict(torch.load(model_folder, map_location='cpu')))

    if craft_args['cuda']:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False

    net.eval()

    # LinkRefiner
    refine_net = None
    poly = craft_args['poly']
    if craft_args['refine']:
        from refinenet import RefineNet
        refine_net = RefineNet()
        print('Loading weights of refiner from checkpoint (' + refiner_model + ')')
        if craft_args['cuda']:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model)))
            refine_net = refine_net.cuda()
            refine_net = torch.nn.DataParallel(refine_net)
        else:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model, map_location='cpu')))

        refine_net.eval()
        poly = True

    t = time.time()

    bboxes = []
    # load data
    for k, image_path in enumerate(image_list):
        print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path))#, end='\r')
        image = loadImage(image_path)

        # find words
        bboxes, polys, score_text = test_net(net, image, craft_args['text_threshold'], craft_args['link_threshold'], craft_args['low_text'], craft_args['cuda'], poly, refine_net)

        # save score text
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = result_folder + "/res_" + filename + '_mask.jpg'
        cv2.imwrite(mask_file, score_text)

        saveResult(image_path, image[:,:,::-1], polys, dirname=result_folder)

    print("elapsed time : {}s".format(time.time() - t))
    return len(bboxes)