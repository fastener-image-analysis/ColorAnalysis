import numpy as np
from skimage.measure import label, regionprops


def compute_background_and_holder_masks(gray, part_masks):
    """
    Background = bright pixels not part of any bolt
    Holder = largest dark region not part of any bolt
    """

    # 1. Combine part masks
    parts_mask = np.zeros_like(gray, dtype=bool)
    for pm in part_masks:
        parts_mask |= pm

    # 2. Remove parts from consideration
    gray_no_parts = gray.copy()
    gray_no_parts[parts_mask] = np.nan

    # 3. Background = bright pixels
    bg_thresh = np.nanpercentile(gray_no_parts, 70)
    background_mask = gray_no_parts > bg_thresh

    # 4. Holder = largest dark region
    dark_mask = (gray_no_parts < bg_thresh) & (~np.isnan(gray_no_parts))

    labels = label(dark_mask)
    regions = regionprops(labels)

    if not regions:
        return background_mask, np.zeros_like(gray, dtype=bool)

    # Largest dark region = holder
    holder_label = max(regions, key=lambda r: r.area).label
    holder_mask = (labels == holder_label)

    return background_mask, holder_mask