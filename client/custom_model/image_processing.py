# file for handling image inputs (images from web and dataset for training)
# see https://towardsdatascience.com/building-efficient-custom-datasets-in-pytorch-2563b946fd9f

import torch
import numpy as np
from PIL import Image
from torch.utils.data.dataset import Dataset


class ImageData(Dataset):
    """ Class to represent image and label input. """

    def __init__(self, yx, is_url=False, width=256, height=256, transform=None):
        self.width = width
        self.height = height
        self.transform = transform
        self.is_url = is_url
        y, x = yx 
        self.y = y # array of label
        self.x = x # array of image paths

    def __getitem__(self, index):
        """ Process image and labels to be sent to the NN. """

        img = Image.open(self.x[index]) if not self.is_url else Image.open(self.x[index].raw)
        img = img.resize((self.width, self.height)) 
        img = img.convert('RGB') #convert image to RGB channel
        if self.transform is not None:
            img = self.transform(img)

        img = np.asarray(img).transpose(-1, 0, 1) # we have to change the dimensions from width x height x channel (WHC) to channel x width x height (CWH)
        img = img/255
        img = torch.from_numpy(np.asarray(img)) # create the image tensor
        label = torch.from_numpy(np.asarray(self.y[index]).reshape([1, 1])) # create the label tensor
        
        return img, label, self.x[index] if not self.is_url else self.x[index].url
    
    def __len__(self):
        return len(self.x)