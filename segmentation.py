import numpy as np
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_holes
from skimage.measure import label, regionprops


def threshold_parts(substrate):
    gray = rgb2gray(substrate)
    thresh = threshold_otsu(gray)
    binary = gray < thresh
    return gray, binary, thresh


def extract_part_regions(binary_mask, min_area=5000):
    mask = remove_small_holes(binary_mask, area_threshold=min_area)
    labels = label(mask)
    regions = regionprops(labels)
    valid = [r for r in regions if r.area >= min_area]
    return labels, valid


def sort_regions_left_to_right(regions):
    return sorted(regions, key=lambda r: r.centroid[1])


def regions_to_masks(labels, regions_sorted):
    return [(labels == r.label) for r in regions_sorted]