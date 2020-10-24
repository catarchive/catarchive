# file for managing the datasets for training

import os 
import zipfile
import requests
from .utils import get_images
from .image_processing import ImageData
from torch.utils.data import DataLoader

class TrainingSet:
    """ Stores state of the training set. """

    def __init__(self, url='https://hosting.greerpage.com/files/greer_page/cats.zip'):
        self.url = url
        self.dir = os.path.abspath(os.path.dirname(__file__)+'/cats')
        self.installed = os.path.isdir(self.dir)
        self.zip = os.path.abspath(os.path.dirname(__file__)+'/cats.zip')

    def install(self):
        """ Install the dataset if necessary. """

        if self.installed:
            print('cats already installed!')
            return

        print('downloading dataset, this will take some time...')
        os.mkdir(self.dir)
        r = requests.get(self.url, allow_redirects=True)
        open(self.zip, 'wb').write(r.content)
        with zipfile.ZipFile(self.zip, 'r') as z:
            z.extractall(os.path.abspath(os.path.dirname(__file__)))
        os.remove(self.zip)

    def make_set(self):
        """ Run the set images through pytorch's DataLoader module. """

        if not self.installed:
            print('dataset not installed')
            return 

        self.data = ImageData(get_images())
        self.set = DataLoader(self.data, batch_size=10, shuffle=True, num_workers=1)