import io
import os
import numpy as np

from utils import load_image, build_results_table
from segmentation import (
    threshold_parts,
    extract_part_regions,
    sort_regions_l2r,
    regions_to_masks,
    compute_background
)
from color_processing import (
    convert_to_lab,
    lab_normalize_from_bg,
    linear_normalize_from_bg,
    get_lab_parts,
    compute_metrics
)
from visualization import show_results, save_numbered_parts_with_metrics

def analyze_image_core(image_input, output_dir=None, return_fig=True):
    img = load_image(image_input)

    gray, binary, thresh = threshold_parts(img)

    labels, regions = extract_part_regions(binary, min_area=3000)
    regions_sorted = sort_regions_l2r(regions)
    part_masks = regions_to_masks(labels, regions_sorted)
    
    bg_mask = compute_background(gray, part_masks)
    
    norm_img = linear_normalize_from_bg(img, bg_mask)
    
    L, a, b = convert_to_lab(norm_img)

    lab_norm_parts = lab_normalize_from_bg(L, a, b, bg_mask, part_masks)

    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(lab_norm_parts)

    df = build_results_table(blackness, color_shift, a_shift, b_shift, gloss)

    combined_save_path = None
    if output_dir is not None:
        combined_save_path = os.path.join(output_dir, 'Results.png')
    
    fig = show_results(
        img,
        gray,
        thresh,
        binary,
        part_masks,
        bg_mask,
        save_path=combined_save_path,
        return_fig=True
    )
    annotated_buf = io.BytesIO()
    save_numbered_parts_with_metrics(img, part_masks, blackness, annotated_buf)
    annotated_buf.seek(0)
    return df, fig, annotated_buf
                                                                      