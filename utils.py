from skimage.io import imread
import numpy as np
import pandas as pd

def load_image(filename):
    """
    Load an image file and return it as a numpy array
    INPUTS:
    filename (string): the path to the image file

    OUTPUTS:
    image (numpy array): the loaded image as a numpy array
    """
    image = imread(filename).astype(float) / 255.0
    return image

def srgb_to_linear(image):
    linear_image = np.where(image <= 0.0031308,
                            image / 12.92,
                            ((image + 0.055) / 1.055) ** 2.4)
    return linear_image

def linear_to_srgb(image):
    srgb_image = np.where(image <= 0.0031308,
                 image * 12.92,
                 1.055 * image ** (1/2.4) - 0.055)
    return srgb_image

def build_results_table(blackness, color_shift, a_shift, b_shift, gloss):
    df = pd.DataFrame({
        'Part #': list(range(1, len(blackness) + 1)),
        'Blackness': blackness,
        'Color Shift': color_shift,
        'Gloss Factor': gloss,
        'Median a*': a_shift,
        'Median b*': b_shift
    })
    return df