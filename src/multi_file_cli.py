import os
from analysis_core import analyze_image_core
from multi_file import analyze_images_in_directory

def main():
    path = input('Enter input directory: ').strip()
    output_dir = input('Enter output directory path: ').strip()

    os.makedirs(output_dir, exist_ok=True)

    analyze_images_in_directory(path, output_dir)
    print('Analysis complete. Results saved to output directory.')

if __name__ == '__main__':
    main()