#!/usr/bin/env python3

import torch
from PIL import Image
from torchvision import models
from torchvision import transforms

from .labels import labels

# Declare our NN model:
resnet = models.resnet50(pretrained=True)

# The preprocessing effects to be applied to each image:
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def classify(img):
    """Runs the given image through the ResNet model and returns the results."""

    # Preprocess the image:
    img_t = preprocess(Image.open(img.raw).convert('RGB'))

    # Feed the image through ResNet:
    batch_t = torch.unsqueeze(img_t, 0)
    resnet.eval()
    out = resnet(batch_t)

    # Calculate and returns the results:
    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    cat = False
    if index[0] in list(range(281,286)):
        cat = True

    _, indices = torch.sort(out, descending=True)
    results = [(labels[idx], int(percentage[idx].item())) for idx in indices[0][:3]]

    return (cat, results)
