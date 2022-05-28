import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.vgg16  import VGG16 

from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import cv2
# model = ResNet50(weights='imagenet')
model = VGG16(weights='imagenet')
# it will return top 3 labels as a list -> (label, confidence)
def predict(img):
    x = img
    # x = image.img_to_array(img) # Converts a PIL Image instance to a Numpy array
    x = np.expand_dims(x, axis=0)

    # The images are converted from RGB to BGR, then each color channel is zero-centered with respect to the ImageNet dataset
    # x = preprocess_input(x)

    # predict label
    preds = model.predict(x)

    # decode the results into a list of tuples (class, description, probability)
    results = decode_predictions(preds, top=3)[0]

    top_1 = results[0][1], float("{:.5f}".format(results[0][2]))
    top_2 = results[1][1], float("{:.5f}".format(results[1][2]))
    top_3 = results[2][1], float("{:.5f}".format(results[2][2]))
    print("top 1: ", top_1)
    print("top 2: ", top_2)
    print("top 3: ", top_3)
    return top_1, top_2, top_3

if __name__ == '__main__':
        # img_path = 'test_img/school_bus.jpg'
        img_path = 'result.png'
        # img_path = 'panda.jpg'
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        predict(img)