# import important libraries
import skimage as ski
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from skimage.morphology import remove_small_objects, remove_small_holes, closing, disk
from skimage.measure import label, regionprops
from skimage.filters import threshold_yen
from skimage.color import rgb2lab
