# Image Captioning

This is adapted from srgvinod/a's tutorial on image captioning: https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Image-Captioning?tab=readme-ov-file

### Overview
This model takes in an input image and creates captions, utilizing a CNN for image processing and an RNN to create word sequences. 
The dataset is the MSCOCO dataset, consisting of thousands of images from daily life.

### Inference
To run the code in the command line:

`python caption.py --img='path/to/image.jpeg' --model='path/to/BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar' --word_map='path/to/WORDMAP_coco_5_cap_per_img_5_min_word_freq.json' --beam_size=5`

Make sure to specify the model path and word-map paths, which can be downloaded [here](https://drive.google.com/open?id=189VY65I_n4RTpQnmLGj7IzVnOF6dmePC). 
