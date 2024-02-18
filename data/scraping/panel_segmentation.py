from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.morphology import dilation
from scipy import ndimage as ndi
from skimage.measure import label
import numpy as np
from skimage.measure import regionprops
import cv2

def do_bboxes_overlap(a, b):
    return (
        a[0] < b[2] and
        a[2] > b[0] and
        a[1] < b[3] and
        a[3] > b[1]
    )

def merge_bboxes(a, b):
    return (
        min(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        max(a[3], b[3])
    )


def segment_panel(img: Image):
    grayscale = rgb2gray(img)

    # edge detector
    edges = canny(grayscale)

    # thicken edges
    thick_edges = dilation(dilation(edges))

    # fill in areas between edges
    segmentation = ndi.binary_fill_holes(thick_edges)


    labels = label(segmentation)
    regions = regionprops(labels)
    panels = []

    # combining panels that were split up
    for region in regions:

        for i, panel in enumerate(panels):
            if do_bboxes_overlap(region.bbox, panel):
                panels[i] = merge_bboxes(panel, region.bbox)
                break
        else:
            panels.append(region.bbox)

    # a list of bboxs
    return panels
