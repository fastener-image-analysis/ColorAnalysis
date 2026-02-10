import numpy as np
from skimage.morphology import closing, disk, remove_small_holes
from skimage.measure import label, regionprops


def compute_background_and_holder_masks(gray, part_masks, holder_min_hole_area=5000):
    parts_mask = np.zeros_like(gray, dtype=bool)
    for m in part_masks:
        parts_mask |= m

    gray_no_parts = gray.copy()
    gray_no_parts[parts_mask] = np.nan

    bg_thresh = np.nanpercentile(gray_no_parts, 40)
    background_mask_initial = gray_no_parts > bg_thresh

    non_background = ~background_mask_initial
    non_background[np.isnan(gray_no_parts)] = False

    labels = label(non_background)
    regions = regionprops(labels)

    if not regions:
        return ~parts_mask, np.zeros_like(gray, dtype=bool)

    regions_sorted = sorted(regions, key=lambda r: r.area, reverse=True)
    holder_label = regions_sorted[0].label
    holder_mask = (labels == holder_label)

    holder_mask = closing(holder_mask, disk(10))
    holder_mask = remove_small_holes(holder_mask, holder_min_hole_area)

    background_mask = ~(parts_mask | holder_mask)
    return background_mask, holder_mask