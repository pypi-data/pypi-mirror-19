from skan import draw
from skimage import io, morphology, filters, color
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('/Users/jni/projects/elegant-scipy/style/elegant.mplstyle')

im = io.imread('urbc-0.tif')
lum = color.rgb2gray(im)
glum = filters.gaussian(lum, sigma=2)

def threshold_function(image, **kwargs):
    footprint = morphology.disk(radius=kwargs.get('radius', 15))
    filtered = filters.median(image, footprint) - kwargs.get('offset', 0)
    return morphology.closing(image * 255 > filtered, np.ones((5, 5)))

binrbc = threshold_function(glum)
skeleton = morphology.skeletonize(binrbc)

draw.overlay_euclidean_skeleton_2d(lum, skeleton, image_cmap='gray',
                                   skeleton_color_source='branch-distance')

plt.show()