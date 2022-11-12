import numpy as np
import pandas as pd

MIETPREIS = './data/mietpreise.csv'


def cost_estimator(mietpreis, flaeche, zimmer, max_score=10):
    frame = pd.read_csv(MIETPREIS, encoding="ANSI", delimiter=';')
    
    bottom, estimate, top = __price(frame, int(zimmer))

    m = (-max_score) / (top - bottom)
    g = max_score - m * bottom

    return np.round(np.clip(g + m * mietpreis, 1, max_score))

    
def __price(frame, zimmer):    
    for line in frame.iterrows():
        info = line[1].to_frame().T
        name = info["INDIKATOR_NAME"].to_string(index=False)

        if f"{zimmer}{'' if zimmer != 6 else '+'}-Zi" not in name:
            continue

        if "VI oberer Wert" in name:
            top = int(info["INDIKATOR_VALUE"].to_string(index=False))
        elif "Schätzwert" in name:
            estimate = int(info["INDIKATOR_VALUE"].to_string(index=False))
        elif "VI unterer Wert" in name:
            bottom = int(info["INDIKATOR_VALUE"].to_string(index=False))

    return bottom, estimate, top
