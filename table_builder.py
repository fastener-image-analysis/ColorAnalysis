import pandas as pd


def build_results_table(blackness, color_shift, gloss, a_shift, b_shift):
    return pd.DataFrame({
        "Part #": list(range(1, len(blackness) + 1)),
        "Blackness": blackness,
        "Color Shift": color_shift,
        "Glossiness": gloss,
        "Median a*": a_shift,
        "Median b*": b_shift,
    })