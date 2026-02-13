from skimage.color import rgb2gray
import numpy as np
from skimage.morphology import dilation, disk, remove_small_holes, binary_closing
from skimage.feature import canny
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes

def threshold_parts(image):
    gray = rgb2gray(image)
    coarse_thresh = np.percentile(gray, 60)
    coarse_mask = gray < coarse_thresh
    coarse_mask = dilation(coarse_mask, disk(6)) # what does dilation do?
    edges = canny(gray, sigma=2) # what does sigma do?
    edges = edges & coarse_mask

    edges_dilated = dilation(edges, disk(2))
    closed = binary_closing(edges_dilated, disk(4))

    filled = binary_fill_holes(closed & coarse_mask)
    filled = remove_small_holes(filled, area_threshold=3000)

    binary = filled
    return gray, binary, coarse_thresh

def extract_part_regions(binary_mask, min_area=5000):
    labels = label(binary_mask) # determine what a label actually does
    regions = regionprops(labels)
    part_regions = []
    for r in regions:
        minr, minc, maxr, maxc = r.bbox # what does bbox do

        if maxr >= binary_mask.shape[0] - 5:
            continue

        if r.area >= min_area:
            part_regions.append(r)
    return labels, part_regions

def sort_regions_l2r(regions):
    sorted_regions = sorted(regions, key=lambda r: r.centroid[1])
    return sorted_regions

def regions_to_masks(labels, regions_sorted):
    return [(labels == r.label) for r in regions_sorted]

def compute_background(gray, part_masks):
    parts_mask = np.zeros_like(gray, dtype=bool)
    for pm in part_masks:
        parts_mask |= pm
    
    gray_no_parts = gray.copy()
    gray_no_parts[parts_mask] = np.nan

    bg_thresh = np.nanpercentile(gray_no_parts, 70)
    print(f'bg thresh: {bg_thresh}')
    bg_mask = gray_no_parts > bg_thresh

    return bg_mask
