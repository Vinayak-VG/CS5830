from PIL import Image
from glob import glob
import os

##### Task 1 #######
def rotate_img(image, angle):
    img = Image.open(image)
    img = img.rotate(angle)     # Used PIL library to rotate the Image
    
    # Saving the Rotated Image appropriately
    if "training" in image:
        img.save(image.replace("training_", f'training_{angle}'))
    if "testing" in image:
        img.save(image.replace("testing_", f'testing_{angle}'))

###################

###### Task 2 #######

def generate_dataset(dataset_root):
    # Training Images
    dirs = sorted(os.listdir(os.path.join(dataset_root, 'training_')))
    rotated = [-30, -20, -10, 10, 20, 30]
    for dir in range(len(dirs)):
        files = sorted(glob(os.path.join(dataset_root, 'training_', dirs[dir], '*.png')))
        for rotate in rotated:
            os.makedirs(os.path.join(dataset_root, f'training_{rotate}', dirs[dir]), exist_ok=True)
            for img_name in files:
                rotate_img(img_name, rotate) # Rotating the Image by the required angle and saving it in a different folder
    
    # Testing Images
    dirs = sorted(os.listdir(os.path.join(dataset_root, 'testing_')))
    rotated = [-30, -20, -10, 10, 20, 30]
    for dir in range(len(dirs)):
        files = sorted(glob(os.path.join(dataset_root, 'testing_', dirs[dir], '*.png')))
        for rotate in rotated:
            os.makedirs(os.path.join(dataset_root, f'testing_{rotate}', dirs[dir]), exist_ok=True)
            for img_name in files:
                rotate_img(img_name, rotate)  # Rotating every Image by the required angle and saving it in a different folder
                
generate_dataset("mnist_png/")   