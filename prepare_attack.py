import os
import cv2
from predictor import predict

def remove_folder():
    for root, dirs, files in os.walk("test_img/imagenet", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def prepare_attack(img):
    remove_folder()
    img = cv2.resize(img, (224, 224))
    top_1, _, _ = predict(img)
    # print(top_1)
    os.mkdir('test_img/imagenet/' + top_1[0])
    cv2.imwrite("original.png", img)
    cv2.imwrite('test_img/imagenet/' + top_1[0] + '/1.png', img)

if __name__ == '__main__':
   img_path = 'test_img/panda.jpg'
   img = cv2.imread(img_path)
   prepare_attack(img) 
   