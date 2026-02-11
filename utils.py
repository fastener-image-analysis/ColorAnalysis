import skimage as ski

def load_image(filename):
    """
    Load an image file and return it as a numpy array
    INPUTS:
    filename (string): the path to the image file

    OUTPUTS:
    image (numpy array): the loaded image as a numpy array
    """
    return ski.io.imread(filename).astype(float) / 255.0