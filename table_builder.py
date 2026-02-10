import pandas as pd


def build_results_table(blackness, color_shift, gloss, a_shift, b_shift):
    """
    Build a results table as a pandas DataFrame from the computed metrics for each part.
    The table includes the following columns:
    - Part #: the part number (starting from 1)
    - Blackness: the computed blackness metric for the part
    - Color Shift: the computed color shift metric for the part
    - Glossiness: the computed glossiness metric for the part
    - Median a*: the computed median a* shift for the part (positive is more red
        negative is more green)
    - Median b*: the computed median b* shift for the part (positive is more yellow
        negative is more blue)
    INPUTS:
    blackness (list): a list of blackness values for each part
    color_shift (list): a list of color shift values for each part
    gloss (list): a list of gloss values for each part
    a_shift (list): a list of a shift values for each part
    b_shift (list): a list of b shift values for each part
    OUTPUTS:
    df (pandas DataFrame): a DataFrame containing the computed metrics for each part
    """
    return pd.DataFrame({
        "Part #": list(range(1, len(blackness) + 1)),
        "Blackness": blackness,
        "Color Shift": color_shift,
        "Glossiness": gloss,
        "Median a*": a_shift,
        "Median b*": b_shift,
    })