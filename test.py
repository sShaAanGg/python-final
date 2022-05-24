import torch
import cv2
import torchvision
import torchvision.models as models
resnet50 = models.resnet50(pretrained = True)


img_path = 'result.png'
img = cv2.imread(img_path)
pred = resnet50(img)