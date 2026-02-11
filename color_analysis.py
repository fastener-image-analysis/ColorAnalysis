import numpy as np
from skimage.color import rgb2lab
from skimage.color import rgb2xyz, xyz2lab
from skimage import color, exposure

def normalize_from_bg(substrate, bg_mask):
    img = srgb_to_linear(substrate)
    bg_pixels = img[bg_mask]
    if np.any(bg_pixels.max(axis=0) > 0.98):
        print('Warning: Background may be clipping!')
    bg_mean = bg_pixels.mean(axis=0)
    correction = 1.0 / bg_mean
    img_normalized = np.clip(img * correction[None, None, :], 0, 1)
    img_normalized = linear_to_srgb(img_normalized)
    return(img_normalized)

def srgb_to_linear(img):
    """Convert sRGB to linear RGB"""
    return np.where(img <= 0.04045,
                    img / 12.92, 
                    ((img + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(img):
    """Convert linear RGB back to sRGB"""
    return np.where(img <= 0.0031308,
                    img * 12.92,
                    1.055 * img ** (1/2.4) - 0.055)

def convert_to_lab(substrate):
    """
    Convert the input RGB image to LAB color space and return the L, a, b channels separately.
    INPUTS:
    substrate (numpy array): the input RGB image as a numpy array
    OUTPUTS:
    L (numpy array): the L channel of the LAB color space
    a (numpy array): the a channel of the LAB color space
    b (numpy array): the b channel of the LAB color space
    """
    lab = rgb2lab(substrate)
    return lab[..., 0], lab[..., 1], lab[..., 2]

def get_lab_parts(L, a, b, part_masks):
    part_lab = []
    for m in part_masks:
        part_lab.append((L[m], a[m], b[m]))
    return part_lab


def normalize_parts(L, a, b, background_mask, part_masks):
    """
    Normalize the L, a, b values of the parts by subtracting the median L, a, b values of the background.
    This helps to account for variations in lighting and color across the substrate.
    INPUTS:
    L (numpy array): the L channel of the LAB color space
    a (numpy array): the a channel of the LAB color space
    b (numpy array): the b channel of the LAB color space
    background_mask (numpy array): a binary mask where True indicates background pixels
    part_masks (list of numpy arrays): a list of binary masks corresponding to the detected parts
    OUTPUTS:
    normalized_parts (list of tuples): a list where each element is a tuple containing the normalized
    L, a, b values for the corresponding part mask in part_masks
    """
    L_ref = np.median(L[background_mask])
    a_ref = np.median(a[background_mask])
    b_ref = np.median(b[background_mask])

    normalized = []
    for m in part_masks:
        normalized.append((L[m] - L_ref, a[m] - a_ref, b[m] - b_ref))
    return normalized


def compute_metrics(normalized_parts):
    """
    Compute color and gloss metrics for each part based on the normalized L, a, b values.
    The metrics include:
    - Blackness: the 10th percentile of the normalized L values (lower is black
    - Color Shift: the mean distance in a-b space from the origin (higher is more color shift)
    - a Shift: the mean of the normalized a values (positive is more red, negative is more green)
    - b Shift: the mean of the normalized b values (positive is more yellow, negative is more blue)
    - Gloss: a combined metric based on the fraction of highlight pixels and their
    intensity, where highlight pixels are defined as those with normalized L values above the 95th percentile (higher is glossier)
    INPUTS:
    normalized_parts (list of tuples): a list where each element is a tuple containing the normalized
    L, a, b values for the corresponding part mask in part_masks
    OUTPUTS:
    blackness (list): a list of blackness values for each part
    color_shift (list): a list of color shift values for each part
    a_shift (list): a list of a shift values for each part
    b_shift (list): a list of b shift values for each part
    gloss (list): a list of gloss values for each part
    """
    blackness = []
    color_shift = []
    a_shift = []
    b_shift = []
    gloss = []

    for (L_norm, a_norm, b_norm) in normalized_parts:
        blackness.append(np.percentile(L_norm, 10))
        color_shift.append(np.sqrt(np.mean(a_norm**2 + b_norm**2)))
        a_shift.append(np.mean(a_norm))
        b_shift.append(np.mean(b_norm))
        high_L = np.percentile(L_norm, 95)
        highlight_mask = L_norm > high_L

        # Fraction of highlight pixels
        fraction = np.mean(highlight_mask)

        if np.any(highlight_mask):
            # Mean intensity of highlight pixels
            intensity = np.mean(L_norm[highlight_mask])
        else:
            intensity = 0

        # Combined gloss score (recommended)
        gloss_score = fraction * intensity

        gloss.append(gloss_score)


    return blackness, color_shift, a_shift, b_shift, gloss