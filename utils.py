import skimage as ski

def load_image(filename):
    return ski.io.imread(filename)