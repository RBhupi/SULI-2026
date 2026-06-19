import pandas as pd


def export_csv(rows, headers, path):

    df = pd.DataFrame(rows, columns=headers)
    df.to_csv(path, index=False)


def export_excel(rows, headers, path):

    df = pd.DataFrame(rows, columns=headers)
    df.to_excel(path, index=False)