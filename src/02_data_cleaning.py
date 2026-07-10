import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "bike_sharing.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "clean_bike_sharing.csv"


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("°", "", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("%", "percent", regex=False)
    )

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = clean_column_names(df)

    df = df.drop_duplicates()

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna()

    return df


if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH, encoding="latin1")

    print("Initial shape:")
    print(df.shape)

    print("\nInitial columns:")
    print(df.columns.tolist())

    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    print("\nDuplicated rows:")
    print(df.duplicated().sum())

    clean_df = clean_data(df)

    print("\nClean shape:")
    print(clean_df.shape)

    print("\nColumns after cleaning:")
    print(clean_df.columns.tolist())

    print("\nMissing values after cleaning:")
    print(clean_df.isnull().sum())

    clean_df.to_csv(CLEAN_DATA_PATH, index=False)

