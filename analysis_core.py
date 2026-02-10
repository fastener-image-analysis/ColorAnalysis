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
from color_analysis import convert_to_lab, normalize_parts, compute_metrics
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

    # 1. Load image
    substrate = load_image(image_input)

    # 2. Segmentation
    gray, binary, thresh = threshold_parts(substrate)

    # 3. Extract bolt regions
    labels, regions = extract_part_regions(binary, min_area=3000)
    regions_sorted = sort_regions_left_to_right(regions)
    part_masks = regions_to_masks(labels, regions_sorted)

    # 4. Background + holder
    background_mask, holder_mask = compute_background_and_holder_masks(
        gray,
        part_masks
    )

    # 5. Lab conversion + normalization
    L, a, b = convert_to_lab(substrate)
    normalized = normalize_parts(L, a, b, background_mask, part_masks)

    # 6. Metrics
    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(normalized)

    # 7. Table
    df = build_results_table(blackness, color_shift, gloss, a_shift, b_shift)

    # 8. Combined figure
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

    # 9. Annotated image buffer
    annotated_buf = io.BytesIO()
    save_numbered_parts_with_metrics(substrate, part_masks, blackness, annotated_buf)
    annotated_buf.seek(0)

    return df, fig, annotated_buf