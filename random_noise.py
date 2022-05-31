import cv2
import numpy as np
from predictor import predict

def add_random_noise(img):
    mean = 0
    var = 30
    sigma = var ** 0.8
    gaussian = np.random.normal(mean, sigma, (img.shape[0],img.shape[1], img.shape[2])) 
    noisy_image = img + gaussian
    cv2.imwrite("result/random_noise_image.png", noisy_image)
    return noisy_image

if __name__ == '__main__':
        # img_path = 'test_img/school_bus.jpg'
        img_path = 'result.png'
        # img_path = 'panda.jpg'
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        noisy_image = add_random_noise(img)
        print("original: ")
        predict(img)
        print("noisy_image: ")
        predict(noisy_image)
        