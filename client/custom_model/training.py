# file for training the NN
# see https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html

import os
import torch
from .net import Net
import torch.nn as nn
from .utils import device
import torch.optim as optim
from .model_manager import ModelManager
from .dataset_manager import TrainingSet

class Training:
    def __init__(self):
        self.net = Net()
        self.device = device
        self.intialized = False
        self.set = TrainingSet()
        self.model = ModelManager()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)

    def train(self, epochs):
        """ Train the NN on the dataset in cats/. """

        if not self.intialized:
            self.initialize_training()

        for epoch in range(epochs):
            for i, data in enumerate(self.set.set, 0):

                inputs, labels, img_name = data
                inputs, labels = inputs.to(self.device), labels.to(self.device).squeeze().long()

                self.optimizer.zero_grad()

                outputs = self.net(inputs.float()) # predicted values (1 if cat 0 if not cat)
                loss = self.criterion(outputs, labels) # calculate the loss
                print('epoch:', epoch, 'loss of batch:', loss.item())
                loss.backward() # calculate improved weights beased on loss
                self.optimizer.step() # optimize with new weights

        print('Finished Training')
        PATH = os.path.abspath(os.path.dirname(__file__)+'/model/net.pth')
        torch.save(self.net.state_dict(), PATH)

    def initialize_training(self):

        self.net = self.net.float()
        self.net.cuda(self.device)

        if not self.model.installed:
            self.model.install()

        self.net.load_state_dict(self.model.load())

        if not self.set.installed:
            self.set.install()

        self.set.make_set()

        self.intialized = True

