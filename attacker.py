import numpy as np
import warnings
warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import json
import torchvision.utils

from torchvision import models
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from tensorflow.keras.preprocessing import image
import cv2
import torchattacks
from predictor import predict
from utils import image_folder_custom_label

# load data 
class_idx = json.load(open("imagenet_class_index.json"))
idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
# print(idx2label)
# exit()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(), # ToTensor : [0, 255] -> [0, 1]   
])

imagnet_data = image_folder_custom_label(root='test_img\imagenet', transform=transform, idx2label=idx2label)
data_loader = torch.utils.data.DataLoader(imagnet_data, batch_size=1, shuffle=False)
images, labels = iter(data_loader).next()
# print("True Image & True Label")
# print(images)
# imshow(torchvision.utils.make_grid(images, normalize=True), [imagnet_data.classes[i] for i in labels])

use_cuda = True
device = torch.device("cuda" if use_cuda else "cpu")

class Normalize(nn.Module):
    def __init__(self, mean, std) :
        super(Normalize, self).__init__()
        self.register_buffer('mean', torch.Tensor(mean))
        self.register_buffer('std', torch.Tensor(std))
        
    def forward(self, input):
        # Broadcasting
        mean = self.mean.reshape(1, 3, 1, 1)
        std = self.std.reshape(1, 3, 1, 1)
        return (input - mean) / std

norm_layer = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

model = nn.Sequential(
    norm_layer,
    models.resnet50(pretrained=True)
).to(device)

model = model.eval()

def attack(img):
    # attacker = torchattacks.BIM(model, eps=16/255, alpha=2/255, steps=100)

    attacker = torchattacks.MIFGSM(model, eps=8/255, alpha=2/255, steps=100)
    # attacker.set_mode_targeted_least_likely(1)  # Targeted attack
    attacker.set_mode_targeted_random()
    # attacker = torchattacks.CW(model, c=1, lr=0.01, steps=100, kappa=0),
    # label, _, _ = predict(img)
    adv_images = attacker(img, labels)

    data = torchvision.utils.make_grid(adv_images.cpu().data, normalize=True)
    npimg = data.numpy()
    npimg = npimg * 255

    # print(np_arr)
    print(npimg.shape)
    npimg = np.transpose(npimg,(1,2,0))
    print(npimg.shape)
    
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB)
    cv2.imwrite("result.png", npimg)
    # attacker.save(data_loader, save_path="result.pt", verbose=True)


if __name__ == '__main__':
    # img_path = 'test_img/cat.jpg'
    # img = image.load_img(img_path, target_size=(224, 224))
    # img = image.img_to_array(img)
    # img = np.expand_dims(img, axis=0)
    # print(img.shape)
    attack(images)