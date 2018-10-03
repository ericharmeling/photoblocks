import subprocess


def image_match(directory, file, target):
    """
    Checks if image is unique
    :param directory: Directory containing classify_image.py
    :param file: Input image file
    :param target: Target image category
    :return: True if image from file matches image category, False if not.
    """
    label = str(subprocess.call(["python", directory + "classify_image.py ", "--image_file", file]))
    if target in label:
        return True

    return False
