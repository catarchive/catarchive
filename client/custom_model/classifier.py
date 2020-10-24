# file that runs classification on given images

import torch
from .net import Net
from .utils import device
from .model_manager import ModelManager
from .image_processing import ImageData

# initialize model (model/net.pth)
model = ModelManager()

# initialize and setup the neural network
net = Net()
net = net.float()
net.cuda(device)

# install model if its not already
if not model.installed:
    model.install()

# load the model into the nn
net.load_state_dict(model.load())

def classify(img, is_url=False):
    """ Runs the given image through the model and returns the results. """
    
    data = ImageData([[True], [img]]) if not is_url else ImageData([[True], [img]], is_url=True)
    tensor_image, _, img_path = data[0]
    tensor_image = tensor_image.to(device).unsqueeze(0)
    
    output = net(tensor_image.float())

    _, predicted = torch.max(output, 1)
    cat = True if predicted.item() == 1 else False

    return cat, img_path


    