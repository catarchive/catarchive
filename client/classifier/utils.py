# utility things

import torch

# define the device for torch to use (cuda is nvidia graphics)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")