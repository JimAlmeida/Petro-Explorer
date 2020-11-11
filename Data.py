import pandas as pd


def readExcel(_fp, queue, sheet_number=0):
    df = pd.read_excel(_fp, sheet_name=sheet_number, header=None)
    queue.put(df)


def readCSV(_fp, queue):
    df = pd.read_csv(_fp, sep=',')
    queue.put(df)


def readTXT(_fp, queue):
    #Standard text file is separated by tabulations
    df = pd.read_csv(_fp, sep='\t')
    queue.put(df)


def toExcel(df, fpath, queue):
    if df is not None:
        df.to_excel(fpath, index=False)
        queue.put(df)


def toCSV(df, fpath, queue):
    if df is not None:
        df.to_csv(fpath, index=False)
        queue.put(df)


def toTXT(df, fpath, queue):
    # Standard text file is separated by tabulations
    if df is not None:
        df.to_csv(fpath, sep='\t')
        queue.put(df)
