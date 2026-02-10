import numpy as np
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation, disk, remove_small_holes, binary_closing
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes


def threshold_parts(substrate):
    """
    Robust bolt segmentation using:
    1. Coarse grayscale threshold to find bolt region (NOT holder)
    2. Edge detection restricted to that region
    3. Controlled filling of bolt interiors
    """

    gray = rgb2gray(substrate)

    # 1. Coarse ROI: bolts are darker than background, holder is darker but excluded later
    coarse_thresh = np.percentile(gray, 60)
    coarse_mask = gray < coarse_thresh

    # Dilate to ensure full bolt coverage
    coarse_mask = dilation(coarse_mask, disk(6))

    # 2. Edge detection inside ROI
    edges = canny(gray, sigma=2)
    edges = edges & coarse_mask

    # 3. Close gaps
    edges_dilated = dilation(edges, disk(2))
    closed = binary_closing(edges_dilated, disk(4))

    # 4. Fill bolt interiors (inside ROI only)
    filled = binary_fill_holes(closed & coarse_mask)

    # 5. Remove tiny junk
    filled = remove_small_holes(filled, area_threshold=3000)

    binary = filled

    return gray, binary, None


def extract_part_regions(binary_mask, min_area=5000):
    """
    Extract bolt regions ONLY.
    Holder is removed by discarding the region touching the bottom edge.
    """

    labels = label(binary_mask)
    regions = regionprops(labels)

    bolt_regions = []
    for r in regions:
        minr, minc, maxr, maxc = r.bbox

        # Holder touches bottom of image → exclude it
        if maxr >= binary_mask.shape[0] - 5:
            continue

        if r.area >= min_area:
            bolt_regions.append(r)

    return labels, bolt_regions


def sort_regions_left_to_right(regions):
    return sorted(regions, key=lambda r: r.centroid[1])


def regions_to_masks(labels, regions_sorted):
    return [(labels == r.label) for r in regions_sorted]