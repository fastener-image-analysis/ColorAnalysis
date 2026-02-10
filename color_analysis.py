import numpy as np
from skimage.color import rgb2lab


def convert_to_lab(substrate):
    lab = rgb2lab(substrate)
    return lab[..., 0], lab[..., 1], lab[..., 2]


def normalize_parts(L, a, b, background_mask, part_masks):
    L_ref = np.median(L[background_mask])
    a_ref = np.median(a[background_mask])
    b_ref = np.median(b[background_mask])

    normalized = []
    for m in part_masks:
        normalized.append((L[m] - L_ref, a[m] - a_ref, b[m] - b_ref))
    return normalized


def compute_metrics(normalized_parts):
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