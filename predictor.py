from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights='imagenet')

def predict(img):
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)

    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    ans = decode_predictions(preds, top=3)[0]
    print("top 1: ", ans[0][1], ans[0][2])
    print("top 2: ", ans[1][1], ans[1][2])
    print("top 3: ", ans[2][1], ans[2][2])
    # print('Predicted:', decode_predictions(preds, top=3)[0])

if __name__ == '__main__':
        img_path = 'cat.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
        predict(img)