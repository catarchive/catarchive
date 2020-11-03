# file to hanle network file (model/net.pth)

import os 
import sys
import time
import torch
import requests

from .utils import device

class ModelManager:
    """ Class to represent the model file. """
    
    def __init__(self, url='https://hosting.greerpage.com/files/greer_page/net.pth'):
        self.path = os.path.abspath(os.path.dirname(__file__)+'/model/net.pth')
        self.dir = os.path.abspath(os.path.dirname(__file__)+'/model')
        self.installed = os.path.isfile(self.path)
        self.url = url

    def install(self):
        """ Download and install the pre-trained net.pth file. """
        
        if self.installed:
            print('Model already installed')
            return

        print('Downloading model to', self.path)

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
            
        with open(self.path, 'wb') as f:
            r = requests.get(self.url, allow_redirects=True, stream=True)
            total_length = round(float(r.headers['Content-Length']) / 1024 / 1024, 1)
            dl = 0
            start = time.time()
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                sys.stdout.write('\r{}/{}MB, {} MB/s'.format(round(dl / 1024 / 1024, 1), total_length, round((dl // (time.time() - start)) / 1024 / 1024, 1)))
            print('')

        return self.path

    def load(self):
        """ Load the model for the NN. """

        return torch.load(self.path, map_location=device)

