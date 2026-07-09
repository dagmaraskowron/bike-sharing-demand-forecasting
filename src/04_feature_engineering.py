import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "clean_bike_sharing.csv"
FEATURE_DATA_PATH = PROJECT_ROOT / "data" / "bike_sharing_features.csv"


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)

    df["IsMorningPeak"] = df["Hour"].isin([7, 8, 9]).astype(int)
    df["IsEveningPeak"] = df["Hour"].isin([17, 18, 19]).astype(int)

    df = df.drop(columns=["Date"])

    return df


if __name__ == "__main__":
    df = pd.read_csv(CLEAN_DATA_PATH)

    print("Initial shape:")
    print(df.shape)

    feature_df = create_features(df)

    print("\nShape after feature engineering:")
    print(feature_df.shape)

    print("\nColumns after feature engineering:")
    print(feature_df.columns.tolist())

    print("\nFirst 5 rows:")
    print(feature_df.head())

    feature_df.to_csv(FEATURE_DATA_PATH, index=False)

    print(f"\nFeature dataset saved to: {FEATURE_DATA_PATH}")