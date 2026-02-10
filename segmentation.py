import numpy as np
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation, disk, remove_small_holes, binary_closing
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes


def threshold_parts(substrate):
    """
    Thresholds the input image to create a binary mask of the parts. Utilizes a combination
    of intensity thresholding, edge detection, and morphological operations.

    INPUTS:
    substrate (numpy array): the input image as a numpy array

    OUTPUTS:
    gray (numpy array): the grayscale version of the input image
    binary (numpy array): the binary mask of the parts
    coarse_thresh (float): the intensity threshold used for the coarse thresholding step
    """

    gray = rgb2gray(substrate)

    # Coarse threshold to find rough bolt locations
    coarse_thresh = np.percentile(gray, 60)
    coarse_mask = gray < coarse_thresh

    # Dilate to ensure full bolt coverage
    coarse_mask = dilation(coarse_mask, disk(6))

    # Edge detection inside region of interest
    edges = canny(gray, sigma=2)
    edges = edges & coarse_mask

    # Close gaps
    edges_dilated = dilation(edges, disk(2))
    closed = binary_closing(edges_dilated, disk(4))

    # Fill bolt interiors (inside ROI only)
    filled = binary_fill_holes(closed & coarse_mask)

    # Remove tiny junk
    filled = remove_small_holes(filled, area_threshold=3000)

    binary = filled

    return gray, binary, coarse_thresh


def extract_part_regions(binary_mask, min_area=5000):
    """
    Extracts connected regions from the binary mask and filters them based on size and position.

    INPUTS:
    binary_mask (numpy array): the binary mask of the parts
    min_area (int): the minimum area threshold for a region to be considered a part

    OUTPUTS:
    labels (numpy array): the labeled image where each connected region has a unique integer label
    bolt_regions (list of skimage.measure._regionprops.RegionProperties): a list of region properties for the detected parts that meet the criteria
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
    """
    Sorts the given list of region properties from left to right based on their centroids.
    INPUTS:
    regions (list of skimage.measure._regionprops.RegionProperties): a list of region properties to sort

    OUTPUTS:
    sorted_regions (list of skimage.measure._regionprops.RegionProperties): the input regions sorted from left to right
    """
    return sorted(regions, key=lambda r: r.centroid[1])


def regions_to_masks(labels, regions_sorted):
    """
    Converts a list of sorted region properties into binary masks for each region.
    INPUTS:
    labels (numpy array): the labeled image where each connected region has a unique integer label
    regions_sorted (list of skimage.measure._regionprops.RegionProperties): a list of region properties sorted from left to right

    OUTPUTS:
    part_masks (list of numpy arrays): a list of binary masks corresponding to each region in
    regions_sorted, where each mask has the same shape as the input labels and contains True for pixels belonging to that region and False elsewhere
    """
    return [(labels == r.label) for r in regions_sorted]