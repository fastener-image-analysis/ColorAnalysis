# Black Color Image Analysis
This purpose of this program is to analyze various images of fasteners such as bolts and nuts, and then provide a value that represents its color. The color black is the primary focus in this program, and it is meant to be normalized against a consistent background for relative analysis.

Future additions will include corrosion analysis through color analysis of red and white corrosion compared to the rest of the part.

## How it works currently
It is currently an ipynb file that takes in an image called 'substrate_image.jpg' and masks out all the individual parts that are in the image based on the contrast difference. It then normalizes it against the background in the L a b color space, calculating the difference in the L value to present a value for blackness. Larger magnitudes of 'blackness' indicate a more black part. To be added are color shift representations and glossiness
