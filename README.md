# handwritten-transcription

## Run demo
1. Download Pytorch CRAFT text detector tool: https://github.com/clovaai/CRAFT-pytorch
2. Unzip folder downloaded in the step 1 and insert it inside PTBR-HTranscription folder
3. Download "General" pretrained model in the section "Test instruction using pretrained model" from https://github.com/clovaai/CRAFT-pytorch
4. Create "weights" folder inside PTBR-HTranscription folder and insert the model file downloaded in the step 3
5. Download SimpleHTR tool: https://github.com/githubharald/SimpleHTR
6. Unzip folder downloaded in the step 5 and insert it inside PTBR-HTranscription folder
7. Download "Model trained on word images" in the section "Run demo" from https://github.com/githubharald/SimpleHTR
8. Insert downloaded files in the step 7 inside "model" folder in PTBR-HTranscription folder
9. Change model_dir at SimpleHTR-master/src/model.py (Line 156) to "./model"
10. Create "data" folder inside PTBR-HTranscription folder
11. Insert image file (.jpg, .jpeg, .gif, .png, .pgm) into a specific folder inside "data" folder.
12. Go to PTBR-HTranscription folder and run "transcriber.py"