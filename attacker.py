import cv2
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import torchvision.utils
from torchvision import models
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from tensorflow.keras.preprocessing import image

import torchattacks
from utils import image_folder_custom_label

from predictor import predict

# load data 
class_idx = json.load(open("imagenet_class_index.json"))
idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(), # ToTensor : [0, 255] -> [0, 1]   
])

# imagnet_data = image_folder_custom_label(root='test_img\imagenet', transform=transform, idx2label=idx2label)
# data_loader = torch.utils.data.DataLoader(imagnet_data, batch_size=1, shuffle=False)
# images, labels = iter(data_loader).next()
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
    # models.resnet50(pretrained=True)
    models.vgg16(pretrained = True)
).to(device)

model = model.eval()

adv_image = 0

def attack(img, mode=None):
    imagnet_data = image_folder_custom_label(root='test_img\imagenet', transform=transform, idx2label=idx2label)
    data_loader = torch.utils.data.DataLoader(imagnet_data, batch_size=1, shuffle=False)
    images, labels = iter(data_loader).next()
    # attacker = torchattacks.BIM(model, eps=8/255, alpha=4/255, steps=150)
    # attacker = torchattacks.CW(model, c=0.1, steps=1000, lr=0.01)
    # attacker = torchattacks.CW(model, c=1, lr=0.01, steps=100, kappa=0),
    attacker = torchattacks.MIFGSM(model, eps=4/255, alpha=2/255, steps=100)

    # set attack mode if requested
    if mode == "random":
        attacker.set_mode_targeted_random()
    elif mode == "least_likely":
        attacker.set_mode_targeted_least_likely(1)  # Targeted attack
    images = images.to(device)
    # attack start
    adv_images = attacker(images, labels)
    outputs = model(adv_images)
    m = nn.Softmax(dim=1)
    logits = m(outputs.data)
    prob = torch.topk(logits, 3)
    _, pre = torch.topk(outputs.data, 3)
    # _, pre = torch.max(outputs.data, 1)
    prob_list = prob[0].tolist()[0]
    top_1 = imagnet_data.classes[pre[0][0]], float("{:.5f}".format(prob_list[0]))
    top_2 = imagnet_data.classes[pre[0][1]], float("{:.5f}".format(prob_list[1]))
    top_3 = imagnet_data.classes[pre[0][2]], float("{:.5f}".format(prob_list[2]))

    print("attack finished!")
    print(top_1)
    print(top_2)
    print(top_3)

    # save adversarial image
    data = torchvision.utils.make_grid(adv_images.cpu().data, normalize=True)
    npimg = data.numpy()
    npimg = npimg * 255
    npimg = np.transpose(npimg,(1,2,0))
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB)
    cv2.imwrite("D:/python_final/python-final/result.png", npimg)
    
    return top_1, top_2, top_3

# def predict():
#     imagnet_data = image_folder_custom_label(root='test_img\imagenet', transform=transform, idx2label=idx2label)
#     data_loader = torch.utils.data.DataLoader(imagnet_data, batch_size=1, shuffle=False)
#     images, labels = iter(data_loader).next()
#     images = images.to(device)
#     outputs = model(images)
#     m = nn.Softmax(dim=1)
#     logits = m(outputs.data)
#     prob = torch.topk(logits, 3)
#     _, pre = torch.topk(outputs.data, 3)
#     # _, pre = torch.max(outputs.data, 1)
#     prob_list = prob[0].tolist()[0]
#     top_1 = imagnet_data.classes[pre[0][0]], float("{:.3f}".format(prob_list[0]))
#     top_2 = imagnet_data.classes[pre[0][1]], float("{:.3f}".format(prob_list[1]))
#     top_3 = imagnet_data.classes[pre[0][2]], float("{:.3f}".format(prob_list[2]))

#     print("attack finished!")
#     print(top_1)
#     print(top_2)
#     print(top_3)
#     return top_1, top_2, top_3
if __name__ == '__main__':
    pass