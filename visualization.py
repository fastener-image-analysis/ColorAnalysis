import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops


def save_plot(fig, save_path):
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")


def show_threshold_visualization(substrate, gray, thresh, binary, save_path=None):
    fig, axes = plt.subplots(ncols=3, figsize=(10, 3))
    ax0, ax1, ax2 = axes

    ax0.imshow(substrate)
    ax0.set_title("Original")
    ax0.axis("off")

    ax1.hist(gray.ravel(), bins=256)
    ax1.axvline(thresh, color="r", linestyle="--")
    ax1.set_title("Histogram + Threshold")

    ax2.imshow(binary, cmap="gray")
    ax2.set_title("Binary Mask")
    ax2.axis("off")

    plt.tight_layout()
    save_plot(fig, save_path)
    plt.close(fig)


def show_part_masks_overlay(substrate, part_masks, save_path=None):
    fig = plt.figure(figsize=(6, 6))
    mask_combined = np.zeros(part_masks[0].shape, dtype=bool)
    for m in part_masks:
        mask_combined |= m

    plt.imshow(substrate)
    plt.imshow(mask_combined, cmap="jet", alpha=0.4)
    plt.title("Parts Overlay")
    plt.axis("off")

    save_plot(fig, save_path)
    plt.close(fig)


def show_background_and_holder(substrate, background_mask, holder_mask, save_path=None):
    fig = plt.figure(figsize=(6, 6))
    plt.imshow(substrate)
    plt.imshow(background_mask, cmap="Greens", alpha=0.4)
    plt.imshow(holder_mask, cmap="Reds", alpha=0.4)
    plt.title("Background (green) + Holder (red)")
    plt.axis("off")

    save_plot(fig, save_path)
    plt.close(fig)


def show_numbered_parts(substrate, part_masks, save_path=None):
    combined = np.zeros_like(part_masks[0], dtype=int)
    for i, pm in enumerate(part_masks):
        combined[pm] = i + 1

    regions = regionprops(combined)

    fig = plt.figure(figsize=(6, 6))
    plt.imshow(substrate)
    plt.axis("off")

    for i, region in enumerate(regions):
        y, x = region.centroid
        plt.text(
            x, y, f"{i+1}",
            color="yellow", fontsize=14, weight="bold",
            ha="center", va="center",
            bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )

    plt.title("Numbered Parts")
    save_plot(fig, save_path)
    plt.close(fig)


def save_numbered_parts_with_metrics(substrate, part_masks, blackness, filename):
    combined = np.zeros_like(part_masks[0], dtype=int)
    for i, pm in enumerate(part_masks):
        combined[pm] = i + 1

    regions = regionprops(combined)

    fig = plt.figure(figsize=(6, 6))
    plt.imshow(substrate)
    plt.axis("off")

    for i, region in enumerate(regions):
        y, x = region.centroid
        plt.text(
            x, y, f"{i+1}",
            color="yellow", fontsize=14, weight="bold",
            ha="center", va="center",
            bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )

    plt.title("Numbered Parts (saved)")
    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def show_combined_results(
    substrate,
    gray,
    thresh,
    binary,
    part_masks,
    background_mask,
    holder_mask,
    save_path=None
):
    combined = np.zeros_like(part_masks[0], dtype=int)
    for i, pm in enumerate(part_masks):
        combined[pm] = i + 1
    regions = regionprops(combined)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    ax0, ax1, ax2, ax3, ax4, ax5 = axes.ravel()

    ax0.imshow(substrate)
    ax0.set_title("Original")
    ax0.axis("off")

    ax1.hist(gray.ravel(), bins=256)
    ax1.axvline(thresh, color="r", linestyle="--")
    ax1.set_title("Histogram + Threshold")

    ax2.imshow(binary, cmap="gray")
    ax2.set_title("Binary Mask")
    ax2.axis("off")

    mask_combined = np.zeros(part_masks[0].shape, dtype=bool)
    for m in part_masks:
        mask_combined |= m
    ax3.imshow(substrate)
    ax3.imshow(mask_combined, cmap="jet", alpha=0.4)
    ax3.set_title("Parts Overlay")
    ax3.axis("off")

    ax4.imshow(substrate)
    ax4.imshow(background_mask, cmap="Greens", alpha=0.4)
    ax4.imshow(holder_mask, cmap="Reds", alpha=0.4)
    ax4.set_title("Background (green) + Exclusion (red)")
    ax4.axis("off")

    ax5.imshow(substrate)
    for i, region in enumerate(regions):
        y, x = region.centroid
        ax5.text(
            x, y, f"{i+1}",
            color="yellow", fontsize=14, weight="bold",
            ha="center", va="center",
            bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )
    ax5.set_title("Numbered Parts")
    ax5.axis("off")

    plt.tight_layout()

    save_plot(fig, save_path)

    # Show blocking so it stays open
    plt.show()