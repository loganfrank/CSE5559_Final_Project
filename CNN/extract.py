## Basic Python libraries
import os
from PIL import Image

## Deep learning and array processing libraries
import numpy as np 
import torch
import torch.nn.functional as F 
import torchvision
import torchvision.transforms as transforms 

## Inner-project imports
from model import EncoderCNN, DecoderRNN

##### Code begins #####

# Path to config file
image_directory = './CNN/images/'
network_directory = './CNN/models/'

# Setting up other necessary paths
encoder_path = f'{network_directory}encoder-5-3000.pkl'

# Define the compute device (either GPU or CPU)
if torch.cuda.is_available():
    compute_device = torch.device('cuda:0')
else:
    compute_device = torch.device('cpu')
print(f'Using device: {compute_device}')

# Create the data transforms for evaluating
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

# Configure network
network = EncoderCNN(embed_size=256)
network = network.eval()
network.load_state_dict(torch.load(encoder_path, map_location='cpu'))
network = network.to(compute_device)

def get_visual_features(img):
    """
    Extracts the visual features from an input image. Converts input
    into PIL Image, normalizes the image, then feeds it through a CNN.
    The features returned from the CNN are then pooled into a 1x512x1x1
    and finally squeezed to produce our [512] array output.

    Input
    img :: 3D NumPy array
        Takes a [x, y, 3] NumPy array to be converted into a PIL Image

    Output
    features :: 1D NumPy array
        Returns a [512] NumPy array of the visual features from the CNN
    """

    # Convert to PIL Image and perform transformation
    img = Image.fromarray(img).convert('RGB')
    img = img.resize([224, 224], Image.LANCZOS)
    img = transform(img)

    # Add a 4th dimension and send to compute device (GPU or CPU)
    img = img.unsqueeze(0)
    img = img.to(compute_device)

    # Feed input through CNN
    features = network(img)

    # Squeeze into a [512] vector
    features = features.squeeze()

    # Convert to NumPy
    features = features.cpu().detach().numpy()
    return features

# Below is only there for testing, commented out for now
"""
if __name__ == '__main__':
    # Inference
    img = Image.open(f'{image_directory}input/1.png')
    img = np.asarray(img)
    features = get_visual_features(img)
    print('End')
"""