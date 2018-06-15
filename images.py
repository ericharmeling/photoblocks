import subprocess

def image_match(file, label):
    """
    :param file: Input image file
    :param target: Target image category
    :return: True if image from file matches image category, False if not.
    """
    image = subprocess.run(["models/tutorials/image/imagenet/classify_image.py", "--image-file" + file])
    return image == label
