# file for state of net class

from .net import Net
from .utils import device
from .model_manager import ModelManager
from .image_processing import ImageData
from .dataset_manager import TrainingSet
import torch.nn as nn
import torch.optim as optim

class InitializeNet:
    """ Class to store the state of the net and other necessary things. """
    
    def __init__(self, training=False):
        self.device = device
        self.net = Net()
        self.net = self.net.float()
        self.model = ModelManager()
        self.set = TrainingSet()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)