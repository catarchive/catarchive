from .image_processing import ImageData
from .net import Net
from .model_manager import ModelManager
from .utils import device
import torch



model = ModelManager()

net = Net()
net = net.float()
net.cuda(device)

if not model.installed:
    model.install()

net.load_state_dict(model.load())

def classify(img):
    """ Runs the given image through the model and returns the results. """
    
    data = ImageData([[True], [img]])
    tensor_image, label, img_path = data[0]
    tensor_image, label = tensor_image.to(device).unsqueeze(0), label.to(device)
    
    output = net(tensor_image.float())

    _, predicted = torch.max(output, 1)

    return predicted.item()


    