import io
import os

from utils import load_image
from segmentation import (
    threshold_parts,
    extract_part_regions,
    sort_regions_left_to_right,
    regions_to_masks,
)
from background import compute_background_and_holder_masks
from color_analysis import convert_to_lab, normalize_parts, compute_metrics, get_normalized_lab_diff
from table_builder import build_results_table
from visualization import (
    show_threshold_visualization,
    show_part_masks_overlay,
    show_background_and_holder,
    show_numbered_parts,
    save_numbered_parts_with_metrics,
    show_combined_results,
)


def analyze_image_core(image_input, output_dir=None, return_fig=True):
    """
    Core function to analyze the input image and produce the results table, combined figure, and annotated image buffer.
    INPUTS:
    image_input (str or numpy array): the input image, either as a file path or a numpy array
    output_dir (str, optional): the directory where the combined figure will be saved. If None, the combined figure will not be saved. Default is None.
    return_fig (bool, optional): whether to return the combined figure object. Default is True.
    OUTPUTS:
    df (pandas DataFrame): a DataFrame containing the computed metrics for each part
    fig (matplotlib Figure, optional): the combined figure showing the original image, thresholding results, part masks, background/holder masks, and numbered parts. Only returned if return_fig is True.
    annotated_buf (BytesIO): a BytesIO buffer containing the annotated image with numbered parts, which can be saved or displayed as needed
    """
    # Load image
    substrate = load_image(image_input)

    # Segmentation
    gray, binary, thresh = threshold_parts(substrate)

    # Extract bolt regions
    labels, regions = extract_part_regions(binary, min_area=3000)
    regions_sorted = sort_regions_left_to_right(regions)
    part_masks = regions_to_masks(labels, regions_sorted)

    # Background + holder
    background_mask, holder_mask = compute_background_and_holder_masks(
        gray,
        part_masks
    )

    # Lab conversion + normalization
    # L, a, b = convert_to_lab(substrate)
    L, a, b = get_normalized_lab_diff(substrate, background_mask)
    normalized = normalize_parts(L, a, b, background_mask, part_masks)

    # Metrics
    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(normalized)

    # Table
    df = build_results_table(blackness, color_shift, gloss, a_shift, b_shift)

    # Combined figure
    combined_save_path = None
    if output_dir is not None:
        combined_save_path = os.path.join(output_dir, "combined.png")

    fig = show_combined_results(
        substrate,
        gray,
        thresh,
        binary,
        part_masks,
        background_mask,
        holder_mask,
        save_path=combined_save_path,
        return_fig=True
    )

    # Annotated image buffer. Purpose is to allow Streamlit to display the annotated image without needing to save it to disk first.
    annotated_buf = io.BytesIO()
    save_numbered_parts_with_metrics(substrate, part_masks, blackness, annotated_buf)
    annotated_buf.seek(0)

    return df, fig, annotated_buf