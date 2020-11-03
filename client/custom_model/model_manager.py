# file to hanle network file (model/net.pth)

import os 
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
            print('model already installed')
            return

        print('downloading model...')

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
            
        r = requests.get(self.url, allow_redirects=True)
        open(self.path, 'wb').write(r.content)

        return self.path

    def load(self):
        """ Load the model for the NN. """

        return torch.load(self.path, map_location=device)

