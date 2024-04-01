from PIL import Image
from torch.utils.data import Dataset
import os
from glob import glob
import torchvision.transforms as transforms
import torch

class MNIST(Dataset):
    """
    _summary_

    Args:
        root_dir: Path to the Main Dataset
        Mode: Load the Train Images or Test Images
        Rotate_List: Indicates which rotation values to be included in the dataset
        Perc_Data: Indicates the proportion of complete MNIST Data
    """
    def __init__(self, root_dir, mode = 'train', rotate_list=["", "-30"], perc_data=0.5):
        self.data_dir = root_dir
        self.mode = mode
        self.rotate_list = rotate_list
        self.perc_data = perc_data
        self._init_dataset()
        self._init_transform()

    def _init_dataset(self):
        self.files = []
        self.labels = []
        dirs = sorted(os.listdir(os.path.join(self.data_dir, 'training_')))  # Listing the directories which are 0, 1, 2, 3...
        if self.mode == 'train':                    # Load the train dataset
            for rotate_id in self.rotate_list:      # For every rotate_id listed in rotate_list
                for dir in range(len(dirs)):
                    files = sorted(glob(os.path.join(self.data_dir, f'training_{rotate_id}', dirs[dir], '*.png')))    # Extracting all the image path from a particular directory
                    files = files[:int(len(files)*self.perc_data)]    # Only selecting a portion of the original data
                    self.labels += [dir]*len(files)                   # Assigning the Corresponding Labels
                    self.files += files
        elif self.mode == 'test':                   # Load the train dataset
            for rotate_id in self.rotate_list:      # For every rotate_id listed in rotate_list
                for dir in range(len(dirs)):
                    files = sorted(glob(os.path.join(self.data_dir, f'testing_{rotate_id}', dirs[dir], '*.png')))     # Extracting all the image path from a particular directory
                    files = files[:int(len(files)*self.perc_data)]    # Only selecting a portion of the original data
                    self.labels += [dir]*len(files)                   # Assigning the Corresponding Labels
                    self.files += files
        else:
            print("No Such Dataset Mode")
            return None

    def _init_transform(self):
        # Converting the PIL Image to Torch Tensor and Normalising
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean = [0.5], std  = [0.5])
        ])

    def __getitem__(self, index):
        img = Image.open(self.files[index]).convert('L')     # "L" refers to Black & White, i.e loading the image in (H, W) format
        label = self.labels[index]

        img = self.transform(img)

        label = torch.tensor(label, dtype = torch.long)     # Converting the label to tensor and Long Data type

        return img, label

    def __len__(self):
        return len(self.files)