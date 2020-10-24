# file containing the network model
# see https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html

import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    ''' class representing the neural network '''

    def __init__(self):
        ''' initialie the model with appropriate starting weights '''
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 256, 256)
        self.pool = nn.MaxPool2d(1, 1)
        self.conv2 = nn.Conv2d(256, 16, 1)
        self.fc1 = nn.Linear(16 * 1 * 1, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        ''' calculations based on image tensor input '''

        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 1 * 1) # see https://discuss.pytorch.org/t/runtimeerror-shape-1-400-is-invalid-for-input-of-size/33354/5
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x