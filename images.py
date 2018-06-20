import subprocess


def image_match(file, target):
    """
    Checks if image is unique
    :param file: Input image file
    :param target: Target image category
    :return: True if image from file matches image category, False if not.
    """
    label = str(subprocess.run(["classify_image.py ", "--image-file " + file]))
    if target in label:
        return True

    return False
