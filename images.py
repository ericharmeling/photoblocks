import subprocess


def image_match(directory, file_loc, target):
    """
    Checks if image is unique
    :param directory: Directory containing classify_image.py
    :param file_loc: Input image file location
    :param target: Target image category
    :return: True if image from file matches image category, False if not.
    """
    d = directory + "/models/tutorials/image/imagenet/"
    score = str(subprocess.check_output(["python", d + "classify_image.py ", "--image_file", file_loc]))
    print(score)
    if target in score:
        return True

    return False
