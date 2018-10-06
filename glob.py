import pandas as pd
import numpy as np

# All globals stored in here
msgDuration = 5000
fieldRowHeight = 25

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def make_red_font(x, i, j):
    x.iloc[i, j] = "background-color: red"

    return x


def get_special_years(name, planyear):
    if name == "精密化學材料技術及應用開發四年計畫":
        if planyear >= 96 and planyear <= 99:
            return '96OR97OR98OR99'
        elif planyear >= 100 and planyear <= 103:
            return '100OR101OR102OR103'
    elif name == "工研院環境建構總計畫":
        if planyear >= 101 and planyear <= 103:
            return '101OR102OR103'
        elif planyear == 104:
            return '104'
        elif planyear >= 105 and planyear <= 107:
            return '105OR106OR107'
    elif name == "機械與系統領域工業基礎技術研究計畫":
        if planyear >= 102 and planyear <= 105:
            return '102OR103OR104OR105'
        elif planyear >= 106 and planyear <= 108:
            return '106OR107OR108'
    elif name == "能源與環境領域環境建構計畫":
        if planyear == 95:
            return '95'
        elif planyear >= 96 and planyear <= 100:
            return '96OR97OR98OR99OR100'
    elif name == "電子電機與軟體領域工業基礎技術研究計畫":
        if planyear >= 102 and planyear >= 105:
            return '102OR103OR104OR105'
        elif planyear >= 106 and planyear <= 108:
            return '106OR107OR108'
    elif name == "資訊與通訊領域環境建構計畫":
        if planyear >= 95 and planyear <= 99:
            return '95OR96OR97OR98OR99'
        elif planyear == 100:
            return '100'
    elif name == "民生福祉領域工業基礎技術研究計畫":
        if planyear >= 102 and planyear <= 105:
            return '102OR103OR104OR105'
        elif planyear >= 106 and planyear <= 108:
            return '106OR107OR108'
    elif name == "電子與光電領域環境建構計畫":
        if planyear >= 95 and planyear <= 99:
            return '95OR96OR97OR98OR99'
        elif planyear == 100:
            return '100'
    elif name == "生技與醫藥領域環境建構計畫":
        if planyear == 95:
            return '95'
        elif planyear >= 96 and planyear <= 100:
            return '96OR97OR98OR99OR100'
    elif name == "材料與化工領域環境建構計畫":
        if planyear >= 102 and planyear <= 105:
            return '102OR103OR104OR105'
        elif planyear >= 106 and planyear <= 108:
            return '106OR107OR108'
    elif name == "機械與系統領域環境建構計畫":
        if planyear == 95:
            return '95'
        elif planyear >= 96 and planyear <= 100:
            return '96OR97OR98OR99OR100'
    elif name == "精密機械技術研究發展四年計畫":
        if planyear >= 92 and planyear <= 95:
            return '92OR93OR94OR95'
    elif name == "科技美學設計加值計畫":
        if planyear == 101:
            return '101'
        elif planyear >= 102 and planyear <= 105:
            return '102OR103OR104OR105'
