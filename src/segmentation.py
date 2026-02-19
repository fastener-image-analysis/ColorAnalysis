from skimage.color import rgb2gray
import numpy as np
from skimage.morphology import dilation, disk, remove_small_holes, binary_closing
from skimage.feature import canny
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes

def threshold_parts(image):
    """
    Takes in an image and creates binary image to seperate parts out from the background using a coarse thresholding method as well as edge detection
    INPUTS:
    image ():
    OUTPUTS:
    gray (): 
    binary ():
    coarse_thresh (int): The value [0, 1] that represents where the coarse thresh ended up
    """
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
    """
    Extracts regions for each part based on the binary mask and assigns them labels
    INPUTS:
    binary_mask (bool numpy Array): the binary mask used to seperate out the parts from the background
    min_area(int): the minimum area that should register as a part
    OUTPUTS:
    labels (list): the labels that represent each part
    part_regions (): The regions that each part lies in
    """
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
    """
    Sorts each part region from left to right, with left being 1, and ascending to the right by their centroids
    INPUTS:
    regions (): the region that each part lies in
    OUTPUTS
    sorted_regions (): regions sorted by left to right
    """
    sorted_regions = sorted(regions, key=lambda r: r.centroid[1])
    return sorted_regions

def regions_to_masks(labels, regions_sorted):
    """
    Finalizes masking of the regions
    """
    return [(labels == r.label) for r in regions_sorted]

def compute_background(gray, part_masks):
    """
    Determines masking of the background in order to be later normalized against
    INPUTS:
    gray (numpy Array): the grayscale version of the image represented by a numpy array
    part_masks (list): A list arrays that each represent the mask of the parts
    OUTPUTS:
    bg_mask (array): an array representing the mask of the background
    """
    parts_mask = np.zeros_like(gray, dtype=bool)
    for pm in part_masks:
        parts_mask |= pm
    
    gray_no_parts = gray.copy()
    gray_no_parts[parts_mask] = np.nan

    bg_thresh = np.nanpercentile(gray_no_parts, 70)
    print(f'bg thresh: {bg_thresh}')
    bg_mask = gray_no_parts > bg_thresh

    return bg_mask
