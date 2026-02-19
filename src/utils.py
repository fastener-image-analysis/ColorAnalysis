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
    """
    Converts an image in the SRGB colorspace to the linear RGB colorspace
    INPUTS:
    image (array): an array representing the full SRGB image
    OUTPUTS
    linear_image(array)L an array representing the full linear RGB image
    """
    linear_image = np.where(image <= 0.0031308,
                            image / 12.92,
                            ((image + 0.055) / 1.055) ** 2.4)
    return linear_image

def linear_to_srgb(image):
    """
    Converts an image in the linear RGB colorspace to the SRGB colorspace
    INPUTS:
    image (array): an array representing the full linear RGB image
    OUTPUTS
    srgb_image (array): an array representing the full SRGB image
    """
    srgb_image = np.where(image <= 0.0031308,
                 image * 12.92,
                 1.055 * image ** (1/2.4) - 0.055)
    return srgb_image

def build_results_table(blackness, color_shift, a_shift, b_shift, gloss):
    """
    Builds a pandas DataFrame that contains the response variables of analysis
    INPUTS:
    blackness (list): A list of calculated blackness values for each part
    color_shift (list): A list of calculated color shift values for each part
    a_shift (list): A list of calculated median a values for each part
    b_shift (list): A list of calculated median b values for eahc part
    gloss (list): A list of calculated gloss score values for each part
    OUTPUTS:
    df (pandas DataFrame): a dataframe consisting of all the analyzed parts and their respective response variables
    """
    df = pd.DataFrame({
        'Part #': list(range(1, len(blackness) + 1)),
        'Blackness': blackness,
        'Color Shift': color_shift,
        'Gloss Factor': gloss,
        'Median a*': a_shift,
        'Median b*': b_shift
    })
    return df