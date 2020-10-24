# utility things

import os
import torch

# define the device for torch to use (cuda is nvidia graphics)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# get all of the images for the data set
def get_images():
    image_values = {}
    data = [[], []]
    cats, not_cats = os.path.abspath(os.path.dirname(__file__) + '/cats/cats/'), os.path.abspath(os.path.dirname(__file__) + '/cats/not_cats/')
    for x in os.listdir(cats):
        image_values[cats+'/'+x] = True 
    for x in os.listdir(not_cats):
        image_values[not_cats+'/'+x] = False
    
    for x in image_values:
        data[0].append(True) if image_values[x] else data[0].append(False)
        data[1].append(x)

    return data
