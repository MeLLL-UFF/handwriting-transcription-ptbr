# handwritten-transcription

## Run demo
1. Download [Pytorch CRAFT text detector](https://github.com/clovaai/CRAFT-pytorch) tool
2. Unzip folder downloaded in the step 1 and insert it inside `PTBR-HTranscription` folder
3. Create `\__init\__.py` file and insert it in unzipped folder
4. Download ***General*** pretrained model in the section "*[Test instruction using pretrained model](https://github.com/clovaai/CRAFT-pytorch#test-instruction-using-pretrained-model)*" from CRAFT tool
5. Create `weights` folder inside `PTBR-HTranscription` folder and insert the model file downloaded in the step 3
6. Download [Handwritten Text Recognition with TensorFlow (SimpleHTR)](https://github.com/githubharald/SimpleHTR) tool
7. Unzip folder downloaded in the step 6 and insert it inside `PTBR-HTranscription` folder
8. Create `\__init\__.py` file and insert it in unzipped folder
9. Download ***Model trained on word images*** in the section "*[Run demo](https://github.com/githubharald/SimpleHTR#run-demo)*" from SimpleHTR tool
10. Insert downloaded files in the step 9 inside `model` folder in `PTBR-HTranscription` folder
11. Change ***model_dir*** at `SimpleHTR-master/src/model.py` (Line 156) to *"./model"*
12. Create `data` folder inside `PTBR-HTranscription` folder
13. Insert image file *(.jpg, .jpeg, .gif, .png, .pgm)* into a subfolder inside `data` folder.
14. Download [Brazilian Portuguese dictionary](https://sites.icmc.usp.br/taspardo/dicionario_port.zip)
15. Insert unzipped downloaded file in the step 14 inside `PTBR-HTranscription` folder
16. Install `requirements.txt` from each tool (*consider installing newer versions of deprecated dependencies*)
17. Go to `PTBR-HTranscription` folder and run `transcriber.py`
