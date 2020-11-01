# file that defines external functions

import os 
import torch
from .net import Net
from .image_processing import ImageData
from .initialize_net import InitializeNet

# initilaize the state for the NN and other necessary info
i = InitializeNet()
net, device, model, dset, optimizer, criterion = i.net, i.device, i.model, i.set, i.optimizer, i.criterion

# install model if its not isntalled
if not model.installed:
    model.install()

# set up the NN
net.cuda(device)
net.load_state_dict(model.load())

def classify(img, is_url=False):
    """ Runs the given image through the model and returns the results. """

    data = ImageData([[True], [img]]) if not is_url else ImageData([[True], [img]], is_url=True) # pass image to be "tensorized"
    tensor_image, _, img_path = data[0] # get image tensor etc
    tensor_image = tensor_image.to(device).unsqueeze(0) # format image tensor
    
    output = net(tensor_image.float()) # run image tensor through network to get predicted value (1 is cat 0 is not)

    _, predicted = torch.max(output, 1)
    cat = True if predicted.item() == 1 else False

    return cat, img_path

def train(epochs, start_from_scratch=False):
    """ Train the NN on the dataset in cats/. """
        
    n = Net() if start_from_scratch else net
    n.cuda(device)

    if not dset.installed:
         dset.install()

    dset.make_set()

    for epoch in range(epochs):
        for _, data in enumerate(dset.set, 0):

            inputs, labels, _ = data
            inputs, labels = inputs.to(device), labels.to(device).squeeze().long()

            optimizer.zero_grad()

            outputs = n(inputs.float()) # predicted values (1 if cat 0 if not cat)
            loss = criterion(outputs, labels) # calculate the loss
            print('epoch:', epoch, 'loss of batch:', loss.item())
            loss.backward() # calculate improved weights based on loss
            optimizer.step() # optimize with new weights

    print('Finished Training')
    PATH = os.path.abspath(os.path.dirname(__file__)+'/model/net.pth')
    torch.save(net.state_dict(), PATH)