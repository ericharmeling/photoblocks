import torch

class Image:
    def __init__(self, image, label, transformer, model):
        self.raw_image = image
        self.label = label
        self.transformer = transformer
        self.model = model
        self.validated = False

    @property
    def transformed_image(self):
        return self.transformer(self.image)

    @property
    def preprocessed_image(self):
        return torch.unsqueeze(self.transformed_image)

    def image_match(image, label):
        """
        Checks if image is unique
        :param image: Input image
        :param label: Input label
        :return: True if image from file matches image category, False if not.
        """
        score = str(subprocess.check_output(["python", d + "classify_image.py ", "--image_file", file_loc]))
        print(score)
        if target in score:
            return True

        return False
