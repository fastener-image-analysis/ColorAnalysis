import numpy as np
from skimage.measure import label, regionprops


def compute_background_and_holder_masks(gray, part_masks):
    """
    Compute background and holder masks based on the grayscale image and part masks.
    The background is defined as the bright regions that are not part of the detected parts.
    The holder is defined as the largest dark region that is not part of the detected parts.
    INPUTS:
    gray (numpy array): the grayscale image of the substrate
    part_masks (list of numpy arrays): a list of binary masks corresponding to the detected parts
    OUTPUTS:
    background_mask (numpy array): a binary mask where True indicates background pixels
    holder_mask (numpy array): a binary mask where True indicates holder pixels
    """

    # Combine part masks
    parts_mask = np.zeros_like(gray, dtype=bool)
    for pm in part_masks:
        parts_mask |= pm

    # Remove parts from consideration
    gray_no_parts = gray.copy()
    gray_no_parts[parts_mask] = np.nan

    # Background = bright pixels, using 70th percentile to exclude outliers
    bg_thresh = np.nanpercentile(gray_no_parts, 70)
    background_mask = gray_no_parts > bg_thresh

    # Holder = largest dark region, using 30th percentile to exclude outliers
    dark_mask = (gray_no_parts < bg_thresh) & (~np.isnan(gray_no_parts))

    # Label connected dark regions
    labels = label(dark_mask)
    regions = regionprops(labels)

    if not regions:
        return background_mask, np.zeros_like(gray, dtype=bool)

    # Largest dark region = holder
    holder_label = max(regions, key=lambda r: r.area).label
    holder_mask = (labels == holder_label)

    return background_mask, holder_mask