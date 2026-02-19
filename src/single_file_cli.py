import os
from analysis_core import analyze_image_core

def main():
    path = input('Enter image path: ').strip()
    output_dir = input('Enter output directory path: ').strip()

    os.makedirs(output_dir, exist_ok=True)

    df, fig, annotated_buf = analyze_image_core(
        image_input=path,
        output_dir=output_dir,
        return_fig=True
    )

    csv_path = os.path.join(output_dir, 'metrics.csv')
    df.to_csv(csv_path, index=False)

    print('\nPer-Part Metrics:\n')
    print(df)
    fig.show()

if __name__ == '__main__':
    main()