import os
from analysis_core import analyze_image_core


def main():
    """
    Main function to run the image analysis pipeline through the command line. It prompts the user for an image filename and an output directory, then runs the analysis and saves the results.
    The results include a CSV file with the computed metrics for each part, and a combined figure showing the original image, thresholding results, part masks, 
    background/holder masks, and numbered parts. 
    The combined figure is saved to the specified output directory, and the annotated image with numbered parts is saved as a BytesIO buffer for potential use in Streamlit or other applications.
    INPUTS:
    None (the function prompts the user for inputs)
    OUTPUTS:
    df (pandas DataFrame): a DataFrame containing the computed metrics for each part,
    fig (matplotlib Figure): the combined figure showing the original image, thresholding results, part masks, background/holder masks, and numbered parts,
    annotated_buf (BytesIO): a BytesIO buffer containing the annotated image with numbered parts, which can be saved or displayed as needed
    """
    path = input("Enter image filename: ").strip()
    output_dir = input("Enter output directory: ").strip()

    os.makedirs(output_dir, exist_ok=True)

    df, fig, annotated_buf = analyze_image_core(
        image_input=path,
        output_dir=output_dir,
        return_fig=True  # we want the figure object to show it
    )

    # Save CSV
    csv_path = os.path.join(output_dir, "metrics.csv")
    df.to_csv(csv_path, index=False)

    print("\nPer-part metrics:\n")
    print(df)

    # Show combined figure (blocking)
    fig.show()


if __name__ == "__main__":
    main()