import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops

def save_plot(fig, save_path):
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

def show_results(
        image,
        gray,
        thresh,
        binary,
        part_masks,
        bg_mask,
        save_path=None,
        return_fig=False
):
    combined = np.zeros_like(part_masks[0], dtype=int)
    for i, pm in enumerate(part_masks):
        combined[pm] = i + 1
    regions = regionprops(combined)
    del combined  # prevent regionprops memory retention

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    ax0, ax1, ax2, ax3, ax4, ax5 = axes.ravel()

    ax0.imshow(image)
    ax0.set_title("Original")
    ax0.axis('off')

    ax1.hist(gray.ravel(), bins=256)
    ax1.set_title('Histogram')

    ax2.imshow(binary, cmap='gray')
    ax2.set_title('Binary Part Mask')
    ax2.axis('off')  # FIXED

    mask_combined = np.zeros(part_masks[0].shape, dtype=bool)
    for pm in part_masks:
        mask_combined |= pm
    ax3.imshow(image)
    ax3.imshow(mask_combined, cmap='jet', alpha=0.4)
    ax3.set_title('Parts Overlay')
    ax3.axis('off')
    del mask_combined

    ax4.imshow(image)
    ax4.imshow(bg_mask, cmap='Greens', alpha=0.4)
    ax4.set_title('Background (green)')
    ax4.axis('off')

    ax5.imshow(image)
    for i, region in enumerate(regions):
        y, x = region.centroid
        ax5.text(
            x, y, f'{i+1}',
            color='yellow', fontsize=14, weight='bold',
            ha='center', va='center',
            bbox=dict(facecolor='black', alpha=0.5, pad=2)
        )
    ax5.set_title('Numbered Parts')
    ax5.axis('off')

    plt.tight_layout()

    if return_fig:
        return fig

    plt.close(fig)

def save_numbered_parts_with_metrics(substrate, part_masks, blackness, file_or_buffer):
    combined = np.zeros_like(part_masks[0], dtype=int)
    for i, pm in enumerate(part_masks):
        combined[pm] = i + 1

    regions = regionprops(combined)
    del combined  # prevent memory retention

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(substrate)
    ax.axis("off")

    for i, region in enumerate(regions):
        y, x = region.centroid
        ax.text(
            x, y, f"{i+1}",
            color="yellow", fontsize=14, weight="bold",
            ha="center", va="center",
            bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )

    ax.set_title("Numbered Parts (saved)")

    if isinstance(file_or_buffer, str):
        fig.savefig(file_or_buffer, dpi=300, bbox_inches="tight")
    else:
        fig.savefig(file_or_buffer, format="jpg", dpi=300, bbox_inches="tight")

    plt.close(fig)