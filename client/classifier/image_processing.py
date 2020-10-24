# File for handling image inputs (images from web and dataset for training)
# see https://towardsdatascience.com/building-efficient-custom-datasets-in-pytorch-2563b946fd9f

import numpy as np
from PIL import Image
from torch.utils.data.dataset import Dataset

# Class to handle image and label input
class ImageData(Dataset):
    def __init__(self, yx, width=256, height=256, transform=None):
        self.width = width
        self.height = height
        self.transform = transform
        y, x = yx # y is an array of labels, x is an array of images
        self.y = y
        self.x = x

    def __getitem__(self, index):
        img = Image.open(self.x[index]) # use pillow to open a file
        img = img.resize((self.width, self.height)) # resize the file to 256x256
        img = img.convert('RGB') #convert image to RGB channel
        if self.transform is not None:
            img = self.transform(img)

        img = np.asarray(img).transpose(-1, 0, 1) # we have to change the dimensions from width x height x channel (WHC) to channel x width x height (CWH)
        img = img/255
        img = torch.from_numpy(np.asarray(img)) # create the image tensor
        label = torch.from_numpy(np.asarray(self.y[index]).reshape([1, 1])) # create the label tensor
        return img, label, self.x[index]
    
    def __len__(self):
        return len(self.x)