# file that runs classification on given images

import torch
from .image_processing import ImageData
from .initialize_net import InitializeNet

def classify(img, is_url=False):
    """ Runs the given image through the model and returns the results. """

    i = InitializeNet()
    net, device, model = i.net, i.device, i.model

    if not model.installed:
        model.install()
    
    net.cuda(device)
    net.load_state_dict(model.load())
    
    data = ImageData([[True], [img]]) if not is_url else ImageData([[True], [img]], is_url=True)
    tensor_image, _, img_path = data[0]
    tensor_image = tensor_image.to(device).unsqueeze(0)
    
    output = net(tensor_image.float())

    _, predicted = torch.max(output, 1)
    cat = True if predicted.item() == 1 else False

    return cat, img_path

def train(self, epochs):
    """ Train the NN on the dataset in cats/. """

    

    for epoch in range(epochs):
        for i, data in enumerate(self.set.set, 0):

            inputs, labels, img_name = data
            inputs, labels = inputs.to(self.device), labels.to(self.device).squeeze().long()

            self.optimizer.zero_grad()

            outputs = self.net(inputs.float()) # predicted values (1 if cat 0 if not cat)
            loss = self.criterion(outputs, labels) # calculate the loss
            print('epoch:', epoch, 'loss of batch:', loss.item())
            loss.backward() # calculate improved weights based on loss
            self.optimizer.step() # optimize with new weights

    print('Finished Training')
    PATH = os.path.abspath(os.path.dirname(__file__)+'/model/net.pth')
    torch.save(self.net.state_dict(), PATH)

    