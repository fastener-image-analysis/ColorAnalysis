import os
import gc
import pandas as pd
from analysis_core import analyze_image_core_batch

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
