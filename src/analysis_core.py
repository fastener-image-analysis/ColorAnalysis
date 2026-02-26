import io
import os
import numpy as np
import gc
import pandas as pd

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
    linear_normalize_from_bg,
    get_lab_parts,
    compute_metrics
)
from visualization import show_results, save_numbered_parts_with_metrics

def analyze_image_core_single(image_input, output_dir=None, return_fig=True):
    """
    Core analysis code to take an image input and output the processing timeline as well as
    response variables for the color of parts within the image. To be used by any access method.
    INPUTS:
    image_input (str): file path of the image to be analyzed
    output_dir (str): directory path to where files will be stored if desired
    return_fig (bool): to return a annotated image or not.

    OUTPUTS:
    df (pandas DataFrame): a dataframe of all the response variables
    fig (plt Plot): a plot showing relevant graphs of the image analysis timeline
    annotated_buf: a buffer in order for streamlit to download an image.
    """
    img = load_image(image_input)

    gray, binary, thresh = threshold_parts(img)

    labels, regions = extract_part_regions(binary, min_area=3000)
    regions_sorted = sort_regions_l2r(regions)
    part_masks = regions_to_masks(labels, regions_sorted)
    
    bg_mask = compute_background(gray, part_masks)
    
    norm_img = linear_normalize_from_bg(img, bg_mask)
    
    L, a, b = convert_to_lab(norm_img)

    lab_parts = get_lab_parts(L, a, b, part_masks)

    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(lab_parts)

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

    to_delete = [
        'img', 'gray', 'binary', 'thresh',
        'labels', 'regions', 'regions_sorted',
        'part_masks', 'bg_mask', 'norm_img',
        'L', 'a', 'b', 'lab_parts',
        'blackness', 'color_shift', 'a_shift', 'b_shift', 'gloss'
    ]

    for var in to_delete:
        if var in locals():
            del locals()[var]

    gc.collect()

    return df, fig, annotated_buf

def analyze_image_core_batch(image_input):
    """
    Batch-only core: no figures, no buffers, just metrics.
    """
    img = load_image(image_input)

    gray, binary, thresh = threshold_parts(img)
    labels, regions = extract_part_regions(binary, min_area=3000)
    regions_sorted = sort_regions_l2r(regions)
    part_masks = regions_to_masks(labels, regions_sorted)
    bg_mask = compute_background(gray, part_masks)
    norm_img = linear_normalize_from_bg(img, bg_mask)
    L, a, b = convert_to_lab(img)
    lab_parts = get_lab_parts(L, a, b, part_masks)
    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(lab_parts)
    df = build_results_table(blackness, color_shift, a_shift, b_shift, gloss)

    del img, gray, binary, thresh
    del labels, regions, regions_sorted, part_masks, bg_mask
    del L, a, b, lab_parts
    del norm_img
    del blackness, color_shift, a_shift, b_shift, gloss
    gc.collect()

    return df

def analyze_images_in_directory(image_directory, output_directory):
    """
    Batch runner: no figures, streams metrics to a single CSV.
    """
    os.makedirs(output_directory, exist_ok=True)
    combined_path = os.path.join(output_directory, "combined_metrics.csv")
    first_write = True

    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            print("Processing:", filename)
            image_path = os.path.join(image_directory, filename)

            df = analyze_image_core_batch(image_path)

            base = os.path.splitext(filename)[0]
            df["group"] = base

            # append to combined CSV incrementally
            df.to_csv(
                combined_path,
                mode="a",
                header=first_write,
                index=False
            )
            first_write = False

            # optional: also save per-image metrics
            df.to_csv(
                os.path.join(output_directory, f"{base}_metrics.csv"),
                index=False
            )

            del df
            gc.collect()



                                                                      