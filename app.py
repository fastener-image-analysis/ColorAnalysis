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


def analyze_single_image(filename, output_dir=".", min_area=5000):
    """
    Runs the full analysis pipeline on a single image.
    Saves all individual plots, the combined figure, the annotated image, and the CSV.
    Shows only the combined figure at the end.
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Base name for saving files
    basename = os.path.splitext(os.path.basename(filename))[0]

    # 1. Load image
    substrate = load_image(filename)

    # 2. Threshold parts
    gray, binary, thresh = threshold_parts(substrate)

    # 3. Extract and sort regions
    labels, regions = extract_part_regions(binary, min_area=min_area)
    regions_sorted = sort_regions_left_to_right(regions)
    part_masks = regions_to_masks(labels, regions_sorted)

    # 4. Background + holder
    background_mask, holder_mask = compute_background_and_holder_masks(gray, part_masks)

    # 5. Lab + normalization
    L, a, b = convert_to_lab(substrate)
    normalized = normalize_parts(L, a, b, background_mask, part_masks)

    # 6. Metrics
    blackness, color_shift, a_shift, b_shift, gloss = compute_metrics(normalized)

    # 7. Table
    df = build_results_table(blackness, color_shift, gloss, a_shift, b_shift)

    # 8. Save individual plots (no showing)
    show_threshold_visualization(
        substrate, gray, thresh, binary,
        save_path=os.path.join(output_dir, f"{basename}_threshold.png")
    )
    show_part_masks_overlay(
        substrate, part_masks,
        save_path=os.path.join(output_dir, f"{basename}_parts_overlay.png")
    )
    show_background_and_holder(
        substrate, background_mask, holder_mask,
        save_path=os.path.join(output_dir, f"{basename}_background_holder.png")
    )
    show_numbered_parts(
        substrate, part_masks,
        save_path=os.path.join(output_dir, f"{basename}_numbered.png")
    )

    # 9. Save annotated image
    save_numbered_parts_with_metrics(
        substrate, part_masks, blackness,
        filename=os.path.join(output_dir, f"{basename}_annotated.jpg")
    )

    # 10. Save CSV
    df.to_csv(os.path.join(output_dir, f"{basename}_metrics.csv"), index=False)

    # 11. Print table BEFORE showing combined figure
    print("\nPer-part metrics:\n")
    print(df)

    # 12. Show combined window at the end (blocking)
    show_combined_results(
        substrate,
        gray,
        thresh,
        binary,
        part_masks,
        background_mask,
        holder_mask,
        save_path=os.path.join(output_dir, f"{basename}_combined.png")
    )

    return df


def main():
    """
    CLI entry point.
    Asks for a single image file and an output directory.
    """

    path = input("Enter image filename: ").strip()
    output_dir = input("Enter output directory: ").strip()

    df = analyze_single_image(path, output_dir=output_dir)

    # Data already printed inside analyze_single_image()


if __name__ == "__main__":
    main()