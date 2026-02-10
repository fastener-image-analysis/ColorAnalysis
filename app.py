import os
from analysis_core import analyze_image_core


def main():
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