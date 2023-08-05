import numpy as np

from pyezzi.laplace import solve_3D as laplace_solver
from pyezzi.yezzi import iterative_relaxation_3D as yezzi_solver


def compute_thickness(labeled_image,
                      label_inside=1,
                      label_wall=2,
                      laplace_tolerance=0.05,
                      laplace_max_iter=500,
                      yezzi_tolerance=0.05,
                      yezzi_max_iter=500,
                      crop=True,
                      debug=False):
    """
    Returns wall thicknesses

    Input image must be labeled as specified

    :param labeled_image:np.ndarray of ints
    :param label_inside:int The label of the object's interior
    :param label_wall:int The label of the object's wall
    :param laplace_tolerance:float Maximum error allowed for Laplacian resolution
    :param laplace_max_iter:int Maximum iterations allowed for Laplacian resolution
    :param yezzi_tolerance:float Maximum error allowed for thickness computation
    :param yezzi_max_iter:int Maximum iterations allowed for thickness computation
    ;param crop:bool Crop image before computations
    :param debug:bool Print debug messages
    :return:np.ndarray of floats
    """

    if crop:
        cropped_image, limits = crop_img(labeled_image)
    else:
        cropped_image = labeled_image

    wall = cropped_image == label_wall
    endo = cropped_image == label_inside
    epi = wall | endo

    init = np.zeros_like(cropped_image, float)
    init[np.logical_not(epi)] = 1
    laplace_grid, _, __ = laplace_solver(wall, init,
                                         tolerance=laplace_tolerance,
                                         max_iterations=laplace_max_iter)
    if debug:
        print("Laplacian: {} iterations, max_error = {}".format(_, __))

    L0, L1, _, __ = yezzi_solver(wall, laplace_grid,
                                 tolerance=yezzi_tolerance,
                                 max_iterations=yezzi_max_iter)

    if debug:
        print("PDE: {} iterations, max_error = {}".format(_, __))

    cropped_thickness = L0 + L1

    if crop:
        thickness = np.pad(cropped_thickness,
                           ((limits[0], labeled_image.shape[0] - limits[1]),
                            (limits[2], labeled_image.shape[1] - limits[3]),
                            (limits[4], labeled_image.shape[2] - limits[5])),
                           mode="constant")
    else:
        thickness = cropped_thickness

    return thickness


def crop_img(nda_image, margins=1):
    min_slice, max_slice = np.argwhere(nda_image.sum(axis=(1, 2)))[[0, -1]]
    min_row, max_row = np.argwhere(nda_image.sum(axis=(0, 2)))[[0, -1]]
    min_col, max_col = np.argwhere(nda_image.sum(axis=(0, 1)))[[0, -1]]
    min_row -= margins
    min_col -= margins
    min_slice -= margins
    max_row += margins
    max_col += margins
    max_slice += margins
    min_slice, max_slice, min_row, max_row, min_col, max_col = \
        [int(x) for x in
         (min_slice, max_slice, min_row, max_row, min_col, max_col)]
    cropped_img = nda_image[min_slice:max_slice,
                  min_row:max_row,
                  min_col:max_col]

    limits = (min_slice, max_slice,
              min_row, max_row,
              min_col, max_col)

    return cropped_img, limits
