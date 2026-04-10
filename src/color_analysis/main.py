import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
from color_analysis.analysis_core import analyze_images_in_directory, analyze_image_core_single

def main():
    print('Select mode:')
    print('1. Single File Analysis')
    print('2. Multi File Analysis')
    choice = input('Enter choice (1 or 2)').strip()

    if choice =='1':
        path = input('Enter image path: ').strip()
        output_dir = input('Enter output directory path: ').strip()

        os.makedirs(output_dir, exist_ok = True)

        df, fig, annotated_buf = analyze_image_core_single(
            image_input = path,
            output_dir = output_dir,
            return_fig = True
        )

        csv_path = os.path.join(output_dir, 'metrics.csv')
        df.to_csv(csv_path, index=False)
        print('\nPer-Part Metrics:\n')
        print(df)
        fig.show()
    
    elif choice == '2':
        path = input('Enter input directory: ').strip()
        output_dir = input('Enter output directory path: ').strip()

        os.makedirs(output_dir, exist_ok=True)

        analyze_images_in_directory(path, output_dir)
        print('Analysis complete. Results saved to output directory.')
    else:
        print('Invalid choice. Please enter 1 or 2.')

if __name__ == "__main__":
    main()
