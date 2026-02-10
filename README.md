# Black Color Image Analysis
This purpose of this program is to analyze various images of fasteners such as bolts and nuts, and then provide a value that represents its color. The color black is the primary focus in this program, and it is meant to be normalized against a consistent background for relative analysis.

Future additions will include corrosion analysis through color analysis of red and white corrosion compared to the rest of the part.

## How it works currently
It is currently an ipynb file that takes in an image called 'substrate_image.jpg' and masks out all the individual parts that are in the image based on the contrast difference. It then normalizes it against the background in the L a b color space, calculating the difference in the L value to present a value for blackness. Larger magnitudes of 'blackness' indicate a more black part. To be added are color shift representations and glossiness

## Running program in command line
Make sure you have python installed on your device, and you have all the required packages.
You can view the required packages in the `requirements.txt` file, and you can install them through a bash script by running `bash install.sh`

In order to run image analysis on a certain image, you will want to navigate to the ColorAnalysis directory, and then run `python app.py`

This will then lead you to input the file path of the image you want to analyze. The base folder that it is in currently is the ColorAnalysis directory.

Next it will tell you to input the directory path of where you want all images and csv files of the image analysis to be stored.

What this will output is a table of the Blackness, Color Shift, Glossiness, median a* and b* values, and plots representing the masking and regions for the parts. You can end the program by closing out of the plots.

To run all this through Stremlit UI, run 'streamlit run streamlit_app.py'
