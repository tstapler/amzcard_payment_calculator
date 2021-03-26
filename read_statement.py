from pathlib import Path

import camelot
from pandas import DataFrame

lattice_args = {
    "process_background": True,
    "line_scale": 15,
    "resolution": 600,
    "pages": "2",
}


def clean_up_cells(df: DataFrame) -> DataFrame:
    return (df.replace("\n", " ", regex=True)
            .replace('(^\s+|\s+$)', '', regex=True)
            .replace('^-$', '', regex=True)
            .replace(',', '', regex=True)
            )


def remove_index_column(df: DataFrame) -> DataFrame:
    return df.rename(columns=df.iloc[0]).drop(df.index[0])

def remove_summary(df: DataFrame) -> DataFrame:
    return df[df["New Statement Balance"] != ""]

def main(statement: Path, output: Path = None):
    if not output:
        output = statement.with_suffix(".csv")
    tables = camelot.read_pdf(str(statement), flavor='lattice', **lattice_args)
    df = tables[1].df
    df = clean_up_cells(df)
    df = remove_index_column(df)
    df = remove_summary(df)
    print(f"Saving to {output}")
    df.to_csv(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
    A parser that uses opencv (via camelot-py) to read a Amazon Synchrony bank statement pdf, and convert it to a csv.""")
    parser.add_argument('--statement', dest="statement", type=Path, required=True, help="""
    Your statement, downloaded from https://amazon.syf.com/eService/EBill/eBillAction.action
    """)
    parser.add_argument('--output', dest="output", type=Path, help="""
    The csv you want to store your statement info within. Defaults to {statement}.csv""")

    args = parser.parse_args()
    main(args.statement, args.output)
