import numpy as np
from skimage.color import rgb2lab
from utils import linear_to_srgb, srgb_to_linear

def linear_normalize_from_bg(image, bg_mask):
    image = srgb_to_linear(image)
    bg_pixels = image[bg_mask]
    bg_mean = bg_pixels.mean(axis=0)
    correction = 1.0 / bg_mean
    image_normalized = np.clip(image * correction[None, None, :], 0, 1)
    image_normalized = linear_to_srgb(image_normalized)
    return(image_normalized)

def normalize_from_gray_card(image, card_mask):
    image = srgb_to_linear(image)
    card_pixels = image[card_mask]
    card_mean = card_pixels.mean(axis=0)
    print(f'current card mean is: {card_mean}')
    correction = 0.215 / card_mean
    image_normalized = np.clip(image * correction[None, None,:], 0, 1)
    image_normalized = linear_to_srgb(image_normalized)
    return(image_normalized)

import numpy as np

def convert_to_lab(image):
    lab = rgb2lab(image)
    return lab[..., 0], lab[..., 1], lab[..., 2]

def get_lab_parts(L, a, b, part_masks):
    part_lab = []
    for pm in part_masks:
        part_lab.append((L[pm], a[pm], b[pm]))

def lab_normalize_from_bg(L, a, b, bg_mask, part_masks):
    L_ref = np.median(L[bg_mask])
    a_ref = np.median(a[bg_mask])
    b_ref = np.median(b[bg_mask])

    normalized = []
    for pm in part_masks:
        normalized.append((L[pm] - L_ref, a[pm] - a_ref, b[pm] - b_ref))
    return normalized

def compute_metrics(normalized_parts):
    blackness = []
    color_shift = []
    a_shift = []
    b_shift = []
    gloss = []

    for (L, a, b) in normalized_parts:
        high_L = np.percentile(L, 95)
        diffuse_mask = L < high_L
        Ld = L[diffuse_mask]
        ad = a[diffuse_mask]
        bd = b[diffuse_mask]
        blackness.append(np.percentile(Ld, 10))
        color_shift.append(np.sqrt(np.mean(ad**2 + bd**2)))
        a_shift.append(np.median(ad))
        b_shift.append(np.median(bd))
        highlight_mask = L > high_L
        fraction = np.mean(highlight_mask)

        if np.any(highlight_mask):
            intensity = np.mean(L[highlight_mask])
        else:
            intensity = 0
        gloss_score = fraction * intensity
        gloss.append(gloss_score)
    return blackness, color_shift, a_shift, b_shift, gloss
