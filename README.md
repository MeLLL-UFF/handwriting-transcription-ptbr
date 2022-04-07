# handwritten-transcription

## Run demo
1. Download Pytorch CRAFT text detector tool: https://github.com/clovaai/CRAFT-pytorch .
2. Download "General" pretrained model in the section "Test instruction using pretrained model": https://github.com/clovaai/CRAFT-pytorch .
3. Create "weights" folder and insert model file downloaded at step 2.
4. Download SimpleHTR tool: https://github.com/githubharald/SimpleHTR
5. Download "Model trained on word images" in the section "Run demo": https://github.com/githubharald/SimpleHTR
6. Insert download files at step 5 in the "model" folder
7. Change model_dir at SimpleHTR-master/src/model.py (Line 156) to "./model"
8. Create "data" folder
8. Insert image file (.jpg, .jpeg, .gif, .png, .pgm) into a specific folder inside "data" folder.
9. Run "transcriber.py"