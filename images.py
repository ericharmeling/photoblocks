import subprocess

def unique_image(file):
    """
    Checks if image is unique
    :param file: Input image file
    :param label: Target image category
    :return: True if image from file matches image category, False if not.
    """
    is_unique = subprocess.run(["unique.py", "--image-file" + file])
    return is_unique
