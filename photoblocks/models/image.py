from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

class Image:
    """
    Image classifier
    """

    def __init__(self, image_path, label=None):
        self.image_path = image_path
        self.label = label
        self.validated = False
        self.model = VGG16(weights='imagenet', include_top=False)

    @property
    def loaded_image(self):
        return image.load_img(self.image_path, target_size=(224, 224))

    @property
    def preprocessed_image(self):
        img = image.img_to_array(self.loaded_image)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        return img


    def image_match(self):
        features = self.model.predict(self.preprocessed_image)
        if self.label in features:
            return True
        else:
            return False
