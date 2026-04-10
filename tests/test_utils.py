import pytest
from color_analysis.utils import load_image, srgb_to_linear, linear_to_srgb, build_results_table
import numpy as np


def test_load_image():
    img = load_image('tests/test_image.jpg')
    assert img.ndim == 3
    assert img.shape[2] == 3

def test_srgb_linear_conversion():
    img = load_image("tests/test_image.jpg")
    linear_img = srgb_to_linear(img)
    srgb_img = linear_to_srgb(linear_img)

    diff = np.abs(img - srgb_img)
    assert diff.mean() < 1e-4
    assert diff.max() < 1e-2

def test_build_results_table():
    blackness = [0.1, 0.2, 0.3]
    color_shift = [10, 20, 30]
    a_shift = [5, 15, 25]
    b_shift = [2, 12, 22]
    gloss = [0.5, 0.6, 0.7]

    df = build_results_table(blackness, color_shift, a_shift, b_shift, gloss)
    assert df.shape == (3, 6)
    assert list(df.columns) == ['Part #', 'Blackness', 'Color Shift', 'Gloss Factor', 'Median a*', 'Median b*']
    assert df['Part #'].tolist() == [1, 2, 3]
    assert df['Blackness'].tolist() == blackness
    assert df['Color Shift'].tolist() == color_shift
    assert df['Gloss Factor'].tolist() == gloss
    assert df['Median a*'].tolist() == a_shift
    assert df['Median b*'].tolist() == b_shift

def test_build_results_table_empty():
    blackness = []
    color_shift = []
    a_shift = []
    b_shift = []
    gloss = []

    df = build_results_table(blackness, color_shift, a_shift, b_shift, gloss)
    assert df.shape == (0, 6)
    assert list(df.columns) == ['Part #', 'Blackness', 'Color Shift', 'Gloss Factor', 'Median a*', 'Median b*']

def test_build_results_table_mismatched_lengths():
    blackness = [0.1, 0.2]
    color_shift = [10]
    a_shift = [5, 15, 25]
    b_shift = [2, 12]
    gloss = [0.5, 0.6]

    with pytest.raises(ValueError):
        build_results_table(blackness, color_shift, a_shift, b_shift, gloss)


